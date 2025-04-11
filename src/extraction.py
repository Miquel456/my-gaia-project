from astroquery.gaia import Gaia
import pandas as pd
import src.transformation as trs
import sys

# ========================================================================
# SQL GAIA 3DR QUERY
# ========================================================================
def gaia_query(random = False):
    # MESSAGE FOR RANDOM AND FIXED QUERIES
    wait_rand = ("Querying Gaia DR3 for 500k random sources where parallax > 0\n" 
                "Wait for the job to finish and get the results...")
    wait_fixed = ("Querying Gaia DR3 for 500k fixed sources where parallax > 0\n"
                "Wait for the job to finish and get the results...")
    # RANDOM QUERY OPTION
    if random == True:
        print(wait_rand)
        # GAIA DR3 QUERY TO GET THE DATA FOR THE STARS IN THE MILKY WAY
        query = ("SELECT "
                # LIMIT THE NUMBER TO 500K SOURCES (EVERYTIME WILL BE DIFFERENT)
                "TOP 500000 "
                # COORDINATES PARAMETERS
                "gs.source_id, gs.ref_epoch, gs.ra, gs.dec, gs.parallax, "
                # CLASS PROBABILITIES PARAMETERS
                "ap.classprob_dsc_combmod_quasar, ap.classprob_dsc_combmod_galaxy, ap.classprob_dsc_combmod_star, "
                "ap.classprob_dsc_combmod_whitedwarf, ap.classprob_dsc_combmod_binarystar, ap.classprob_dsc_specmod_quasar, "
                "ap.classprob_dsc_specmod_galaxy, ap.classprob_dsc_specmod_star, ap.classprob_dsc_specmod_whitedwarf, "
                "ap.classprob_dsc_specmod_binarystar, ap.classprob_dsc_allosmod_quasar, ap.classprob_dsc_allosmod_galaxy, "
                "ap.classprob_dsc_allosmod_star, "
                # HR DIAGRAM PARAMETERS
                "ap.teff_gspphot, ap.mg_gspphot, ap.ebpminrp_gspphot, ap.lum_flame, "
                # DISTANCE PARAMETERS
                "ap.distance_gspphot, "
                # STELLAR PARAMETERS
                "ap.logg_gspphot, ap.radius_flame, ap.mass_flame, ap.flags_flame "
                # GAIA_SOURCE TABLE
                "FROM gaiadr3.gaia_source AS gs "
                # ASTROPHYSICAL_PARAMETERS TABLE
                "INNER JOIN gaiadr3.astrophysical_parameters AS ap "
                    "ON gs.source_id = ap.source_id "
                # PARALLAX FILTER
                "WHERE gs.parallax IS NOT NULL AND gs.parallax > 0 "
                )
        # NAME OF THE FILE
        name = 'gaia_raw_random.csv'
    # FIXED QUERY OPTION
    else:
        print(wait_fixed)
        # GAIA DR3 QUERY TO GET THE DATA FOR THE STARS IN THE MILKY WAY
        query = ("SELECT "
                # COORDINATES PARAMETERS
                "gs.source_id, gs.ref_epoch, gs.ra, gs.dec, gs.parallax, "
                # CLASS PROBABILITIES PARAMETERS
                "ap.classprob_dsc_combmod_quasar, ap.classprob_dsc_combmod_galaxy, ap.classprob_dsc_combmod_star, "
                "ap.classprob_dsc_combmod_whitedwarf, ap.classprob_dsc_combmod_binarystar, ap.classprob_dsc_specmod_quasar, "
                "ap.classprob_dsc_specmod_galaxy, ap.classprob_dsc_specmod_star, ap.classprob_dsc_specmod_whitedwarf, "
                "ap.classprob_dsc_specmod_binarystar, ap.classprob_dsc_allosmod_quasar, ap.classprob_dsc_allosmod_galaxy, "
                "ap.classprob_dsc_allosmod_star, "
                # HR DIAGRAM PARAMETERS
                "ap.teff_gspphot, ap.mg_gspphot, ap.ebpminrp_gspphot, ap.lum_flame, "
                # DISTANCE PARAMETERS
                "ap.distance_gspphot, "
                # STELLAR PARAMETERS
                "ap.logg_gspphot, ap.radius_flame, ap.mass_flame, ap.flags_flame "
                # GAIA_SOURCE TABLE
                "FROM gaiadr3.gaia_source AS gs "
                # ASTROPHYSICAL_PARAMETERS TABLE
                "INNER JOIN gaiadr3.astrophysical_parameters AS ap "
                    "ON gs.source_id = ap.source_id "
                # PARALLAX FILTER
                "WHERE gs.parallax IS NOT NULL AND gs.parallax > 0 "
                # FIXED SAMPLE OF SOURCES (WILL GET THE SAME SOURCES EVERYTIME)
                    "AND random_index BETWEEN 0 AND 500000 " 
                )
        # NAME OF THE FILE
        name = 'gaia_raw_fixed.csv'
    
    # MAKE THE QUERY AND SAVE
    job = Gaia.launch_job_async(query)
    # PATH FILE
    carpet = 'data'
    subcarpet = 'raw'
    full_name = f"{carpet}/{subcarpet}/{name}"
    # MESSAGE AFTER FINISHING QUERY AND SAVE THE FILE
    print(f"File '{name}' created in '{carpet}/{subcarpet}' succesfully!")
    job.get_results().to_pandas().to_csv(full_name, index=False)

    # RETURN THE PATH OF THE FILE CREATED
    return name 

# ========================================================================
# FILE TYPE
# ========================================================================
def answer(file):
    while True:
        try:
            # PROBABILITY TRANSFORMATION
            trs.model_file(file)
            # DISTANCE TRANSFORMATION
            trs.dist_file(file)
            # COORDINATES TRANSFORMATION
            trs.coord_file(file)
            # GRAVITY TRANSFORMATION
            trs.grav_file(file)
            # HR DIAGRAM TRANSFORMATION
            trs.hrd_file(file)
            break
        except:
            sys.exit()
    return