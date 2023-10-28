import streamlit as st
from PIL import Image
import path
import sys

QUESTIONS_NUMBER = 10

dir = path.Path(__file__).abspath().parent.parent.parent
sys.path.append(dir.parent.parent.parent)

def click_button():
    st.session_state.clicked = True

def get_next_question():
    pass

def prepare_question(question_number):
    correct = False
    f = open(dir+'/code/questions.txt', 'r')
    lines = f.readlines()
    q = lines[0]
    a = lines[1]
    while st.session_state.current_question <= QUESTIONS_NUMBER:
        placeholder = st.empty()
        with placeholder.container():
            st.write("Question", str(question_number))
            st.write(q)

            form = st.form("Answer")
            answer = form.text_input("Enter your answer here")
            submitted = form.form_submit_button("Check")
            while not submitted:
                continue
            else:
                if answer == a:
                    form.write("Correct!")
                    correct = True
                    st.session_state.current_question += 1
                else:
                    form.write("Incorrect! Try again")
                    correct = False
                placeholder.empty()
    f.close()
    return correct


def start_quiz():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 1
    level=0
    num = level/7
    string = "Level "+str(level)
    st.progress(num, string)
    prepare_question(st.session_state.current_question)


def createPage():
    st.title("Learn")
    col1, col2, col3 = st.columns([1, 2, 1])

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
            button.empty()
            start_quiz()