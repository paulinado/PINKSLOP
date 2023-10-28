import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import pickle
from pathlib import Path
from views import Learn, Progress, Settings
import re

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

st.set_page_config(page_title='NumberNinjas!', page_icon='🥷', initial_sidebar_state='expanded')


try:
    #users = fetch_users()
    # emails = []
    # usernames = []
    # passwords = []

    names = ["Peter Parker", "Rebecca Miller"]
    usernames = ["pparker", "rmiller"]
    
    # for user in users:
    #     emails.append(user['key'])
    #     usernames.append(user['username'])
    #     passwords.append(user['password'])

    # credentials = {'usernames': {}}
    # for index in range(len(emails)):
    #     credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}
    
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)
        authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "numberninjas", "abcdef")

    # Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

    name, authentication_status, username = authenticator.login("Login", "main")

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
                    options=["Learn", "Progress", "Settings"],  # required
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
