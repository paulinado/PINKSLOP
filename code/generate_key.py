import streamlit as st

import streamlit_authenticator as stauth

from deta import Deta

deta = Deta(st.secrets["data_key"])
db = deta.Base("users2")

usernames = ["pparker", "rmiller"]
passwords = ["pass123", "pass123"]

hashed_passwords = stauth.Hasher(passwords).generate()

for index in range(len(usernames)):
    db.put({'username': usernames[index], 'password': hashed_passwords[index]})