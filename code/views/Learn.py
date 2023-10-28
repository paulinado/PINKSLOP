import streamlit as st
from PIL import Image
import path
import sys

def click_button():
    st.session_state.clicked = True

def start_quiz():
    level=0
    num = level/7
    string = "Level "+str(level)
    st.progress(num, string)
    st.text('This is some text.')
        
def createPage():
    st.title("Learn")
    col1, col2, col3 = st.columns([1, 2, 1])

    dir = path.Path(__file__).abspath().parent.parent.parent
    sys.path.append(dir.parent.parent.parent)
    
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False
    
    with col3:
        path_to_image = dir + "/elements/polly_pig.jpg"
        image = Image.open(path_to_image)
        st.image(image=image)

    with col2:
        button = st.empty()
        click = button.button("Begin Learning 🎉", on_click=click_button)
        if st.session_state.clicked:
            start_quiz()
            button.empty()