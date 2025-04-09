import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

# ========================================================================
# MODEL PROBABILITIES GRAPH
# ========================================================================
def model_graph(file):
    leng = len(file['classprob_dsc_combmod_quasar'])
    model_data = {
        "Model": np.repeat(['Combmod', 'Specmod', 'Allosmod'], leng),
        "Quasar": np.concatenate([file['classprob_dsc_combmod_quasar'], 
                                file['classprob_dsc_specmod_quasar'], 
                                file['classprob_dsc_allosmod_quasar']]),
        "Galaxy": np.concatenate([file['classprob_dsc_combmod_galaxy'], 
                                file['classprob_dsc_specmod_galaxy'], 
                                file['classprob_dsc_allosmod_galaxy']]),
        "Star": np.concatenate([file['classprob_dsc_combmod_star'], 
                                    file['classprob_dsc_specmod_star'], 
                                    file['classprob_dsc_allosmod_star']]),
        "White Dwarf": np.concatenate([file['classprob_dsc_combmod_whitedwarf'], 
                                        file['classprob_dsc_specmod_whitedwarf'],
                                        [0 for i in range(leng)]]),
        "Binary Star": np.concatenate([file['classprob_dsc_combmod_binarystar'],
                                        file['classprob_dsc_specmod_binarystar'],
                                        [0 for i in range(leng)]])
    }


    df = pd.DataFrame(model_data)
    # Transformar a format llarg per Seaborn
    df_melted = df.melt(id_vars=['Model'], var_name='Class', value_name='Probability')

    # Gràfica
    plt.figure(figsize=(10, 6))
    ax = sns.stripplot(x='Class', y='Probability', hue='Model', data=df_melted, 
              palette={"Combmod": "r", "Specmod": "g", "Allosmod": "b"},
              jitter=True, dodge=True, marker=".", alpha=0.3, size=3)
    for i, cls in enumerate(df_melted['Class'].unique()):
        for j, model in enumerate(df_melted['Model'].unique()):
            subset = df_melted[(df_melted['Class'] == cls) & (df_melted['Model'] == model)]
            if subset.empty:
                continue
            mean = subset['Probability'].mean()

            xpos = i + (j - 1) * 0.27 
            ax.hlines(mean, xpos - 0.08, xpos + 0.08, color='black', linewidth=1, label=None)  # mitjana
    plt.legend(title='Model', loc='upper right', markerscale=5)
    plt.title("Distribution of probability by class and model (Mean)")
    plt.tight_layout()
    plt.savefig("images/prob_model_dist.png")
    plt.clf()  # Clear the figure after saving
    print(f'Probabilities distribution of models generated and saved!')

    return

# ========================================================================
# DISTANCE GRAPH
# ========================================================================
def dist_graph(file):
    plt.figure()  # Create a new figure
    dist_hist = sns.histplot(data=file, x='distance_gspphot', bins=100, kde=True)
    dist_hist.set_title('Distance Distribution')
    dist_hist.set_xlabel('log10 (d [pc])')
    dist_hist.set_ylabel('Count')
    dist_hist.set_xlim(0, max(file['distance_gspphot']))
    dist_hist.text(10000,20000, f"Stadistical information for X-axis:\n\
                       Min: {round(file['distance_gspphot'].min(),2)}\n\
                       Max: {round(file['distance_gspphot'].max(),2)}\n\
                       Average: {round(file['distance_gspphot'].mean(),2)}\n\
                       Standard desviation: {round(file['distance_gspphot'].std(),2)}", fontsize= 10)
    dist_hist.get_figure().savefig("images/distance_hist.png")
    plt.clf()  # Clear the figure after saving
    print(f'Histogram of distances generated and saved!')

    return

# ========================================================================
# 3D MAP
# ========================================================================
def coord_graph(file):

    x = file['coord_x']
    y = file['coord_y']
    z = file['coord_z']

    fig = plt.figure(figsize=(16, 12))

    # ========================
    # 3D
    # ========================
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.scatter(x, y, z, c='blue', marker='.', alpha=0.3)
    ax1.set_xlabel('X [pc]')
    ax1.set_ylabel('Y [pc]')
    ax1.set_zlabel('Z [pc]')
    ax1.set_title("3D 'Star' map")
    ax1.set_xlim(min(x), max(x))
    ax1.set_ylim(min(y), max(y))
    ax1.set_zlim(min(z), max(z))

    # ========================
    # Plant (XY)
    # ========================
    ax2 = fig.add_subplot(222)
    ax2.scatter(x, y, c='green', s=1, alpha=0.5)
    ax2.set_xlabel('X [pc]')
    ax2.set_ylabel('Y [pc]')
    ax2.set_title("Plan (Profile XY)")
    ax2.set_xlim(min(x), max(x))
    ax2.set_ylim(min(y), max(y))

    # ========================
    # 3. Elevation (XZ)
    # ========================
    ax3 = fig.add_subplot(223)
    ax3.scatter(x, z, c='red', s=1, alpha=0.5)
    ax3.set_xlabel('X [pc]')
    ax3.set_ylabel('Z [pc]')
    ax3.set_title("Elevation (Profile XZ)")
    ax3.set_xlim(min(x), max(x))
    ax3.set_ylim(min(z), max(z))

    # ========================
    # 4. Section (YZ)
    # ========================
    ax4 = fig.add_subplot(224)
    ax4.scatter(y, z, c='purple', s=1, alpha=0.5)
    ax4.set_xlabel('Y [pc]')
    ax4.set_ylabel('Z [pc]')
    ax4.set_title("Section (Profile YZ)")
    ax4.set_xlim(min(y), max(y))
    ax4.set_ylim(min(z), max(z))

    plt.suptitle("Profile projections of the 'Stars'", fontsize=16)
    plt.tight_layout()
    plt.savefig("images/3d_projections.png", dpi=300)
    plt.clf()  # Clear the figure after saving
    print(f'3D map generated and saved!')

    return

# ========================================================================
# GRAVITY GRAPH
# ========================================================================
def grav_graph(file):
    G = 6.67430e-11  # m³/kg/s²
    gravity = file[file['G_rel_error_percent'] < 5].copy()
    not_to_rpt_col = {0: 'blue', 1: 'red', 2: 'green'}
    giant_col = {10: 'cyan', 11: 'magenta', 12: 'brown'}
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 4), sharex=False)
    columns = 0
    for i in range(0, 2):
        if columns == 0:
            tg_s = gravity[(gravity['flags_flame'].isin([0, 1, 2]))]  # Use a temporary DataFrame
            tg = tg_s
            colors = not_to_rpt_col
        else:
            tg_g = gravity[(gravity['flags_flame'].isin([10, 11, 12]))]
            tg = tg_g
            colors = giant_col
        for flag_value, df in tg.groupby('flags_flame'):
            axs[columns].errorbar(df['constant_G'], df['ID'], 
                    fmt='x', capsize=0.1, capthick=0.1, elinewidth=0.1,
                    color=colors[flag_value], label=f"Flags_FLAME: {flag_value}")
        max_val = tg['constant_G'].max()
        min_val = tg['constant_G'].min()
        max_limit = (max_val) if max_val > G else (G)
        min_limit = (min_val) if min_val < G else (G)
        axs[columns].set_xlim(min_limit, max_limit)
        axs[columns].set_ylim(0, len(gravity['ID']))
        axs[columns].axvline(x=G, color='black', linewidth=3)
        y_min, y_max = axs[columns].get_ylim()
        axs[columns].annotate(f'G', xy=(G, y_max),
                    xytext=(G, y_max + 20))  # Adjusted xytext for better placement
        axs[columns].set_ylabel(f"ID")
        columns += 1

    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', title=f"Stars (#{len(tg_s)}) ", bbox_to_anchor=(0.2, 0.1))
    axs[0].set_xlabel("Constant G")

    handles, labels = axs[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', title=f"Giants (#{len(tg_g)})", bbox_to_anchor=(0.7, 0.1))
    axs[1].set_xlabel("Constant G")
    plt.suptitle("Gravitational constant (G) by percentiles with relative error < 5%", fontsize=12)

    plt.tight_layout()
    plt.savefig("images/constant_g.png", bbox_inches='tight', dpi=300)
    plt.clf()  # Clear the figure after saving
    print(f'Gravitational constant results by percentiles generated and saved!')

    return

# ========================================================================
# HR DIAGRAM GRAPH
# ========================================================================
def hrd_graph(file):
    plt.figure(figsize=(10, 6))
    plt.hexbin(file['ebpminrp_gspphot'], file['mg_gspphot'], gridsize=250, cmap='plasma', bins='log')
    plt.xlabel("E(GBP-GRP)")
    plt.ylabel("Absolute Magnitude G")
    plt.xlim(min(file['ebpminrp_gspphot']), max(file['ebpminrp_gspphot']))
    plt.ylim(min(file['mg_gspphot']), max(file['mg_gspphot']))
    plt.gca().invert_yaxis()
    plt.colorbar(label='Number of stars')
    plt.gca().add_patch(plt.Rectangle((0.0, 2), 2.2, 8, edgecolor='cyan', facecolor='cyan', alpha=0.2, label='Main sequence'))
    plt.gca().add_patch(plt.Rectangle((1.0, -5), 2.5, 7, edgecolor='red', facecolor='red', alpha=0.2, label='Giants'))
    plt.gca().add_patch(plt.Rectangle((-0.2, 10), 1.5, 5, edgecolor='green', facecolor='green', alpha=0.2, label='White dwarfs'))
    plt.text(0.5, 3, "Main Sequence", color='cyan', fontsize=10)
    plt.text(1.5, -4, "Giants", color='red', fontsize=10)
    plt.text(0.6, 11, "White Dwarfs", color='green', fontsize=10)

    plt.legend()
    plt.title("Absolute Magnitude G vs E(GBP-GRP)", fontsize = 12)
    plt.tight_layout()
    plt.savefig("images/hr_diagram.png")
    plt.clf()  # Clear the figure after saving
    print('Hertzsprung-Russel diagram generated and saved!')

    return