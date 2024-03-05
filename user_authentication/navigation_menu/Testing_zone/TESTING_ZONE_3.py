import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np


mydb = mysql.connector.connect(
    host="localhost", user="root", password="hacker@123", database="diabetes_record"
)


mycursor = mydb.cursor()
def delete():
    with st.form(key="delete", clear_on_submit=True):

        st.title("Delete a Record")
        
        sql = "select * from users"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        record = []
        for row in result:
            record.append(row)

        record_df = pd.DataFrame(
            record,
            columns=[
                "ID",
                "Name",
                "Email ID",
                "Age",
                "Date of Birth",
                "Date of Registration",
                "Registration_Time",
                "Phone",
                "Aadhar",
            ],
            index=range(1, len(record) + 1),
    )

        id_option = list(record_df["ID"])
        st.write(id_option)
        option1 = st.selectbox(
            "Choose from the list of ids", id_option, placeholder="enter id value..."
        )
        st.write("You selected:", option1)
        
       
        delete_button = st.form_submit_button("Delete")

        if delete_button:
            sql = "delete from users where id = %s"
            val = (id,)
            mycursor.execute(sql, val)

            mydb.commit()
            st.success("successfully deleted record!!!")

delete()
