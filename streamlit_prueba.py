
# 1. Libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import requests
from io import StringIO
import matplotlib.pyplot as plt



# 2. Page Configuration
st.set_page_config(
    page_title="Casa Monarca Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


# ----------------------------------------------------------------------------------------------------------------------
# 3. Data Loading
# PRUEBA. DISPLAY DASHBOARD
url = 'https://raw.githubusercontent.com/PameRuiz25/pruebas/main/kobo_data.csv'
response = requests.get(url)

if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))
    st.write(df)
else:
    st.write("Failed to load data from GitHub.")
# ----------------------------------------------------------------------------------------------------------------------


# 4. Data Processing
# add a new column for year and month
df['year'] = pd.DatetimeIndex(df['Fecha_de_atención']).year
df['month'] = pd.DatetimeIndex(df['Fecha_de_atención']).month


# 5. Sidebar

with st.sidebar:
    st.title('CASA MONARCA')
    
    # 5.1 Filters
    year_values = df.year.unique()
    sorted_year_values = sorted([m for m in year_values if m is not None])
    year_list = [None] + sorted_year_values  # Add None as the default option
    selected_year = st.selectbox('Año de consulta', year_list)

    month_values = df.month.unique()
    sorted_month_values = sorted([m for m in month_values if m is not None])
    month_list = [None] + sorted_month_values  # Add None as the default option
    selected_month = st.selectbox('Mes de consulta', month_list)

    population_list = [None] + sorted(df['Tipo_de_población'].unique())
    selected_population = st.selectbox('Tipo de población', population_list)

if selected_year is not None:
    df_filtered = df[df.year == selected_year]
else:
    df_filtered = df

if selected_month is not None:
    df_filtered = df_filtered[df_filtered.month == selected_month]
else:
    df_filtered = df_filtered

if selected_population is not None:
    df_filtered = df_filtered[df_filtered.Tipo_de_población == selected_population]
else:
    df_filtered = df_filtered



# 6. Data Visualization
# Create three columns
col1, col2 = st.columns(2)
# 6.1 Display total amount of consultations
total_consultations = df_filtered.shape[0]


# 6.3 Display donut chart of percentage of consultations invited in
def make_donut(input_response, input_text):
    chart_color = ['#29b5e8', '#155F7A']

    source = pd.DataFrame({
        "Acceso": ['', input_text],
        "% value": [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Acceso": ['', input_text],
        "% value": [100, 0]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color=alt.Color("Acceso:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)

    text = plot.mark_text(align='center', color=chart_color[0], font="Lato", fontSize=25, fontWeight=700,
                          fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color=alt.Color("Acceso:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)

    return plot_bg + plot + text

# Calculate percentage of allowed access
allowed_percentage = (df_filtered["Acceso_a_Casa_Monarca"] == 1).mean() * 100



with col1:
    st.markdown('##### Registros Totales')
    st.markdown(f'### {total_consultations}')
    st.markdown('##### Porcentaje de Acceso a Casa Monarca')
    st.altair_chart(make_donut(allowed_percentage, 'Acceso permitido'))





# 6.2 Display a line chart for the number of consultations by year
# Assuming df_filtered contains a column 'Fecha_de_atención'
with col2:
    if not df_filtered.empty:
        consultations_by_year = df_filtered.groupby('year').size().reset_index(name='registros')
        line_chart = alt.Chart(consultations_by_year).mark_line(point=True).encode(
            x='year:O',
            y='registros:Q'
        ).properties(
            title='Resgirtos por Año',
            width=500,
            height=300
        )
        st.altair_chart(line_chart)












    

    