import pandas as pd
import streamlit as st
from datetime import date, time, datetime
import requests
import plotly.express as px


def worldwide():
    # containers
    header = st.container()
    dataset = st.container()
    features = st.container()

    '''
        start_date = st.sidebar.date_input('Start date', date(2019, 7, 6))
    end_date = st.sidebar.date_input('End date', date(2020, 7, 6))

    if start_date < end_date:
        st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else:
        st.error('Error: End date must fall after start date.')
   '''
    with header:
        st.write("""
        # COVID-19 Worldwide
        Current global ***COVID-19*** statistics 
    
        """)

    with dataset:
        total_global_url = "https://disease.sh/v3/covid-19/all"
        global_dic = requests.get(total_global_url).json()
        # st.write("Last Update " + str.global_dic["updated"])
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        # Display metrics
        col1.metric("Cases", global_dic['cases'], global_dic['todayCases'])
        col2.metric("Deaths", global_dic['deaths'], global_dic['todayDeaths'])
        col3.metric("Recovered", global_dic['recovered'], global_dic['todayRecovered'])

        # get date
        # today = datetime.today().strftime('%m/%d/%Y')

    with features:
        st.write(" ")
        selc_type = st.radio(
            "Select Chart",
            ('Cases history over time', 'Countries Comparison'))

        # input_box = st.selectbox("Object", options=["cases", "deaths", "recovered"])

        if selc_type == 'Cases history over time':
            # Chart
            st.write("Chart")
            global_dic_byDate = requests.get("https://disease.sh/v3/covid-19/historical/all?lastdays=all").json()

            # st.bar_chart(global_dic_byDate)
            c_pairs = global_dic_byDate["cases"]
            # st.dataframe(c_pairs)

            data_cases = []
            data_set_cases = global_dic_byDate['cases']

            df = pd.DataFrame.from_dict(c_pairs, orient='index', columns=['cases'])
            # data_set_recovered = global_dic_byDate['recovered']
            # data_set_deaths = global_dic_byDate['deaths']

            # st.dataframe(df)
            fig3 = px.line(df, y="cases", range_y=[0, 600000000], title=" Cases History")
            # df = pd.DataFrame(data_set_cases)
            # st.line_chart(data_cases)
            st.write(fig3)
        elif selc_type == 'Countries Comparison':


            covid = pd.read_csv(
                'https://raw.githubusercontent.com/shinokada/covid-19-stats/master/data/daily-new-confirmed-cases-of-covid-19-tests-per-case.csv')
            covid.columns = ['Country', 'Code', 'Date', 'Confirmed', 'Days since confirmed']
            covid['Date'] = pd.to_datetime(covid['Date']).dt.strftime('%Y-%m-%d')
            #st.write(covid)

            country_options = covid['Country'].unique().tolist()
            date_options = covid['Date'].unique().tolist()
            #date = st.selectbox('Which date would you like to see?', date_options, 100)
            country = st.multiselect("Which country would you like to see?", country_options, ['United States', 'Brazil', 'Spain'])


            covid = covid[covid['Country'].isin(country)]
            #covid = covid[covid["Date"] == date]
            fig1= px.line(covid, x="Date", y="Confirmed", color="Country", range_y=[0, 35000])
            fig2 = px.bar(covid, x="Country", y="Confirmed", color="Country", range_y=[0, 35000], animation_frame='Date', animation_group="Country")
            fig2.update_layout(width=800)
            fig1.update_layout(width=800)

            fig2.layout.updatemenus[0].buttons[0].args[1]['frame']['duration']= 30
            fig2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration']= 5

            st.caption("Animated Chart")
            st.write(fig2)
            st.caption("Line Chart")
            st.write(fig1)



        #st.line_chart(df)


def covid_sta():
    global state_selected

    # get the list of all countries
    countries_url = "https://disease.sh/v3/covid-19/countries?"
    countries_dict = requests.get(countries_url).json()

    countries_list = []
    for country in countries_dict:
        countries_list.append(country["country"])
    countries_list.insert(0, "USA")
    countries_list.insert(0, "Worldwide")

    # st.dataframe(countries_dict)
    # sideBar
    country_selected = st.sidebar.selectbox("Select a country:", options=countries_list)

    # df = pd.DataFrame.from_dict(countries_dict,  orient='index', columns=['cases'])

    # st.write(df)

    # USA ###############################################################
    # get the STA for each state in the USA
    states_url = "https://disease.sh/v3/covid-19/states"
    states_dict = requests.get(states_url).json()
    states_list = []
    # store all states into dic
    for state in states_dict:
        states_list.append(state["state"])
    states_list.insert(0, "All states")

    # if USA is selected, open selection box for states
    if country_selected == "USA":
        # sidebar box for states
        state_selected = st.sidebar.selectbox("Select a state:", options=states_list)

    # if worldwide is selected, open worldwide sta
    if country_selected == "Worldwide":
        worldwide()

    # if a state is selected, open sta for the state
    elif country_selected == "USA" and state_selected != "All states":
        st.title(state_selected)
        states_url = "https://disease.sh/v3/covid-19/states/{0}".format(state_selected)
        states_dict = requests.get(states_url).json()

        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        # Display metrics
        st.write("")
        st.write("")
        st.write("")
        col1.metric("Cases", states_dict['cases'], states_dict['todayCases'])
        col2.metric("Deaths", states_dict['deaths'], states_dict['todayDeaths'])
        col3.metric("Recovered", states_dict['recovered'], 0)

        # General STA
        st.write("""""")
        st.text("Statistics totals")
        st.write("Cases: ", states_dict['cases'])
        st.write("Cases today: ", states_dict['todayCases'])
        st.write("Deaths: ", states_dict['deaths'])
        st.write("Deaths today: ", states_dict['todayDeaths'])
        st.write("Recovered: ", states_dict['recovered'])
        st.write("Active: ", states_dict['active'])
        st.write("Tests: ", states_dict['tests'])
        st.write("Cases Per One Million: ", states_dict['casesPerOneMillion'])
        st.write("Deaths Per One Million: ", states_dict['deathsPerOneMillion'])


        """#################### MAP #######################
        geo = requests.get("https://gist.githubusercontent.com/meiqimichelle/7727723/raw/"
                           "0109432d22f28fd1a669a3fd113e41c4193dbb5d/USstates_avg_latLong")
        geo_dict = geo.json()
        lat = 37.0902
        long = -95.7129
        for i in geo_dict:
            if i["state"] == state_selected:
                lat = i["latitude"]
                long = i["longitude"]
        #st.write("MAP")
        df = pd.DataFrame(
            np.random.randn(states_dict['active'], 2) / [1, 1] + [lat, long],
            columns=['lat', 'lon'])"""
        st.write("Active Cases: ", states_dict['active'])
        #st.map(df)

    # open sta for countries
    else:

        #containers
        header = st.container()
        features = st.container()

        country_historical_url = "https://disease.sh/v3/covid-19/countries/{0}".format(country_selected)
        country_sta_dic = requests.get(country_historical_url).json()



        with header:
            st.title(country_sta_dic['country'])
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            col1.image(country_sta_dic['countryInfo']['flag'], width=150)
            # Display metrics
            col2.metric("Cases", country_sta_dic['cases'], country_sta_dic['todayCases'])
            col3.metric("Deaths", country_sta_dic['deaths'], country_sta_dic['todayDeaths'])
            col4.metric("Recovered", country_sta_dic['recovered'], country_sta_dic['todayRecovered'])


        # Display STA for country
        with features:
            with col1:

                st.write("""""")
                st.write("""""")
                st.write("""""")
                st.write("""""")
                st.text("Statistics totals")
                st.write("Cases: ", country_sta_dic['cases'])
                st.write("Cases today: ", country_sta_dic['todayCases'])
                st.write("Deaths: ", country_sta_dic['deaths'])
                st.write("Deaths today: ", country_sta_dic['todayDeaths'])
                st.write("Recovered: ", country_sta_dic['recovered'])
                st.write("Recovered today: ", country_sta_dic['todayRecovered'])
                st.write("Active: ", country_sta_dic['active'])
                st.write("Critical: ", country_sta_dic['critical'])

                # display STA for vaccines
                vaccines_url = "https://disease.sh/v3/covid-19/vaccine/coverage/countries/{0}?lastdays=1&fullData=true".format(
                    country_selected)
                vaccines_dic = requests.get(vaccines_url).json()
                vaccines = []
                for i in vaccines_dic["timeline"]:
                    vaccines.append(i["total"])

                st.write("Vaccines rolled our: ", vaccines[0])

            with col2:
                countries_historical_url = "https://disease.sh/v3/covid-19/historical/{0}?lastdays=all".format(country_selected)
                countries_sta_dic = requests.get(countries_historical_url).json()
                c_pairs = countries_sta_dic["timeline"]
                w_cases = []
                #st.dataframe(c_pairs)
                #st.dataframe(c_pairs)

                df = pd.DataFrame.from_dict(c_pairs)
                #st.write(df)
                fig1 = px.line(df, y="cases", range_y=[0, country_sta_dic['cases']])
                st.write(" ")
                st.write(fig1)
