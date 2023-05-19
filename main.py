"""
Created on Fri Dez 8 10:42:58 2022

@author: schneiderFTM
"""

# Module Import
import numpy as np
from dieselTruck import DieselTruck
from batteryElectricTruck import BatteryElectricTruck
from battery_dimensioning import battery_dimensioning
from calc_energy_consumption import calc_energy_total
from calculate_tco import calculate_tco
from calculate_tco import calc_charging_cost
from calculate_tco import TCOparityanalysis
from Plots import plot_minimal_battery_size
from Plots import plot_cell_gravimetric_density
from Plots import plot_cell_volumetric_density
from Plots import plot_range_parity
from Plots import plot_cell_price
from Plots import plot_setup
from Plots import plot_charging_efficiency
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------------------
# -Parameter Initialization LDS-
dieselTruck = DieselTruck()  # Parameter-Class Diesel Truck
bet = BatteryElectricTruck(dieselTruck)  # Parameter-Class Battery electric truck based on diesel truck parameters
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# -Szenario Definition-
# According to Figure 2
scenario_1 = [[0], [45]]  # 45 mins with Regulation
scenario_2 = [[0], [60], [15, 30, 15]]  # 60 mins with Regulation
scenario_3 = [[0], [45], [22.5, 22.5], [15, 15, 15]]  # 45 mins without Regulation

scenario_list = [scenario_1, scenario_2, scenario_3]
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# ---Consumption Calculation---
# Quasi-static distance-based longitudinal dynamics model

energy_total_dim, energy_total_avg, con_per_km_total_dim, con_per_km_total_avg = calc_energy_total(bet, dieselTruck)
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# -Parameter Initialization Cell Requirements-
charging_power = np.linspace(100, 3750, 122)  # [kW] Charging Power available at every Charging Point

Variation_Percentage = 0.1
# WorstCase // Average // BestCase
battery_dimensioning_parameter = []
battery_dimensioning_parameter.append([0.8, 0.8, 0.8])  # End of Life Criterion // [%] Percentage of initial Capacity
battery_dimensioning_parameter.append([0.07, 0.07, 0.07])  # Usable Amount of Energy // [%] Usable Energy
battery_dimensioning_parameter.append([7, 6, 5])
# [min] Time which is lost per Stop for connecting and disconnecting to Charging Infrastructure
battery_dimensioning_parameter.append([0.75, 0.8, 0.85])
# [%]Percentage of Initial Capacity which is available for fast charging
battery_dimensioning_parameter.append([energy_total_dim[0], energy_total_dim[1], energy_total_dim[2]])
# Total Energy consumed over 9 hours of driving // [kWh]

cell2pack_grav = [0.495, 0.59, 0.742]  # Cell2Pack Factor / Gravimetric
cell2pack_vol = [0.168, 0.353, 0.528]  # Cell2Pack Factor / Volumetric
annual_mileage = [180000, 116000, 98000]  # Annual mileage in km
servicelife = [10, 8, 5]  # service life in years
annual_mileage_price = [98000, 116000, 180000]  # Annual mileage in km
servicelife_price = [5, 8, 10]  # service life in years / reversed for sensitivity analysis

cell2pack_cost = [1.47, 1.4, 1.32]  # Cell2System Factor / Cell Price
payload_max = [dieselTruck.m_max - 13153, dieselTruck.m_max - 15251.25, dieselTruck.m_max - 17999]  # Maximum payload
volume_max = [bet.volume_bat_max * (1 - Variation_Percentage), bet.volume_bat_max,
              bet.volume_bat_max * (1 + Variation_Percentage)]  # Maximal Volume for battery integration
c_diver_wage = [14, 15, 19.38]  # driver wage

# ----------------------------------------------------------------------------------------
# Plot Setup
fig1, axes1, fig2, axes2, fig3, axes3, legend_elements_1, legend_elements_2, legend_elements_3 = plot_setup()
# ----------------------------------------------------------------------------------------

# Generate Plots for each Scenario
for stop_list_idx, stop_list in enumerate(scenario_list):  # Loop over every scenario

    # ----------------------------------------------------------------------------------------
    # Initialization
    minimal_capacity = np.zeros((len(stop_list), len(battery_dimensioning_parameter[0]), len(charging_power)))
    c_rate = np.zeros((len(stop_list), len(battery_dimensioning_parameter[0]), len(charging_power)))
    c_rate_continous = np.zeros((len(stop_list), len(battery_dimensioning_parameter[0]), len(charging_power)))
    charging_power_at_station = np.zeros((len(stop_list), len(battery_dimensioning_parameter[0]), len(charging_power)))
    parity_bat_grav_density = np.zeros((len(stop_list), len(battery_dimensioning_parameter[0]), len(cell2pack_grav),
                                        len(charging_power)))
    parity_bat_vol_density = np.zeros((len(stop_list), len(battery_dimensioning_parameter[0]), len(cell2pack_grav),
                                       len(charging_power)))

    for i in range(len(stop_list)):  # Loop over every operation strategy in every scenario

        for k in range(len(battery_dimensioning_parameter[0])):  # Loop over every sensitivity option for battery sizing
            # -Battery Dimensioning // Minimal Battery Capacity to fulfill the 9h driving UseCase
            minimal_capacity[i, k], c_rate[i, k], c_rate_continous[i, k], charging_power_at_station[i, k] = \
                battery_dimensioning(bet, dieselTruck, stop_list[i],
                                     battery_dimensioning_parameter[2][k], battery_dimensioning_parameter[4][k],
                                     charging_power,
                                     battery_dimensioning_parameter[0][k], battery_dimensioning_parameter[1][k],
                                     battery_dimensioning_parameter[3][k])

            for j in range(len(cell2pack_grav)):  # Loop over every sensitivity option for cell requirements
                #  Required gravimetric energy density for being capabile to carry the same payload as a diesel truck
                parity_bat_grav_density[i, k, j] = ((minimal_capacity[i, k] * 1000) / (
                        42000 - payload_max[j] - bet.m_chassis - bet.m_drivetrain - bet.m_trailer)) \
                                                   / cell2pack_grav[j]
                #  Required volumetric energy density for being capabile fit the battery in the possible package space
                #  of a diesel truck without the conventional powertrain
                parity_bat_vol_density[i, k, j] = ((minimal_capacity[i, k] * 1000) / volume_max[j]) / cell2pack_vol[j]

    # ----------------------------------------------------------------------------------------
    # -Range Parity // Required EFC for reaching same mileage over lifetime as a diesel truck-
    EFC_Parity = np.zeros((len(stop_list), len(minimal_capacity[0, :, 0]), len(annual_mileage), len(charging_power)))
    for i in range(len(stop_list)):  # Loop over every scenario
        for k in range(len(minimal_capacity[0, :, 0])):  # Sensitivity over every result of battery sizing
            for j in range(len(annual_mileage)):  # Additional sensitivity for EFC parity
                lifetime_range = servicelife[j] * annual_mileage[j]
                EFC_Parity[i, k, j] = (lifetime_range * con_per_km_total_avg) / minimal_capacity[i, k]
    # ----------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------
    # Calculate Charging Cost according to Fast-Charge-Percentage // Linear Extrapolation
    # Charging powers for linear extrapolation of the charging price
    c_elec_fc_power = [22, 350]
    # Charging Rates # at defined points
    c_fc = [0.29 * (1 + Variation_Percentage), 0.29, 0.29 * (1 - Variation_Percentage)]

    fc_cost_inter = []
    for i in range(len(c_fc)):  # Calculation of 3 extrapolation functions according to charging prices
        c_elec_fc_cost = [0.21 / 1.19, c_fc[i] / 1.19]  # charging prices excluding VAT
        fc_cost_inter.append(interp1d(c_elec_fc_power, c_elec_fc_cost, kind='linear', fill_value='extrapolate'))

    # Calculate TCO-Cost of diesel Truck
    tco_diesel = []
    for i in range(len(annual_mileage)):
        tco_diesel.append(
            calculate_tco(dieselTruck, annual_mileage[i], servicelife[i], 0, 0, dieselTruck.con, 0, 0, [45], 0,
                          c_diver_wage[0]))

    # Calculate Cost-Parity Price for given EFC
    # Initialization
    c_bat_par = np.zeros((len(stop_list), len(minimal_capacity[0, :, 0]), len(annual_mileage), len(charging_power)))
    for i in range(len(stop_list)):  # Loop over every Scenario
        for k in range(len(minimal_capacity[0, :, 0])):  # Sensitivity over every result of battery sizing
            for j in range(len(annual_mileage)):  # Sensitivity Cost-Parity (electricity cost // annual mileage)

                # Charging Cost (min/max) incl. sensitivity
                c_elec = calc_charging_cost(minimal_capacity[i, k], stop_list[i], fc_cost_inter[j],
                                            charging_power_at_station[i, k], )
                for n in range(len(charging_power)):
                    c_bat_par[i, k, j, n] = TCOparityanalysis(tco_diesel[j][0], bet, minimal_capacity[i, k, n],
                                                              con_per_km_total_avg,
                                                              c_elec[n], servicelife_price[j], annual_mileage_price[j],
                                                              EFC_Parity[i, k, j, n], stop_list[i], cell2pack_cost[j],
                                                              c_diver_wage[j])

    # ----------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------
    # -Plots-

    # Figure 3 // Minimal Battery Size
    name = f"Scenario{stop_list_idx}_Minimal_Battery_Size"
    plot_minimal_battery_size(minimal_capacity, c_rate, stop_list, charging_power_at_station, name, stop_list_idx,
                              axes2)
    # Figure 4 // Gravimetric Density
    name = f"Scenario{stop_list_idx}_Cell_GravimetricDensity"
    plot_cell_gravimetric_density(c_rate, parity_bat_grav_density, stop_list, charging_power, name, stop_list_idx,
                                  axes3)
    # Figure 4 // Volumetric Density
    name = f"Scenario{stop_list_idx}_Cell_VolumetricDensity"
    plot_cell_volumetric_density(c_rate, parity_bat_vol_density, stop_list, name, stop_list_idx, axes3)

    # Figure 4 // Equivalent Full Cycles
    name = f"Scenario{stop_list_idx}_Cell_EFC"
    plot_range_parity(EFC_Parity, c_rate, stop_list, name, stop_list_idx, axes3)

    # Figure 4 // TCO
    name = f"Scenario{stop_list_idx}_Cell_Price"
    plot_cell_price(c_bat_par, c_rate_continous, stop_list, name, stop_list_idx, axes3)
    # ----------------------------------------------------------------------------------------

fig1.legend(legend_elements_1,
            ['0-Stop Strategy', '1-Stop Strategy', '2-Stop Strategy', '3 Stop Strategy'],
            loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4)
fig2.legend(legend_elements_2,
            ['0-Stop-Strategy', 'Sizing Uncertainty', '1-Stop Strategy', 'Sizing Uncertainty', '2-Stop Strategy',
             'Sizing Uncertainty', '3-Stop Strategy', 'Sizing Uncertainty'],
            loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4)
fig3.legend(legend_elements_3,
            ['1-Stop Strategy', 'Sizing Uncertainty', 'System Uncertainty', 'Tesla Model3', '2-Stop Strategy',
             'Sizing Uncertainty', 'System Uncertainty', '3-Stop Strategy', 'Sizing Uncertainty', 'System Uncertainty',
             'LFP cell price[14,17]', 'NMC cell price[14,17]', 'VW ID.3'],
            loc='upper center', bbox_to_anchor=(0.5, 0.06), ncol=4)

fig1.savefig("results/" + "Scenarios" + ".pdf", bbox_inches='tight')
fig2.savefig("results/" + "BatterySizing" + ".pdf", bbox_inches='tight')
fig3.savefig("results/" + "CellProperties" + ".pdf", bbox_inches='tight')

# Figure B7 // Charging Efficiency
plot_charging_efficiency()
plt.show()
