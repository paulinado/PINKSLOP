import streamlit as st
import pandas as pd
from auth0_component import login_button
 
st.write("""
# My first app
Hello *world!*
""")

clientId = "cONtS7pEn44avXLyIsdJngqkDu0bwGqj"
domain = "dev-ep7cvhbpossvx8o6.uk.auth0.com"

user_info = login_button(clientId, domain = domain)
st.write(user_info)
 
st.header("Home")
