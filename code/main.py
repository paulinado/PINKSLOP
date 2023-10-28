import streamlit as st
import pandas as pd
from auth0_component import login_button

st.header("Home")

clientId = "cONtS7pEn44avXLyIsdJngqkDu0bwGqj"
domain = "dev-ep7cvhbpossvx8o6.uk.auth0.com"

login_button(clientId, domain = domain)
