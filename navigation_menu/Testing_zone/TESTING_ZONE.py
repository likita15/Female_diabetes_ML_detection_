import streamlit as st
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost", user="root", password="hacker@123", database="diabetes_record"
)


mycursor = mydb.cursor()




query_age = 'select age from users WHERE id = %s'
patient_id = ('idr542369875652m',)
mycursor.execute(query_age,patient_id)
result = mycursor.fetchall()
st.write(result)


st.write(result[0][0])

st.number_input(
    "Update age",
    placeholder="Enter value",
    value = result[0][0]
    
)

