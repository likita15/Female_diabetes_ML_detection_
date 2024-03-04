import streamlit as st
from streamlit_option_menu import option_menu
import json
from streamlit_lottie import st_lottie
import requests
import records
st.set_page_config(
    page_title = "Multipage App",
    page_icon=":chart_with_upwards_trend:",  
    layout="wide"
    
)


with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home","Account","Patient Records"],
        icons=['house-fill','person-circle','database '],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    st.title(f"Female Diabetes :violet[Test Portal]")
    
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




