"""
Created on Fri Dez 10 8:38:41 2022

@author: schneiderFTM
"""

from pandas import read_csv
from simulation import Simulation

# Import driving cycle for LDS
drivingcycle = read_csv("inputs/Mission Profiles/LongHaul.vdri")  # Load long haul driving cycle

# Sensitivity Analysis: WorstCase // Average // BestCase
cd_a = [8.77, 5.68, 4.22]
motor_power = [206000, 352240, 552000]
fr = [0.0084, 0.0058, 0.0039]


def energy_consumption_driving_dim(bet):
    # Calculte Energy Consumtion for battery dimensioning

    # Initialize
    con_per_km_dim = []
    v_avg_dim =[]
    sim = Simulation(drivingcycle)  # LDS

    for i in range(len(cd_a)):  # Loop over every sensitivity parameter
        bet.cd_a = cd_a[i]
        bet.motor_power = motor_power[i]
        bet.fr = fr[i]
        lds_result = [sim.run(bet, 42000)]  # LDS at 42t
        con_per_km = lds_result[0][0]  # kW/km LDS-Results for 42t Vecto Cylce
        v_avg = lds_result[0][1]  # km/h
        con_per_km_dim.append(con_per_km)
        v_avg_dim.append(v_avg)

    return con_per_km_dim, v_avg_dim


def energy_consumption_driving_oper(bet, dieselTruck):
    # Calculte Energy Consumtion during operation

    bet.cd_a = cd_a[1]
    bet.motor_power = motor_power[1]
    bet.fr = fr[1]

    sim = Simulation(drivingcycle)  # LDS
    lds_result = [
        sim.run(bet, (42000 - dieselTruck.payload_max) + 19300)]  # Simulation with 19.3t (Assumption: Payload Parity)
    con_193 = lds_result[0][0]
    v_193 = lds_result[0][1]
    lds_result = [
        sim.run(bet, (42000 - dieselTruck.payload_max) + 2600)]  # Simulation with 2.6t (Assumption: Payload Parity)
    con_26 = lds_result[0][0]
    v_26 = lds_result[0][1]
    con_per_km_avg = (0.7 * con_193 + 0.3 * con_26)
    v_avg_avg = (0.7 * v_193 + 0.3 * v_26)

    return con_per_km_avg, v_avg_avg


def calc_energy_total(bet, dieselTruck):
    # Collecting results and refactoring

    con_per_km_dim, v_avg_dim = energy_consumption_driving_dim(bet)
    con_per_km_avg, v_avg_avg = energy_consumption_driving_oper(bet, dieselTruck)

    con_per_km_total_dim = [con_per_km_dim_val + (2.3 / v_avg_dim_val) for con_per_km_dim_val, v_avg_dim_val in
                            zip(con_per_km_dim, v_avg_dim)]

    con_per_km_total_avg = con_per_km_avg + 2.3 / v_avg_avg

    energy_total_dim = [(con_per_km_dim_val * v_avg_dim_val) * 9 for
                        con_per_km_dim_val, v_avg_dim_val in
                        zip(con_per_km_dim, v_avg_dim)]  # [kwh] driving and auxillary energy consumption

    energy_total_avg = ((con_per_km_avg * v_avg_avg ) +2.3 / v_avg_avg) * 9  # [kWh]

    return energy_total_dim, energy_total_avg, con_per_km_total_dim, con_per_km_total_avg
