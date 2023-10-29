import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from deta import Deta
import numpy as np

def get_user_data(key):
    deta = Deta(st.secrets["data_key"])
    db = deta.Base("progress-new")
    user = db.get(key)
    level = user['level']
    levels = np.arrange(1, level+1)
    first_time_correct = user['first_time_correct']
    data = {'Levels' : levels, 'Correct answers': first_time_correct}
    return data

def createPage(key):
    st.title("Progress")
    st.text("Check out your learning progress so far!")
    correct_answers = pd.DataFrame(get_user_data(key), columns=["Levels", "Correct answers"])
    fig, ax = plt.subplots()
    ax.plot(correct_answers["Levels"], correct_answers["Correct answers"], color="#5069af")
    ax.set_title("Questions answered correctly on first try")
    ax.set_xlabel("Level")
    ax.set_ylabel("Correct answers")
    ax.set_xticks(correct_answers["Levels"])
    st.pyplot(fig)

    # st.line_chart(correct_answers, x="Number of correct answers", y="Level")