# A LITTLE, QUICK VIEW TO GAIA DR3 PROJECT

## INTRODUCTION

This project aims to make a general observation on the data that the European Space Agency's Gaia mission has collected in its third release: Gaia Data Release 3 (DR3).

Using ASTROQUERY API for Python (https://astroquery.readthedocs.io/en/latest/index.html), the program asks a query to two tables from Gaia TAP+ (https://astroquery.readthedocs.io/en/latest/gaia/gaia.html): 'gaia_source' and 'astrophysical_parameters'. NOTE: Look at INSTRUCTIONS part to run the 'main.py' program and Streamlit App 'dash.py' correctly.

### TABLE 'gaia_source':
- URL = 'https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html'
- Parameters/columns:

    • source_id : Unique source identifier (unique within a particular Data Release) (long)

    • ref_epoch : Reference epoch (double, Time[Julian Years])

    • ra : Right ascension (double, Angle[deg])

    • dec : Declination (double, Angle[deg])

    • parallax : Parallax (double, Angle[mas] )

### TABLE 'astrophysical_parameters':
- URL = 'https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_astrophysical_parameter_tables/ssec_dm_astrophysical_parameters.html'
- Parameters/columns:

    • source_id : Source Identifier (long)

    • classprob_dsc_combmod_quasar : Probability from DSC-Combmod of being a quasar (data used: BP/RP spectrum, photometry, astrometry) (float)

    • classprob_dsc_combmod_galaxy : Probability from DSC-Combmod of being a galaxy (data used: BP/RP spectrum, photometry, astrometry) (float)

    • classprob_dsc_combmod_star : Probability from DSC-Combmod of being a single star (but not a white dwarf) (data used: BP/RP spectrum, photometry, astrometry) (float)

    • classprob_dsc_combmod_whitedwarf : Probability from DSC-Combmod of being a white dwarf (data used: BP/RP spectrum, photometry, astrometry) (float)

    • classprob_dsc_combmod_binarystar : Probability from DSC-Combmod of being a binary star (data used: BP/RP spectrum, photometry, astrometry) (float)

    • classprob_dsc_specmod_quasar : Probability from DSC-Specmod of being a quasar (data used: BP/RP spectrum) (float)

    • classprob_dsc_specmod_galaxy : Probability from DSC-Specmod of being a galaxy (data used: BP/RP spectrum) (float)

    • classprob_dsc_specmod_star : Probability from DSC-Specmod of being a single star (but not a white dwarf) (data used: BP/RP spectrum) (float)

    • classprob_dsc_specmod_whitedwarf : Probability from DSC-Specmod of being a white dwarf (data used: BP/RP spectrum) (float)

    • classprob_dsc_specmod_binarystar : Probability from DSC-Specmod of being a binary star (data used: BP/RP spectrum) (float)

    • classprob_dsc_allosmod_quasar : Probability from DSC-Allosmod of being a quasar (data used: photometry, astrometry) (float)

    • classprob_dsc_allosmod_galaxy : Probability from DSC-Allosmod of being a galaxy (data used: photometry, astrometry) (float)

    • classprob_dsc_allosmod_star : Probability from DSC-Allosmod of being a star (data used: photometry, astrometry) (float)

    • teff_gspphot : Effective temperature from GSP-Phot Aeneas best library using BP/RP spectra (float, Temperature[K])

    • logg_gspphot : Surface gravity from GSP-Phot Aeneas best library using BP/RP spectra (float, GravitySurface[log cgs])

    • distance_gspphot : Distance from GSP-Phot Aeneas best library using BP/RP spectra (float, Length & Distance[pc])

    • ebpminrp_gspphot : Reddening E(GBP−GRP) from GSP-Phot Aeneas best library using BP/RP spectra (float, Magnitude[mag])

    • mg_gspphot : Absolute magnitude MG from GSP-Phot Aeneas best library using BP/RP spectra (float, Magnitude[mag])

    • lum_flame : Luminosity of the star from FLAME using G band magnitude, extinction (ag_gspphot), parallax or distance, and a bolometric correction bc_flame (float, Luminosity[Solar Luminosity])

    • radius_flame : Radius of the star from FLAME using teff_gspphot and lum_flame (float, Length & Distance[Solar Radius])

    • mass_flame : Mass of the star from FLAME using stellar models, lum_flame, and teff_gspphot (float, Mass[Solar Mass])

    • flags_flame : Flags indicating quality and processing information from FLAME (string)

## HYPOTHESIS
### HYPOTHESIS 1
#### The values ​​of the models of the probability of cataloging different objects, in general, should be the same or similar.
- To find the results, a stripplot is generated for each class: Quasar, Galaxy, Star, White Dwarf and Binary Star. The visualization is located in the Streamlit dashboard.
### HYPOTHESIS 2
#### The distances, in module, will be large and with a lot of dispersion.
- Generating an histogram, it can be found stadistical information in search of mean value and standar deviation. The visualization is located in the Streamlit dashboard.
### HYPOTHESIS 3
#### With such scattered distances, it is to be expected that their Cartesian coordinates will also be scattered.
- According to that hypothesis, a 3D map with their projections would show disperse sources. The visualization is located in the Streamlit dashboard.
### HYPOTHESIS 4
#### The calculus for the mass and distance are validated through the Second Law of Motion and being reliable.
- Using the Second Law of Motion: gravity_surface = universal_constant_g * mass / distance**2 and values for mass, gravity_surface and distance it is calculated the value for universal_constant_g. The closer the value the better the value would be. The visualization is located in the Streamlit dashboard.
### HYPOTHESIS 5
#### A Hertzsprung-Russell Diagram can be plotted and shows a clearly figure of the evolution stage of the different sources.
- Making a hexagonal bin map, it is figured the quantity of sources analysed in the different regions as Main Sequence, Giants or White Dwarfs.

## INSTRUCTIONS
### Running the program
0. Check the video 'running_program.mp4' in images carpet for a quick look.
1. To begin, open the Terminal and activate the environment in the project path.
2. Second, run the main program as 'python main.py'.
3. The next step is answer the questions 'main.py' asks. The first question: "Do you have Gaia DR3 data? [y/n]:" input a 'n' the every first time the program runs. After that, a second question pops up: "A 500k random sources? [y/n]:". Here, it is up to the protagonist to decide which answer ('y'/'n') would want. Mention that for a random sources, the dataset generated will not always be the same, with the exception of a fixed dataset by answering with 'n'.
4. After these inputs, the program will created a main table with all columns explained above saved as a CSV file named 'gaia_raw_fixed.csv' or 'gaia_raw_random.csv'. Immediately, another 5 tables are generated: 'model_class.csv', 'distance.csv', 'coordinates.csv', 'gravity.csv' and 'hrd.csv'. Once a table is saved, graphs are plotted and saves as: 'prob_model_dist.png', 'distance_hist.png', '3d_projections.png', 'constant_g.png' and 'hr_diagram.png', respectively.

For fixed results, respectively:

![image](https://raw.githubusercontent.com/Miquel456/my-gaia-project/refs/heads/main/images/prob_model_dist.png?token=GHSAT0AAAAAADBZ6URGYBH5MELA4MDDOVV4Z7ZDW6Q)

![image](https://raw.githubusercontent.com/Miquel456/my-gaia-project/refs/heads/main/images/distance_hist.png?token=GHSAT0AAAAAADBZ6URGQHC2VIGDT6ZY6DPKZ7ZDWWQ)

![image](https://raw.githubusercontent.com/Miquel456/my-gaia-project/refs/heads/main/images/3d_projections.png?token=GHSAT0AAAAAADBZ6URHJWDWNXBRCNO5MY7OZ7ZDWMQ)

![image](https://raw.githubusercontent.com/Miquel456/my-gaia-project/refs/heads/main/images/constant_g.png?token=GHSAT0AAAAAADBZ6URGIKR32JVLBDCPPLCWZ7ZDWAA)

![image](https://raw.githubusercontent.com/Miquel456/my-gaia-project/refs/heads/main/images/hr_diagram.png?token=GHSAT0AAAAAADBZ6URHLT4LIGUQELMRF5MWZ7ZDVWA)

The relation between tables are represented in 'database_relation.png' in 'images' carpet.

![image](https://raw.githubusercontent.com/Miquel456/my-gaia-project/refs/heads/main/images/database_relation.png?token=GHSAT0AAAAAADBZ6URG3BKXISINORVPICWEZ7ZDPIQ)

5. Once every file and every plot is saved, the program returns to the first question. Input 'exit' to close the program. NOTE: generating another dataset rewrites the previous results, losing them.
6. Now, it is time to visualize the results. In the terminal, write 'streamlit run dash.py'. It will redirect to an interactive Internet page. NOTE: make sure to have Internet connection. Otherwise, background images will not show.
7. Feel free to explore! On the sidebar (left) there is an option to choose the different results.
8. To leave and close Streamlit App, in the terminal press 'Ctrl'+'C' and close the Internet window.



## REFERENCES
• Gaia Collaboration et al. (2016b): The Gaia mission (provides a description of the Gaia mission including spacecraft, instruments, survey and measurement principles, and operations)

• Gaia Collaboration et al. (2023j): Gaia DR3: Summary of the contents and survey properties.

This work has made use of data from the European Space Agency (ESA) mission Gaia (https://www.cosmos.esa.int/gaia), processed by the Gaia Data Processing and Analysis Consortium (DPAC, https://www.cosmos.esa.int/web/gaia/dpac/consortium). Funding for the DPAC has been provided by national institutions, in particular the institutions participating in the Gaia Multilateral Agreement.