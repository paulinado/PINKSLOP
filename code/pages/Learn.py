import streamlit as st
from PIL import Image
import path
import sys

level=0
col1, col2, col3 = st.columns([1, 2, 1])

dir = path.Path(__file__).abspath()
sys.path.append(dir.parent.parent.parent)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

def start_quiz():
    st.header("Learn")
    st.progress(level/7, "Level "+str(level))

with col3:
    path_to_image = "./../elements/polly_pig.jpg"
    image = Image.open(path_to_image)
    st.image(image=image)

with col2:
    button = st.empty()
    click = button.button("Begin Learning 🎉", on_click=click_button)
    if st.session_state.clicked:
        start_quiz()
        button.empty()