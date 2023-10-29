import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def get_user_data():
    correct = {"Levels": [1, 2, 3], "Correct answers": [8, 5, 10]}
    return correct

def createPage():
    st.title("Progress")
    st.text("Check out your learning progress so far!")
    correct_answers = pd.DataFrame(get_user_data(), columns=["Levels", "Correct answers"])
    fig, ax = plt.subplots()
    ax.plot(correct_answers["Levels"], correct_answers["Correct answers"], color="#5069af")
    ax.set_title("Questions answered correctly on first try")
    ax.set_xlabel("Level")
    ax.set_ylabel("Correct answers")
    ax.set_xticks(correct_answers["Levels"])
    st.pyplot(fig)

    # st.line_chart(correct_answers, x="Number of correct answers", y="Level")