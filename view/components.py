import streamlit as st
import pandas as pd
from data.data import fetch_wilayas


def map():
    df = pd.DataFrame(
        {
            'lat' : st.session_state['lats'],
            'lon' : st.session_state['lngs'],
        })

    st.map(df,latitude='lat',longitude='lon',size=15000,use_container_width=True)


def location_multiselect(): 
    lats = []
    lngs = []
    nodes = fetch_wilayas()
    st.session_state['lats'] = [36.7539]
    st.session_state['lngs'] = [3.0589]
    st.session_state['nodes'] = ['depot']
    options = st.multiselect('Choose the nodes',nodes.keys(),[])
    for wilaya in options:
        lats.append(float(nodes[wilaya][0]))
        lngs.append(float(nodes[wilaya][1]))
    st.session_state['lats'] = lats
    st.session_state['lngs'] = lngs
    st.session_state['nodes'] = options

    


def result():
    st.title('Result')