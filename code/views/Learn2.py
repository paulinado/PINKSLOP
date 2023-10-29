import streamlit as st
import path
import sys
import json


dir = path.Path(__file__).abspath().parent.parent.parent
sys.path.append(dir.parent.parent.parent)

def get_all_questions():
    f = open(dir+'/code/questions2.txt', 'r')
    lines = f.readlines()
    questions = []
    for each in lines:
        questions.append(json.loads(each))
    f.close()
    return questions
    
    
# Define a function to display the current question and options
def display_question():
    # Handle first case
    if len(st.session_state.questions) == 0:
        try:
            questionset = get_all_questions()
        except  Exception as e:
            print(e)
            st.error("Uhm oops, it seems you have no questions...")
            return
        for each in questionset:
            st.session_state.questions.append(each)

    # Disable the submit button if the user has already answered this question
    submit_button_disabled = st.session_state.current_question in st.session_state.answers

    # Get the current question from the questions list
    question = st.session_state.questions[st.session_state.current_question]

    # Display the question prompt
    st.write(f"{st.session_state.current_question + 1}. {question['question']}")

    # Use an empty placeholder to display the radio button options
    options = st.empty()

    # Display the radio button options and wait for the user to select an answer
    user_answer = options.radio("Your answer:", question["options"], key=st.session_state.current_question)

    # Display the submit button and disable it if necessary
    submit_button = st.button("Submit", disabled=submit_button_disabled)

    # If the user has already answered this question, display their previous answer
    if st.session_state.current_question in st.session_state.answers:
        index = st.session_state.answers[st.session_state.current_question]
        options.radio(
            "Your answer:",
            question["options"],
            key=float(st.session_state.current_question),
            index=index,
        )

    # If the user clicks the submit button, check their answer and show the explanation
    if submit_button:
        # Record the user's answer in the session state
        st.session_state.answers[st.session_state.current_question] = question["options"].index(user_answer)

        # Check if the user's answer is correct and update the score
        if user_answer == question["answer"]:
            st.write("Correct!")
            st.session_state.right_answers += 1
        else:
            st.write(f"Sorry, the correct answer was {question['answer']}.")
            st.session_state.wrong_answers += 1

        # Show an expander with the explanation of the correct answer
        with st.expander("Explanation"):
            st.write(question["explanation"])

    # Display the current score
    st.write(f"Right answers: {st.session_state.right_answers}")
    st.write(f"Wrong answers: {st.session_state.wrong_answers}")

def prev_question():
    if st.session_state.current_question > 0:
        st.session_state.current_question -= 1
        st.session_state.explanation = None

def next_question():
    # Move to the next question in the questions list
    if st.session_state.current_question < len(st.session_state.questions):
        st.session_state.current_question += 1

    # # If we've reached the end of the questions list, get a new question
    # if st.session_state.current_question > len(st.session_state.questions) - 1:
    #     try:
    #         next_question = get_quiz_from_topic(topic, api_key)
    #     except openai.error.AuthenticationError:
    #         st.session_state.current_question -= 1
    #         return
    #     st.session_state.questions.append(next_question)

def createPage():
    # Initialize session state variables if they don't exist yet
    if "current_question" not in st.session_state:
        st.session_state.answers = {}
        st.session_state.current_question = 0
        st.session_state.questions = []
        st.session_state.right_answers = 0
        st.session_state.wrong_answers = 0

        # Create a 3-column layout for the Prev/Next buttons and the question display
    col1, col2, col3 = st.columns([1, 6, 1])

    # Add a Prev button to the left column that goes to the previous question
    with col1:
        if col1.button("Prev"):
            prev_question()

    # Add a Next button to the right column that goes to the next question
    with col3:
        if col3.button("Next"):
            next_question()

    # Display the actual quiz question
    with col2:
        display_question()