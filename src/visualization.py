import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

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
    sns.stripplot(x='Class', y='Probability', hue='Model', data=df_melted, 
                palette={"Combmod": "r", "Specmod": "g", "Allosmod": "b"},
                jitter=True, dodge=True, marker=".", alpha=0.5, size=3)
    plt.legend(title='Model', loc='upper right', markerscale=5)
    plt.title("Distribution of probability by class and model").get_figure().savefig("images/prob_model_dist.png")
    plt.clf()  # Clear the figure after saving
    print(f'Probabilities distribution of models generated and saved!')

    return

def dist_graph(file):
    plt.figure()  # Create a new figure
    dist_hist = sns.histplot(data=file, x='distance_gspphot', bins=100, kde=True)
    dist_hist.set_title('Distance Distribution')
    dist_hist.set_xlabel('log10 (d [pc])')
    dist_hist.set_ylabel('Count')
    dist_hist.set_xlim(0, max(file['distance_gspphot']))
    dist_hist.get_figure().savefig("images/distance_hist.png")
    plt.clf()  # Clear the figure after saving
    print(f'Histogram of distances generated and saved!')

    return

def coord_graph(file):

    x = file['coord_x']
    y = file['coord_y']
    z = file['coord_z']

    fig = plt.figure(figsize=(16, 12))

    # ========================
    # 1. Gràfica 3D principal
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
    # 2. Planta (vista des de dalt) -> X vs Y
    # ========================
    ax2 = fig.add_subplot(222)
    ax2.scatter(x, y, c='green', s=1, alpha=0.5)
    ax2.set_xlabel('X [pc]')
    ax2.set_ylabel('Y [pc]')
    ax2.set_title("Plan (Profile XY)")
    ax2.set_xlim(min(x), max(x))
    ax2.set_ylim(min(y), max(y))

    # ========================
    # 3. Perfil longitudinal (X vs Z)
    # ========================
    ax3 = fig.add_subplot(223)
    ax3.scatter(x, z, c='orange', s=1, alpha=0.5)
    ax3.set_xlabel('X [pc]')
    ax3.set_ylabel('Z [pc]')
    ax3.set_title("Elevation (Profile XZ)")
    ax3.set_xlim(min(x), max(x))
    ax3.set_ylim(min(z), max(z))

    # ========================
    # 4. Perfil transversal (Y vs Z)
    # ========================
    ax4 = fig.add_subplot(224)
    ax4.scatter(y, z, c='purple', s=1, alpha=0.5)
    ax4.set_xlabel('Y [pc]')
    ax4.set_ylabel('Z [pc]')
    ax4.set_title("Section (Profile YZ)")
    ax4.set_xlim(min(y), max(y))
    ax4.set_ylim(min(z), max(z))

    # Guardar i mostrar
    plt.suptitle("Profile projections of the 'Stars'", fontsize=16)
    plt.tight_layout()
    plt.savefig("images/3d_projeccions.png", dpi=300)
    plt.clf()  # Clear the figure after saving
    print(f'3D map generated and saved!')

    return

def grav_graph(file):
    G = 6.67430e-11  # m³/kg/s²
    division = ["0-20","20-40","40-60","60-80","80-100"]
    gravity = file[file['G_rel_error_percent'] < 5].copy()
    gravity.loc[:, 'percentile'] = pd.qcut(gravity['G_abs_error'], q=5, labels=division)
    not_to_rpt_col = {0: 'blue', 1: 'red', 2: 'magenta'}
    giant_col = {10: 'green', 11: 'orange', 12: 'purple'}
    fig, axs = plt.subplots(nrows=5, ncols=2, figsize=(15, 15), sharex=False)
    rows, columns = [0,0]
    for i in range(0,2):
        for percent in division:
            if columns == 0:
                tg = gravity[(gravity['percentile'] == percent) & (gravity['flags_flame'].isin([0, 1, 2]))]  # Use a temporary DataFrame
                colors = not_to_rpt_col
            else:
                tg = gravity[(gravity['percentile'] == percent) & (gravity['flags_flame'].isin([10, 11, 12]))]
                colors = giant_col
            for flag_value, df in tg.groupby('flags_flame'):
                axs[rows,columns].errorbar(df['constant_G'], df['ID'], 
                        fmt='x', capsize=0.1, capthick=0.1, elinewidth=0.1,
                        color=colors[flag_value], label=f"Flags_FLAME: {flag_value}")
            max_val = tg['constant_G'].max()
            min_val = tg['constant_G'].min()
            max_limit = (max_val) if max_val > G else (G)
            min_limit = (min_val) if min_val < G else (G)
            axs[rows,columns].set_xlim(min_limit, max_limit)
            axs[rows,columns].set_ylim(0, len(gravity['ID']))
            axs[rows,columns].axvline(x=G, color='black', linewidth = 3)
            y_min, y_max = axs[rows,columns].get_ylim()
            axs[rows,columns].annotate(f'G', xy=(G, y_max),
                        xytext=(G, y_max+500))  # Adjusted xytext for better placement
            axs[rows,columns].set_ylabel(f"ID  {percent}%")
            rows += 1
        columns += 1
        rows = 0

    handles, labels = axs[0,0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', title="Flags", bbox_to_anchor=(0.5, 0.19))

    handles, labels = axs[1,1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', title="Flags", bbox_to_anchor=(1, 0.19))

    plt.xlabel("Constant G")
    plt.suptitle("Gravitational constant (G) by percentiles with relative error < 5%")

    plt.tight_layout()
    plt.savefig("images/constant_g.png")
    plt.clf()  # Clear the figure after saving
    print(f'Gravitational constant results by percentiles generated and saved!')

    return

def hrd_graph(file):
    plt.figure(figsize=(10, 6))
    plt.hexbin(file['ebpminrp_gspphot'], file['mg_gspphot'], gridsize=250, cmap='plasma', bins='log')
    plt.xlabel("E(GBP-GRP)")
    plt.ylabel("Absolute Magnitude G")
    plt.xlim(min(file['ebpminrp_gspphot']), max(file['ebpminrp_gspphot']))
    plt.ylim(min(file['mg_gspphot']), max(file['mg_gspphot']))
    plt.gca().invert_yaxis()
    plt.colorbar(label='Number of stars')
    plt.gca().add_patch(plt.Rectangle((0.0, 2), 2.2, 8, edgecolor='cyan', facecolor='cyan', alpha=0.2, label='Principal sequence'))
    plt.gca().add_patch(plt.Rectangle((1.0, -5), 2.5, 7, edgecolor='red', facecolor='red', alpha=0.2, label='Gigants'))
    plt.gca().add_patch(plt.Rectangle((-0.2, 10), 1.5, 5, edgecolor='green', facecolor='green', alpha=0.2, label='White dwarfs'))
    plt.text(0.5, 3, "Main Sequence", color='cyan', fontsize=10)
    plt.text(1.5, -3, "Giants", color='red', fontsize=10)
    plt.text(0.2, 12, "White Dwarfs", color='green', fontsize=10)

    plt.legend()
    plt.tight_layout()
    plt.title("Absolute Magnitude G vs E(GBP-GRP) ").get_figure().savefig("images/hrd_diagram.png")
    plt.clf()  # Clear the figure after saving
    print('Hertzsprung-Russel diagram generated and saved!')

    return