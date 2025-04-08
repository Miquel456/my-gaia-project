import pandas as pd
import numpy as np
import src.visualization as viz

# ========================================================================
# MODEL PROBABILITIES FILE
# ========================================================================
def model_file(file):
    file = str(file)
    data = pd.read_csv(f"data/raw/{file}")
    model_class = pd.DataFrame(data[[ 'source_id', 
        'classprob_dsc_combmod_quasar', 'classprob_dsc_combmod_galaxy', 
            'classprob_dsc_combmod_star', 'classprob_dsc_combmod_whitedwarf', 'classprob_dsc_combmod_binarystar', # Comb Model
        'classprob_dsc_specmod_quasar', 'classprob_dsc_specmod_galaxy', 'classprob_dsc_specmod_star', 
            'classprob_dsc_specmod_whitedwarf', 'classprob_dsc_specmod_binarystar',                               # Spec Model
        'classprob_dsc_allosmod_quasar', 'classprob_dsc_allosmod_galaxy', 'classprob_dsc_allosmod_star']])        # All others Model
    model_class = model_class.dropna()
    mod_clas_index = pd.Series([i for i in range(1,len(model_class['source_id'])+1)])
    model_class['ID'] = mod_clas_index.values
    model_class_df = model_class[['ID', 'source_id', 
        'classprob_dsc_combmod_quasar', 'classprob_dsc_combmod_galaxy', 
            'classprob_dsc_combmod_star', 'classprob_dsc_combmod_whitedwarf', 'classprob_dsc_combmod_binarystar', 
        'classprob_dsc_specmod_quasar', 'classprob_dsc_specmod_galaxy', 'classprob_dsc_specmod_star', 
            'classprob_dsc_specmod_whitedwarf', 'classprob_dsc_specmod_binarystar', 
        'classprob_dsc_allosmod_quasar', 'classprob_dsc_allosmod_galaxy', 'classprob_dsc_allosmod_star']]
    
    model = model_class_df # Rename for visualization

    # Path destination
    carpet = "data"           # Carpet destination
    subcarpet = "processed"   # Subcarpet destination
    name = "model_class.csv"  # CSV file name
    full_name = f"{carpet}/{subcarpet}/{name}"  
    model_class_df.to_csv(full_name, index=False) # Saving pandas DataFrame to CSV
    print(f"Succesfully saved '{name}' in '{carpet}/{subcarpet}'!")

    # Creating 3D map
    viz.model_graph(model)
    
    return

# ========================================================================
# DISTANCE FILE
# ========================================================================
def dist_file(file):
    file = str(file)
    data = pd.read_csv(f"data/raw/{file}")
    distance = pd.DataFrame(data[['source_id', 'distance_gspphot']])
    # distance = distance.rename(columns={'distance_gspphot': 'distance [pc]'})
    distance = distance.dropna()
    dist_index = pd.Series([i for i in range(1,len(distance['source_id'])+1)])
    distance['ID'] = dist_index.values
    distance_df = distance[['ID', 'source_id', 'distance_gspphot']]
    dist = distance_df # Rename for visualization

    # Path destination
    carpet = "data"           # Carpet destination
    subcarpet = "processed"   # Subcarpet destination
    name = "distance.csv"  # CSV file name
    full_name = f"{carpet}/{subcarpet}/{name}"  
    distance_df.to_csv(full_name, index=False) # Saving pandas DataFrame to CSV
    print(f"Succesfully saved '{name}' in '{carpet}/{subcarpet}'!")

    viz.dist_graph(dist)

    return

# ========================================================================
# COORDINATES FILE 
# ========================================================================
def coord_file(file):
    file = str(file)
    data = pd.read_csv(f"data/raw/{file}")
    # Converting data to pandas DataFrame
    coords = pd.DataFrame(data[['source_id', 'ra', 'dec', 'parallax']])                                                                                            
    coords = coords.dropna() # Drop NaN values from selected columns
    coords['ra'] = np.radians(coords['ra'])   # Degrees to radians
    coords['dec'] = np.radians(coords['dec']) # Degrees to radians
    # Conversion coordinates
    coords['coord_x'] = 1000*np.cos(coords['dec'])*np.cos(coords['ra'])/coords['parallax'] # X coordinate conversion
    coords['coord_y'] = 1000*np.cos(coords['dec'])*np.sin(coords['ra'])/coords['parallax'] # Y coordinate conversion
    coords['coord_z'] = 1000*np.sin(coords['dec'])/coords['parallax']                      # Z coordinate conversion
    coord_index = pd.Series([i for i in range(1,len(coords['source_id'])+1)])
    coords['ID'] = coord_index.values # Index column
    coords_df = coords[['ID', 'source_id', 'ra', 'dec', 'parallax',    # Order and reselect columns
        'coord_x', 'coord_y', 'coord_z']]
    coords = coords_df # Rename for visualization

    # Path destination
    carpet = "data"           # Carpet destination
    subcarpet = "processed"   # Subcarpet destination
    name = "coordinates.csv"  # CSV file name
    full_name = f"{carpet}/{subcarpet}/{name}"  
    coords_df.to_csv(full_name, index=False) # Saving pandas DataFrame to CSV
    print(f"Succesfully saved '{name}' in '{carpet}/{subcarpet}'!")

    # Creating 3D map
    viz.coord_graph(coords)

    return

# ========================================================================
# GRAVITY FILE
# ========================================================================
def grav_file(file):
    file = str(file)
    data = pd.read_csv(f"data/raw/{file}")
    gravity = pd.DataFrame(data[['source_id', 'logg_gspphot', 'radius_flame', 'mass_flame', 'flags_flame']])
    gravity = gravity[gravity['flags_flame'].isin([0, 1, 2, 10, 11, 12])].astype({'flags_flame': 'int'})
    gravity = gravity.dropna()
    gravity['gravity'] = 10**(gravity['logg_gspphot']) / 100
    G = 6.67430e-11  # m³/kg/s²
    sun_radius = 6.9634e8  # m
    sun_mass = 1.9884e30  # kg
    gravity['constant_G'] = gravity['gravity'] * (gravity['radius_flame'] * sun_radius)**2 / (gravity['mass_flame'] * sun_mass)
    gravity['G_abs_error'] = np.abs(gravity['constant_G'] - G)
    gravity['G_rel_error_percent'] = gravity['G_abs_error'] / G * 100
    grav_index = pd.Series([i for i in range(1,len(gravity['source_id'])+1)])
    gravity['ID'] = grav_index.values
    gravity_df = gravity[['ID', 'source_id', 'logg_gspphot', 'radius_flame', 'mass_flame',
        'gravity', 'constant_G', 'G_abs_error', 'G_rel_error_percent', 'flags_flame']]
    grav = gravity_df # Rename for visualization

    # Path destination
    carpet = "data"           # Carpet destination
    subcarpet = "processed"   # Subcarpet destination
    name = "gravity.csv"  # CSV file name
    full_name = f"{carpet}/{subcarpet}/{name}"  
    gravity_df.to_csv(full_name, index=False) # Saving pandas DataFrame to CSV
    print(f"Succesfully saved '{name}' in '{carpet}/{subcarpet}'!")

    viz.grav_graph(grav)

    return

# ========================================================================
# HR DIAGRAM FILE
# ========================================================================
def hrd_file(file):
    file = str(file)
    data = pd.read_csv(f"data/raw/{file}")
    hrd = pd.DataFrame(data[['source_id', 'teff_gspphot', 'mg_gspphot', 'ebpminrp_gspphot', 'lum_flame']])
    hrd = hrd.dropna()
    hrd_index = pd.Series([i for i in range(1,len(hrd['source_id'])+1)])
    hrd['ID'] = hrd_index.values
    hrd_df = hrd[['ID', 'source_id', 'teff_gspphot', 'mg_gspphot', 'ebpminrp_gspphot', 'lum_flame']]
    hrd = hrd_df # Rename for visualization

    # Path destination
    carpet = "data"           # Carpet destination
    subcarpet = "processed"   # Subcarpet destination
    name = "hrd.csv"  # CSV file name
    full_name = f"{carpet}/{subcarpet}/{name}"  
    hrd_df.to_csv(full_name, index=False) # Saving pandas DataFrame to CSV
    print(f"Succesfully saved '{name}' in '{carpet}/{subcarpet}'!")

    viz.hrd_graph(hrd)
    
    return