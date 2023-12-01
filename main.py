import extra_streamlit_components as stx
import streamlit as st
import pandas as pd
from view.components import *
from time import sleep


# if 'data' not in st.session_state:
#     st.session_state['data'] = []
# 
# if 'nodes' not in st.session_state:
#     st.session_state['nodes'] = []
# 
# if 'lats' not in st.session_state:
#     st.session_state['lats'] = []
# 
# if 'lngs' not in st.session_state:
#     st.session_state['lngs'] = []
# 

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
            map(st.session_state['lats'],st.session_state['lngs'],np.array(st.session_state['demands']) * 5100)
        # _,_,center,_,_ = st.columns(5,gap='large')
        # with center :
        #     st.button('aa',use_container_width=True)
    case 1:
        st.title('Entre the demand values')
        st.session_state['demands'] = [1] * len(st.session_state['nodes'])
        col1,col2 = st.columns(2,gap="medium")
        with col1:
            for idx,node in enumerate(st.session_state['nodes']):
                st.session_state['demands'][idx] = st.number_input(node,min_value=1,max_value=5)
        with col2:
            map(st.session_state['lats'],st.session_state['lngs'],np.array(st.session_state['demands']) * 1100)
        #st.write(st.session_state)
    case 2:
        show_result()
        

    
