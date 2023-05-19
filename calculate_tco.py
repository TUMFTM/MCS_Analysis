"""
Created on Fri Dez 3 8:42:33 2022

@author: schneiderFTM
"""

# Cost - Model which calculates the TCO of a diesel truck and an electric truck without the battery cost

import numpy as np
from scipy.optimize import bisect

# Unterschiedliche Ladeleistungen -> Veränderter Charging-Preis
# Unterschiedliche Invest-Kosten -> veränderte Batteriegröße


# Cost parameters
r = 1.095  # interest rate [Assumption]
c_diesel = 1.82 / 1.19  # Cost of diesel fuel in €/liter
c_elec_sc = 0.2515  # Slow charging electricity cost in EUR/kWh excl. VAT [ISI - LFS III 2021]
c_driver_wage = 14.79  # €/h


def residualValue(total_mileage):
    # Return relative resale value
    # Model adopted from Friedrich und Kleiner (2017)
    result = 0.951 * np.exp(-0.002 * total_mileage / 1000)  # Result in % of original NLP
    return result


def calc_charging_cost(minimal_capacity, stop_pattern, fc_cost_inter, charging_power):
    # Input: 1x vector minimal capacity // 1x vector charging_power // fc_cost_inter
    # Output: 1x c_elec vector

    c_elec = np.zeros((len(charging_power)))
    for j in range(len(charging_power)):
        e_fc = (sum(stop_pattern) / 60) * charging_power[j]
        e_sc = minimal_capacity[j] * (1 - 0.25)
        c_elec[j] = e_fc / (e_fc + e_sc) * fc_cost_inter(charging_power[j]) + e_sc / (e_fc + e_sc) * c_elec_sc

    return c_elec


def calculate_tco(veh, annual_mileage, servicelife, minimal_capacity, c_elec, con, EFC, cbat_spec, stop_list,
                  cell2pack_cost, c_diver_wage):
    # Powertrain cost
    c_pt_residual = (veh.c_pt * residualValue(annual_mileage * servicelife)
                     * r ** -servicelife)  # residual value
    c_pt_imputed_interest = (veh.c_pt + c_pt_residual) / 2 * (r ** servicelife - 1)  # imputed interest
    c_pt = veh.c_pt - c_pt_residual + c_pt_imputed_interest  # total powertrain cost

    # Taxes (due once a year)
    c_tax = sum([veh.c_tax * r ** -t
                 for t in range(1, servicelife + 1)])

    # Maintenance costs (due twice a year)
    c_maint = sum([veh.c_maintenance * annual_mileage / 2 * r ** (-t / 2)
                   for t in range(0, 2 * servicelife)])

    # Toll costs (due weekly)
    c_toll = sum([veh.c_toll * annual_mileage / 52 * r ** (-t / 52)
                  for t in range(0, 52 * servicelife)])

    # Energy consumption costs (due weekly)
    c_ene_spec = c_elec if minimal_capacity != 0 else c_diesel
    c_ene = sum([c_ene_spec * con * annual_mileage / 52 * r ** (-t / 52)
                 for t in range(0, 52 * servicelife)])

    # Additional Driver Cost
    c_wage_additional = sum([(c_driver_wage * ((sum(stop_list) / 60) - 0.75)) * 3 / 52 * r ** (-t / 52)
                             for t in range(0, 52 * servicelife)])

    # Calculate Battery Cost:
    if minimal_capacity != 0:

        bat_life_km = (EFC * minimal_capacity) / con

        # Determine required battery replacements
        n_replacements = int(annual_mileage * servicelife / bat_life_km)  # number of replacements
        t_installation = [bat_life_km * n / annual_mileage for n in
                          range(0, n_replacements + 1)]  # time of replacments in years
        t_scrappage = t_installation[1:]  # time of scrappage in years

        # Battery investment costs
        c_bat_inv = [cbat_spec * cell2pack_cost * minimal_capacity * r ** -t for t in t_installation]

        # Scrappage value
        c_bat_scrappage = [veh.bat_scrappage * cbat_spec * cell2pack_cost * minimal_capacity * r ** -t
                           for t in t_scrappage]  # scrappage values

        # Residual value
        bat_eol_soh = (
                1 - annual_mileage * servicelife / bat_life_km % 1)  # remaining capacity at end of lifetime
        c_bat_residual = ((veh.bat_scrappage + bat_eol_soh * (1 - veh.bat_scrappage))
                          * cbat_spec * cell2pack_cost * minimal_capacity * r ** -servicelife)

        # Imputed interest
        t_operation = [bat_life_km / annual_mileage] * n_replacements  # investment till scrappage
        t_operation += [servicelife - t_installation[-1]]  # investment till resale
        avg_bound_investment = [(c_purchase + c_scrap) / 2 for (c_purchase, c_scrap)
                                in zip(c_bat_inv[:-1], c_bat_scrappage)]  # investment till scrappage
        avg_bound_investment += [(c_bat_inv[-1] + c_bat_residual) / 2]  # investment till resale
        c_bat_imputed_interests = [invest * (r ** t - 1) for (invest, t)
                                   in zip(avg_bound_investment, t_operation)]

        # Total battery costs
        c_bat = (sum(c_bat_inv)
                 - sum(c_bat_scrappage)
                 - c_bat_residual
                 + sum(c_bat_imputed_interests))

    else:
        c_bat = 0

    # Total costs
    c_tot = sum([c_pt, c_tax, c_toll, c_maint, c_ene, c_bat, c_wage_additional])

    return c_tot, c_pt, c_tax, c_toll, c_maint, c_ene, c_bat, c_wage_additional


def TCOparityanalysis(dt_rco, bet, minimal_capacity, con, c_elec, servicelife, annual_mileage, EFC, stop_list,
                      cell2pack_cost, c_diver_wage):
    cbat_spec_min = 0  # minimum considered specific battery cost in EUR/kWh
    cbat_spec_max = 5000  # maximum considered specific battery cost in EUR/kWh

    try:
        c_bat_par = bisect(
            lambda cbat_spec: dt_rco -
                              calculate_tco(bet, annual_mileage, servicelife, minimal_capacity, c_elec, con, EFC,
                                            cbat_spec, stop_list, cell2pack_cost, c_diver_wage)[0],
            cbat_spec_min, cbat_spec_max)
        return c_bat_par
    except ValueError:
        print(f"Warning: No EFC Parity found!.")
