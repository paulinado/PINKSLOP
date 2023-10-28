import streamlit as st
from PIL import Image

level=0
col1, col2, col3 = st.columns([1, 2, 1])

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

def start_quiz():
    st.header("Learn")
    st.progress(level/7, "Level "+str(level))

with col3:
    image = Image.open('./../elements/polly_pig.jpg')
    st.image(image=image)

with col2:
    button = st.empty()
    click = button.button("Begin Learning 🎉", on_click=click_button)
    if st.session_state.clicked:
        start_quiz()
        button.empty()
