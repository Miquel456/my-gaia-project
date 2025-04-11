import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

# ========================================================================
# MODEL PROBABILITIES GRAPH
# ========================================================================
def model_graph(file):
    # TOTAL SOURCES
    leng = len(file['ID'])
    # LIBRARY FOR VISUALIZATION WITH SEABORN STRPPLOT
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

    # CONVERTING TO DATAFRAME
    df = pd.DataFrame(model_data)
    # TRANSFORMING TO LARGE FORMAT FOR SEABORN
    df_melted = df.melt(id_vars=['Model'], var_name='Class', value_name='Probability')

    # CREATING FIGURE
    plt.figure(figsize=(10, 6))
    # SEABORN STRIPPLOT
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
            # MEAN LINE
            ax.hlines(mean, xpos - 0.08, xpos + 0.08, color='black', linewidth=1, label=None)
    # FIGURE CHARACTERICS
    plt.legend(title='Model', loc='upper right', markerscale=5)
    plt.title(f"Distribution of probability by class and model for {leng} objects")
    plt.tight_layout()
    # SAVING THE FIGURE
    plt.savefig("images/prob_model_dist.png")
    # CLEARING THE FIGURE AFTER SAVING
    plt.clf()
    # PRINT MESSAGE
    print(f'Probabilities distribution of models generated and saved!')

    return

# ========================================================================
# DISTANCE GRAPH
# ========================================================================
def dist_graph(file):
    # CREATING NEW FIGURE
    plt.figure()
    # SEABORN HISTROGRAM
    dist_hist = sns.histplot(data=file, x='distance_gspphot', bins=100, kde=True)
    # FIGURE CHARACTERICS
    dist_hist.set_title('Distance Distribution')
    dist_hist.set_xlabel('Distance [pc])')
    dist_hist.set_ylabel('Count')
    dist_hist.set_xlim(0, max(file['distance_gspphot']))
    # STADISCTICAL INFORMATION FOR DISTANCE
    dist_hist.text(10000,20000, f"Stadistical information of distances (X-axis):\n\
                       Min: {round(file['distance_gspphot'].min(),2)}\n\
                       Max: {round(file['distance_gspphot'].max(),2)}\n\
                       Average: {round(file['distance_gspphot'].mean(),2)}\n\
                       Standard deviation: {round(file['distance_gspphot'].std(),2)}\n\
                       Total #: {len(file['ID'])}", fontsize= 10)
    # GETTING FIGURE AND SAVE
    dist_hist.get_figure().savefig("images/distance_hist.png")
    # CLEARING THE FIGURE AFTER SAVING
    plt.clf()
    # PRINT MESSAGE
    print(f'Histogram of distances generated and saved!')

    return

# ========================================================================
# 3D MAP & PROJECTIONS
# ========================================================================
def coord_graph(file):
    # RENAME COLUMNS
    x = file['coord_x']
    y = file['coord_y']
    z = file['coord_z']

    # CREATING FIGURE 4 SCATTERPLOTS
    fig = plt.figure(figsize=(16, 12))

    # ========================
    # 3D PROJECTION
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.scatter(x, y, z, c='blue', marker='.', alpha=0.3)
    # FIGURE CHARACTERICS
    ax1.set_xlabel('X [pc]')
    ax1.set_ylabel('Y [pc]')
    ax1.set_zlabel('Z [pc]')
    ax1.set_title("3D 'Star' map")
    # LIMITS
    ax1.set_xlim(min(x), max(x))
    ax1.set_ylim(min(y), max(y))
    ax1.set_zlim(min(z), max(z))

    # ========================
    # PLANT (XY) PROJECTION
    ax2 = fig.add_subplot(222)
    ax2.scatter(x, y, c='green', s=10, alpha=0.5, marker="X")
    # FIGURE CHARACTERICS
    ax2.set_xlabel('X [pc]')
    ax2.set_ylabel('Y [pc]')
    ax2.set_title("Plan (Profile XY)")
    # LIMITS
    ax2.set_xlim(min(x), max(x))
    ax2.set_ylim(min(y), max(y))
    # HORIZONTAL AND VERTICAL LINES ORIGIN
    ax2.hlines(0, min(x), max(x), color='black', linewidth=1, label=None)
    ax2.vlines(0, min(y), max(y), color='black', linewidth=1, label=None)

    # ========================
    # 3. ELEVATION (XZ) PROJECTION
    ax3 = fig.add_subplot(223)
    ax3.scatter(x, z, c='orange', s=10, alpha=0.5, marker="X")
    # FIGURE CHARACTERICS
    ax3.set_xlabel('X [pc]')
    ax3.set_ylabel('Z [pc]')
    ax3.set_title("Elevation (Profile XZ)")
    # LIMITS
    ax3.set_xlim(min(x), max(x))
    ax3.set_ylim(min(z), max(z))
    # HORIZONTAL AND VERTICAL LINES ORIGIN
    ax3.hlines(0, min(x), max(x), color='black', linewidth=1, label=None)
    ax3.vlines(0, min(z), max(z), color='black', linewidth=1, label=None)

    # ========================
    # 4. SECTION (YZ) PROJECTION
    ax4 = fig.add_subplot(224)
    ax4.scatter(y, z, c='purple', s=10, alpha=0.5, marker="X")
    # FIGURE CHARACTERICS
    ax4.set_xlabel('Y [pc]')
    ax4.set_ylabel('Z [pc]')
    ax4.set_title("Section (Profile YZ)")
    # LIMITS
    ax4.set_xlim(min(y), max(y))
    ax4.set_ylim(min(z), max(z))
    # HORIZONTAL AND VERTICAL LINES ORIGIN
    ax4.hlines(0, min(y), max(y), color='black', linewidth=1, label=None)
    ax4.vlines(0, min(z), max(z), color='black', linewidth=1, label=None)

    # FIGURE CHARACTERICS
    plt.suptitle("Profile projections of the 'Stars'", fontsize=16)
    plt.tight_layout()
    # GETTING FIGURE AND SAVE
    plt.savefig("images/3d_projections.png", dpi=300)
    # CLEARING THE FIGURE AFTER SAVING
    plt.clf()
    # PRINT MESSAGE
    print(f'3D map generated and saved!')

    return

# ========================================================================
# GRAVITY GRAPH
# ========================================================================
def grav_graph(file):
    # CONSTANT G VALUE
    G = 6.67430e-11  # m³/kg/s²
    # FILTER TO 'g_rel_error_percent' BEING INFERIOR TO 5%
    gravity = file[file['g_rel_error_percent'] < 5].copy()
    # COLORS SET 1 (NORMAL)
    not_to_rpt_col = {0: 'blue', 1: 'red', 2: 'green'}
    # COLORS SET 2 (GIANTS)
    giant_col = {10: 'cyan', 11: 'magenta', 12: 'brown'}
    # CREATING FIGURE
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 4), sharex=False)
    columns = 0
    for i in range(0, 2):
        if columns == 0:
            # USING A TEMPORARY DATAFRAME
            tg_s = gravity[(gravity['flags_flame'].isin([0, 1, 2]))]  # Use a temporary DataFrame
            # RENAME FOR THE LOOP
            tg = tg_s
            # CHOOSING COLOR SET 1
            colors = not_to_rpt_col
        else:
            tg_g = gravity[(gravity['flags_flame'].isin([10, 11, 12]))]
            # RENAME FOR THE LOOP
            tg = tg_g
            # CHOOSING COLOR SET 2
            colors = giant_col
        # GENERATING TWO SCATTER PLOTS
        for flag_value, df in tg.groupby('flags_flame'):
            axs[columns].errorbar(df['constant_g'], df['ID'], 
                    fmt='x', capsize=0.1, capthick=0.1, elinewidth=0.1,
                    color=colors[flag_value], label=f"Flags_FLAME: {flag_value}")
        # LIMITS
        max_val = tg['constant_g'].max()
        min_val = tg['constant_g'].min()
        max_limit = (max_val) if max_val > G else (G)
        min_limit = (min_val) if min_val < G else (G)
        axs[columns].set_xlim(min_limit, max_limit)
        axs[columns].set_ylim(0, len(gravity['ID']))
        # CREATING A VERTICAL LINE AT G VALUE
        axs[columns].axvline(x=G, color='black', linewidth=3)
        # GETTING Y-AXIS LIMITS
        y_min, y_max = axs[columns].get_ylim()
        # ANNOTATING 'G' IN G VERTICAL LINE
        axs[columns].annotate(f'G', xy=(G, y_max),
                    # ADJUSTING XYTEXT FOR BETTER PLACEMENT
                    xytext=(G, y_max + 30))  
        axs[columns].set_ylabel(f"ID")
        columns += 1
    # GENERATING LEGENDS FOR EVERY PLOT
    # PLOT 1 (LEFT)
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', title=f"Stars (#{len(tg_s)}) ", bbox_to_anchor=(0.2, 0.1))
    axs[0].set_xlabel("Constant G")
    # PLOT 2 (RIGHT)
    handles, labels = axs[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', title=f"Giants (#{len(tg_g)})", bbox_to_anchor=(0.7, 0.1))
    axs[1].set_xlabel("Constant G")
    # FIGURE CHARACTERICS
    plt.suptitle("Gravitational constant (G)", fontsize=12)
    plt.tight_layout()
    # GETTING FIGURE AND SAVE
    plt.savefig("images/constant_g.png", bbox_inches='tight', dpi=300)
    # CLEARING THE FIGURE AFTER SAVING
    plt.clf()
    # PRINT MESSAGE
    print(f'Gravitational constant results generated and saved!')

    return

# ========================================================================
# HR DIAGRAM GRAPH
# ========================================================================
def hrd_graph(file):
    # CREATING FIGURE HEXAGONAL BIN MAP
    plt.figure(figsize=(10, 6))
    plt.hexbin(file['ebpminrp_gspphot'], file['mg_gspphot'], gridsize=250, cmap='plasma', bins='log')
    # FIGURE CHARACTERICS
    plt.xlabel("E(GBP-GRP)")
    plt.ylabel("Absolute Magnitude G")
    # LIMITS
    plt.xlim(min(file['ebpminrp_gspphot']), max(file['ebpminrp_gspphot']))
    plt.ylim(min(file['mg_gspphot']), max(file['mg_gspphot']))
    plt.gca().invert_yaxis()
    # COLORBAR
    plt.colorbar(label=f'Number of stars\n Total #: {len(file['ID'])}') 
    # ADDING RECTANGLES FOR STAR REGIONS
    # MAIN SEQUENCE
    plt.gca().add_patch(plt.Rectangle((0.0, 2), 2.2, 8, edgecolor='cyan', facecolor='cyan', alpha=0.2, label='Main sequence'))
    plt.text(0.5, 3, "Main Sequence", color='cyan', fontsize=10)
    # GIANTS
    plt.gca().add_patch(plt.Rectangle((1.0, -5), 2.5, 7, edgecolor='red', facecolor='red', alpha=0.2, label='Giants'))
    plt.text(1.5, -4, "Giants", color='red', fontsize=10)
    # WHITE DWARFS
    plt.gca().add_patch(plt.Rectangle((-0.2, 10), 1.5, 5, edgecolor='green', facecolor='green', alpha=0.2, label='White Dwarfs'))
    plt.text(0.6, 11, "White Dwarfs", color='green', fontsize=10)
    # FIGURE CHARACTERICS 
    plt.legend()
    plt.title("Absolute Magnitude G vs E(GBP-GRP)", fontsize = 12)
    plt.tight_layout()
    # GETTING FIGURE AND SAVE
    plt.savefig("images/hr_diagram.png")
    # CLEARING THE FIGURE AFTER SAVING
    plt.clf()
    # PRINT MESSAGE
    print('Hertzsprung-Russel diagram generated and saved!')

    return