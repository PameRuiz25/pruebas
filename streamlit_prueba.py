
# 1. Libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import requests
from io import StringIO
import matplotlib.pyplot as plt
import re




# 2. Page Configuration
st.set_page_config(
    page_title="Casa Monarca Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

color_scale_10 = ['#1f77b4', '#3b9bcc', '#66c2e5', '#80d4ea', '#a1e3f0', '#c0ecf4', '#d0f2f9', '#e0f7fc']



# ----------------------------------------------------------------------------------------------------------------------
# 3. Data Loading
# PRUEBA. DISPLAY DASHBOARD
url = 'https://raw.githubusercontent.com/PameRuiz25/pruebas/main/kobo_data.csv'
response = requests.get(url)

if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))
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
    st.markdown('##### Filtros de Tiempo')

    year_values = df.year.unique()
    sorted_year_values = sorted([m for m in year_values if m is not None])
    year_list = [None] + sorted_year_values  # Add None as the default option
    selected_year = st.selectbox('Año de consulta', year_list)

    month_values = df.month.unique()
    sorted_month_values = sorted([m for m in month_values if m is not None])
    month_list = [None] + sorted_month_values  # Add None as the default option
    selected_month = st.selectbox('Mes de consulta', month_list)

    st.markdown('#### Filtros Demográficos')

    population_list = [None] + sorted(df['Tipo_de_población'].unique())
    selected_population = st.selectbox('Tipo de población', population_list)

    sexo_list = [None] + sorted(df['Sexo'].unique())
    selected_sexo = st.selectbox('Sexo', sexo_list)

    age_range = st.slider("Rango de edad:", min_value=0, max_value=100, value=(0, 100), step=1)
    df = df[(df['Edad'] >= age_range[0]) & (df['Edad'] <= age_range[1])]

    grupo_list = [None] + sorted(df['Grupo_de_edad_y_acompañamiento'].unique())
    selected_grupo = st.selectbox('Grupo de edad y acompañamiento', grupo_list)

    pais_list = [None] + sorted(df['País_de_origen'].unique())
    selected_pais = st.selectbox('País de origen', pais_list)

    esado_list = [None] + sorted(df['Departamento_Estado'].unique())
    selected_estado = st.selectbox('Estado de origen', esado_list)

    estadocivil_list = [None] + sorted(df['Estado_civil'].unique())
    selected_estadocivil = st.selectbox('Estado Civil', estadocivil_list)

    grado_estudio_list = [None] + sorted(df['Último_grado_de_estudio'].unique())
    selected_grado_estudio = st.selectbox('Último grado de estudio', grado_estudio_list)


    st.write('##### Hijos')
    conhijos = st.checkbox('Con hijos')
    sinhijos = st.checkbox('Sin hijos')

    st.write('##### Alfabetizado')
    alfabetizado = st.checkbox('Alfabetizado')
    noalfabetizado = st.checkbox('No alfabetizado')

    st.write('##### Acceso a Casa Monarca')
    allowed_access = st.checkbox('Permitido el acceso')
    not_allowed_access = st.checkbox('No permitido el acceso')




    
# Aplicación de filtros
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

if selected_sexo is not None:
    df_filtered = df_filtered[df_filtered.Sexo == selected_sexo]
else:
    df_filtered = df_filtered

if selected_grupo is not None:
    df_filtered = df_filtered[df_filtered.Grupo_de_edad_y_acompañamiento == selected_grupo]
else:
    df_filtered = df_filtered

if selected_pais is not None:
    df_filtered = df_filtered[df_filtered.País_de_origen == selected_pais]
else:
    df_filtered = df_filtered

if selected_estado is not None:
    df_filtered = df_filtered[df_filtered.Departamento_Estado == selected_estado]
else:
    df_filtered = df_filtered

if selected_estadocivil is not None:
    df_filtered = df_filtered[df_filtered.Estado_civil == selected_estadocivil]
else:
    df_filtered = df_filtered

if conhijos and not sinhijos:
    df_filtered = df_filtered[df_filtered['Hijos'] == 1]
elif sinhijos and not conhijos:
    df_filtered = df_filtered[df_filtered['Hijos'] == 0]
else:
    df_filtered = df_filtered


if alfabetizado and not noalfabetizado:
    df_filtered = df_filtered[df_filtered['Alfabetizado'] == 1]
elif noalfabetizado and not alfabetizado:
    df_filtered = df_filtered[df_filtered['Alfabetizado'] == 0]
else:
    df_filtered = df_filtered

if allowed_access and not not_allowed_access:
    df_filtered = df_filtered[df_filtered['Acceso_a_Casa_Monarca'] == 1]
elif not_allowed_access and not allowed_access:
    df_filtered = df_filtered[df_filtered['Acceso_a_Casa_Monarca'] == 0]
else:
    df_filtered = df_filtered

if selected_grado_estudio is not None:
    df_filtered = df_filtered[df_filtered.Último_grado_de_estudio == selected_grado_estudio]
else:
    df_filtered = df_filtered











# 6. Data Visualization
# 6.1 Display total amount of consultations
total_consultations = df_filtered.shape[0]


# 6.3 Display donut chart of percentage of consultations invited in
def make_donut(input_response, input_text):
    chart_color = ['#29b5e8', '#155F7A']

    source = pd.DataFrame({
        "Valor": ['', input_text],
        "% value": [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Valor": ['', input_text],
        "% value": [100, 0]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=32, cornerRadius=25).encode(
        theta="% value",
        color=alt.Color("Valor:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)

    text = plot.mark_text(align='center', color=chart_color[0], font="Lato", fontSize=20, fontWeight=700,
                          fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=32, cornerRadius=25).encode(
        theta="% value",
        color=alt.Color("Valor:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)

    return plot_bg + plot + text

# Calculate percentage of allowed access
allowed_percentage = round((df_filtered["Acceso_a_Casa_Monarca"] == 1).mean(), 2) * 100


# Create columns
col1, col2 = st.columns((1, 2))  

with col1:
    st.markdown('##### Registros Totales')
    st.markdown(f'## {total_consultations}')
    st.markdown('##### Personas Atendidas')
    st.markdown(f'## {(df_filtered["Acceso_a_Casa_Monarca"] == 1).sum()}')
    st.markdown('##### Tasa de Aceptación a Casa Monarca')
    st.markdown(f'## {allowed_percentage}%')
with col2:
    st.markdown('##### Servicios Brindados')
    def clean_document(document):
        return re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ ]+', '', document)

    # Convertir la columna 'Idiomas' en un DataFrame de conteo
    documento_counts = df['Servicios_brindados'].str.split(', ').explode().map(clean_document).value_counts().reset_index()
    documento_counts.columns = ['Servicios_brindados', 'Cantidad']
    fig = px.pie(documento_counts, values='Cantidad', names='Servicios_brindados', width=650, height=350, color_discrete_sequence=color_scale_10)
    st.plotly_chart(fig)


# Create columns
col1, col2 = st.columns(2)


with col1:
        st.markdown('##### Registros por Año')
        consultations_by_year = df_filtered.groupby('year').size().reset_index(name='registros')
        line_chart = alt.Chart(consultations_by_year).mark_line(point=True).encode(
            x=alt.X('year:O', title="año", axis=alt.Axis(labelAngle=0)),
            y='registros:Q'
        ).properties(
            width=450,
            height=350
        )
        text = line_chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-5  # Ajustar la posición vertical del texto para mejor visibilidad
        ).encode(
            text='registros:Q'
        )
        chart = (line_chart + text)
        st.altair_chart(chart)





# 6.2 Display a line chart for the number of consultations by year
# Assuming df_filtered contains a column 'Fecha_de_atención'
with col2:
    st.markdown('##### Registros por Mes')
    consultations_by_month = df_filtered.groupby('month').size().reset_index(name='registros')
    line_chart = alt.Chart(consultations_by_month).mark_line(point=True).encode(
        x=alt.X('month', title='Mes', axis=alt.Axis(format='d')),  
        y=alt.Y('registros:Q', title='Registros')
    ).properties(
        width=450,
        height=350
    )

    # Añadir etiquetas de texto
    text = line_chart.mark_text(
        align='left',
        baseline='middle',
        dx=5,  # Ajuste horizontal
        dy=-5  # Ajuste vertical
    ).encode(
        text='registros:Q',  # Usar el valor de 'registros' como texto
        x='month',  # Posicionar la etiqueta en el mismo eje x que los puntos
        y='registros:Q',  # Posicionar la etiqueta en la misma altura que los puntos
    )

    chart_with_labels = line_chart + text
    st.altair_chart(chart_with_labels)


# Add a separator to the layout.
st.markdown("""
    <div style="background-color:#29b5e8; padding:10px; border-radius:5px; margin-top:10px; margin-bottom:20px;">
        <h2 style="color:white; text-align:center;">Demográficos</h2>
    </div>
""", unsafe_allow_html=True)


col1, col2 = st.columns(2)

# 6.4 Display a bar chart for sex distribution
with col1:
    st.markdown('##### Distribución por Sexo')
    if not df_filtered.empty:
        sex_distribution = df_filtered['Sexo'].value_counts().reset_index()
        sex_distribution.columns = ['Sexo', 'Count']

        bar_chart = alt.Chart(sex_distribution).mark_bar().encode(
            x=alt.X('Sexo:N', title='Sexo',  axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Count:Q', title='Cantidad'),
            color=alt.Color('Sexo:N', scale=alt.Scale(range=color_scale_10), legend=None)  # Elimina la leyenda
        ).properties(
            width=450,
            height=300
        )
        text = bar_chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-5  # Ajustar la posición vertical del texto para mejor visibilidad
        ).encode(
            text='Count:Q'
        )
        chart = (bar_chart + text)
        st.altair_chart(chart)

    

    st.markdown('##### Distribución por Estado Civil')
    if not df_filtered.empty:
        sex_distribution = df_filtered['Estado_civil'].value_counts().reset_index()
        sex_distribution.columns = ['Estado_civil', 'Count']
        bar_chart = alt.Chart(sex_distribution).mark_bar().encode(
            x=alt.X('Estado_civil:N', title='Estado_civil',  axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Count:Q', title='Cantidad'),
            color=alt.Color('Estado_civil:N', scale=alt.Scale(range=color_scale_10), legend=None)
        ).properties(
            width=450,
            height=300
        )
        text = bar_chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-5  # Ajustar la posición vertical del texto para mejor visibilidad
        ).encode(
            text='Count:Q'
        )
        chart = (bar_chart + text)
        st.altair_chart(chart)


    st.markdown('##### Distribución de Población por Tipo de Población')
    tipo_poblacion_counts = df_filtered['Tipo_de_población'].value_counts().reset_index()
    tipo_poblacion_counts.columns = ['Tipo_de_población', 'Count']
    fig = px.pie(tipo_poblacion_counts, values='Count', names='Tipo_de_población', width=450, height=350, color_discrete_sequence=color_scale_10)
    st.plotly_chart(fig)



    st.markdown('##### Distribución de Último Grado de Estudio')
    tipo_poblacion_counts = df_filtered['Último_grado_académico'].value_counts().reset_index()
    tipo_poblacion_counts.columns = ['Último_grado_académico', 'Count']
    fig = px.pie(tipo_poblacion_counts, values='Count', names='Último_grado_académico', width=450, height=350, color_discrete_sequence=color_scale_10)
    st.plotly_chart(fig)






with col2:
    st.markdown('##### Distribución por Edad y Acompañamiento')
    if not df_filtered.empty:
        sex_distribution = df_filtered['Grupo_de_edad_y_acompañamiento'].value_counts().reset_index()
        sex_distribution.columns = ['Grupo_de_edad_y_acompañamiento', 'Cantidad']
        bars = alt.Chart(sex_distribution).mark_bar().encode(
            x=alt.X('Grupo_de_edad_y_acompañamiento:N', title='Grupo de Edad y Acompañamiento', axis=alt.Axis(labelAngle=0)),
            y='Cantidad:Q',
            color=alt.Color('Grupo_de_edad_y_acompañamiento:N', scale=alt.Scale(range=color_scale_10), legend=None)
        ).properties(
            width=450,
            height=300
        )
        text = bars.mark_text(
            align='center',
            baseline='bottom',
            dy=-5  # Ajustar la posición vertical del texto para mejor visibilidad
        ).encode(
            text='Cantidad:Q'
        )
        chart = (bars + text)
        st.altair_chart(chart)


    
    st.markdown('##### Distribución por Edad')
    histogram = alt.Chart(df_filtered).mark_bar(color='#3b9bcc').encode(
        x=alt.X('Edad:Q', bin=alt.Bin(maxbins=10), title='Edad'),
        y=alt.Y('count()', title='Frecuencia')
    ).properties(
        width=450,
        height=300
    )

    # Mostrar el histograma
    st.altair_chart(histogram)







    st.markdown('##### Distribución por Estado Civil')
    tipo_poblacion_counts = df_filtered['Estado_civil'].value_counts().reset_index()
    tipo_poblacion_counts.columns = ['Estado_civil', 'Count']
    fig = px.pie(tipo_poblacion_counts, values='Count', names='Estado_civil', width=450, height=350, color_discrete_sequence=color_scale_10)
    st.plotly_chart(fig)


    st.markdown('##### Distibución de Idiomas')
    def clean_document(document):
        return re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ ]+', '', document)

    # Convertir la columna 'Idiomas' en un DataFrame de conteo
    documento_counts = df['Idiomas'].str.split(', ').explode().map(clean_document).value_counts().reset_index()
    documento_counts.columns = ['Idiomas', 'Cantidad']
    fig = px.pie(documento_counts, values='Cantidad', names='Idiomas', width=450, height=350, color_discrete_sequence=color_scale_10)
    st.plotly_chart(fig)





col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('##### Distribución por Alfabetización')
    tipo_poblacion_counts = df_filtered['Alfabetizado'].value_counts().reset_index()
    tipo_poblacion_counts.columns = ['Alfabetizado', 'Count']
    fig = px.pie(tipo_poblacion_counts, values='Count', names='Alfabetizado', width=250, height=300, color_discrete_sequence=color_scale_10)
    st.plotly_chart(fig)

with col2:
    st.markdown('##### Distribución por País de Origen')
    country_consultation_counts = df_filtered['País_de_origen'].value_counts().reset_index()
    country_consultation_counts.columns = ['País_de_origen', 'Consultation_Count']
    country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

    st.dataframe(country_consultation_counts_sorted,
                column_order=("País_de_origen", "Consultation_Count"),
                hide_index=True,
                width=None,
                column_config={
                    "País_de_origen": st.column_config.TextColumn(
                        "País de Origen",
                    ),
                    "Consultation_Count": st.column_config.ProgressColumn(
                        "Cantidad de Personas",
                        format="%d",
                        min_value=0,
                        max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                    )}
                )
    

with col3:
    st.markdown('##### Distribución por Estado de Origen')
    country_consultation_counts = df_filtered['Departamento_Estado'].value_counts().reset_index()
    country_consultation_counts.columns = ['Departamento_Estado', 'Consultation_Count']
    country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

    st.dataframe(country_consultation_counts_sorted,
                column_order=("Departamento_Estado", "Consultation_Count"),
                hide_index=True,
                width=None,
                column_config={
                    "Departamento_Estado": st.column_config.TextColumn(
                        "Estado",
                    ),
                    "Consultation_Count": st.column_config.ProgressColumn(
                        "Cantidad de Personas",
                        format="%d",
                        min_value=0,
                        max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                    )}
                )







st.markdown("""
    <div style="background-color:#29b5e8; padding:10px; border-radius:5px; margin-top:10px; margin-bottom:20px;">
        <h2 style="color:white; text-align:center;">Detalles de Inmigración y Viaje</h2>
    </div>
""", unsafe_allow_html=True)


# Calculate percentage of Alfabetizado, Con hijos, Viene acompañado, Pago a guía
monterrey = round((df_filtered["Destino_Monterrey"] == 1).mean(), 2)*100
monterrey_count = df_filtered["Destino_Monterrey"].sum()
conhijos = round((df_filtered["Hijos"] == 1).mean(), 2)*100
conhijos_count = df_filtered["Hijos"].sum()
vieneacompañado = round((df_filtered["Viene_acompañado"] == 1).mean(), 2)*100
vieneacompañado_count = df_filtered["Viene_acompañado"].sum()
pagoaguia = round((df_filtered["Pago_a_guía"] == 1).mean(), 2)*100
pagoaguia_count = df_filtered["Pago_a_guía"].sum()


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'###### Con Hijos: {conhijos_count}')
    st.altair_chart(make_donut(conhijos, 'Con hijos'))
with col2:
    st.markdown(f'###### Con Acompañante: {vieneacompañado_count}')
    st.altair_chart(make_donut(vieneacompañado, 'Viene acompañado'))
with col3:
    st.markdown(f'###### Pago a Guía: {pagoaguia_count}')
    st.altair_chart(make_donut(pagoaguia, 'Pago a guía'))
with col4:
    st.markdown(f'###### Destino Monterrey: {monterrey_count}')
    st.altair_chart(make_donut(monterrey, 'Destino Monterrey'))
    




col1, col2 = st.columns(2)
with col1:
    st.markdown('##### Acompañantes')
    sex_distribution = df_filtered['Acompañantes'].value_counts().reset_index()
    sex_distribution.columns = ['Acompañantes', 'Count']
    bar_chart = alt.Chart(sex_distribution).mark_bar().encode(
        x=alt.X('Acompañantes:N', title='Acompañantes',  axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Count:Q', title='Cantidad'),
        color=alt.Color('Acompañantes:N', scale=alt.Scale(range=color_scale_10), legend=None)
    ).properties(
        width=450,
        height=300
    )
    text = bar_chart.mark_text(
        align='center',
        baseline='bottom',
        dy=-5  # Ajustar la posición vertical del texto para mejor visibilidad
    ).encode(
        text='Count:Q'
    )
    chart = (bar_chart + text)
    st.altair_chart(chart)






    st.markdown('##### Documentos de Identidad')
    def clean_document(document):
        return re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ ]+', '', document)

    # Convertir la columna 'Documentos_de_identidad' en un DataFrame de conteo
    documento_counts = df['Documentos_de_identidad'].str.split(', ').explode().map(clean_document).value_counts().reset_index()
    documento_counts.columns = ['Documento_de_identidad', 'Cantidad']
    # Crea el gráfico de barras con Altair
    bars = alt.Chart(documento_counts).mark_bar().encode(
        x=alt.X('Documento_de_identidad:N', title='Documento de Identidad', axis=alt.Axis(labelAngle=0)),
        y='Cantidad:Q',
        color=alt.Color('Documento_de_identidad:N', scale=alt.Scale(range=color_scale_10), legend=None),
        tooltip=['Documento_de_identidad', 'Cantidad']
    ).properties(
        width=alt.Step(40)  # Ancho de las barras
    )

    text = bars.mark_text(
        align='center',
        baseline='bottom',
        color='black'
    ).encode(
        text='Cantidad:Q'
    )

    chart = (bars + text).properties(
        width=450,  
        height=300
    )
    st.altair_chart(chart, use_container_width=True)


    



    st.markdown('##### Dinero pagado a Guía')
    sex_distribution = df_filtered['Dinero_pagado_a_guía'].value_counts().reset_index()
    sex_distribution.columns = ['Dinero_pagado_a_guía', 'Count']
    bar_chart = alt.Chart(sex_distribution).mark_bar().encode(
        x=alt.X('Dinero_pagado_a_guía:N', title='Dinero_pagado_a_guía',  axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Count:Q', title='Cantidad'),
        color=alt.Color('Dinero_pagado_a_guía:N', scale=alt.Scale(range=color_scale_10), legend=None)
    ).properties(
        width=450,
        height=300
    )
    text = bar_chart.mark_text(
        align='center',
        baseline='bottom',
        dy=-5  # Ajustar la posición vertical del texto para mejor visibilidad
    ).encode(
        text='Count:Q'
    )
    chart = (bar_chart + text)
    st.altair_chart(chart)










    


with col2:
    st.markdown('##### Cantidad de Hijos Viajando')
    sex_distribution = df_filtered['Cantidad_de_hijos_viajando'].value_counts().reset_index()
    sex_distribution.columns = ['Cantidad_de_hijos_viajando', 'Count']
    bar_chart = alt.Chart(sex_distribution).mark_bar().encode(
        x=alt.X('Cantidad_de_hijos_viajando:N', title='Cantidad_de_hijos_viajando',  axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Count:Q', title='Cantidad'),
        color=alt.Color('Cantidad_de_hijos_viajando:N', scale=alt.Scale(range=color_scale_10), legend=None)
    ).properties(
        width=450,
        height=300
    )
    text = bar_chart.mark_text(
        align='center',
        baseline='bottom',
        dy=-5  # Ajustar la posición vertical del texto para mejor visibilidad
    ).encode(
        text='Count:Q'
    )
    chart = (bar_chart + text)
    st.altair_chart(chart)






    st.markdown('##### Tipo de Documento Migratorio')
    sex_distribution = df_filtered['Tipo_de_documento_migratorio'].value_counts().reset_index()
    sex_distribution.columns = ['Tipo_de_documento_migratorio', 'Count']
    bar_chart = alt.Chart(sex_distribution).mark_bar().encode(
        x=alt.X('Tipo_de_documento_migratorio:N', title='Tipo_de_documento_migratorio',  axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Count:Q', title='Cantidad'),
        color=alt.Color('Tipo_de_documento_migratorio:N', scale=alt.Scale(range=color_scale_10), legend=None)
    ).properties(
        width=450,
        height=300
    )
    text = bar_chart.mark_text(
        align='center',
        baseline='bottom',
        dy=-5  # Ajustar la posición vertical del texto para mejor visibilidad
    ).encode(
        text='Count:Q'
    )
    chart = (bar_chart + text)
    st.altair_chart(chart)






    st.markdown('##### Forma de Viaje')
    tipo_poblacion_counts = df_filtered['Forma_de_viaje'].value_counts().reset_index()
    tipo_poblacion_counts.columns = ['Forma_de_viaje', 'Count']
    fig = px.pie(tipo_poblacion_counts, values='Count', names='Forma_de_viaje', width=450, height=350, color_discrete_sequence=color_scale_10)
    st.plotly_chart(fig)












st.markdown('##### Razones de Salida')
country_consultation_counts = df_filtered['Razón_de_salida'].value_counts().reset_index()
country_consultation_counts.columns = ['Razón_de_salida', 'Consultation_Count']
country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

st.dataframe(country_consultation_counts_sorted,
                column_order=("Razón_de_salida", "Consultation_Count"),
                hide_index=True,
                width=None,
                column_config={
                    "Razón_de_salida": st.column_config.TextColumn(
                        "Razón de salida",
                    ),
                    "Consultation_Count": st.column_config.ProgressColumn(
                        "Cantidad de Personas",
                        format="%d",
                        min_value=0,
                        max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                    )}
                )





st.markdown("""
    <div style="background-color:#29b5e8; padding:10px; border-radius:5px; margin-top:10px; margin-bottom:20px;">
        <h2 style="color:white; text-align:center;">Redes de Apoyo</h2>
    </div>
""", unsafe_allow_html=True)





st.markdown("""
    <div style="background-color:#29b5e8; padding:10px; border-radius:5px; margin-top:10px; margin-bottom:20px;">
        <h2 style="color:white; text-align:center;">Enfermedades y Otras Condiciones</h2>
    </div>
""", unsafe_allow_html=True)








st.markdown("""
    <div style="background-color:#29b5e8; padding:10px; border-radius:5px; margin-top:10px; margin-bottom:20px;">
        <h2 style="color:white; text-align:center;">Abusos de Derechos Humanos</h2>
    </div>
""", unsafe_allow_html=True)


# Calculate percentage of Alfabetizado, Con hijos, Viene acompañado, Pago a guía
monterrey = round((df_filtered["Abuso_de_derechos_humanos_antes_de_México"] == 1).mean(), 2)*100
monterrey_count = df_filtered["Abuso_de_derechos_humanos_antes_de_México"].sum()
conhijos = round((df_filtered["Abuso_de_derechos_humanos_en_México"] == 1).mean(), 2)*100
conhijos_count = df_filtered["Abuso_de_derechos_humanos_en_México"].sum()
vieneacompañado = round((df_filtered["Abuso_en_estación_migratoria"] == 1).mean(), 2)*100
vieneacompañado_count = df_filtered["Abuso_en_estación_migratoria"].sum()
pagoaguia = round((df_filtered["Denuncia_formal_por_abuso"] == 1).mean(), 2)*100
pagoaguia_count = df_filtered["Denuncia_formal_por_abuso"].sum()


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'###### Antes de México: {monterrey_count}')
    st.altair_chart(make_donut(monterrey, 'Antes de México'))
with col2:
    st.markdown(f'###### En México: {conhijos_count}')
    st.altair_chart(make_donut(conhijos, 'En México'))
with col3:
    st.markdown(f'###### En Estación Migratoria: {vieneacompañado_count}')
    st.altair_chart(make_donut(vieneacompañado, 'En Estación Migratoria'))
with col4:
    st.markdown(f'###### Denuncia Formal: {pagoaguia_count}')
    st.altair_chart(make_donut(pagoaguia, 'Denuncia Formal'))


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('##### Abuso Antes de México')
    country_consultation_counts = df_filtered['Tipo_de_abuso_antes_México'].value_counts().reset_index()
    country_consultation_counts.columns = ['Tipo_de_abuso_antes_México', 'Consultation_Count']
    country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

    st.dataframe(country_consultation_counts_sorted,
                    column_order=("Tipo_de_abuso_antes_México", "Consultation_Count"),
                    hide_index=True,
                    width=None,
                    column_config={
                        "Tipo_de_abuso_antes_México": st.column_config.TextColumn(
                            "Abuso antes de México",
                        ),
                        "Consultation_Count": st.column_config.ProgressColumn(
                            "Cantidad de Personas",
                            format="%d",
                            min_value=0,
                            max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                        )}
                    )
with col2:
    st.markdown('##### Abuso en México')
    country_consultation_counts = df_filtered['Tipo_de_abuso_en_México'].value_counts().reset_index()
    country_consultation_counts.columns = ['Tipo_de_abuso_en_México', 'Consultation_Count']
    country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

    # Check if the DataFrame is not empty before displaying it
    if not country_consultation_counts_sorted.empty:
        st.dataframe(country_consultation_counts_sorted,
                        column_order=("Tipo_de_abuso_en_México", "Consultation_Count"),
                        hide_index=True,
                        width=None,
                        column_config={
                            "Tipo_de_abuso_en_México": st.column_config.TextColumn(
                                "Abuso en México",
                            ),
                            "Consultation_Count": st.column_config.ProgressColumn(
                                "Cantidad de Personas",
                                format="%d",
                                min_value=0,
                                max_value=min(country_consultation_counts_sorted['Consultation_Count'].max(), 1000)  # Set a reasonable upper limit
                            )}
                        )
    else:
        st.markdown("No hay datos disponibles para mostrar.")

with col3:
    st.markdown('##### Abuso en Estación Migratoria')
    country_consultation_counts = df_filtered['Descripción_de_visita_a_estación_migratoria'].value_counts().reset_index()
    country_consultation_counts.columns = ['Descripción_de_visita_a_estación_migratoria', 'Consultation_Count']
    country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

    st.dataframe(country_consultation_counts_sorted,
                    column_order=("Descripción_de_visita_a_estación_migratoria", "Consultation_Count"),
                    hide_index=True,
                    width=None,
                    column_config={
                        "Descripción_de_visita_a_estación_migratoria": st.column_config.TextColumn(
                            "Abuso en Estación",
                        ),
                        "Consultation_Count": st.column_config.ProgressColumn(
                            "Cantidad de Personas",
                            format="%d",
                            min_value=0,
                            max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                        )}
                    )
    












    

    



st.write(df)