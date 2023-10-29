import streamlit as st
from deta import Deta
import time

deta = Deta(st.secrets["data_key"])
db = deta.Base("progress-2")

# def updateSetting():
#     st.session_state = count_input.value
#     db.put({'username': st.session_state.username, 'numPerLevel': st.session_state.numPerLevel})

def reset(key):
    db.put({'level': 0, 'questions':[[],[],[]], 'first_time_correct':[0,0,0], 'current_question':0, 'answers':[dict(),dict(),dict()], 'questions_answered':0},key)
    pl = st.empty()
    for k in st.session_state.keys():
        del st.session_state[k]
    pl.success('Your progress has been reset', icon="✅")
    time.sleep(3)
    pl.empty()

def createPage(key):
    # global count_input
    # deta = Deta(st.secrets["data_key"])
    # db = deta.Base("user_settings")

    st.title("Settings")
    clicked = st.button("Reset progress")
    if clicked:
        reset(key)

    # user_settings = db.fetch()
    # for setting in user_settings:
    #      if setting['user'] == st.session_state.username:
    #           st.session_state.numPerLevel = setting['numPerLevel']
    
    # count_input = st.number_input(
    #         label="Counter",
    #         min_value=1,
    #         max_value=100,
    #         value=st.session_state.numPerLevel,
    #         step=1,
    #         onChange=updateSetting,
    #         )
    
