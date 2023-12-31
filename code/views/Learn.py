import streamlit as st
from PIL import Image
from deta import Deta
import path
import sys
import time
import json
sys.path.append("..")
from genquiz_easy import get_easy_question
from genquiz_medium import get_medium_question
from genquiz_hard import get_hard_question

#make a setting to edit number of questions per level
QUESTIONS_NUMBER = 10

dir = path.Path(__file__).abspath().parent.parent.parent
sys.path.append(dir.parent.parent.parent)

def add_question(question):
    st.session_state.questions.append(question)
    st.session_state.attempted.append(False)
    currentQuestions = st.session_state.db.get(st.session_state.key)['questions']
    currentQuestions[st.session_state.level].append(question)

    # currentQuestions = (st.session_state.db).get(st.session_state.key)['questions'][st.session_state.level].append(question)
    st.session_state.db.update({'questions':currentQuestions},st.session_state.key)
    
    #print(st.session_state.db.get(st.session_state.key)['questions'][st.session_state.level])
    #st.session_state.db[st.session_state.key]['questions'][st.session_state.level].append(question)
    #st.session_state.user['questions'][st.session_state.level].append(question)
    # st.session_state.db.append({'questions':st.session_state.questions},st.session_state.key)
        

def incr_current_question():
    st.session_state.current_question += 1
    #st.session_state.db[st.session_state.key]['current_question'].increment()
    st.session_state.db.update({'current_question': st.session_state.current_question},st.session_state.key)
    #st.session_state.user['current_question'] += 1
    #st.session_state.db.update({},st.session_state.key)

def decr_current_question():
    st.session_state.current_question -= 1
    st.session_state.db.update({'current_question': st.session_state.current_question},st.session_state.key)
    #st.session_state.user['current_question'] -= 1
    #st.session_state.db[st.session_state.key]['current_question'].increment(-1)
    # st.session_state.db.update({},st.session_state.key)

def add_answer(answer):
    st.session_state.answers[str(st.session_state.current_question)] = answer
    print(st.session_state.answers)
    currentAnswers = st.session_state.db.get(st.session_state.key)['answers']
    
    if currentAnswers[st.session_state.level] == None:
        currentAnswers[st.session_state.level] = dict()
    currentAnswers[st.session_state.level][st.session_state.current_question] = answer
    st.session_state.db.update({'answers':currentAnswers},st.session_state.key)
    #st.session_state.db[st.session_state.key]['answers'][st.session_state.level].append(answer)
    #st.session_state.user['answers'][st.session_state.level][st.session_state.current_question] = answer
    # st.session_state.db.update({},st.session_state.key)

def incr_questions_answered():
    st.session_state.questions_answered += 1
    st.session_state.db.update({'questions_answered': st.session_state.questions_answered},st.session_state.key)
    #st.session_state.db[st.session_state.key]['questions_answered'].increment()
    #st.session_state.user['questions_answered'] += 1
    # st.session_state.db.update({},st.session_state.key)

def incr_level():
    if st.session_state.level < 2:
        st.session_state.level += 1
        st.session_state.db.update({'level': st.session_state.level},st.session_state.key)
        #st.session_state.user['level'] += 1
        #st.session_state.db[st.session_state.key]['level'].increment()
        # st.session_state.db.update({},st.session_state.key)
    
def incr_first_time_correct():
    st.session_state.first_time_correct += 1
    # print(st.session_state.first_time_correct)
    #st.session_state.db.update({'questions_answered': st.session_state.questions_answered},st.session_state.key)
    f = st.session_state.db.get(st.session_state.key)['first_time_correct']
    f[int(st.session_state.level)] += 1
    
    st.session_state.db.update({'first_time_correct': f},st.session_state.key)

def failed_attempt():
    st.session_state.attempted[st.session_state.current_question] = True
    
def click_button():
    st.session_state.clicked = True

# def get_next_question():
#     f = open(dir+'/code/questions.txt', 'r')
#     lines = f.readlines()
#     question = json.loads(lines[int(st.session_state.current_question)])
#     f.close()
#     return question

def get_next_question():
    #make a button to cheat increase the state level for demonstration
    if st.session_state.level == 0:
        response = get_easy_question(st.secrets['gpt_key'])
    elif st.session_state.level == 1:
        response = get_medium_question(st.secrets['gpt_key'])
    elif st.session_state.level == 2:
        response = get_hard_question(st.secrets['gpt_key'])
    else:
        response = get_hard_question(st.secrets['gpt_key'])
        #you are done??
        pass
    return response

def display_question():
    # Handle first case
    if len(st.session_state.questions) == 0:
        try:
            question = get_next_question()
        except Exception as e:
            print(e)
            st.error(
                "Oops, there appears to be no questions for you right now!"
            )
            return
        add_question(question)

    form_submit_button_disabled  = str(st.session_state.current_question) in st.session_state.answers
    
    try:
        #print(st.session_state.current_question)
        previous_answer = st.session_state.answers[str(st.session_state.current_question)]
    except Exception as e:
        # print(e)
        # print(st.session_state.answers, st.session_state.current_question)
        previous_answer = None
    
    question = st.session_state.questions[st.session_state.current_question]

    st.write("Question", str(st.session_state.current_question + 1))
    st.write(question['question'])
    form = st.form("Answer", clear_on_submit=True)
    answer = form.text_input("Enter your answer here", key=st.session_state.current_question, placeholder=previous_answer  ,disabled=form_submit_button_disabled)
    submitted = form.form_submit_button("Check", disabled=form_submit_button_disabled)
    
    if submitted: 
        if answer == question['answer']:
            add_answer(answer)
            form.write("Correct!")
            incr_questions_answered()
            if not st.session_state.attempted[int(st.session_state.current_question)]:
                incr_first_time_correct()
        else:
            form.write("Incorrect! Try again")
            failed_attempt()

def prev_question():
    if int(st.session_state.current_question) > 0:
        decr_current_question()

def next_question():
    if int(st.session_state.current_question) < QUESTIONS_NUMBER-1:
        incr_current_question()
        next_question = get_next_question()
        add_question(next_question)
        

def createPage(key):
    deta = Deta(st.secrets["data_key"])
    db = deta.Base("progress-2")
    users = db.fetch().items
    keys = []
    for user in users:
        keys.append(user['key'])
    
    #db.put({'level': 0, 'questions':[[],[],[]], 'first_time_correct':[0,0,0], 'current_question':0, 'answers':[{},{},{}], 'questions_answered':0},key)
    if not key in keys:
        db.put({'level': 0, 'questions':[[],[],[]], 'first_time_correct':[0,0,0], 'current_question':0, 'answers':[dict(),dict(),dict()], 'questions_answered':0},key)
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
        if 'first_time_correct' not in st.session_state:
            st.session_state.first_time_correct = 0
    else:
        user = db.get(key)
        # print(user)
        level = user['level']
        questions = user['questions'][level]
        first_time_correct = user['first_time_correct'][level]
        current_question = user['current_question']
        answers = user['answers'][level]
        #print(answers)
        questions_answered =  user['questions_answered']
        
        if 'current_question' not in st.session_state:
            st.session_state.current_question = int(current_question)
        if 'questions' not in st.session_state:
            st.session_state.questions = questions
        if 'answers' not in st.session_state:
            st.session_state.answers = answers
        if 'clicked' not in st.session_state:
            st.session_state.clicked = False
        if 'questions_answered' not in st.session_state:
            st.session_state.questions_answered = questions_answered
        if 'level' not in st.session_state:
            st.session_state.level = int(level)
        if 'first_time_correct' not in st.session_state:
            st.session_state.first_time_correct = first_time_correct
    
    if 'key' not in st.session_state:
        st.session_state.key = key
    
    if 'db' not in st.session_state:
        st.session_state.db = db
        
    #add to db
    if 'attempted' not in st.session_state:
        st.session_state.attempted = []
    
    st.title("Learn")
    col1, col2, col3 = st.columns([1, 2, 1])

    
    
    string = "Level "+str(st.session_state.level)
    if st.session_state.questions_answered >= QUESTIONS_NUMBER:
        st.balloons()
        incr_level()
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