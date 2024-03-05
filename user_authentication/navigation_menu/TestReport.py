import os
import mysql.connector
import streamlit as st
import pandas as pd
import numpy as np


mydb = mysql.connector.connect(
    host="localhost", user="root", password="hacker@123", database="diabetes_record"
)



mycursor = mydb.cursor()
def generate(patient_id):
    
    full_path = "C:/Users/aditya/Desktop/Diabetes_predition/Female_diabetes_ML_detection_/user_authentication/navigation_menu/z_test_file_folder/"


    file_path = full_path+patient_id+".txt"
    

    if os.path.exists(file_path):
        st.warning(f'Test Report file exists already in the location {file_path}')
        delete_button = st.button('Delete Test Report')
        if delete_button:
            os.remove(file_path)
    else:
        cb = st.button('Generate Test Report')
        if cb:
            f_header = open(full_path+"report_header.txt", 'r')
            f_report = open(file_path,'x')
            f_report.close()
            f_report = open(file_path,'a')
            f_report.write(f_header.read())
            
            st.success(f'Test Report created successfully at the location {file_path}')
            


            query = "SELECT * FROM lab_data WHERE id = %s"
            mycursor.execute(query, (patient_id,))

            try:

           
                result_from_id = list(mycursor.fetchone())
                new_list = []
                for i in result_from_id:
                    x = []
                    x.append(i)
                    new_list.append(x)
                


                    

                


                df = pd.DataFrame(
                    new_list,
                    index=[
                        "ID                        ",
                        "Pregnancies               ",
                        "Glucose                   ",
                        "Blood Pressure            ",
                        "Skin Thickness            ",
                        "Insulin                   ",
                        "BMI                       ",
                        "DiabetesPedigree          ",
                        "Age                       ",
                        "outcome                   ",
                    ],
                    columns=['                        values']
                )
                
            

            
                df.to_csv(full_path+'data.txt', index=True, sep='\t')
                f_data_from_df = open(full_path+'data.txt','r')
                f_report.write(f_data_from_df.read())

                if (df['                        values']).values[9] == 1:
                    f_report.write("\n\n\nYour Diabetes test is positive\nThank You for choosing us ......\n\nPlease Contact us at diabetesclinic15022002@gmail.com\nPhone:9334464181")
                else:
                    f_report.write("\n\n\nYour Diabetes test is Negative\nThank You for choosing us ......\n\nPlease Contact us at diabetesclinic15022002@gmail.com\nPhone:9334464181")



                f_report.close()
                f_data_from_df.close()
                f_header.close()



                os.remove(full_path+'data.txt')
                
            except Exception:
                st.title('')




           
            



            









    



    