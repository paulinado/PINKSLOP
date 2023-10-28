import streamlit as st

st.header("Settings")

def reset():
    st.success('Your progress has been reset', icon="✅")

st.button("Reset progress", on_click=reset)

