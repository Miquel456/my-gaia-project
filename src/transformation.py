import pandas as pd
import numpy as np
import src.visualization as viz

# ========================================================================
# MODEL PROBABILITIES FILE
# ========================================================================
def model_file(file):
    # READING THE FILE
    file = str(file)
    data = pd.read_csv(f"data/raw/{file}")
    # CREATING A DATAFRAME
    model_class = pd.DataFrame(data[[ 'source_id', 
        # COMB MODEL PARAMETERS
        'classprob_dsc_combmod_quasar', 'classprob_dsc_combmod_galaxy', 
            'classprob_dsc_combmod_star', 'classprob_dsc_combmod_whitedwarf', 'classprob_dsc_combmod_binarystar',
        # SPEC MODEL PARAMETERS
        'classprob_dsc_specmod_quasar', 'classprob_dsc_specmod_galaxy', 'classprob_dsc_specmod_star', 
            'classprob_dsc_specmod_whitedwarf', 'classprob_dsc_specmod_binarystar',
        # ALLOS MODEL PARAMETERS
        'classprob_dsc_allosmod_quasar', 'classprob_dsc_allosmod_galaxy', 'classprob_dsc_allosmod_star']])
    # DROPPING NULLS
    model_class = model_class.dropna()
    # 'ID' COLUMN
    mod_clas_index = pd.Series([i for i in range(1,len(model_class['source_id'])+1)])
    model_class['ID'] = mod_clas_index.values
    # MODIFYING DATAFRAME TO ADD 'ID' COLUMN
    model_class_df = model_class[['ID', 'source_id', 
        'classprob_dsc_combmod_quasar', 'classprob_dsc_combmod_galaxy', 
            'classprob_dsc_combmod_star', 'classprob_dsc_combmod_whitedwarf', 'classprob_dsc_combmod_binarystar', 
        'classprob_dsc_specmod_quasar', 'classprob_dsc_specmod_galaxy', 'classprob_dsc_specmod_star', 
            'classprob_dsc_specmod_whitedwarf', 'classprob_dsc_specmod_binarystar', 
        'classprob_dsc_allosmod_quasar', 'classprob_dsc_allosmod_galaxy', 'classprob_dsc_allosmod_star']]
    
    # RENAME FOR VISUALIZATION
    model = model_class_df 

    # PATH DESTINATION
    carpet = "data"           
    subcarpet = "processed"   
    name = "model_class.csv"  
    full_name = f"{carpet}/{subcarpet}/{name}"  
    # SAVING PANDAS DATAFRAME TO CSV FILE
    model_class_df.to_csv(full_name, index=False)
    print(f"Succesfully saved '{name}' in '{carpet}/{subcarpet}'!")

    # CREATING STRIPPLOT GRAPH
    viz.model_graph(model)
    
    return

# ========================================================================
# DISTANCE FILE
# ========================================================================
def dist_file(file):
    # READING THE FILE
    file = str(file)
    data = pd.read_csv(f"data/raw/{file}")
    # CREATING A DATAFRAME
    distance = pd.DataFrame(data[['source_id', 'distance_gspphot']])
    # DROPPING NULLS
    distance = distance.dropna()
    # 'ID' COLUMN
    dist_index = pd.Series([i for i in range(1,len(distance['source_id'])+1)])
    distance['ID'] = dist_index.values
    # MODIFYING DATAFRAME TO ADD 'ID' COLUMN
    distance_df = distance[['ID', 'source_id', 'distance_gspphot']]
    # RENAME FOR VISUALIZATION
    dist = distance_df 

    # PATH DESTINATION
    carpet = "data"           
    subcarpet = "processed"   
    name = "distance.csv"     
    full_name = f"{carpet}/{subcarpet}/{name}"
    # SAVING PANDAS DATAFRAME TO CSV FILE
    distance_df.to_csv(full_name, index=False)
    print(f"Succesfully saved '{name}' in '{carpet}/{subcarpet}'!")

    # CREATING DISTANCE HISTOGRAM
    viz.dist_graph(dist)

    return

# ========================================================================
# COORDINATES FILE 
# ========================================================================
def coord_file(file):
    # READING THE FILE
    file = str(file)
    data = pd.read_csv(f"data/raw/{file}")
    # CREATING A DATAFRAME
    coords = pd.DataFrame(data[['source_id','ref_epoch','ra', 'dec', 'parallax']])   
    # DROPPING NULLS                                                                                         
    coords = coords.dropna()
    # CONVERSION OF DEGREES TO RADIANS
    coords['ra'] = np.radians(coords['ra'])   
    coords['dec'] = np.radians(coords['dec']) 
    # CONVERSION OF COORDINATES
    # X CONVERSION
    coords['coord_x'] = 1000*(np.cos(coords['dec']))*(np.cos(coords['ra']))/(coords['parallax'])
    # Y CONVERSION
    coords['coord_y'] = 1000*(np.cos(coords['dec']))*(np.sin(coords['ra']))/(coords['parallax'])
    # Z CONVERSION
    coords['coord_z'] = 1000*(np.sin(coords['dec']))/(coords['parallax'])
    # 'ID' COLUMN
    coord_index = pd.Series([i for i in range(1,len(coords['source_id'])+1)])
    coords['ID'] = coord_index.values
    # MODIFYING DATAFRAME TO ADD 'ID', 'coord_x', 'coord_y' AND 'coord_z' COLUMNS AND ORDER COLUMNS
    coords_df = coords[['ID', 'source_id','ref_epoch', 'ra', 'dec', 'parallax',
        'coord_x', 'coord_y', 'coord_z']]
    # RENAME FOR VISUALIZATION
    coords = coords_df

    # PATH DESTINATION
    carpet = "data"           
    subcarpet = "processed"   
    name = "coordinates.csv"  
    full_name = f"{carpet}/{subcarpet}/{name}"  
    # SAVING PANDAS DATAFRAME TO CSV FILE
    coords_df.to_csv(full_name, index=False) 
    print(f"Succesfully saved '{name}' in '{carpet}/{subcarpet}'!")

    # CREATING 3D MAP
    viz.coord_graph(coords)

    return

# ========================================================================
# GRAVITY FILE
# ========================================================================
def grav_file(file):
    # READING THE FILE
    file = str(file)
    data = pd.read_csv(f"data/raw/{file}")
    # CREATING A DATAFRAME
    gravity = pd.DataFrame(data[['source_id', 'logg_gspphot', 'radius_flame', 'mass_flame', 'flags_flame']])
    # FILTER 'flags_FLAME' IN ORDER TO DISCARD 20, 21 AND 22 VALUES
    gravity = gravity[gravity['flags_flame'].isin([0, 1, 2, 10, 11, 12])].astype({'flags_flame': 'int'})
    # DROPPING NULLS
    gravity = gravity.dropna()
    # RECALCULATE GRAVITY PARAMETER
    gravity['gravity'] = 10**(gravity['logg_gspphot']) / 100
    # VALUE OF G CONSTANT
    G = 6.67430e-11  # m³/kg/s²
    # VALUE OF SUN RADII
    sun_radius = 6.9634e8  # m
    # VALUE OF SUN MASS
    sun_mass = 1.9884e30  # kg
    # CALCULATING CONTANT G FOR EVERY SOURCE
    gravity['constant_g'] = gravity['gravity'] * (gravity['radius_flame'] * sun_radius)**2 / (gravity['mass_flame'] * sun_mass)
    # CALCULATING ABSOLUTE ERROR
    gravity['g_abs_error'] = np.abs(gravity['constant_g'] - G)
    # CALCULATING RELATIVE ERROR IN PERCENT
    gravity['g_rel_error_percent'] = gravity['g_abs_error'] / G * 100
    # 'ID' COLUMN
    grav_index = pd.Series([i for i in range(1,len(gravity['source_id'])+1)])
    gravity['ID'] = grav_index.values
    # MODIFYING DATAFRAME TO ADD 'ID', 'gravity', 'constant_g', 'g_abs_error' AND 'G_rel_error_percent' COLUMNS AND ORDER COLUMNS
    gravity_df = gravity[['ID', 'source_id', 'logg_gspphot', 'radius_flame', 'mass_flame',
        'gravity', 'constant_g', 'g_abs_error', 'g_rel_error_percent', 'flags_flame']]
    # RENAME FOR VISUALIZATION
    grav = gravity_df

    # PATH DESTINATION
    carpet = "data"           
    subcarpet = "processed"   
    name = "gravity.csv"  
    full_name = f"{carpet}/{subcarpet}/{name}"  
    # SAVING PANDAS DATAFRAME TO CSV FILE
    gravity_df.to_csv(full_name, index=False)
    print(f"Succesfully saved '{name}' in '{carpet}/{subcarpet}'!")

    # GRAVITY DISPERSION GRAPH
    viz.grav_graph(grav)

    return

# ========================================================================
# HR DIAGRAM FILE
# ========================================================================
def hrd_file(file):
    # READING THE FILE
    file = str(file)
    data = pd.read_csv(f"data/raw/{file}")
    # CREATING A DATAFRAME
    hrd = pd.DataFrame(data[['source_id', 'teff_gspphot', 'mg_gspphot', 'ebpminrp_gspphot', 'lum_flame']])
    # DROPPING NULLS
    hrd = hrd.dropna()
    # 'ID' COLUMN
    hrd_index = pd.Series([i for i in range(1,len(hrd['source_id'])+1)])
    hrd['ID'] = hrd_index.values
    # MODIFYING DATAFRAME TO ADD 'ID' COLUMN
    hrd_df = hrd[['ID', 'source_id', 'teff_gspphot', 'mg_gspphot', 'ebpminrp_gspphot', 'lum_flame']]
    # RENAME FOR VISUALIZATION
    hrd = hrd_df

    # PATH DESTINATION
    carpet = "data"           
    subcarpet = "processed"   
    name = "hrd.csv"  
    full_name = f"{carpet}/{subcarpet}/{name}"  
    # SAVING PANDAS DATAFRAME TO CSV FILE
    hrd_df.to_csv(full_name, index=False) 
    print(f"Succesfully saved '{name}' in '{carpet}/{subcarpet}'!")

    # HR DIAGRAM GRAPH
    viz.hrd_graph(hrd)
    
    return