import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ['aditya kshatriya', 'aditya jyoti sahu']
usernames = ['kshatriya15','jyotibabu']  # Changed to dictionary
passwords = ['ksh1234', 'jyoti1234']

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"

# Open file in binary write mode
with file_path.open("wb") as file:
    # Pickle the data
    pickle.dump(hashed_passwords, file)

# Optionally, print a message to confirm successful pickling
print("Data pickled successfully!")
