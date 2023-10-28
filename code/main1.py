import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import pickle
from pathlib import Path
from views import Learn, Progress, Settings
import re

st.set_page_config(page_title='NumberNinjas', page_icon='🥷', initial_sidebar_state='collapsed')
v_menu = ["Learn", "Progress", "Settings"]

def validate_username(username):
    """
    Checks Validity of userName
    :param username:
    :return True if username is valid else False:
    """

    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False

def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader('Sign Up')
        username = st.text_input('Username', placeholder='Enter Your Username')
        password1 = st.text_input('Password', placeholder='Enter Your Password', type='password')
        password2 = st.text_input('Confirm Password', placeholder='Confirm Your Password', type='password')

        if validate_username(username):
            if username not in []: #get_usernames():
                    if len(password1) >= 6:
                        if password1 == password2:
                            # Add User to DB
                            hashed_password = stauth.Hasher([password2]).generate()
                            #insert_user(email, username, hashed_password[0])
                            st.success('Account created successfully!!')
                            st.balloons()
                        else:
                            st.warning('Passwords Do Not Match')
                    else:
                        st.warning('Password is too Short')
            else:
                st.warning('Username Already Exists')

        else:
            st.warning('Invalid Username')


        st.form_submit_button('Sign Up')

def log_in():
    names = ["Peter Parker", "Rebecca Miller"]
    usernames = ["pparker", "rmiller"]

    # load hashed passwords
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)
        authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "numberninjas", "abcdef")

    name, authentication_status, username = authenticator.login("Login", "main")


    if authentication_status == False:
        st.warning("Incorrect username/password")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        with st.sidebar:
            authenticator.logout("Logout", "sidebar")
            st.header(f"Welcome {name}")
            selected = option_menu(menu_title=None,  # required
            options=v_menu,  # required
            icons=None,  # optional
            menu_icon="menu-down",  # optional
            default_index=0,  # optional
            )
            
        
        if selected=="Learn":
            Learn.createPage()
        
        if selected=="Progress":
            Progress.createPage()
        
        if selected=="Settings":
            Settings.createPage()


def signinPage():
    col1,col2 = st.columns(2)
    with col1:
            log_in()
    
    with col2:
            sign_up()

st.title("🥷 Welcome to NumberNinjas! 🥷")
signinPage()

# btn1, btn2 = st.columns(2)

# with btn2:
#     sign_up()
# with btn1:
#     log_in()