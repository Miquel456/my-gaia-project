import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Crea un conjunt de dades d'exemple
# data = {'Mesos': ['Gener', 'Febrer', 'Març', 'Abril', 'Maig'],
#         'Vendes': [100, 200, 300, 400, 500]}
# df = pd.DataFrame(data)

# Títol del dashboard
st.title('GAIA DR3 Dashboard')

# # Mostrar la taula
st.write('Some images')

# # Gràfic de línies
# # st.subheader('Gràfic de les vendes per mesos')
st.image("images/prob_model_dist.png", caption="Probailites model distribution", use_container_width=True)
# fig, ax = plt.subplots()
# ax.plot(df['Mesos'], df['Vendes'])
# st.pyplot(fig)

# Filtres interactius
# st.sidebar.header('Filtres')
# month = st.sidebar.selectbox('Escull un mes', df['Mesos'])
# st.write(f'Vendes al mes de {month}: {df[df["Mesos"] == month]["Vendes"].values[0]}')