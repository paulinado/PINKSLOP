import streamlit as st
from deta import Deta

def updateSetting():
    deta = Deta(st.secrets["data_key"])
    db = deta.Base("user_settings")
    st.session_state = count_input.value
    db.put({'username': st.session_state.username, 'numPerLevel': st.session_state.numPerLevel})

def reset():
    st.success('Your progress has been reset', icon="✅")

def createPage():
    global count_input
    deta = Deta(st.secrets["data_key"])
    db = deta.Base("user_settings")

    st.title("Settings")
    st.button("Reset progress", on_click=reset)

    user_settings = db.fetch()
    for setting in user_settings:
         if setting['user'] == st.session_state.username:
              st.session_state.numPerLevel = setting['numPerLevel']
    
    count_input = st.number_input(
            label="Counter",
            min_value=1,
            max_value=100,
            value=st.session_state.numPerLevel,
            step=1,
            onChange=updateSetting,
            )
    
