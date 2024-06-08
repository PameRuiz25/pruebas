
# 0. Todo es una función

def dashboard():

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



    def page1():
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
            st.title('REGISTRO KOBO')
            
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

            st.write('##### Con Acompañante')
            with_accompaniment = st.checkbox('Con acompañante')
            without_accompaniment = st.checkbox('Sin acompañante')

            st.write('##### Con Enfermedad')
            with_disease = st.checkbox('Con enfermedad')
            without_disease = st.checkbox('Sin enfermedad')

            st.write('##### Con Alergias')
            with_allergies = st.checkbox('Con alergias')
            without_allergies = st.checkbox('Sin alergias')

            st.write('##### Embarazo')
            with_pregnancy = st.checkbox('Embarazada')
            without_pregnancy = st.checkbox('No embarazada')






            
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

        if with_accompaniment and not without_accompaniment:
            df_filtered = df_filtered[df_filtered['Viene_acompañado'] == 1]
        elif without_accompaniment and not with_accompaniment:
            df_filtered = df_filtered[df_filtered['Viene_acompañado'] == 0]
        else:
            df_filtered = df_filtered

        if with_disease and not without_disease:
            df_filtered = df_filtered[df_filtered['Padece_enfermedad'] == 1]
        elif without_disease and not with_disease:
            df_filtered = df_filtered[df_filtered['Padece_enfermedad'] == 0]
        else:
            df_filtered = df_filtered

        if with_allergies and not without_allergies:
            df_filtered = df_filtered[df_filtered['Padece_alergias'] == 1]
        elif without_allergies and not with_allergies:
            df_filtered = df_filtered[df_filtered['Padece_alergias'] == 0]
        else:
            df_filtered = df_filtered

        if with_pregnancy and not without_pregnancy:
            df_filtered = df_filtered[df_filtered['Embarazo'] == 1]
        elif without_pregnancy and not with_pregnancy:
            df_filtered = df_filtered[df_filtered['Embarazo'] == 0]
        else:
            df_filtered = df_filtered




        st.markdown("""
            <div style="background-color:#1f77b4; padding:10px; border-radius:5px; margin-top:10px; margin-bottom:20px;">
                <h2 style="color:white; text-align:center; margin:0;">CASA MONARCA</h2>
                <h3 style="color:white; text-align:center; margin:0;">Registros Kobo</h3>
            </div>
        """, unsafe_allow_html=True)






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

            if not country_consultation_counts_sorted.empty:
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

            if not country_consultation_counts_sorted.empty:
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
                <h2 style="color:white; text-align:center;">Enfermedades y Otras Condiciones</h2>
            </div>
        """, unsafe_allow_html=True)

        # Calculate percentage of Alfabetizado, Con hijos, Viene acompañado, Pago a guía
        monterrey = round((df_filtered["Padece_enfermedad"] == 1).mean(), 2)*100
        monterrey_count = df_filtered["Padece_enfermedad"].sum()
        conhijos = round((df_filtered["Padece_alergias"] == 1).mean(), 2)*100
        conhijos_count = df_filtered["Padece_alergias"].sum()
        vieneacompañado = round((df_filtered["Embarazo"] == 1).mean(), 2)*100
        vieneacompañado_count = df_filtered["Embarazo"].sum()
        pagoaguia = round((df_filtered["Control_prenatal"] == 1).mean(), 2)*100
        pagoaguia_count = df_filtered["Control_prenatal"].sum()


        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'###### Enfermedad: {monterrey_count}')
            st.altair_chart(make_donut(monterrey, 'Enfermedad'))
        with col2:
            st.markdown(f'###### Alergias: {conhijos_count}')
            st.altair_chart(make_donut(conhijos, 'Alergias'))
        with col3:
            st.markdown(f'###### Embarazos: {vieneacompañado_count}')
            st.altair_chart(make_donut(vieneacompañado, 'Embarazos'))
        with col4:
            st.markdown(f'###### Control Prenatal: {pagoaguia_count}')
            st.altair_chart(make_donut(pagoaguia, 'Control Prenatal'))













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




            st.markdown('##### Destinos Finales')
            country_consultation_counts = df_filtered['Destino_final'].value_counts().reset_index()
            country_consultation_counts.columns = ['Destino_final', 'Consultation_Count']
            country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

            if not country_consultation_counts_sorted.empty:
                st.dataframe(country_consultation_counts_sorted,
                                column_order=("Destino_final", "Consultation_Count"),
                                hide_index=True,
                                width=None,
                                column_config={
                                    "Destino_final": st.column_config.TextColumn(
                                        "Destino Final",
                                    ),
                                    "Consultation_Count": st.column_config.ProgressColumn(
                                        "Cantidad de Personas",
                                        format="%d",
                                        min_value=0,
                                        max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                                    )}
                                )







            


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
            fig = px.pie(tipo_poblacion_counts, values='Count', names='Forma_de_viaje', width=450, height=300, color_discrete_sequence=color_scale_10)
            st.plotly_chart(fig)


            st.markdown('##### Razones de Salida')
            country_consultation_counts = df_filtered['Razón_de_salida'].value_counts().reset_index()
            country_consultation_counts.columns = ['Razón_de_salida', 'Consultation_Count']
            country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

            if not country_consultation_counts_sorted.empty:
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

            if not country_consultation_counts_sorted.empty:
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

            if not country_consultation_counts_sorted.empty:
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
                





        col1, col2 = st.columns(2)

        with col1:
            st.markdown('##### Posibilidad de Regresar al País de Origen') 
            tipo_poblacion_counts = df_filtered['Posibilidad_de_reingresar_al_país_de_origen'].value_counts().reset_index()
            tipo_poblacion_counts.columns = ['Posibilidad_de_reingresar_al_país_de_origen', 'Count']
            fig = px.pie(tipo_poblacion_counts, values='Count', names='Posibilidad_de_reingresar_al_país_de_origen', width=450, height=350, color_discrete_sequence=color_scale_10)
            st.plotly_chart(fig)


        with col2:
            st.markdown('##### Razón de No Retorno al País de Origen')
            country_consultation_counts = df_filtered['Razón_de_no_retorno_al_país_de_origen'].value_counts().reset_index()
            country_consultation_counts.columns = ['Razón_de_no_retorno_al_país_de_origen', 'Consultation_Count']
            country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

            if not country_consultation_counts_sorted.empty:
                st.dataframe(country_consultation_counts_sorted,
                                column_order=("Razón_de_no_retorno_al_país_de_origen", "Consultation_Count"),
                                hide_index=True,
                                width=None,
                                column_config={
                                    "Razón_de_no_retorno_al_país_de_origen": st.column_config.TextColumn(
                                        "Razón de no Retorno",
                                    ),
                                    "Consultation_Count": st.column_config.ProgressColumn(
                                        "Cantidad de Personas",
                                        format="%d",
                                        min_value=0,
                                        max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                                    )}
                                )



    def page2():
        st.markdown("""
            <div style="background-color:#1f77b4; padding:10px; border-radius:5px; margin-top:10px; margin-bottom:20px;">
                <h2 style="color:white; text-align:center; margin:0;">CASA MONARCA</h2>
                <h3 style="color:white; text-align:center; margin:0;">Atención Humanitaria</h3>
            </div>
        """, unsafe_allow_html=True)





        url = 'https://raw.githubusercontent.com/PameRuiz25/pruebas/main/atencion_data.csv'
        response = requests.get(url)

        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
        else:
            st.write("Failed to load data from GitHub.")
        # ----------------------------------------------------------------------------------------------------------------------


        # 4. Data Processing
        # add a new column for year and month
        df['year'] = pd.DatetimeIndex(df['Fecha_de_recepcion']).year
        df['month'] = pd.DatetimeIndex(df['Fecha_de_recepcion']).month




        with st.sidebar:
            st.markdown("## Filtros")
            year_values = df.year.unique()
            sorted_year_values = sorted([m for m in year_values if m is not None])
            year_list = [None] + sorted_year_values  # Add None as the default option
            selected_year = st.selectbox('Año de consulta', year_list)

            month_values = df.month.unique()
            sorted_month_values = sorted([m for m in month_values if m is not None])
            month_list = [None] + sorted_month_values  # Add None as the default option
            selected_month = st.selectbox('Mes de consulta', month_list)

            population_list = [None] + sorted(df['Tipo_de_poblacion'].unique())
            selected_population = st.selectbox('Tipo de población', population_list)

            sexo_list = [None] + sorted(df['Sexo'].unique())
            selected_sexo = st.selectbox('Sexo', sexo_list)

            nacionalidad_list = [None] + sorted(df['Nacionalidad'].unique())
            selected_nacionalidad = st.selectbox('Nacionalidad', nacionalidad_list)

            age_range = st.slider("Rango de edad:", min_value=0, max_value=100, value=(0, 100), step=1)
            df = df[(df['Edad'] >= age_range[0]) & (df['Edad'] <= age_range[1])]


            if selected_year is not None:
                filtered_df = df[df['year'] == selected_year]
            else:
                filtered_df = df
            
            if selected_month is not None:
                filtered_df = filtered_df[filtered_df['month'] == selected_month]
            else:
                filtered_df = filtered_df
            
            if selected_population is not None:
                filtered_df = filtered_df[filtered_df['Tipo_de_población'] == selected_population]
            else:
                filtered_df = filtered_df

            if selected_sexo is not None:
                filtered_df = filtered_df[filtered_df['Sexo'] == selected_sexo]
            else:
                filtered_df = filtered_df

            if selected_nacionalidad is not None:
                filtered_df = filtered_df[filtered_df['Nacionalidad'] == selected_nacionalidad]
            else:
                filtered_df = filtered_df

            
        st.markdown("### Total de personas atendidas: {}".format(len(filtered_df)))



        # GRÁFICOS BÁSICOS (TEMPORALES)
        # Create columns
        col1, col2 = st.columns(2)


        with col1:
                st.markdown('##### Atención por Año')
                consultations_by_year = filtered_df.groupby('year').size().reset_index(name='registros')
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
            st.markdown('##### Atención por Mes')
            consultations_by_month = filtered_df.groupby('month').size().reset_index(name='registros')
            line_chart = alt.Chart(consultations_by_month).mark_line(point=True).encode(
                x=alt.X('month', title='Mes', axis=alt.Axis(format='d')),  
                y=alt.Y('registros:Q', title='Atención')
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


        # GRÁFICOS BÁSICOS (DEMOGRÁFICOS)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('##### Población por Sexo')
            tipo_poblacion_counts = filtered_df['Sexo'].value_counts().reset_index()
            tipo_poblacion_counts.columns = ['Sexo', 'Count']
            fig = px.pie(tipo_poblacion_counts, values='Count', names='Sexo', width=300, height=350, color_discrete_sequence=color_scale_10)
            st.plotly_chart(fig)

        with col2:
            st.markdown('##### Población por Nacionalidad')
            tipo_poblacion_counts = filtered_df['Nacionalidad'].value_counts().reset_index()
            tipo_poblacion_counts.columns = ['Nacionalidad', 'Count']
            fig = px.pie(tipo_poblacion_counts, values='Count', names='Nacionalidad', width=300, height=350, color_discrete_sequence=color_scale_10)
            st.plotly_chart(fig)
        with col3:
            st.markdown('##### Población por Tipo de Población')
            tipo_poblacion_counts = filtered_df['Tipo_de_poblacion'].value_counts().reset_index()
            tipo_poblacion_counts.columns = ['Tipo_de_poblacion', 'Count']
            fig = px.pie(tipo_poblacion_counts, values='Count', names='Tipo_de_poblacion', width=300, height=350, color_discrete_sequence=color_scale_10)
            st.plotly_chart(fig)


        






        bit_columns = [
            "Embarazo",
            "Afiliacion_al_IMSS",
            "Acompanamiento_para_atencion_medica",
            "Acompanamiento_para_acceso_a_la_vivienda",
            "Acompanamiento_para_apertura_de_cuenta_bancaria",
            "Menor_de_edad_acompanado_a_inscripcion_escolar",
            "Grado_academico_inscrito",
            "Acompanamiento_para_INEA",
            "Nivel_de_estudios_certificado",
            "Acompanamiento_para_la_revalidacion_de_estudios",
            "Nivel_de_estudios_mas_alto",
            "Hogar_informado_sobre_el_acceso_a_la_educacion",
            "Acompanamiento_para_certificaciones_tecnicas",
            "Habilidades_blandas",
            "Canalizacion_a_empresa_u_organizacion_para_vinculacion_laboral",
            "Canalizacion_a_empresa_para_insercion_laboral",
            "Canalizacion_a_bolsa_de_empleo_para_insercion_laboral",
            "Canalizacion_a_organizacion_para_insercion_laboral",
            "Atencion_psicosocial_y_psicologica_por_primera_vez",
            "Canalizacion_a_servicios_relevantes",
            "Acompanamiento_para_SMAPS",
            "Atencion_de_primeros_auxilios_psicologicos",
            "Atencion_de_psicoterapia_individual_o_familiar",
            "Atencion_de_psicoterapia_grupal",
            "Participacion_en_talleres_psicoeducativos",
            "Canalizacion_a_servicios_de_psiquiatria",
            "Canalizacion_al_ACNUR_para_apoyos_economicos_para_la_integracion_local",
            "Canalizacion_al_ACNUR_para_la_insercion_escolar",
            "Canalizacion_al_ACNUR_para_apoyo_por_certificacion_de_primaria_y_secundaria",
            "Canalizacion_al_ACNUR_para_apoyo_economico_por_revalidacion_de_estudios",
        ]

        # Contar valores
        counts = {col: filtered_df[col].sum() for col in bit_columns}

        st.write("Conteos de registros por cada columna:")
        counts_df = pd.DataFrame(list(counts.items()), columns=['Columna', 'Conteo'])
        st.table(counts_df)



        






    def page3():
        st.markdown("""
            <div style="background-color:#1f77b4; padding:10px; border-radius:5px; margin-top:10px; margin-bottom:20px;">
                <h2 style="color:white; text-align:center; margin:0;">CASA MONARCA</h2>
                <h3 style="color:white; text-align:center; margin:0;">Atención Legal</h3>
            </div>
        """, unsafe_allow_html=True)





        url = 'https://raw.githubusercontent.com/PameRuiz25/pruebas/main/output_legal.csv'
        response = requests.get(url)

        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
        else:
            st.write("Failed to load data from GitHub.")
        # ----------------------------------------------------------------------------------------------------------------------




        # 4. Data Processing
        # add a new column for year and month
        df['year'] = pd.DatetimeIndex(df['Fecha_de_registro']).year
        df['month'] = pd.DatetimeIndex(df['Fecha_de_registro']).month




        with st.sidebar:
            st.markdown("## Filtros")

            population_list = [None] + sorted(df['Base'].unique())
            selected_base = st.selectbox('Base', population_list)


            year_values = df.year.unique()
            sorted_year_values = sorted([m for m in year_values if m is not None])
            year_list = [None] + sorted_year_values  # Add None as the default option
            selected_year = st.selectbox('Año de consulta', year_list)

            month_values = df.month.unique()
            sorted_month_values = sorted([m for m in month_values if m is not None])
            month_list = [None] + sorted_month_values  # Add None as the default option
            selected_month = st.selectbox('Mes de consulta', month_list)

            population_list = [None] + sorted(df['Tipo_de_poblacion'].unique())
            selected_population = st.selectbox('Tipo de población', population_list)

            sexo_list = [None] + sorted(df['Sexo'].unique())
            selected_sexo = st.selectbox('Sexo', sexo_list)

            nacionalidad_list = [None] + sorted(df['Nacionalidad'].unique())
            selected_nacionalidad = st.selectbox('Nacionalidad', nacionalidad_list)

            age_range = st.slider("Rango de edad:", min_value=0, max_value=100, value=(0, 100), step=1)
            df = df[(df['Edad'] >= age_range[0]) & (df['Edad'] <= age_range[1])]
            
            tipo_de_atencion_list = st.selectbox('Tipo de Atención', ['None', 'Primera vez', 'Seguimiento'])
            atencion = df[df['Tipo_de_atencion'] == tipo_de_atencion_list]


            if selected_year is not None:
                filtered_df = df[df['year'] == selected_year]
            else:
                filtered_df = df

            if selected_base is not None:
                filtered_df = filtered_df[filtered_df['Base'] == selected_base]
            else:
                filtered_df = filtered_df
            
            if selected_month is not None:
                filtered_df = filtered_df[filtered_df['month'] == selected_month]
            else:
                filtered_df = filtered_df
            
            if selected_population is not None:
                filtered_df = filtered_df[filtered_df['Tipo_de_población'] == selected_population]
            else:
                filtered_df = filtered_df

            if selected_sexo is not None:
                filtered_df = filtered_df[filtered_df['Sexo'] == selected_sexo]
            else:
                filtered_df = filtered_df

            if selected_nacionalidad is not None:
                filtered_df = filtered_df[filtered_df['Nacionalidad'] == selected_nacionalidad]
            else:
                filtered_df = filtered_df

            if tipo_de_atencion_list != 'None':
                filtered_df = filtered_df[filtered_df['Tipo_de_atencion'] == tipo_de_atencion_list]
            else:
                filtered_df = filtered_df




        st.write("### Total de personas atendidas: {}".format(len(filtered_df)))


        # GRÁFICOS BÁSICOS (TEMPORALES)
        # Create columns
        col1, col2 = st.columns(2)


        with col1:
                st.markdown('##### Atención por Año')
                consultations_by_year = filtered_df.groupby('year').size().reset_index(name='registros')
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
            st.markdown('##### Atención por Mes')
            consultations_by_month = filtered_df.groupby('month').size().reset_index(name='registros')
            line_chart = alt.Chart(consultations_by_month).mark_line(point=True).encode(
                x=alt.X('month', title='Mes', axis=alt.Axis(format='d')),  
                y=alt.Y('registros:Q', title='Atendidos')
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




            # GRÁFICOS BÁSICOS (DEMOGRÁFICOS)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('##### Población por Sexo')
            tipo_poblacion_counts = filtered_df['Sexo'].value_counts().reset_index()
            tipo_poblacion_counts.columns = ['Sexo', 'Count']
            fig = px.pie(tipo_poblacion_counts, values='Count', names='Sexo', width=300, height=350, color_discrete_sequence=color_scale_10)
            st.plotly_chart(fig)

        with col2:
            st.markdown('##### Población por Nacionalidad')
            tipo_poblacion_counts = filtered_df['Nacionalidad'].value_counts().reset_index()
            tipo_poblacion_counts.columns = ['Nacionalidad', 'Count']
            fig = px.pie(tipo_poblacion_counts, values='Count', names='Nacionalidad', width=300, height=350, color_discrete_sequence=color_scale_10)
            st.plotly_chart(fig)
        with col3:
            st.markdown('##### Población por Tipo de Población')
            tipo_poblacion_counts = filtered_df['Tipo_de_poblacion'].value_counts().reset_index()
            tipo_poblacion_counts.columns = ['Tipo_de_poblacion', 'Count']
            fig = px.pie(tipo_poblacion_counts, values='Count', names='Tipo_de_poblacion', width=300, height=350, color_discrete_sequence=color_scale_10)
            st.plotly_chart(fig)



        st.markdown("""
            <div style="background-color:#66c2e5; padding:1px; border-radius:5px; margin-top:1px; margin-bottom:20px;">
                <h4 style="color:black; text-align:center; margin:0;">Orientación</h4>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3= st.columns(3)
        with col1:
            st.markdown('##### Orientacion')
            country_consultation_counts = filtered_df['Orientacion'].value_counts().reset_index()
            country_consultation_counts.columns = ['Orientacion', 'Consultation_Count']
            country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

            if not country_consultation_counts_sorted.empty:
                st.dataframe(country_consultation_counts_sorted,
                            column_order=("Orientacion", "Consultation_Count"),
                            hide_index=True,
                            width=None,
                            column_config={
                                "Orientacion": st.column_config.TextColumn(
                                    "Orientación",
                                ),
                                "Consultation_Count": st.column_config.ProgressColumn(
                                    "Cantidad de Personas",
                                    format="%d",
                                    min_value=0,
                                    max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                                )}
                            )
        with col2:
            st.markdown('##### Orientacion_TM_INM')
            country_consultation_counts = filtered_df['Orientacion_TM_INM'].value_counts().reset_index()
            country_consultation_counts.columns = ['Orientacion_TM_INM', 'Consultation_Count']
            country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

            if not country_consultation_counts_sorted.empty:
                st.dataframe(country_consultation_counts_sorted,
                            column_order=("Orientacion_TM_INM", "Consultation_Count"),
                            hide_index=True,
                            width=None,
                            column_config={
                                "Orientacion_TM_INM": st.column_config.TextColumn(
                                    "Orientacion_TM_INM",
                                ),
                                "Consultation_Count": st.column_config.ProgressColumn(
                                    "Cantidad de Personas",
                                    format="%d",
                                    min_value=0,
                                    max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                                )}
                            )
            
        with col3:
            st.markdown('##### Orientacion General')
            country_consultation_counts = filtered_df['Orientacion_General'].value_counts().reset_index()
            country_consultation_counts.columns = ['Orientacion_General', 'Consultation_Count']
            country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

            if not country_consultation_counts_sorted.empty:
                st.dataframe(country_consultation_counts_sorted,
                            column_order=("Orientacion_General", "Consultation_Count"),
                            hide_index=True,
                            width=None,
                            column_config={
                                "Orientacion_General": st.column_config.TextColumn(
                                    "Orientación",
                                ),
                                "Consultation_Count": st.column_config.ProgressColumn(
                                    "Cantidad de Personas",
                                    format="%d",
                                    min_value=0,
                                    max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                                )}
                            )

        st.markdown("""
            <div style="background-color:#66c2e5; padding:1px; border-radius:5px; margin-top:1px; margin-bottom:20px;">
                <h4 style="color:black; text-align:center; margin:0;">PRCR</h4>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3= st.columns(3)
        with col1:
            st.markdown('##### PRCR')
            country_consultation_counts = filtered_df['PRCR'].value_counts().reset_index()
            country_consultation_counts.columns = ['PRCR', 'Consultation_Count']
            country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

            if not country_consultation_counts_sorted.empty:
                st.dataframe(country_consultation_counts_sorted,
                            column_order=("PRCR", "Consultation_Count"),
                            hide_index=True,
                            width=None,
                            column_config={
                                "PRCR": st.column_config.TextColumn(
                                    "PRCR",
                                ),
                                "Consultation_Count": st.column_config.ProgressColumn(
                                    "Cantidad de Personas",
                                    format="%d",
                                    min_value=0,
                                    max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                                )}
                            )
        with col2:
            st.markdown('##### PRCR_TM_INM')
            country_consultation_counts = filtered_df['PRCR_TM_INM'].value_counts().reset_index()
            country_consultation_counts.columns = ['PRCR_TM_INM', 'Consultation_Count']
            country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

            if not country_consultation_counts_sorted.empty:
                st.dataframe(country_consultation_counts_sorted,
                            column_order=("PRCR_TM_INM", "Consultation_Count"),
                            hide_index=True,
                            width=None,
                            column_config={
                                "PRCR_TM_INM": st.column_config.TextColumn(
                                    "PRCR_TM_INM",
                                ),
                                "Consultation_Count": st.column_config.ProgressColumn(
                                    "Cantidad de Personas",
                                    format="%d",
                                    min_value=0,
                                    max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                                )}
                            )
            
        with col3:
            st.markdown('##### PRCR COMAR')
            country_consultation_counts = filtered_df['PRCR_COMAR'].value_counts().reset_index()
            country_consultation_counts.columns = ['PRCR_COMAR', 'Consultation_Count']
            country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

            if not country_consultation_counts_sorted.empty:
                st.dataframe(country_consultation_counts_sorted,
                            column_order=("PRCR_COMAR", "Consultation_Count"),
                            hide_index=True,
                            width=None,
                            column_config={
                                "PRCR_COMAR": st.column_config.TextColumn(
                                    "PRCR_COMAR",
                                ),
                                "Consultation_Count": st.column_config.ProgressColumn(
                                    "Cantidad de Personas",
                                    format="%d",
                                    min_value=0,
                                    max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                                )}
                            )

        col1, col2, col3= st.columns(3)
        with col1:
            st.markdown('#####  PRCR General')
            country_consultation_counts = filtered_df['PRCR_General'].value_counts().reset_index()
            country_consultation_counts.columns = ['PRCR_General', 'Consultation_Count']
            country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

            if not country_consultation_counts_sorted.empty:
                st.dataframe(country_consultation_counts_sorted,
                            column_order=("PRCR_General", "Consultation_Count"),
                            hide_index=True,
                            width=None,
                            column_config={
                                "PRCR_General": st.column_config.TextColumn(
                                    "PRCR_General",
                                ),
                                "Consultation_Count": st.column_config.ProgressColumn(
                                    "Cantidad de Personas",
                                    format="%d",
                                    min_value=0,
                                    max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                                )}
                            )
        with col2:
            st.markdown('##### PRCR Exp General')
            country_consultation_counts = filtered_df['PRCR_Exp_General'].value_counts().reset_index()
            country_consultation_counts.columns = ['PRCR_Exp_General', 'Consultation_Count']
            country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

            if not country_consultation_counts_sorted.empty:
                st.dataframe(country_consultation_counts_sorted,
                            column_order=("PRCR_Exp_General", "Consultation_Count"),
                            hide_index=True,
                            width=None,
                            column_config={
                                "PRCR_Exp_General": st.column_config.TextColumn(
                                    "PRCR_Exp_General",
                                ),
                                "Consultation_Count": st.column_config.ProgressColumn(
                                    "Cantidad de Personas",
                                    format="%d",
                                    min_value=0,
                                    max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                                )}
                            )
            
        with col3:
            st.markdown('##### PRCR Otros')
            country_consultation_counts = filtered_df['PRCR_Otros'].value_counts().reset_index()
            country_consultation_counts.columns = ['PRCR_Otros', 'Consultation_Count']
            country_consultation_counts_sorted = country_consultation_counts.sort_values(by='Consultation_Count', ascending=False)

            if not country_consultation_counts_sorted.empty:
                st.dataframe(country_consultation_counts_sorted,
                            column_order=("PRCR_Otros", "Consultation_Count"),
                            hide_index=True,
                            width=None,
                            column_config={
                                "PRCR_Otros": st.column_config.TextColumn(
                                    "PRCR_Otros",
                                ),
                                "Consultation_Count": st.column_config.ProgressColumn(
                                    "Cantidad de Personas",
                                    format="%d",
                                    min_value=0,
                                    max_value=country_consultation_counts_sorted['Consultation_Count'].max()
                                )}
                            )




















        

    # Sidebar navigation without any default selection
    page = st.sidebar.radio(
        "PÁGINA",
        ("Kobo", "Atención Humanitaria", "Atención Legal"),
        index=None
    )

    # Display the selected page
    if page == "Kobo":
        page1()
    elif page == "Atención Humanitaria":
        page2()
    elif page == "Atención Legal":
        page3()
    



dashboard()

















    

    

