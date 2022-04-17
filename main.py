import streamlit as st
from datetime import date, time, datetime
import requests

import Homepage
import world_statistics

st.set_page_config(
    page_title="Project 2 - Streamlit App",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. "
    }
)

# SIDEBAR
sidebar_selectbox = st.sidebar.selectbox(
    "Select a Project",
    ["COVID-19 Statistics","About"]
)



if sidebar_selectbox == "COVID-19 Statistics":
    # containers
    st.title("Coronavirus (COVID-19) Statistics Data")
    header = st.container()
    dataset = st.container()
    features = st.container()

    world_statistics.covid_sta()






else:
    Homepage.about()




