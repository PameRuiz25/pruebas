# 1. Libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# 2. Page Configuration
st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# PRUEBA DE QUE FUNCIONA STREAMLIT
st.write("Streamlit is working!")

# PRUEBA. DISPLAY DASHBOARD
df = pd.read_csv('data_complete.csv')
st.write(df)






