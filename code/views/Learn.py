import streamlit as st
from PIL import Image
import path
import sys
import time

QUESTIONS_NUMBER = 10

dir = path.Path(__file__).abspath().parent.parent.parent
sys.path.append(dir.parent.parent.parent)

def click_button():
    st.session_state.clicked = True

def get_next_question():
    f = open(dir+'/code/questions.txt', 'r')
    lines = f.readlines()
    q = lines[st.session_state.current_question*2].strip()
    a = lines[st.session_state.current_question*2+1].strip()
    f.close()
    return (q, a)

def display_question():
    q, a = get_next_question()

    if st.session_state.current_question in st.session_state.answers:
        index = st.session_state.answers[st.session_state.current_question]

    st.write("Question", str(st.session_state.current_question + 1))
    st.write(q)
    form = st.form("Answer", clear_on_submit=True)
    answer = form.text_input("Enter your answer here")
    submitted = form.form_submit_button("Check")
    if submitted:
        st.session_state.answers[st.session_state.current_question] = answer
        if answer == a:
            form.write("Correct!")
            st.session_state.questions_answered += 1
        else:
            form.write("Incorrect! Try again")

def prev_question():
    if st.session_state.current_question > 0:
        st.session_state.current_question -= 1

def next_question():
    if st.session_state.current_question < QUESTIONS_NUMBER-1:
        st.session_state.current_question += 1

def createPage():
    st.title("Learn")
    col1, col2, col3 = st.columns([1, 2, 1])

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False
    if 'questions_answered' not in st.session_state:
        st.session_state.questions_answered = 0
    if 'level' not in st.session_state:
        st.session_state.level = 0
    
    string = "Level "+str(st.session_state.level)
    if st.session_state.questions_answered >= QUESTIONS_NUMBER:
        st.balloons()
        st.session_state.level += 1
        st.session_state.questions_answered = 0
        st.session_state.current_question = 0

    with col1:
        if col1.button("Prev"):
            prev_question()
    
    with col3:
        if col3.button("Next"):
            next_question()
        path_to_image = dir + "/elements/polly_pig.jpg"
        image = Image.open(path_to_image)
        st.image(image=image)

    with col2:
        button = st.empty()
        click = button.button("Begin Learning 🎉", on_click=click_button)
        if st.session_state.clicked:
            button.empty()
            st.progress(st.session_state.questions_answered/10, string)
            display_question()