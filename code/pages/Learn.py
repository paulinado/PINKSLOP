import streamlit as st

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
    st.image(image='../../elements/polly_pig.jpg')

with col2:
    button = st.empty()
    click = button.button("Begin Learning 🎉", on_click=click_button)
    if st.session_state.clicked:
        start_quiz()
        button.empty()
