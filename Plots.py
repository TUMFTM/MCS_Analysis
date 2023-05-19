"""
Created on Fri Dez 10 18:38:44 2022

@author: schneiderFTM
"""


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


def plot_setup():
    plt.rcParams["font.family"] = "Times New Roman"

    def cm2inch(value):
        return value / 2.54

    col_width_two_col_doc_in_cm = 8.89
    col_width_two_col_doc_in_pt = 252

    SMALL_SIZE = 8
    MEDIUM_SIZE = 10
    BIGGER_SIZE = 12

    plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=SMALL_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=SMALL_SIZE)  # fontsize of the figure title

    color_TUM = []
    color_TUM.append('#003359')  # DarkBlue
    color_TUM.append('#0065BD')  # Blue
    color_TUM.append('#E37222')  # Orange
    color_TUM.append('#A2AD00')  # Green
    color_TUM.append('#98C6EA')  # Green

    # Definition of Master-Plots
    # Scenarios
    fig1, axes1 = plt.subplots(nrows=1,
                               ncols=3,
                               figsize=(
                                   cm2inch(2 * col_width_two_col_doc_in_cm), cm2inch(4.5)))  # Width, height in inches

    legend_elements_1 = [Line2D([0], [0], color=color_TUM[0], lw=2, label='0-Stop-Strategy'),
                         Line2D([0], [0], color=color_TUM[1], lw=2, label='1-Stop-Strategy'),
                         Line2D([0], [0], color=color_TUM[2], lw=2, label='2-Stop-Strategy'),
                         Line2D([0], [0], color=color_TUM[3], lw=2, label='3-Stop-Strategy')]

    # BatterySizing
    fig2, axes2 = plt.subplots(nrows=1,
                               ncols=3,
                               figsize=(
                               cm2inch(2 * col_width_two_col_doc_in_cm), cm2inch(4.5)))  # Width, height in inches

    legend_elements_2 = [Line2D([0], [0], color=color_TUM[0], lw=2, label='0-Stop-Strategy'),
                         Patch(facecolor=color_TUM[0], edgecolor=color_TUM[0], alpha=0.3, ),
                         Line2D([0], [0], color=color_TUM[1], lw=2, label='1-Stop-Strategy'),
                         Patch(facecolor=color_TUM[1], edgecolor=color_TUM[1], alpha=0.3, ),
                         Line2D([0], [0], color=color_TUM[2], lw=2, label='2-Stop-Strategy'),
                         Patch(facecolor=color_TUM[2], edgecolor=color_TUM[2], alpha=0.3, ),
                         Line2D([0], [0], color=color_TUM[3], lw=2, label='3-Stop-Strategy'),
                         Patch(facecolor=color_TUM[3], edgecolor=color_TUM[3], alpha=0.3, )]

    #  CellProperties
    fig3, axes3 = plt.subplots(nrows=4,
                               ncols=3,
                               figsize=(
                                   cm2inch(2 * col_width_two_col_doc_in_cm), cm2inch(20)))  # Width, height in inches
    legend_elements_3 = [Line2D([0], [0], color=color_TUM[1], lw=2, label='1-Stop-Strategy'),
                         Patch(facecolor=color_TUM[1], edgecolor=color_TUM[1], alpha=0.3, ),
                         Patch(facecolor=color_TUM[1], edgecolor=color_TUM[1], alpha=0.1, ),
                         Line2D([], [], color=color_TUM[0], marker='s', linestyle='None', markersize=4),
                         Line2D([0], [0], color=color_TUM[2], lw=2, label='2-Stop-Strategy'),
                         Patch(facecolor=color_TUM[2], edgecolor=color_TUM[2], alpha=0.3, ),
                         Patch(facecolor=color_TUM[2], edgecolor=color_TUM[2], alpha=0.1, ),
                         Line2D([0], [0], color=color_TUM[3], lw=2, label='3-Stop-Strategy'),
                         Patch(facecolor=color_TUM[3], edgecolor=color_TUM[3], alpha=0.3, ),
                         Patch(facecolor=color_TUM[3], edgecolor=color_TUM[3], alpha=0.1, ),
                         Line2D([0], [0], color=color_TUM[0], lw=2, linestyle='dotted'),
                         Line2D([0], [0], color=color_TUM[0], lw=2, linestyle='solid'),
                         Line2D([], [], color=color_TUM[0], marker='o', linestyle='None', markersize=4),
                         ]

    return fig1, axes1, fig2, axes2, fig3, axes3, legend_elements_1, legend_elements_2, legend_elements_3,


def plot_minimal_battery_size(minimal_capacity, crate, stop_list, charging_power, name, stop_list_idx, axes):
    axes[stop_list_idx].grid(True, alpha=0.5)
    color_TUM = []
    color_TUM.append('#003359')  # DarkBlue
    color_TUM.append('#0065BD')  # Blue
    color_TUM.append('#E37222')  # Orange
    color_TUM.append('#A2AD00')  # Green
    color_TUM.append('#98C6EA')  # Green

    # Plot Operation-Strategy without charging only in the first Scenario
    if stop_list_idx == 0:
        start_plot = 0
        axes[stop_list_idx].set_ylabel('Battery Capacity in kWh')
        axes[stop_list_idx].set_title('Scenario 1')
    if stop_list_idx == 1:
        color_TUM[2], color_TUM[3] = color_TUM[3], color_TUM[2]
        start_plot = 1
        axes[stop_list_idx].set_title('Scenario 2')
    if stop_list_idx == 2:
        # color_TUM[2], color_TUM[3] = color_TUM[3], color_TUM[2]
        start_plot = 1
        axes[stop_list_idx].set_title('Scenario 3')

    axes[stop_list_idx].text(1500, 1750, '1C', rotation=90 * ((500 / 500) / 1.5))
    axes[stop_list_idx].text(2900, 1600, '2C', rotation=90 * ((250 / 500) / 1.3))
    axes[stop_list_idx].text(3200, 1150, '3C', rotation=90 * ((500 / 1500) / 1.4))
    axes[stop_list_idx].text(3400, 950, '4C', rotation=90 * ((500 / 2000) / 1.4))
    axes[stop_list_idx].axline((0, 0), slope=1, label='1C', color="grey", alpha=0.7, linestyle='dotted', linewidth=0.75)
    axes[stop_list_idx].axline((0, 0), slope=0.5, label='2C', color="grey", alpha=0.7, linestyle='dotted',
                               linewidth=0.75)
    axes[stop_list_idx].axline((0, 0), slope=0.33, label='3C', color="grey", alpha=0.7, linestyle='dotted',
                               linewidth=0.75)
    axes[stop_list_idx].axline((0, 0), slope=0.25, label='4C', color="grey", alpha=0.7, linestyle='dotted',
                               linewidth=0.75)

    for i in range(start_plot, len(stop_list)):
        axes[stop_list_idx].plot(charging_power[i, 1, :], minimal_capacity[i, 1, :],
                                 label=f"Stopping Pattern: {stop_list[i]}",
                                 color=color_TUM[i], linewidth=1.5)  # Avg-Values

        axes[stop_list_idx].plot(charging_power[i, 0, :], minimal_capacity[i, 0, :], linestyle='dashed',
                                 color=color_TUM[i],
                                 alpha=0.5, linewidth=0.75)  # WorstCase-Values
        axes[stop_list_idx].plot(charging_power[i, 2, :], minimal_capacity[i, 2, :], linestyle='dashed',
                                 color=color_TUM[i],
                                 alpha=0.5, linewidth=0.75)  # BestCase-Values

        xfill = np.sort(np.concatenate([charging_power[i, 0, :], charging_power[i, 2, :]]))
        y1fill = np.interp(xfill, charging_power[i, 0, :], minimal_capacity[i, 0, :])
        y2fill = np.interp(xfill, charging_power[i, 2, :], minimal_capacity[i, 2, :])

        axes[stop_list_idx].fill_between(xfill, y1fill, y2fill, color=color_TUM[i],
                                         alpha=0.3)

    if stop_list_idx != 0:
        axes[stop_list_idx].yaxis.set_ticklabels([])
    axes[stop_list_idx].set_xlabel('Charging Power in kW')
    axes[stop_list_idx].set_xlim(0, 3750)
    axes[stop_list_idx].set_ylim(0, 2000)


def plot_cell_gravimetric_density(crate, parity_bat_grav_density, stop_list, charging_power, name, stop_list_idx, axes):
    axes[0, stop_list_idx].grid(True, alpha=0.5)
    color_TUM = []
    color_TUM.append('#003359')  # DarkBlue
    color_TUM.append('#0065BD')  # Blue
    color_TUM.append('#E37222')  # Orange
    color_TUM.append('#A2AD00')  # Green
    color_TUM.append('#98C6EA')  # Green
    color_TUM.append('#98C6EA')  # Green
    color_TUM.append('#98C6EA')  # Green
    color_TUM.append('#98C6EA')  # Green

    if stop_list_idx == 0:
        axes[0, stop_list_idx].set_ylabel('Energy Density in Wh/kg \n to achieve payload-parity')
        axes[0, stop_list_idx].set_title('Scenario 1')
    if stop_list_idx == 1:
        color_TUM[2], color_TUM[3] = color_TUM[3], color_TUM[2]
        axes[0, stop_list_idx].set_title('Scenario 2')
    if stop_list_idx == 2:
        axes[0, stop_list_idx].set_title('Scenario 3')

    for i in range(1, len(stop_list)):
        # Interpolate Results to joint C-Rate vector to plot shade
        crate_vec = np.arange(max(np.nanmin(crate[i, :], axis=1)), min(np.nanmax(crate[i, :], axis=1)), 0.01)
        parity_bat_density_trim = np.nan * np.ones(
            (len(parity_bat_grav_density[0, :, 0, 0]), len(parity_bat_grav_density[0, 0, :, 0]), len(crate_vec)))
        for k in range(len(parity_bat_grav_density[0, :, 0, 0])):
            for n in range(len(parity_bat_grav_density[0, 0, :, 0])):
                parity_bat_density_trim[k, n] = np.interp(crate_vec, crate[i, k], parity_bat_grav_density[i, k, n])

        # Size Avg // C2P Avg
        axes[0, stop_list_idx].plot(crate[i, 1, :], parity_bat_grav_density[i, 1, 1, :],
                                    label=f"Stopping Pattern: {stop_list[i]}",
                                    color=color_TUM[i], linewidth=1.5)
        # Size Worst // C2P avg
        axes[0, stop_list_idx].plot(crate[i, 0, :], parity_bat_grav_density[i, 0, 1, :], linestyle='dashed',
                                    color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)
        # Size Best // C2P avg
        axes[0, stop_list_idx].plot(crate[i, 2, :], parity_bat_grav_density[i, 2, 1, :], linestyle='dashed',
                                    color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)
        # Size Worst // C2P Worst
        axes[0, stop_list_idx].plot(crate[i, 0, :], parity_bat_grav_density[i, 0, 0, :], linestyle='dotted',
                                    color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)
        # Size Best // C2P Best
        axes[0, stop_list_idx].plot(crate[i, 2, :], parity_bat_grav_density[i, 2, 2, :], linestyle='dotted',
                                    color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)

        # Plot shade between min/max battery size + min max Cell2Pack
        axes[0, stop_list_idx].fill_between(crate_vec, parity_bat_density_trim[0, 1], parity_bat_density_trim[2, 1],
                                            color=color_TUM[i], alpha=0.3)
        axes[0, stop_list_idx].fill_between(crate_vec, parity_bat_density_trim[0, 0], parity_bat_density_trim[2, 2],
                                            color=color_TUM[i], alpha=0.1)

    axes[0, stop_list_idx].plot(1.38, 273, marker="o", markersize=4, color=color_TUM[0])  # ID3
    axes[0, stop_list_idx].plot(1.81, 166.19, marker="s", markersize=4, color=color_TUM[0])  # Model3

    axes[0, stop_list_idx].xaxis.set_ticklabels([])
    if stop_list_idx != 0:
        axes[0, stop_list_idx].yaxis.set_ticklabels([])

    axes[0, stop_list_idx].set_ylim(0, 1600)
    axes[0, stop_list_idx].set_xlim(0, 6)


def plot_cell_volumetric_density(crate, parity_bat_vol_density, stop_list, name, stop_list_idx, axes):
    axes[1, stop_list_idx].grid(True, alpha=0.5)
    color_TUM = []
    color_TUM.append('#003359')  # DarkBlue
    color_TUM.append('#0065BD')  # Blue
    color_TUM.append('#E37222')  # Orange
    color_TUM.append('#A2AD00')  # Green
    color_TUM.append('#98C6EA')  # Green
    color_TUM.append('#98C6EA')  # Green
    color_TUM.append('#98C6EA')  # Green
    if stop_list_idx == 0:
        axes[1, stop_list_idx].set_ylabel('Volumetric Energy Density in Wh/l \n to achieve package compatibility')
    if stop_list_idx == 1:
        color_TUM[2], color_TUM[3] = color_TUM[3], color_TUM[2]

    for i in range(1, len(stop_list)):
        # Interpolate Results to joint C-Rate vector to plot shade
        crate_vec = np.arange(max(np.nanmin(crate[i, :], axis=1)), min(np.nanmax(crate[i, :], axis=1)), 0.01)
        parity_bat_vol_density_trim = np.nan * np.ones(
            (len(parity_bat_vol_density[0, :, 0, 0]), len(parity_bat_vol_density[0, 0, :, 0]), len(crate_vec)))
        for k in range(len(parity_bat_vol_density[0, :, 0, 0])):
            for n in range(len(parity_bat_vol_density[0, 0, :, 0])):
                parity_bat_vol_density_trim[k, n] = np.interp(crate_vec, crate[i, k], parity_bat_vol_density[i, k, n])

        # Size Avg // C2P Avg
        axes[1, stop_list_idx].plot(crate[i, 1, :], parity_bat_vol_density[i, 1, 1, :],
                                    label=f"Stopping Pattern: {stop_list[i]}",
                                    color=color_TUM[i], linewidth=1.5)
        # Size Worst // C2P avg
        axes[1, stop_list_idx].plot(crate[i, 0, :], parity_bat_vol_density[i, 0, 1, :], linestyle='dashed',
                                    color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)
        # Size Best // C2P avg
        axes[1, stop_list_idx].plot(crate[i, 2, :], parity_bat_vol_density[i, 2, 1, :], linestyle='dashed',
                                    color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)
        # Size Worst // C2P Worst
        axes[1, stop_list_idx].plot(crate[i, 0, :], parity_bat_vol_density[i, 0, 0, :], linestyle='dotted',
                                    color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)
        # Size Best // C2P Best
        axes[1, stop_list_idx].plot(crate[i, 2, :], parity_bat_vol_density[i, 2, 2, :], linestyle='dotted',
                                    color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)

        # Plot shade between min/max battery size + min max Cell2Pack
        axes[1, stop_list_idx].fill_between(crate_vec, parity_bat_vol_density_trim[0, 1],
                                            parity_bat_vol_density_trim[2, 1],
                                            color=color_TUM[i], alpha=0.3)
        axes[1, stop_list_idx].fill_between(crate_vec, parity_bat_vol_density_trim[0, 0],
                                            parity_bat_vol_density_trim[2, 2],
                                            color=color_TUM[i], alpha=0.1)

    axes[1, stop_list_idx].plot(1.38, 685, marker="o", markersize=4, color=color_TUM[0])  # ID3
    axes[1, stop_list_idx].plot(1.81, 362.92, marker="s", markersize=4, color=color_TUM[0])  # Model3

    axes[1, stop_list_idx].xaxis.set_ticklabels([])
    if stop_list_idx != 0:
        axes[1, stop_list_idx].yaxis.set_ticklabels([])
    axes[1, stop_list_idx].set_ylim(0, 2800)
    axes[1, stop_list_idx].set_xlim(0, 6)


def plot_range_parity(EFC, crate, stop_list, name, stop_list_idx, axes):
    axes[2, stop_list_idx].grid(True, alpha=0.5)
    color_TUM = []
    color_TUM.append('#003359')  # DarkBlue
    color_TUM.append('#0065BD')  # Blue
    color_TUM.append('#E37222')  # Orange
    color_TUM.append('#A2AD00')  # Green
    color_TUM.append('#98C6EA')  # Green
    color_TUM.append('#98C6EA')  # Green
    color_TUM.append('#98C6EA')  # Green
    color_TUM.append('#98C6EA')  # Green
    if stop_list_idx == 0:
        axes[2, stop_list_idx].set_ylabel('Equivalent Full Cycles \n to achieve lifetime-parity')
    if stop_list_idx == 1:
        color_TUM[2], color_TUM[3] = color_TUM[3], color_TUM[2]

    for i in range(1, len(stop_list)):
        # Interpolate Results to joint C-Rate vector to plot shade
        crate_vec = np.arange(max(np.nanmin(crate[i, :], axis=1)), min(np.nanmax(crate[i, :], axis=1)), 0.01)
        parity_EFC_trim = np.nan * np.ones(
            (len(EFC[0, :, 0, 0]), len(EFC[0, 0, :, 0]), len(crate_vec)))
        for k in range(len(EFC[0, :, 0, 0])):
            for n in range(len(EFC[0, 0, :, 0])):
                parity_EFC_trim[k, n] = np.interp(crate_vec, crate[i, k], EFC[i, k, n])

        # Size Avg // Mileage Avg
        axes[2, stop_list_idx].plot(crate[i, 1, :], EFC[i, 1, 1, :], label=f"Stopping Pattern: {stop_list[i]}",
                                    color=color_TUM[i], linewidth=1.5)
        # Size Worst // Mileage avg
        axes[2, stop_list_idx].plot(crate[i, 0, :], EFC[i, 0, 1, :], linestyle='dashed', color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)
        # Size Best // Mileage avg
        axes[2, stop_list_idx].plot(crate[i, 2, :], EFC[i, 2, 1, :], linestyle='dashed', color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)
        # Size Worst // Low Mileage
        axes[2, stop_list_idx].plot(crate[i, 0, :], EFC[i, 0, 2, :], linestyle='dotted', color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)
        # Size Best // High Mileage
        axes[2, stop_list_idx].plot(crate[i, 2, :], EFC[i, 2, 0, :], linestyle='dotted', color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)

        # Plot shade between min/max battery size + min max Cell2Pack
        axes[2, stop_list_idx].fill_between(crate_vec, parity_EFC_trim[0, 1], parity_EFC_trim[2, 1],
                                            color=color_TUM[i], alpha=0.3)
        axes[2, stop_list_idx].fill_between(crate_vec, parity_EFC_trim[0, 2], parity_EFC_trim[2, 0],
                                            color=color_TUM[i], alpha=0.2)
        axes[2, stop_list_idx].xaxis.set_ticklabels([])

        axes[2, stop_list_idx].plot(1.38, 363.1, marker="o", markersize=4, color=color_TUM[0])  # ID3
        axes[2, stop_list_idx].plot(1.81, 345.2, marker="s", markersize=4, color=color_TUM[0])  # Model3

        if stop_list_idx != 0:
            axes[2, stop_list_idx].yaxis.set_ticklabels([])

        axes[2, stop_list_idx].set_ylim(0, 8000)
        axes[2, stop_list_idx].set_xlim(0, 6)


def plot_cell_price(c_bat_par, crate, stop_list, name, stop_list_idx, axes):
    axes[3, stop_list_idx].grid(True, alpha=0.5)
    color_TUM = []
    color_TUM.append('#003359')  # DarkBlue
    color_TUM.append('#0065BD')  # Blue
    color_TUM.append('#E37222')  # Orange
    color_TUM.append('#A2AD00')  # Green
    color_TUM.append('#98C6EA')  # Green
    color_TUM.append('#98C6EA')  # Green
    color_TUM.append('#98C6EA')  # Green
    color_TUM.append('#98C6EA')  # Green

    if stop_list_idx == 0:
        axes[3, stop_list_idx].set_ylabel('Cell Price in €/kWh \n achieving TCO-Parity')

    if stop_list_idx == 1:
        color_TUM[2], color_TUM[3] = color_TUM[3], color_TUM[2]

    for i in range(1, len(stop_list)):  # Operation Strategy in each Scenario
        # Interpolate Results to joint C-Rate vector to plot shade
        crate_vec = np.arange(max(np.nanmin(crate[i, :], axis=1)), 6, 0.01)
        parity_cell_price_shade = np.nan * np.ones(
            (len(c_bat_par[0, :, 0, 0]), len(c_bat_par[0, 0, :, 0]), len(crate_vec)))
        for k in range(len(c_bat_par[0, :, 0, 0])):  # Sizing Worst/Avg/Best
            for n in range(len(c_bat_par[0, 0, :, 0])):  # Propterty worst/avg/best
                parity_cell_price_shade[k, n] = np.interp(crate_vec, crate[i, k], c_bat_par[i, k, n])

                # Replace Nan with 0 to get the complete shade of the cell parity price plot
                for m in reversed(range(len(parity_cell_price_shade[k, n]))):
                    if np.isnan(parity_cell_price_shade[k, n, m]):
                        parity_cell_price_shade[k, n, m] = 0
                    else:
                        break

        # Size Avg // Price Avg
        axes[3, stop_list_idx].plot(crate[i, 1, :], c_bat_par[i, 1, 1, :], label=f"Stopping Pattern: {stop_list[i]}",
                                    color=color_TUM[i], linewidth=1.5)
        # Size Worst // Price avg
        axes[3, stop_list_idx].plot(crate[i, 0, :], c_bat_par[i, 0, 1, :], linestyle='dashed', color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)
        # Size Best // Price avg
        axes[3, stop_list_idx].plot(crate[i, 2, :], c_bat_par[i, 2, 1, :], linestyle='dashed', color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)
        # Size Worst // System Worst
        axes[3, stop_list_idx].plot(crate[i, 0, :], c_bat_par[i, 0, 2, :], linestyle='dotted', color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)
        # Size Best // System Best
        axes[3, stop_list_idx].plot(crate[i, 2, :], c_bat_par[i, 2, 0, :], linestyle='dotted', color=color_TUM[i],
                                    alpha=0.5, linewidth=0.75)

        # Plot shade between min/max battery size + min max Cell2Pack
        axes[3, stop_list_idx].fill_between(crate_vec, parity_cell_price_shade[0, 1], parity_cell_price_shade[2, 1],
                                            color=color_TUM[i], alpha=0.3)
        axes[3, stop_list_idx].fill_between(crate_vec, parity_cell_price_shade[0, 2], parity_cell_price_shade[2, 0],
                                            color=color_TUM[i], alpha=0.1)

        if stop_list_idx != 0:
            axes[3, stop_list_idx].yaxis.set_ticklabels([])
        axes[3, stop_list_idx].set_xlabel('Required C-Rate in 1/h')
        axes[3, stop_list_idx].set_ylim(0, 800)
        axes[3, stop_list_idx].set_xlim(0, 6)
        axes[3, stop_list_idx].axline((100, 100), slope=0, color=color_TUM[0], alpha=1, linestyle='solid',
                                      linewidth=1.3)
        axes[3, stop_list_idx].axline((70, 70), slope=0, color=color_TUM[0], alpha=1, linestyle='dotted',
                                      linewidth=1.3)


def plot_charging_efficiency():
    def cm2inch(value):
        return value / 2.54

    col_width_two_col_doc_in_cm = 8.89

    color_TUM = []
    color_TUM.append('#003359')  # DarkBlue
    color_TUM.append('#0065BD')  # Blue
    color_TUM.append('#E37222')  # Orange
    color_TUM.append('#A2AD00')  # Green
    color_TUM.append('#98C6EA')  # Green

    crate = np.arange(0, 4.2, 0.2)
    eta_tesla = 1 / (1 + (0.00079 * crate * 164.53) / 3.2)
    eta_vw = 1 / (1 + (0.0018 * crate * 79.3) / 3.67)

    fig4, ax_eff = plt.subplots(nrows=1,
                                ncols=1,
                                figsize=(
                                    cm2inch(col_width_two_col_doc_in_cm), cm2inch(4.5)))

    line1 = ax_eff.plot(crate, eta_tesla, color=color_TUM[1], label='Tesla Model 3')
    line2 = ax_eff.plot(crate, eta_vw, color=color_TUM[2], label='VW ID.3')
    ax_eff.grid(True, alpha=0.5)
    ax_eff.set_ylabel('Charging efficiency in %')
    ax_eff.set_ylim(0.86, 1)
    ax_eff.set_xlabel('C-Rate in 1/h')
    ax_eff.set_xlim(0, 4)
    ax_eff.legend()

    fig4.savefig("results/" + "Charging_Efficiency" + ".pdf", bbox_inches='tight')

    return
