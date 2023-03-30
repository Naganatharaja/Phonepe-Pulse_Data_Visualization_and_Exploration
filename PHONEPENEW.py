import streamlit as st
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
import plotly.express as px
import geopandas as gpd
from streamlit_option_menu import option_menu
import requests
from streamlit_lottie import st_lottie

# ----------------------------------MySQl server connection--------------------------------------------

try:
    conn = msql.connect(host='localhost',
                        database='aaj',
                        user='root',
                        password='Aaj2606')
    if conn.is_connected():
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM AggTransByStates")
        records1 = cursor.fetchall()
        AggTransByStates = pd.DataFrame(records1,
                           columns=[i[0] for i  in cursor.description])

        cursor.execute("SELECT * FROM AggUserByBrand")
        records2 = cursor.fetchall()
        AggUserByBrand = pd.DataFrame(records2,
                         columns=[i[0] for i in cursor.description])

        cursor.execute("SELECT * FROM mapTransByDistrict")
        records3 = cursor.fetchall()
        mapTransByDistrict = pd.DataFrame(records3,
                             columns=[i[0] for i in cursor.description])

        cursor.execute("SELECT * FROM mapUserByDistReg")
        records4 = cursor.fetchall()
        mapUserByDistReg = pd.DataFrame(records4,
                                          columns=[i[0] for i in cursor.description])


        conn.commit()
        cursor.close()
        conn.close()
except Error as e:
    pass
# ------------------------------------ MySQl server connection End------------------------------------------------------


# ------------------------------------Side Bar--------------------------------------------------------------------------
with st.sidebar:
    menu = option_menu(
                       menu_title='Main Menu',
                       options=['Home',
                                'APP Registered',
                                'Geo Map',
                                'User Mobile Brand',
                                'Brand percentage'],
                       icons=['house', 'app',
                              'geo-alt', 'phone', 'pie-chart'],
                       default_index=0)

if menu == 'Home':
    # Header or Title of the page
    st.markdown("<h1 style='text-align:center; color:red;'"
                ">Phonepe Pulse Data Visualization and Exploration</h1>",
                unsafe_allow_html=True)

    # ----------------------------------------Lottie Animation----------------------------------------------------------
    def load_lottieURl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_dashboard = load_lottieURl("https://assets10.lottiefiles.com/packages/lf20_91rvnawv.json")
    st_lottie(lottie_dashboard, height=300, width=700, key='Transaction')

    # ------------------------------------Lottie Animation----------------------------------------------------------
    st.write(" PhonePe is an Indian digital payments and financial technology firm based in Bengaluru,"
             " Karnataka. Sameer Nigam, Rahul Chari, and Burzin Engineer started PhonePe"
             " in December 2015. In August 2016, the PhonePe app, which is based on the"
             " Unified Payments Interface (UPI), went live. Flipkart, a Walmart affiliate,"
             " owns it. PhonePe is available in 11 different Indian languages."
             " PhonePe allows users to transfer and receive money.")
# ---------------------------------------Inputs-------------------------------------------------------------------------
yearTuple = ('2018', '2019', '2020', '2021', '2022')
quaterTuple = ('Q1', 'Q2', 'Q3', 'Q4')
stateTuple= ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                 'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                 'uttarakhand', 'west-bengal')

# ---------------------------------------Inputs--------------------------------------------------------------------------

# -----------------------------------App Registered User by District----------------------------------------------------
if menu == 'APP Registered':
    st.markdown("<h1 style='text-align:center; color:red;'"
                ">App Registered User By District</h1>",
                unsafe_allow_html=True)

    barYear = st.selectbox('Select the Year:', yearTuple)
    st.write(' ')

    state = st.selectbox('Select the State:', stateTuple, index=30)

    mapUserByDistReg_filter = mapUserByDistReg[(mapUserByDistReg['State'] == state)
                                     & (mapUserByDistReg['Year'] == int(barYear))]

    dist_reg = mapUserByDistReg_filter.groupby(['District']).sum(numeric_only=True)[['Registered_user','App_opening']]
    dist_reg = dist_reg.reset_index()

    fig1 = px.bar(dist_reg,
                  x="District",
                  y=["Registered_user"],
                  color='District',
                  title=f"District wise registered user in {state}:")
    fig1.update_traces(width=1)
    st.plotly_chart(fig1)

# -----------------------------------App Registered User by District----------------------------------------------------


# ----------------------------------Geo map visualization---------------------------------------------------------------

state_lat_lon = pd.read_csv(r'C:\Users\saran\OneDrive\Desktop\Phonepe\state_lat_lon.csv')

if menu == 'Geo Map':
    st.markdown("<h1 style='text-align:center; color:red;'"
                ">Transaction by State</h1>",
                unsafe_allow_html=True)

    Year = st.radio('Please select the Year', yearTuple, horizontal=True)
    st.write(' ')
    Quarter = st.radio('Please select the Quarter', quaterTuple, horizontal=True)
    st.write(' ')

    AggTransByStates_filter = AggTransByStates.groupby(
                          ['State', 'Year', 'Quater']).sum(numeric_only=True)[['Transacion_amount','Transacion_count']]
    AggTransByStates_filter = AggTransByStates_filter.reset_index()

    yrQtrTrans_filter = AggTransByStates_filter[(AggTransByStates_filter['Year'] == int(Year))
                    & (AggTransByStates_filter['Quater'] == Quarter)]

    lat_lon_df = pd.merge(state_lat_lon, yrQtrTrans_filter)
    lat_lon_df = lat_lon_df.rename(columns={'State': 'state'})

    # getting some geojson for India.  Reduce complexity of geometry to make it more efficient
    url = "https://raw.githubusercontent.com/Subhash9325/GeoJson-Data-of-Indian-States/master/Indian_States"
    gdf = gpd.read_file(url)
    gdf["geometry"] = gdf.to_crs(gdf.estimate_utm_crs()).simplify(1000).to_crs(gdf.crs)
    india_states = gdf.rename(columns={"NAME_1": "ST_NM"}).__geo_interface__

    # create the scatter geo plot
    fig1 = px.scatter_geo(lat_lon_df,
                          lat="latitude",
                          lon="longitude",
                          color="Transacion_amount",
                          size=lat_lon_df["Transacion_count"],
                          hover_name="state",
                          hover_data=["state",
                                     'Transacion_amount',
                                     'Transacion_count',
                                     'Year',
                                     'Quater'],
                          title='State',
                          size_max=10,)

    fig1.update_traces(marker={'color': "#CC0044", 'line_width': 1})

    fig = px.choropleth(
          pd.json_normalize(india_states["features"])["properties.ST_NM"],
          locations="properties.ST_NM",
          geojson=india_states,
          featureidkey="properties.ST_NM",
          color_discrete_sequence=["lightgreen"],)

    fig.update_geos(fitbounds="locations", visible=False)
    fig.add_trace(fig1.data[0])

    fig.update_layout(height=500, width=600)

    # remove white background
    fig.update_geos(bgcolor='#F8F8F8', showland=True)

    st.plotly_chart(fig)
# ------------------------------------Geo map visualization end---------------------------------------------------------

# ------------------------------------User Mobile Brand analysis--------------------------------------------------------
if menu == 'User Mobile Brand':

    st.markdown("<h1 style='text-align:center; color:red;'"
                ">Mobile Brand Analysis by State</h1>",
                unsafe_allow_html=True)

    StateBar = st.selectbox('Please select State', stateTuple, index=30)
    yearBar = st.radio('Please select the Year:', yearTuple, horizontal=True)
    QuaterBar = st.radio('Please select the Quarter:', quaterTuple, horizontal=True)

    UserByBrand_filter = AggUserByBrand[(AggUserByBrand['State'] == StateBar)
                                        & (AggUserByBrand['Year'] == int(yearBar))
                                        & (AggUserByBrand['Quater'] == QuaterBar)]

    userBrand = px.bar(UserByBrand_filter,
                       x='Brand',
                       y='Brand_count',
                       color='Brand',
                       title='User Mobile Brand Analysis ',
                       color_continuous_scale='magma', )

    st.plotly_chart(userBrand)
# ------------------------------------User Mobile Brand Percentage Analysis---------------------------------------------
if menu == 'Brand percentage':
    st.markdown("<h1 style='text-align:center; color:red;'"
                ">Mobile Brand Percentage Analysis</h1>",
                unsafe_allow_html=True)

    StatePie = st.selectbox('Please Choose State', stateTuple, index=30)
    yearPie = st.radio('Please Choose the Year:', yearTuple, horizontal=True)
    QuaterPie = st.radio('Please choose the Quarter:', quaterTuple, horizontal=True)

    UserByBrand_filterPie = AggUserByBrand[(AggUserByBrand['State'] == StatePie)
                                        & (AggUserByBrand['Year'] == int(yearPie))
                                        & (AggUserByBrand['Quater'] == QuaterPie)]

    BrandPercent = px.pie(UserByBrand_filterPie,
                       names='Brand',
                       values='Brand_percentage',
                       color='Brand',
                       template='plotly_dark',
                       title='User Mobile Brand in percentage ',
                       width=800,
                       height=600)

    BrandPercent.update_traces(textposition='inside',
                               textinfo='percent+label',
                               textfont_size=15,
                               insidetextorientation='radial',
                               pull=[0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               marker=dict(line=dict(color='#000000', width=2)))

    BrandPercent.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    st.plotly_chart(BrandPercent)