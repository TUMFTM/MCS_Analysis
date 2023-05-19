"""
Created on Fri Dez 9 12:48:51 2022

@author: schneiderFTM
"""

# Parameter - Base for all corresponding calculations focusing on battery electric

from scipy.interpolate import interp1d


class BatteryElectricTruck:

    def __init__(self, dt):
        # Vehicle simulation parameters
        self.motor_power = dt.motor_power  # motor power in W, equal to diesel truck
        self.fr = dt.fr  # rolling friction coefficient, equal to diesel truck
        self.cd_a = dt.cd_a  # drag coefficient x Front surface area in m^2, equal to diesel Truck
        self.p_aux = dt.p_aux  # auxiliary power consumption in W, equivalent to diesel truck
        self.eta = 0.85  # overall powertrain efficiency [Earl 2018]

        # vehicle mass
        self.m_max = 42e3  # maximum gross vehicle weight in kg [§ 34 StVZO, Punkt 6a, Satz 2]
        self.m_chassis = dt.m_szm - dt.m_powertrain  # chassis mass in kg
        self.m_drivetrain = 450  # drivetrain mass in kg [Mareev et al. 2017]
        self.m_trailer = dt.m_trailer  # same as diesel trailer

        # vehicle volume
        self.volume_bat_max = 3250  # l Bstieler, Manuel

        # battery Thermal System
        self.Pcooler = 10e3  # Cooling power in W [Schimpe et al.]
        self.Pheater = 11.2e3  # Heating power in W [Schimpe et al.]
        self.COPcool = -3  # Coefficient of performance of cooling system in pu [Schimpe et al.]
        self.COPheat = 1  # Coefficient of performance of heating system in pu [Schimpe et al.]
        self.Ebat_Neubauer = 22.1e3  # Battery size used by Neubauer et al. in Wh [Neubauer et al.]
        self.Rth_Neubauer = 1 / 4.343  # Thermal resistance between housing and ambient  in K/W [Neubauer et al.]
        self.Cth_Neubauer = 182e3  # Thermal mass of battery in J/K [Neubauer]
        self.T_Cool_on = 32.5  # Activation Cooling Threshold [Neubauer et al.]
        self.T_Cool_off = 32.4  # Deactivation Cooling Threshold [ID3 Paper]
        self.T_Heat = 10  # Heating Threshold [Neubauer et al.]

        # reference loads
        self.share_low_load = dt.share_low_load  # Share of low load operation for Category 5-LH [VECTO]
        self.share_ref_load = dt.share_ref_load  # Share of reference load operation for Category 5-LH
        self.low_load = 2.6e3  # Low load mass in kg [VECTO]
        self.ref_load = 19.3e3  # Reference load mass in kg [VECTO]

        # cost parameters
        dmc_motor = 19.3  # motor direct manufacturing cost in €/kW [Link et al. 2021]
        dmc_pe_hv = 29.3  # power electronics direct manufacturing cost in €/kW [Link et al. 2021]
        c_motor = self.motor_power / 1000 * dmc_motor * dt.imc  # motor cost in €
        c_pe = self.motor_power / 1000 * dmc_pe_hv * dt.imc  # power electronics cost in €
        self.c_pt = c_motor + c_pe  # powertrian cost in €
        self.c_toll = 0  # Electric vehicles are exempt from toll [BFStrMG]
        self.c_tax = 0.5 * dt.c_tax  # Electric vehicles get a 50% tax deduction [Kraftstg §9 Ab. (2)]
        self.c_maintenance = 0.098  # €/km [Kleiner et al.]
        self.bat_scrappage = 0.15  # residual value of battery at end of life in % [Burke and Fulton 2019]
        self.c_sc = 0.21  # €/kWh
        c_fc = 0.31  # €/kWh
        c_mw = 0.37  # €/kWh
        self.c_charging_func = interp1d([350, 1000], [c_fc, c_mw], kind="linear", fill_value='extrapolate')
        self.syear = 80091
        self.operationyears = 5
