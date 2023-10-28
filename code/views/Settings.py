import streamlit as st



def reset():
    st.success('Your progress has been reset', icon="✅")

def createPage():
    st.title("Settings")
    st.button("Reset progress", on_click=reset)