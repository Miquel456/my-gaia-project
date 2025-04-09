import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Crea un conjunt de dades d'exemple
# data = {'Mesos': ['Gener', 'Febrer', 'Març', 'Abril', 'Maig'],
#         'Vendes': [100, 200, 300, 400, 500]}
# df = pd.DataFrame(data)

# Títol del dashboard
st.title('A quick, little view to GAIA DR3')

# # Mostrar la taula
st.write("Gaia is the mission's name of a European Space Agency (ESA) project to study and determinate the position of 2 " \
        "billion stellar objects (2·10^9). Gaia satellite was launched on 19 December 2013 and earn its 'retirement' " \
        "on 27 March 2025 after achieving around 1 PetaByte (1 million GigaBytes) of information. " \
        "The full dataset is composed in three dates or releases: Data Release 1 -- 14 September 2016, " \
        "Data Release 2 -- 25 April 2018 and Data Release 3 -- 13 June 2022")
st.write("That said, here it is collected some parameters and representation of 289.373 unique sources from Gaia Data Release 3 " \
        "(DR3).")


# Filtres interactius
param = ['None','Distance & coordinates', 'Probability', 'Gravity', 'HD Diagram']
st.sidebar.header('GRAPHS')
graph = st.sidebar.selectbox('Choose a parameter to analyze:', param)
if graph == 'None':
    st.image("images/prob_model_dist.png", caption="Probailites model distribution", use_container_width=True)
if graph == 'Distance & coordinates':
    st.image("images/distance_hist.png", caption="Distance Histogram", use_container_width=True)
    st.image("images/3d_projections.png", caption="3D map and their projections", use_container_width=True)
if graph == 'Probability':
    st.image("images/prob_model_dist.png", caption="Probailites model distribution", use_container_width=True)
if graph == 'Gravity':
    st.image("images/constant_g.png", caption="Gravitational constant G best values", use_container_width=True)
if graph == 'HD Diagram':
    st.image("images/hr_diagram.png", caption="Hertzsprung-Russel diagram", use_container_width=True)
# st.write(f'Vendes al mes de {month}: {df[df["Mesos"] == month]["Vendes"].values[0]}')