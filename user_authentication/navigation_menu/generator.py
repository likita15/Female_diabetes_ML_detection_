import pickle
from pathlib import Path
import json

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from streamlit_lottie import st_lottie


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


# --- USER AUTHENTICATION ---
import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ['aditya kshatriya', 'aditya jyoti sahu']
usernames = ['kshatriya15','jyotibabu']  # Changed to dictionary
passwords = ['ksh1234', 'jyoti1234']

credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password":passwords[0]
                },
            usernames[1]:{
                "name":names[1],
                "password":passwords[1]
                }            
            }
        }

hashed_passwords = stauth.Hasher(passwords).generate()

# Save hashed passwords to a pickle file
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)

# Initialize the Authenticate object
authenticator = stauth.Authenticate(credentials,"sales_dashboard", "abcdef")


name, authentication_status, username = authenticator.login(fields={'Form name': 'Login','Username': 'username','Password': 'password','Login': 'Login' },location='sidebar')



if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.title('Female Diabetes :violet[Portal]')
    hide_st_style = '<iframe src="https://lottie.host/embed/eb921a98-135d-47b6-9a9a-56c3d299a752/WfKZkLBNcp.json"></iframe>'
    st.markdown(hide_st_style, unsafe_allow_html=True)

if authentication_status==True:
    
    
    

    
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.header("Please Filter Here:")
    