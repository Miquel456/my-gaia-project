from astroquery.gaia import Gaia
import pandas as pd

def gaia_query(random = False):

    wait_rand = ("Querying Gaia DR3 for 1 million random sources where parallax > 0\n" 
                "Wait for the job to finish and get the results...")
    wait_fixed = ("Querying Gaia DR3 for 1 million fixed sources where parallax > 0\n"
                "Wait for the job to finish and get the results...")
    
    if random == True:
        print(wait_rand)
        # Gaia DR3 query to get the data for the stars in the Milky Way
        query = ("SELECT "
                "TOP 1000000 " # Limit the number of sources to 1 million
                "gs.source_id, gs.ref_epoch, gs.ra, gs.dec, gs.parallax, " # Coordinates
                "ap.classprob_dsc_combmod_quasar, ap.classprob_dsc_combmod_galaxy, ap.classprob_dsc_combmod_star, "
                "ap.classprob_dsc_combmod_whitedwarf, ap.classprob_dsc_combmod_binarystar, ap.classprob_dsc_specmod_quasar, "
                "ap.classprob_dsc_specmod_galaxy, ap.classprob_dsc_specmod_star, ap.classprob_dsc_specmod_whitedwarf, "
                "ap.classprob_dsc_specmod_binarystar, ap.classprob_dsc_allosmod_quasar, ap.classprob_dsc_allosmod_galaxy, "
                "ap.classprob_dsc_allosmod_star, " # Class probabilities
                "ap.teff_gspphot, ap.mg_gspphot, ap.ebpminrp_gspphot, ap.lum_flame, " # HRD parameters
                "ap.distance_gspphot, " # Distance
                "ap.logg_gspphot, ap.radius_flame, ap.mass_flame, ap.flags_flame " # Stellar parameters
                "FROM gaiadr3.gaia_source AS gs " # Gaia source table
                "INNER JOIN gaiadr3.astrophysical_parameters AS ap " # Astrophysical parameters table
                    "ON gs.source_id = ap.source_id "
                "WHERE gs.parallax IS NOT NULL AND gs.parallax > 0 " # Parallax filter
                )
        name = 'gaia_raw_random.csv'
    else:
        print(wait_fixed)
        # Gaia DR3 query to get the data for the stars in the Milky Way
        query = ("SELECT "
                "gs.source_id, gs.ref_epoch, gs.ra, gs.dec, gs.parallax, " # Coordinates
                "ap.classprob_dsc_combmod_quasar, ap.classprob_dsc_combmod_galaxy, ap.classprob_dsc_combmod_star, "
                "ap.classprob_dsc_combmod_whitedwarf, ap.classprob_dsc_combmod_binarystar, ap.classprob_dsc_specmod_quasar, "
                "ap.classprob_dsc_specmod_galaxy, ap.classprob_dsc_specmod_star, ap.classprob_dsc_specmod_whitedwarf, "
                "ap.classprob_dsc_specmod_binarystar, ap.classprob_dsc_allosmod_quasar, ap.classprob_dsc_allosmod_galaxy, "
                "ap.classprob_dsc_allosmod_star, " # Class probabilities
                "ap.teff_gspphot, ap.mg_gspphot, ap.ebpminrp_gspphot, ap.lum_flame, " # HRD parameters
                "ap.distance_gspphot, " # Distance
                "ap.logg_gspphot, ap.radius_flame, ap.mass_flame, ap.flags_flame " # Stellar parameters
                "FROM gaiadr3.gaia_source AS gs " # Gaia source table
                "INNER JOIN gaiadr3.astrophysical_parameters AS ap " # Astrophysical parameters table
                    "ON gs.source_id = ap.source_id "
                "WHERE gs.parallax IS NOT NULL AND gs.parallax > 0 " # Parallax filter
                    "AND random_index BETWEEN 0 AND 1000000 " # Fixed sample of sources (Will get the same sources every time)
                )
        name = 'gaia_raw_fixed.csv'
    

    job = Gaia.launch_job_async(query) # Make the query and saved
    carpet = 'data'
    subcarpet = 'raw'
    full_name = f"{carpet}/{subcarpet}/{name}"

    print(f"File '{name}' created in '{carpet}/{subcarpet}' succesfully!")

    job.get_results().to_pandas().to_csv(full_name, index=False) # Save the results to a csv file
    return name # Return the path of the file created