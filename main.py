import extra_streamlit_components as stx
import streamlit as st
import pandas as pd
from view.components import *
from src.main import *

st.set_page_config(layout="wide")
val = stx.stepper_bar(steps=["Pick locations","Set demand values" ,"Result"],lock_sequence=False)

match val:
    case 0:
        st.title('Choose your client destinations')
        st.divider()
        col1,col2 = st.columns(2,gap="large")
        with col1:
            location_multiselect()
        with col2:
            map()
        # _,_,center,_,_ = st.columns(5,gap='large')
        # with center :
        #     st.button('aa',use_container_width=True)
    case 1:
        st.session_state['demands'] = [0.01] * len(st.session_state['nodes'])
        for idx,node in enumerate(st.session_state['nodes']):
            st.session_state['demands'][idx] = st.number_input(node,min_value=0.01)
        st.write(st.session_state)
    case 2:
        data = {}
        data['capacity'] = 5
        data['nodes'] = []
        for index,node in enumerate(st.session_state['nodes']):
            demand = st.session_state['demands'][index]
            lat= st.session_state['lats'][index]
            lng= st.session_state['lngs'][index]
            depot = {'label' : node, 'demand' : demand, 'posX' : lat, 'posY' : lng}
            data['nodes'].append(depot)
        with st.spinner('Wait for it...'):
            result,cost = vrp(data=data,popsize=50,iterations=100)
        st.write(result)
        st.write(cost)
        

    
