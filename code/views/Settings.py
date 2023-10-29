import streamlit as st
from deta import Deta

# def updateSetting():
#     st.session_state.db.update({'numPerLevel': st.session_state.numPerLevel},st.session_state.key)

def reset():
    st.success('Your progress has been reset', icon="✅")

def createPage(key):
    deta = Deta(st.secrets["data_key"])
    db = deta.Base("user_settings")

    st.title("Settings")
    st.button("Reset progress", on_click=reset)

    user_settings = db.fetch()
    print("Checking user settings:")
    print(user_settings)    

    for setting in user_settings.items:
         print(setting)
         if setting['key'] == key:
                st.session_state.numPerLevel = setting['numPerLevel']

    print("making counter")
    count_input = st.number_input(
            label="Number of questions per Level",
            min_value=1,
            max_value=100,
            value=st.session_state.numPerLevel,
            step=1,
            # onChange=lambda:st.session_state.db.update({'numPerLevel': st.session_state.numPerLevel},st.session_state.key)
            )
    
    print("Writing output")
    st.write(count_input)
    st.write(count_input.value)

    
