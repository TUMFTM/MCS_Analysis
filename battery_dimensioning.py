"""
Created on Fri Dez 15 11:48:51 2022

@author: schneiderFTM
"""

import numpy as np


def battery_dimensioning(bet, dieselTruck, stop_pattern, connection_time, energy_total, charging_power, eol_crit,
                         safety_percentage, fc_percentage):
    longest_stop = []
    shortest_stop = []
    stop_list_minute = stop_pattern.copy()
    if not 0 in stop_pattern and stop_pattern != 0:
        stop_list_minute = [stop / 60 - connection_time / 60 for stop in stop_pattern]
    longest_stop.append(max(stop_list_minute))
    shortest_stop.append(min(stop_list_minute))

    minimal_capacity = np.zeros((len(charging_power)))
    crate = np.zeros((len(charging_power)))
    c_rate_continous = np.zeros((len(charging_power)))
    charging_power_at_station = np.zeros((len(charging_power)))

    for j in range(len(charging_power)):
        # Is the rechargable energy in the additional breaks limiting ?
        minimal_capacity_crit1 = (energy_total - (
                    (charging_power[j]) * (len(stop_list_minute) - 1) * shortest_stop[0])) / \
                                 (1 + fc_percentage)

        #  Is the fast-chargable energy limiting ?
        minimal_capacity_crit2 = energy_total / (1 + len(stop_list_minute) * fc_percentage)

        #  Is the total rechargable energy limiting ?
        minimal_capacity_crit3 = (energy_total - ((charging_power[j]) * (sum(stop_list_minute))))

        # Check if crit1 is needed:
        if all(element == stop_list_minute[0] for element in stop_list_minute):
            minimal_capacity_crit1 = 0

        max_crit = [minimal_capacity_crit1, minimal_capacity_crit2, minimal_capacity_crit3]
        minimal_capacity[j] = max(max_crit) / (eol_crit * (1 - safety_percentage))

        # Calculate Charging Efficiency
        eta = 1 / (1 + (0.00079 * (charging_power[j] / minimal_capacity[j]) * 164.53) / 3.2)

        # Calculate needed Charging Power at Charging Station
        charging_power_at_station[j] = charging_power[j] / eta

        crate[j] = charging_power_at_station[j] / minimal_capacity[j]
        c_rate_continous[j] = charging_power_at_station[j] / minimal_capacity[j]


    if len(minimal_capacity) > 1:
        for i in range(len(minimal_capacity) - 1):
            if minimal_capacity[i + 1] == minimal_capacity[i]:
                crate[i + 1] = 6

    return minimal_capacity, crate, c_rate_continous, charging_power_at_station
