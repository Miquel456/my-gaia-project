import streamlit as st
import pandas as pd

# URLS FOR IMAGE. MAKE SURE TO HAVE INTERNET CONNECTION
image1 = "https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2022/06/gaia_observes_the_milky_way/24305944-1-eng-GB/Gaia_observes_the_Milky_Way_pillars.jpg"
image2 = "https://www.esa.int/var/esa/storage/images/science_exploration/space_science/gaia/19716907-3-eng-GB/Gaia_pillars.jpg"
# STREAMLIT FORMAT
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{image1}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* For all streamlit widgets and elements */
    html, body, [class^="css"] {{
        color: green !important;
        font-family: 'Arial', sans-serif;
    }}

    h1, h2, h3, h4, h5, h6{{
        color: white !important;
    }}

    p {{
        color: white !important;
    }}
    .stMarkdown {{
        color: white !important;
    }}
    section[data-testid="stSidebar"] {{
        background-image: url("{image2}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        }}
    
    </style>
    """,
    unsafe_allow_html=True
)

# DASHBOARD TITLE
st.title('A quick, little view to GAIA DR3')

# DESCRIPTION
st.write("Gaia is the mission's name of the European Space Agency (ESA) project to study and determinate the position of 2 " \
        "billion or 2·10^9 stellar objects. Gaia's satellite was launched on 19 December 2013 and earn its 'retirement' " \
        "on 27 March 2025 after achieving around 1 PetaByte (1 million GigaBytes) of information. " \
        "The full dataset is composed of three datas or releases: Data Release 1 -- 14 September 2016, " \
        "Data Release 2 -- 25 April 2018 and Data Release 3 -- 13 June 2022.")
st.write("That said, here it is collected some parameters and representation of 289.373 unique sources from Gaia Data Release 3 " \
        "(DR3).")

# PARAMETERS FOR PROBABILITY MODEL
file = pd.read_csv(f"data/processed/model_class.csv")
prob_model_numb = len(file['ID'])
comb_quasar_avg = (f"Combmod ==> {round(file["classprob_dsc_combmod_quasar"].mean()*100,3)}%")
spec_quasar_avg = (f"Specmod ==> {round(file["classprob_dsc_specmod_quasar"].mean()*100,3)}%")
allos_quasar_avg = (f"Allosmod ==> {round(file["classprob_dsc_allosmod_quasar"].mean()*100,3)}%")
comb_galaxy_avg = (f"Combmod ==> {round(file["classprob_dsc_combmod_galaxy"].mean()*100,3)}%")
spec_galaxy_avg = (f"Specmod ==> {round(file["classprob_dsc_specmod_galaxy"].mean()*100,3)}%")
allos_galaxy_avg = (f"Allosmod ==> {round(file["classprob_dsc_allosmod_galaxy"].mean()*100,3)}%")
comb_star_avg = (f"Combmod ==> {round(file["classprob_dsc_combmod_star"].mean()*100,3)}%")
spec_star_avg = (f"Specmod ==> {round(file["classprob_dsc_specmod_star"].mean()*100,3)}%")
allos_star_avg = (f"Allosmod --> {round(file["classprob_dsc_allosmod_star"].mean()*100,3)}%")
comb_whitedwarf_avg = (f"Combmod ==> {round(file["classprob_dsc_combmod_whitedwarf"].mean()*100,3)}%")
spec_whitedwarf_avg = (f"Specmod ==> {round(file["classprob_dsc_specmod_whitedwarf"].mean()*100,3)}%")
comb_binarystar_avg = (f"Combmod ==> {round(file["classprob_dsc_combmod_binarystar"].mean()*100,3)}%")
spec_binarystar_avg = (f"Specmod ==> {round(file["classprob_dsc_specmod_binarystar"].mean()*100,3)}%")
#PARAMETERS FOR DISTANCE
file = pd.read_csv(f"data/processed/distance.csv")
dist_numb = len(file['distance_gspphot'])
dist_avg = round(file['distance_gspphot'].mean(),2)
dist_std = round(file['distance_gspphot'].std(),2)
# PARAMETERS FOR COORDINATES
file = pd.read_csv(f"data/processed/coordinates.csv")
coord_ref_epoch = str(file['ref_epoch'].unique()[0])
# PARAMETERS FOR GRAVITY
file = pd.read_csv(f"data/processed/gravity.csv")
grav_numb = len(file['ID'])
grav_numb_ntr = len(file['flags_flame'].isin([0, 1, 2]))
grav_numb_giant = len(file['flags_flame'].isin([10, 11, 12]))
# PARAMETERS FOR HR DIAGRAM
file = pd.read_csv(f"data/processed/hrd.csv")
hrd_numb = len(file['ID'])
# SIDEBAR OPERATIONS
param = ['None','Method','Probability', 'Distance & coordinates', 'Gravity', 'HD Diagram','Extra']
st.sidebar.header('MENU')
st.sidebar.subheader('Results')
graph = st.sidebar.selectbox('Choose a parameter to analyze:', param)
# METHOD OPTION
if graph == param[1]:
    st.subheader(f"{param[1].upper()}")
    # VIDEO DESCRIPTION
    st.write("A Python program runs the query to Astroquery API asking for 500k sources with some parameters from 'gaia_source' and " \
        "'astrophysical_parameters' tables with the condition that sources have 'parallax' > 0. First, the program asks if we have " \
        "a 'cvs' file to give. The first time it should be answered negatively by pressing 'n'. After that, the program suggests to generate " \
        "a query with random sources. Every time it is choosed for random query, the results will differ. Nonetheless, if it is decided to be " \
        "conservative, every time the program runs rejecting the random query, the results will always be the same. Feel free to explore." \
    )
    st.video("images/running_program.mp4")
    st.caption("Video 1. Running the main program")
    # RELATIONAL TABLE DESCRIPTION
    st.write("Once the answers are selected, the program will generate 6 'csv' files: one main file that recopiles all the sources " \
        "of the query. Then, the others files are created according to the objective of the data selected, as Figure 1 shows below. " \
        "At the same time, graphs are generated to visualize the results.")
    st.image("images/database_relation.png", caption="Figure 1. Representation of relational tables made.", use_container_width=True)
# PROBABILITY OPTION
if graph == param[2]:
    st.subheader(f"{param[2].upper()}")
    # PROBABILITY DESCRIPTION
    st.write("Collecting the probability of the differents Discrete Source Classifiers (DSC): Specmod, Allosmod and Combmod, " \
        "it is generated a stripplot (see Figure 2) for every class possibility: Quasar, Galaxy, Star, White Dwarf and Binary Star. " \
        f"The total of sources collected is {prob_model_numb}.")
    st.image("images/prob_model_dist.png", caption="Figure 2. Probabilites model distribution. Red corresponds to DSC-Combmod, " \
        "green corresponds to DSC-Specmod and blue to DSC-Allosmod.", use_container_width=True)
    # PROBABILITY MEAN VALUES
    st.write("For quasars, the average for every DSC is:")
    st.markdown(f"- {comb_quasar_avg}.\n" \
                f"- {spec_quasar_avg}.\n" \
                f"- {allos_quasar_avg}.")
    st.write("For galaxies, the average for every DSC is:")
    st.markdown(f"- {comb_galaxy_avg}.\n" \
                f"- {spec_galaxy_avg}.\n" \
                f"- {allos_galaxy_avg}.")
    st.write("For stars, the average for every DSC is:")
    st.markdown(f"- {comb_star_avg}.\n" \
                f"- {spec_star_avg}.\n" \
                f"- {allos_star_avg}.")
    st.write("For white dwarfs, the average for every DSC is:")
    st.markdown(f"- {comb_whitedwarf_avg}.\n" \
                f"- {spec_whitedwarf_avg}.")
    st.write("For binary stars, the average for every DSC is:")
    st.markdown(f"- {comb_binarystar_avg}.\n" \
                f"- {spec_binarystar_avg}.")
# DISTANCE & COORDINATES OPTION
if graph == param[3]:
    st.subheader(f"{param[3].upper()}")
    # DISTANCE DESCRIPTION
    st.write(f"Looking at distance modulus of {dist_numb} objects, it is found the following histogram distribution " \
             f"plotted in Figure 3, with an average distance of {dist_avg} parsecs or {round(dist_avg*3.26,2)} light-years, where " \
             f"the standard deviation is {dist_std} parsecs or {round(dist_std*3.26,2)} light-years.")
    st.image("images/distance_hist.png", caption="Figure 3. Distance histogram of the stellar objects", use_container_width=True)
    # COORDINATES DESCRIPTION
    st.write("After calculating the conversion between coordinates of right ascension (RA), declination (DEC) and parallax, " \
            f"with reference epoch {coord_ref_epoch}, to cartesian coordinates X, Y and Z, it is represented a 3D map allong " \
            "with their projections: plant, section and elevation. The results are showed in Figure 4.")
    st.image("images/3d_projections.png", caption="Figure 4. 3D map and their projections. From left to right "
            "and top to bottom: 3D, plant (XY), elevation (XZ) and section (YZ).", use_container_width=True)
# GRAVITY OPTION
if graph == param[4]:
    st.subheader(f"{param[4].upper()}")
    # GRAVITY DESCRIPTION
    st.write("Whit the second law of motions that relates gravity, mass, distance and the gravitational constant G with a " \
        "value of 6.67430e-11 [m³/kg/s²], it is tried to find the value of this universal constant using the values " \
        f"measured and collected in DR3. A total of {grav_numb} objects considered as stars, where {grav_numb_ntr} " \
        f"stars have no objetion on their properties (firts digit = 0) whereas {grav_numb_giant} stars are considered Giants " \
        " (first digit = 1) and their mass has an uncertainty of 20-30%. Furthermore, for calculating their properties " \
        "such as gravity or mass, some parameters are used over others, for instance, there are some stars that " \
        "use parallax (second digit = 0), others use distance modulus (second digit = 1) and parallax again " \
        "due to convergence problems with distance modulus (second digit = 2). Notice that distance modulus is " \
        "used for calculating the square power of the distance in the law of motion. In Figure 5, only those values " \
        "of the constant G which the relative error are lower than 5% are represented.")
    st.image("images/constant_g.png", caption="Figure 5. Gravitational constant G values of stars (left) and Giants (right) "
        "where the black vertical line corresponds to G = 6.67430e-11 [m³/kg/s²].", use_container_width=True)
# HR DIAGRAM OPTION
if graph == param[5]:
    st.subheader(f"{param[5].upper()}")
    # HR DIAGRAM DESCRIPTION
    st.write(f"Lastly, Figure 6 pictures a map bin for over {hrd_numb} astronomical objects comparing their absolute magnitude " \
        " G with their redding E(GBP -GRP). Moreover, it is painted the regions where Giants, White Dwarfs and Stars " \
        "in the Main Sequence can be found.")
    st.image("images/hr_diagram.png", caption="Figure 6. Hexagonal bin map or Hertzsprung-Russel diagram. Red rectangle " \
        "is the region for Giant stars, cyan rectangle for Main Sequence Stars and green rectangle for" \
        "White Dwarfs", use_container_width=True)
# EXTRA OPTION
if graph == param[6]:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    # NOTIFICATION/WARNING
    st.subheader("NOTE:")
    st.write("These results should not be considered as a reliable, thrustful data but could be seeing as a model to follow and " \
        "represent data from DR3. Any suggestions for improvement will be welcome!")