import streamlit as st


def about():
    st.title("About")

    st.write("The COVID-19 pandemic continues to impact countries around the world. Many people are still being infected, and the number of new coronavirus cases around the world is fluctuating. Several COVID-19 vaccines have been authorized for use in several countries, and immunization campaigns are currently underway. Nonetheless, it is critical for the people to remain cautious, take safety precautions, and observe all rules and regulations.")
    st.write("This is an app that shows the most recent data available on total cases, deaths, and recovered cases. ")
    st.write("For general information including symptoms, testing, and community safety, visit https://www.cdc.gov.")

    st.write("""
            # Information
            ***This app was created by Luis Socarras, a student at Florida International University***
            
            """)

    st.write("""
    # Resources
    """)
    st.info("""[Open Disease API](https://disease.sh/) """)
    st.info("""[Our World in Data](https://ourworldindata.org/epi-curve-covid-19) """)