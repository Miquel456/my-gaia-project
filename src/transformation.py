import pandas as pd
import numpy as np
import src.visualization as viz


def coord_file(file, graph=False):
    file = str(file)
    data = pd.read_csv(f"data/raw/{file}")
    # Converting data to pandas DataFrame
    coords = pd.DataFrame(data[['source_id', 'ra', 'dec', 'parallax', 'distance_gspphot']]) # 'distance_gspphot' is 
                                                                                            # colected for visualization
    coords = coords.dropna() # Drop NaN values from selected columns
    coords['ra'] = np.radians(coords['ra'])   # Degrees to radians
    coords['dec'] = np.radians(coords['dec']) # Degrees to radians
    # Conversion coordinates
    coords['coord_x'] = 1000*np.cos(coords['dec'])*np.cos(coords['ra'])/coords['parallax'] # X coordinate conversion
    coords['coord_y'] = 1000*np.cos(coords['dec'])*np.sin(coords['ra'])/coords['parallax'] # Y coordinate conversion
    coords['coord_z'] = 1000*np.sin(coords['dec'])/coords['parallax']                      # Z coordinate conversion
    coord_index = pd.Series([i for i in range(1,len(coords['source_id'])+1)])
    coords['ID'] = coord_index.values # Index column
    coords = coords[['ID', 'source_id', 'ra', 'dec', 'parallax',    # Order and reselect columns
        'coord_x', 'coord_y', 'coord_z', 'distance_gspphot']]
    # Path destination
    carpet = "data"           # Carpet destination
    subcarpet = "processed"   # Subcarpet destination
    name = "coordinates.csv"  # CSV file name
    full_name = f"{carpet}/{subcarpet}/{name}"  
    coords.to_csv(full_name, index=False) # Saving pandas DataFrame to CSV
    print(f"Succesfully saved '{name}' in '{carpet}/{subcarpet}'!")

    # Choice of having 3D map in one step
    if graph == True:
        pass
    else:
        return full_name