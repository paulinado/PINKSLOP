import streamlit as st
 
learn, progress, settings = st.tabs(["Learn", "Progress", "Settings"])

with learn:
    st.header("Learn")

with progress:
    st.header("Progress")

with settings:
    st.header("Settings")