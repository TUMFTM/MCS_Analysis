"""
Created on Fri Dez 8 11:42:58 2022

@author: schneiderFTM
"""

# Parameter - Base for all corresponding calculations focusing on diesel trucks

class DieselTruck():

    def __init__(self):
        # Vehicle constants
        self.motor_power = 352.3675316051114e3  # Max power in W [EEA average]
        self.fr = 0.005475931706892298  # Rolling friction coefficient [EEA average]
        self.cd_a = 5.679362188060499  # Drag coefficient x Front surface area in m^2 [EEA average]
        self.p_aux = 2.3e3  # auxiliary power consumption in W [Zhao 2013]

        self.vol_pt = 3000  # Available volume [Master thesis supervised by Sebastian Wolff]
        self.m_max = 40e3  # maximum gross vehicle weight in kg [§ 34 StVZO]
        self.m_szm = 7753.136555182494  # Mass of semi-truck tractor in kg[EEA Average]
        self.m_powertrain = 0.25 * self.m_szm  # Mass of all powertrain components [Phadke 2021]
        self.m_trailer = 7500  # trailer mass in kg [Norris and Escher 2017]
        self.payload_max = self.m_max - self.m_trailer - self.m_szm

        # Energy consumption
        con_ll = 24.72226283 / 100  # Energy consumption in L/km [EEA average Class 5-LH 4x2]
        con_rl = 32.35729932 / 100  # Energy consumption in L/km [EEA average Class 5-LH 4x2]
        self.share_low_load = 0.27 / 0.9  # Share of low load operation for Category 5-LH [VECTO]
        self.share_ref_load = 0.63 / 0.9  # Share of reference load operation for Category 5-LH
        self.con = self.share_low_load * con_ll + self.share_ref_load * con_rl

        # Toll costs
        c_toll_road = 0.169  # €/km Mautsatz für Infrastruktur für LKW>18t & ab 4 Achsen [BFStrMG]
        c_toll_air = 0.011  # €/km Mautsatz für Luftverschmutzung EURO6 Diesel [BFStrMG]
        c_toll_noise = 0.002  # €/km Mautsatz für Lärmbelästigung EURO6 Diesel [BFStrMG]
        toll_share = 0.92  # Share of toll roads in total mileage % [Hülsmann]
        self.c_toll = toll_share * (c_toll_road + c_toll_air + c_toll_noise)

        # Taxes
        self.c_tax = 556  # €/a [Kraftstg §9 Ab. (1) No. 4a]

        # Maintenance cost
        # €/km [Kleiner et al.] Machen explizit Angaben für 40t tractor-trailer in long haul operation für DT & BET.
        self.c_maintenance = 0.147

        # Indirect manufacturing costs
        self.imc = 1.45  # indirect manufacturing costs.

        # Powertrain components
        dmc_ice = 72.0  # engine direct manufacturing costs in €/kW [Link et al. 2021]
        dmc_tank = 2.0  # tank direct manufacturing costs in €/L [Link et al. 2021]
        dmc_eat = 19.8  # transmission direct manufacturing cost in €/kW [Link et al. 2021]
        vol_tank = 800  # Tank volume in L [Assumption]
        c_ice = self.motor_power / 1000 * dmc_ice * self.imc  # cost of engine in €
        c_tank = vol_tank * dmc_tank * self.imc  # cost of tank in €
        c_eat = self.motor_power / 1000 * dmc_eat * self.imc  # cost of transmission in €
        self.c_pt = (c_tank + c_eat + c_ice)  # cost of powertrain components in €
