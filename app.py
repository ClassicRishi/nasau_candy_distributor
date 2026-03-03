from features import TimeDelayFeatures,ShippingLeadTime,RouteVolume,NormalizedLeadTime
import streamlit as stl
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
import pandas as pd
from datetime import datetime
import numpy as np

stl.sidebar.title("Nasau Candy Distributor")

shipping_lead_time = ShippingLeadTime()

stl.set_page_config(
    page_title="Nasau_Shipping_Route_Analysis",
    page_icon="🍬"
)

page = stl.sidebar.radio("Select",["Shipment Delay","Average Lead Time","Route_Volume","Shipment Delay Frequency","Normalized Lead Time Performance"])

if page == "Shipment Delay":
    col1,col2 = stl.columns(2)
    with col1:
        fromdate = stl.date_input("ORDER DATE FROM",value=datetime(2020,1,3),max_value="today")
    with col2:
        todate = stl.date_input("ORDER DATE TO",value=datetime(2020,1,4))

    time_de_features = TimeDelayFeatures(fromdate,todate)

    dataset = time_de_features.ExtractFeatures()
    delay_df = pd.DataFrame({
        'factory': dataset[0],
        'delay in days': dataset[1]
    })

    chart = alt.Chart(delay_df).mark_arc().encode(
        theta='delay in days',
        color='factory',
        tooltip=['factory','delay in days']
    )

    delay_fig = go.Figure(data=[
        go.Bar(
            x=delay_df['factory'],
            y=delay_df['delay in days'],
            width=[0.4,0.4,0.4,0.4,0.4],
            text=[i for i in delay_df['delay in days']]
        )
    ])

    delay_fig.update_layout(
        xaxis_title="Factory",
        yaxis_title="Delay In Days"
    )

    stl.plotly_chart(delay_fig)
elif page == "Average Lead Time":
    # mean shipping lead time analysis

    col1,col2,col3,col4,col5,col6 = stl.columns(6)
    city1,city2,city3,city4,city5,type = None,None,None,None,None,None
    with col1:
        city1 = stl.selectbox("City1",shipping_lead_time.get_cities(),index=5)
    with col2:
        city2 = stl.selectbox("City2",shipping_lead_time.get_cities(),index=10)
    with col3:
        city3 = stl.selectbox("City3",shipping_lead_time.get_cities(),index=56)
    with col4:
        city4 = stl.selectbox("City4",shipping_lead_time.get_cities(),index=78)
    with col5:
        city5 = stl.selectbox("City5",shipping_lead_time.get_cities(),index=110)
    with col6:
        type = stl.selectbox("Type",["Line","Bar","Scatter"],index=1)

    mean_leadtime = shipping_lead_time.GatherAverage(city1,city2,city3,city4,city5)

    mean_leadtime_df = pd.DataFrame({
        "factory": [i[0] for i in mean_leadtime],
        "Average Lead Time": [i[1] for i in mean_leadtime],
    })

    if type == "Bar":

        average_leadtime_fig = go.Figure(data=[
            go.Bar(
                x=mean_leadtime_df['factory'],
                y=mean_leadtime_df['Average Lead Time'],
                width=[0.4,0.4,0.4,0.4,0.4],
                text=mean_leadtime_df['Average Lead Time']
            )
        ])

        average_leadtime_fig.update_layout(
            xaxis_title="factory",
            yaxis_title="Average Lead Time"
        )

        stl.plotly_chart(average_leadtime_fig)
    elif type == "Line":

        # Average Lead Time visualization
        average_leadtime_visual = px.line(mean_leadtime_df,x="factory",y="Average Lead Time",markers="o")

        stl.plotly_chart(average_leadtime_visual)
    elif type == "Scatter":
        # Average Lead Time visualization
        average_leadtime_visual = px.scatter(mean_leadtime_df,x="factory",y="Average Lead Time")

        stl.plotly_chart(average_leadtime_visual)

elif page == "Route_Volume":

    col1,col2,col3,col4,col5 = stl.columns(5)
    city1,city2,city3,city4,city5 = None,None,None,None,None
    with col1:
        city1 = stl.selectbox("City1",shipping_lead_time.get_cities(),index=5)
    with col2:
        city2 = stl.selectbox("City2",shipping_lead_time.get_cities(),index=10)
    with col3:
        city3 = stl.selectbox("City3",shipping_lead_time.get_cities(),index=56)
    with col4:
        city4 = stl.selectbox("City4",shipping_lead_time.get_cities(),index=78)
    with col5:
        city5 = stl.selectbox("City5",shipping_lead_time.get_cities(),index=110)

    # Route Volume
    route_volume_data = RouteVolume().GatherRouteVolume(city1,city2,city3,city4,city5)
    route_volume_df = pd.DataFrame({
        'city': [i[0] for i in route_volume_data],
        'route_volume': [i[1] for i in route_volume_data]
    })

    # route volume visualization
    route_volume_visual = px.line(route_volume_df,x="city",y="route_volume",markers="o")

    stl.plotly_chart(route_volume_visual)
elif page == "Shipment Delay Frequency":
    col1,col2 = stl.columns(2)
    with col1:
        fromdate = stl.date_input("ORDER DATE FROM",value=datetime(2020,1,3),max_value="today")
    with col2:
        todate = stl.date_input("ORDER DATE TO",value=datetime(2020,1,29))

    time_de_features = TimeDelayFeatures(fromdate,todate)

    dataset = time_de_features.ExtractFeatures()
    delay_df = pd.DataFrame({
        'factory': dataset[0],
        'delay frequency': dataset[1]
    })

    delay_freq = px.histogram(delay_df['delay frequency'],nbins=len(dataset[0]))

    delay_freq.update_traces(
        textposition="inside",
        text=dataset[0]
    )

    stl.plotly_chart(delay_freq)
else:
    col1,col2,col3,col4 = stl.columns(4)

    with col1:
        fromdate = stl.date_input("ORDER DATE FROM",value=datetime(2020,1,3),max_value="today")
    with col2:
        todate = stl.date_input("ORDER DATE TO",value=datetime(2020,1,4))
    with col3:
        expected_lead_time = stl.number_input("Expected Lead Time",min_value=1,max_value=200,value=10,step=1)
    with col4:
        customer_id = stl.number_input("Customer_ID",step=1,min_value=100000,value=112326)

    time_de_features = TimeDelayFeatures(fromdate,todate)

    dataset = time_de_features.ExtractFeatures()
    delay_df = pd.DataFrame({
        'factory': dataset[0],
        'delay in days': dataset[1]
    })

    normalized_time = NormalizedLeadTime()
    normalizeddataframe = normalized_time.GatherNormalizedLeadTime(customer_id,expected_lead_time)

    normalized_visual = px.line(normalizeddataframe,x="factories",y="Delay in %(Acc. to Expected days)",markers="o")

    stl.plotly_chart(normalized_visual)