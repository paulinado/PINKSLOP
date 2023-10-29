import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import pickle
from pathlib import Path
from views import Learn, Progress, Settings, ExampleDB, Learn2
import re
from deta import Deta

def new_user(username, password):
    return db.put({'username': username, 'password': password})

def get_all_users():
    users = db.fetch()
    return users.items

def get_all_usernames():
    users = db.fetch()
    usernames = []
    for user in users.items:
        usernames.append(user['username'])
    return usernames

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
        submitted = st.form_submit_button('Sign Up')
        
        if validate_username(username):
            if username not in get_all_usernames():
                    if len(password1) >= 6:
                        if password1 == password2:
                            # Add User to DB
                            hashed_password = stauth.Hasher([password2]).generate()
                            if submitted:
                                new_user(username, hashed_password[0])
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

        
        
deta = Deta(st.secrets["data_key"])
db = deta.Base("users")
st.set_page_config(page_title='NumberNinjas!', page_icon='🥷', initial_sidebar_state='expanded')


try:
    users = get_all_users()
    keys = []
    usernames = []
    hashed_passwords = []
    
    for user in users:
        keys.append(user['key'])
        usernames.append(user['username'])
        hashed_passwords.append(user['password'])
    
    authenticator = stauth.Authenticate(keys, usernames, hashed_passwords, "numberninjas", "abcdef")
    
    key, authentication_status, username = authenticator.login("Login", "main")

    info, info1 = st.columns(2)

    if not authentication_status:
        sign_up()

    if username:
        if username in usernames:
            if authentication_status:
                # let User see app
                st.sidebar.subheader(f'Welcome {username}')
                authenticator.logout('Log Out', 'sidebar')
                
                with st.sidebar:
                    selected = option_menu(menu_title=None,  # required
                    options=["Learn", "Progress", "Settings", "ExampleDB", "Learn2"],  # required
                    icons=None,  # optional
                    menu_icon="menu-down",  # optional
                    default_index=0,  # optional
                    )
            
        
                if selected=="Learn":
                    Learn.createPage()
                
                if selected=="Learn2":
                    Learn2.createPage()
                
                if selected=="Progress":
                    Progress.createPage()
                
                if selected=="Settings":
                    Settings.createPage()
                
                if selected=="ExampleDB":
                    ExampleDB.createPage(deta)

            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            else:
                with info:
                    st.warning('Please feed in your credentials')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')


except:
    pass