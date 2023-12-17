import streamlit as st
import pandas as pd
import plotly.express as px
import main
import json
import pathForecast
from efficientFrontier import get_efficentFrontierOPT, get_GraphefficentFrontier
st.set_page_config(layout="wide")


with st.sidebar:
    sidebar = st.selectbox("Select operation", ["Simulations", "Simulations vizualizations", 
                                                "GBM Forecast", "Universal Forecast", "Efficient Frontier"])

df = pd.read_csv('csv/tickers.csv')

if sidebar == "Simulations":
    edited_df = st.data_editor(df)
    if st.button('Save changed df'):
        edited_df.to_csv('csv/tickers.csv', index=False)

    option = st.selectbox("Select ticker for simulation", df["ticker"].to_list())
    k = st.number_input("Number of symulations", 1, 900000000000, 1000, step=1000)
    if st.button('Start single simulation'):
        denst = main.get_valuationDistribution(df, [option], 10, k)
        st.write(denst)
        fig = px.bar(x = denst[1], y = denst[0])
        st.plotly_chart(fig)
        
    if st.button('Start all simulations'):
        denst = main.get_valuationDistribution(df, df["ticker"].to_list(), 10, k)

if sidebar == "Simulations vizualizations":
    f = open('jsons/valJSON.json')
    data = json.loads(json.loads(f.read()))
    for ticker in data.keys():
        fig = px.bar(x =data[ticker]["x"], y = data[ticker]["y"], title=ticker)
        st.plotly_chart(fig)
        
if sidebar == "GBM Forecast":
    f = open('jsons/gbmForecast.json')
    data = json.loads(json.loads(f.read()))
    
    if st.button("Run new GBM simulation"):
        pathForecast.forecastGBMAllPaths()
    
    for ticker in data.keys():
        if ticker == "years" or ticker == "simNum":
            continue
        
        df = pd.DataFrame.from_dict(data[ticker])
        fig = px.line(df, x = "time",  y = list(df.columns)[:-1], title=ticker )
        st.plotly_chart(fig)
        
if sidebar == "Universal Forecast":
    f = open('jsons/universalForecast.json')
    data = json.loads(json.loads(f.read()))
    
    if st.button("Run new universal simulation"):
        pathForecast.forecastUniversalAllPaths()
    
    for ticker in data.keys():
        if ticker == "years" or ticker == "simNum":
            continue
        
        df = pd.DataFrame.from_dict(data[ticker])
        fig = px.line(df, x = "time",  y = list(df.columns)[:-1], title=ticker )
        st.plotly_chart(fig)
        
if sidebar == "Efficient Frontier":
    #ef = get_efficentFrontierOPT("jsons/universalForecast.json", percentage=50)
    st.write("universalForecast.json")
    fig, sharpe, vol = get_GraphefficentFrontier("jsons/universalForecast.json", percentage=50)
    st.write(sharpe)
    st.pyplot(fig)
    
    #ef = get_efficentFrontierOPT("jsons/gbmForecast.json", percentage=60)
    st.write("gbmForecast.json")
    fig, sharpe, vol = get_GraphefficentFrontier("jsons/gbmForecast.json", percentage=75)
    st.write(sharpe)
    st.pyplot(fig)
