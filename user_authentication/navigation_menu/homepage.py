import streamlit as st
from streamlit_option_menu import option_menu
import json
from streamlit_lottie import st_lottie
import streamlit_authenticator as stauth 
import records
import pickle
from pathlib import Path








# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title = "Multipage App",
    page_icon=":chart_with_upwards_trend:",  
    layout="wide"
    
)



names = ['Peter Parker', 'Rebecca Miller']
usernames = ['pparker','rmiller']  # Changed to dictionary
passwords = ['abc123', 'def456']

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


def load_lottiefile(filepath:str):
    with open(filepath , "r") as f:
        return json.load(f)

if authentication_status == False:
    st.error("Username/password is incorrect")


if authentication_status == None:
    st.header('Welcome to our :violet[Diabetes Test Portal]')
    lottie_index = load_lottiefile('lottie_second.json')

    st_lottie(
        lottie_index,
        speed=1,
        reverse=False,
        loop=True,
        height=600,
        width=1000
    )
    
    

if authentication_status==True:
    



    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home","Account","Patient Records"],
            icons=['house-fill','person-circle','database '],
            menu_icon="cast",
            default_index=0,
        )
        authenticator.logout("Logout", "sidebar")
        

    if selected == "Home":
        st.title(f"Diabetes :violet[Test Portal]")
        
        def load_lottiefile(filepath:str):
            with open(filepath , "r") as f:
                return json.load(f)
        lottie_index = load_lottiefile('lottie.json')

        st_lottie(
            lottie_index,
            speed=1,
            reverse=False,
            loop=True,
            height=600,
            width=1000
        )

        



    if selected == 'Patient Records':
        records.show()




