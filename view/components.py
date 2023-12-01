import streamlit as st
import pandas as pd
import numpy as np
from data.data import fetch_wilayas
from src.main import *



def map(lat,lng,size):
    df = pd.DataFrame(
        {
            'lat' : lat,
            'lon' : lng,
            'size' : size,
        })
    st.map(df,latitude='lat',longitude='lon',size='size',use_container_width=True)


def location_multiselect(): 
    lats = []
    lngs = []
    nodes = fetch_wilayas()
    st.session_state['demands'] = []
    st.session_state['lats'] = []
    st.session_state['lngs'] = []
    st.session_state['nodes'] = []
    st.session_state['data'] = {'Depot': [3.0589,36.7539]}
    options = st.multiselect('Choose the nodes',nodes.keys(),[])
    for wilaya in options:
        lats.append(float(nodes[wilaya][0]))
        lngs.append(float(nodes[wilaya][1]))
        st.session_state['data'].update({wilaya : [float(nodes[wilaya][1]),float(nodes[wilaya][0])]})
        
    st.session_state['demands'] = [1] * len(options)
    st.session_state['lats'] = lats
    st.session_state['lngs'] = lngs
    st.session_state['nodes'] = options
    # st.write(st.session_state)
    

    
def show_result():
    st.title('Result')
    data = {}
    data['nodes'] = [{'label' : 'Depot', 'demand' : 0, 'posX' : 36.7539, 'posY' : 3.0589}]
    for index,node in enumerate(st.session_state['nodes']):
        demand = st.session_state['demands'][index]
        lat= st.session_state['lats'][index]
        lng= st.session_state['lngs'][index]
        depot = {'label' : node, 'demand' : demand, 'posX' : lat, 'posY' : lng}
        data['nodes'].append(depot)
    with st.spinner('Wait for it...'):
        result,cost = vrp(data=data)        
    for wilaya in result:                        
        st.markdown(f'#### {wilaya}')
    st.markdown('## The cost is :green[{:.2f}]'.format(cost))
        # df = []
# 
        # for index in range(len(result) - 1):
        #     current_wilaya = result[index]
        #     next_wilaya = result[index+1]
        #     entry = {
        #         'name' : f'{current_wilaya} - {next_wilaya}',
        #         'path' : [
        #             st.session_state['data'][current_wilaya],
        #             st.session_state['data'][next_wilaya]
        #         ],
        #     }
        #     print(entry)
        #     df.append(entry)
        # df = pd.DataFrame.from_dict(df)
# 
        # color_lookup = pdk.data_utils.assign_random_colors(df['name'])
        # df['color'] = df.apply(lambda row: color_lookup.get(row['name']), axis=1)
        # print(df)
        # layer = pdk.Layer(
        # type="PathLayer",
        # data=df,
        # pickable=True,
        # get_color="color",
        # width_scale=20,
        # width_min_pixels=2,
        # get_path="path",
        # get_width=5,
        # )
        # view_state = pdk.ViewState(zoom=10)
        # r = pdk.Deck(layers=[layer],initial_view_state=view_state, tooltip={"text": "{name}"})
        # 
        # st.pydeck_chart(r)
        
        
        

