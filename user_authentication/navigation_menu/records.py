import streamlit as st
import numpy as np
from datetime import datetime
import mysql.connector
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


import predictor, TestReport, MailTest_report


mydb = mysql.connector.connect(
    host="localhost", user="root", password="hacker@123", database="diabetes_record"
)

                
                
            

mycursor = mydb.cursor()
def send_email(sender, password, receiver, smtp_server, smtp_port, email_message, subject, attachment=None):

    message = MIMEMultipart()
    message['To'] = Header(receiver)
    message['From'] = Header(sender)
    message['Subject'] = Header(subject)
    message.attach(MIMEText(email_message, 'plain', 'utf-8'))

    if attachment:
        with attachment as file:
            file_content = file.read()
            file_name = file.name
        att = MIMEApplication(file_content)
        att.add_header('Content-Disposition', 'attachment', filename=file_name)
        message.attach(att)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.ehlo()
    server.login(sender, password)
    text = message.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()

def ToMail(option_id):
        
        query = "SELECT * FROM users WHERE id = %s"
        mycursor.execute(query, (option_id,))


        result_from_id = np.array(list(mycursor.fetchone())).reshape(1, 9)

    

        record_df_results = pd.DataFrame(
            result_from_id,
            columns=[
                "ID",
                "Name",
                "Email",
                "Age",
                "dob",
                "dor",
                "regis_time",
                "phone",
                "Aadhar",
                
            ],
            index=range(1, 2),
        )
    
        


        

        with st.form("Email form",clear_on_submit=True):
            subject = st.text_input(label='Subject', placeholder='Please enter subject of your mail',value="Regarding your Diabetes Test Result")
            # fullName = st.text_input(label='Full Name', placeholder='Enter name',value=record_df_results['Name'].values[0])
            email = st.text_input(label='Email', placeholder='Enter email',value=record_df_results['Email'].values[0])
            message_body = st.text_area(label='Message', placeholder='Enter message',value='Mam Your test result has came please consider the below attachment of your report in the email')
            uploaded_file = st.file_uploader('Attachment')
            submit_res = st.form_submit_button(label='Send')

            if submit_res:
                send_email(sender="adityacodesf1502@gmail.com", password="lwbl xrcx jlqf wnlh", receiver=email,
                        smtp_server="smtp.gmail.com", smtp_port=587, email_message=message_body,
                        subject=subject, attachment=uploaded_file)


def input():

    with st.form(key="insert", clear_on_submit=True):
        st.title("Enter Patients Details:")
        name = st.text_input("Name", placeholder="patient's name..")
        age = st.number_input("Age", min_value=0, max_value=110, placeholder="age")
        dob = st.date_input("Date of birth")
        number = st.number_input(
            "Phone number",
            value=None,
            placeholder="Phone",
            min_value=0,
            max_value=9999999999,
        )
        email = st.text_input("Email", placeholder="email")
        aadhar = st.text_input("Aadhar:", type="password", placeholder="aadhar")

        dor = st.date_input("Date of Registration", value="today")

        now = st.time_input(
            "Current time:", value=datetime.now().time().replace(microsecond=0)
        )

        submit_button = st.form_submit_button("submit")

    if submit_button:
        id = "id" + name[0:1] + str(aadhar) + name[len(name) - 2 : len(name) - 1]
        sql_record = "insert into users (id , name , email , age , dob , dor , regis_time , phone , aadhar) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val_record = (id, name, email, age, dob, dor, now, number, aadhar)
        mycursor.execute(sql_record, val_record)
        update_id(id)

        mydb.commit()
        st.success("Record created successfully!!!")


def update():
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
   
    option1 = st.selectbox(
        "Choose from the list of ids", id_option, placeholder="enter id value...",key='forupdates'
    )

    st.write("You selected:", option1)

    id = option1

   
    st.title("Update a Record")

    option = st.selectbox('Choose what you want to Update:',('Update Name','Update Age','Update DOB','Update Phone','Update Email','Update Aadhar'))
    st.write(option)

    if option == 'Update Name':
        with st.form(key="update_NAME", clear_on_submit=True):
                id = st.text_input("Enter Id:",value=id)
                name_new = st.text_input("Name", placeholder="name")
                update_button = st.form_submit_button("Update")
        if update_button:
            query = "update users set name = %s where id = %s "
            val = (name_new,id)

            mycursor.execute(query, val)
            mydb.commit()
            st.success("Successfully updated!!!")

    elif option == 'Update Age':
        with st.form(key="update_AGE", clear_on_submit=True):
                id = st.text_input("Enter Id:",value=id)
                name_age = st.number_input("Age",placeholder="age",min_value=0,max_value=110)
                update_button = st.form_submit_button("Update")
        if update_button:
            query = "update users set age = %s where id = %s "
            val = (name_age,id)

            mycursor.execute(query, val)
            mydb.commit()
            st.success("Successfully updated!!!")

    elif option == 'Update DOB':
        with st.form(key="update_DOB", clear_on_submit=True):
                id = st.text_input("Enter Id:",value=id)
                dob_new = st.date_input("Date of birth")
                update_button = st.form_submit_button("Update")
        if update_button:
            query = "update users set dob = %s where id = %s "
            val = (dob_new,id)

            mycursor.execute(query, val)
            mydb.commit()
            st.success("Successfully updated!!!")

    elif option == 'Update Phone':
        with st.form(key="Update_PHONE", clear_on_submit=True):
                id = st.text_input("Enter Id:",value=id)
                Phone_new = st.number_input("Phone",placeholder="Phone",min_value=0,max_value=9999999999)
                update_button = st.form_submit_button("Update")
        if update_button:
            query = "update users set phone = %s where id = %s "
            val = (Phone_new,id)

            mycursor.execute(query, val)
            mydb.commit()
            st.success("Successfully updated!!!")
            
    elif option == 'Update Email':
        with st.form(key="Update_EMAIL", clear_on_submit=True):
                id = st.text_input("Enter Id:",value=id,placeholder="Email")
                Email_new = st.text_input("Email")
                update_button = st.form_submit_button("Update")
        if update_button:
            query = "update users set email = %s where id = %s "
            val = (Email_new,id)

            mycursor.execute(query, val)
            mydb.commit()
            st.success("Successfully updated!!!")

    elif option == 'Update Aadhar':
        with st.form(key="Update_EMAIL", clear_on_submit=True):
                id = st.text_input("Enter Id:",value=id)
                aadhar_new = st.number_input("Aadhar",placeholder="aadhar",min_value=0)
                update_button = st.form_submit_button("Update")
        if update_button:
            query = "update users set aadhar = %s where id = %s "
            val = (aadhar_new,id)

            mycursor.execute(query, val)
            mydb.commit()
            st.success("Successfully updated!!!")
            














       


def delete():
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
      
        option1 = st.selectbox(
            "Choose from the list of ids", id_option, placeholder="enter id value..."
        )

        st.write("You selected:", option1)
        id = option1

        with st.form(key="delete", clear_on_submit=True):

            st.title("Delete a Record")
            
            delete_button = st.form_submit_button("Delete")

            if delete_button:
                sql1 = "delete from users where id = %s"
                sql2 = "delete from lab_data where id = %s"

                val1 = (id,)
                val2 = (id,)
                mycursor.execute(sql1, val1)
                mycursor.execute(sql2, val2)

                mydb.commit()
                st.success("successfully deleted record!!!")


        
            
        


def read_record():
    st.title("Records")
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
    st.write(record_df)


def update_id(id):
    sql_id = "insert into ids (id) values (%s)"
    val_id = (id,)
    mycursor.execute(sql_id, val_id)

    mydb.commit()


def show():

    tab1, tab2, tab3, tab4,tab5,tab6 = st.tabs(
        ["➕Add New Record","📑View Records",  "📝Update", "🗑️Delete","LabRecords","Results"]
    )
    with tab1:
        input()
        

    with tab2:
        read_record()

    with tab3:
        update()

    with tab4:
        delete()

    with tab5:

        st.title("Lab Records:")
        option = st.selectbox(
            "Choose Record Operation:",
            ("Add New Record", "Update Record", "View Record"),
            key="chooseRecord"
        )

        if option == "Add New Record":
            st.title("Enter Patient lab Test Results")

            sql = "select * from ids"
            mycursor.execute(sql)
            result = mycursor.fetchall()
            record = []
            for row in result:
                record.append(row)

            record_df = pd.DataFrame(
                record,
                columns=[
                    "id",
                ],
                index=range(1, len(record) + 1),
            )

            option = st.selectbox("Choose ids for the record:", list(record_df["id"]),key='idsADDrecord')

            query_age = "select age from users WHERE id = %s"
            age_value = (option,)
            mycursor.execute(query_age, age_value)
            result = mycursor.fetchall()
            if result:
                age = result[0][0]
            else:
                age = 0

            with st.form(key="add_record", clear_on_submit=True):

                patient_id = option
                st.write(option)
                pregnancies = st.number_input(
                    "No. of Pregnancies",
                    placeholder="Enter value",
                    min_value=0,
                    max_value=50,
                    step=1,
                )
                glucose = st.number_input(
                    "Glucose",
                    placeholder="Enter value",
                    min_value=0,
                    max_value=500,
                    step=1,
                )
                bloodpressure = st.number_input(
                    "Blood Pressure",
                    placeholder="Enter value",
                    min_value=0,
                    max_value=500,
                    step=1,
                )
                skinthickness = st.number_input(
                    "Skin Thickness",
                    placeholder="Enter value",
                    min_value=0,
                    max_value=500,
                    step=1,
                )
                insulin = st.number_input(
                    "Insulin",
                    placeholder="Enter value",
                    min_value=0,
                    max_value=500,
                    step=1,
                )
                bmi = st.number_input("BMI", placeholder="Enter value", format="%.3f")
                diabetespedigree = st.number_input(
                    "Diabetes Pedigree", placeholder="Enter value", format="%.3f"
                )

                st.number_input("age", placeholder="Enter value", value=age)

                submit_button = st.form_submit_button("Submit")
                if submit_button:

                    sql_del = "delete from ids where id = %s"
                    val_del = ((patient_id),)
                    mycursor.execute(sql_del, val_del)

                    x_predict = predictor.detect_diabetes(
                        [
                            pregnancies,
                            glucose,
                            bloodpressure,
                            skinthickness,
                            insulin,
                            bmi,
                            diabetespedigree,
                            age,
                        ]
                    )
                    sql_record = "insert into lab_data (id,pregnancies,glucose,bloodpressure,skinthickness,insulin,bmi,diabetespedigree,age,outcome) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val_record = (
                        patient_id,
                        pregnancies,
                        glucose,
                        bloodpressure,
                        skinthickness,
                        insulin,
                        bmi,
                        diabetespedigree,
                        age,
                        x_predict,
                    )
                    mycursor.execute(sql_record, val_record)

                    mydb.commit()
                    st.success("lab record added successfully....")

        elif option == "Update Record":
            st.title("Update Patient lab Test Results")

            sql = "SELECT id FROM lab_data"

            mycursor.execute(sql)
            result = mycursor.fetchall()
            record = []
            for row in result:
                record.append(row)

            record_df = pd.DataFrame(
                record,
                columns=[
                    "id",
                ],
                index=range(1, len(record) + 1),
            )

            option_inside = st.selectbox("select desired ids:",list(record_df["id"]), key="choose_lab")

            patient_id = option_inside
            st.title("Update a Record")

            option = st.selectbox('Choose what you want to Update:',('Update Pregnacies','Update glucose','Update bloodpressure','Update skinthickness','Update insulin','Update bmi','Update diabetespedigree'),key='cho')
            st.write(option)

            try:
                query = "SELECT * FROM lab_data WHERE id = %s"
                mycursor.execute(query, (patient_id,))

                result_from_id = np.array(list(mycursor.fetchone())).reshape(1, 10)

                st.write(mycursor.fetchone())

                record_df_results = pd.DataFrame(
                    result_from_id,
                    columns=[
                        "ID",
                        "Pregnancies",
                        "Glucose",
                        "Blood Pressure",
                        "Skin Thickness",
                        "Insulin",
                        "BMI",
                        "DiabetesPedigree",
                        "Age",
                        "outcome",
                    ],
                    index=range(1, 2),
                )

            except Exception:
                st.title('No record')

            pregnancies=record_df_results['Pregnancies'].values[0]
            glucose=record_df_results['Glucose'].values[0]
            bloodpressure=record_df_results['Blood Pressure'].values[0]
            skinthickness=record_df_results['Skin Thickness'].values[0]
            insulin=record_df_results['Insulin'].values[0]
            bmi=record_df_results['BMI'].values[0]
            diabetespedigree=record_df_results['DiabetesPedigree'].values[0]
            age=record_df_results['Age'].values[0]

            if option == 'Update Pregnacies':
                with st.form(key="Update Pregnacies", clear_on_submit=True):
                        
                        pregnancies_new = st.number_input("Pregnacies", placeholder="Enter",min_value=0,max_value=50)
                        update_button = st.form_submit_button("Update")
                if update_button:
                    query = "update lab_data set pregnancies = %s where id = %s "
                    val = (pregnancies_new,patient_id)

                    mycursor.execute(query, val)
                    mydb.commit()
                    update_ml_value(pregnancies_new,glucose,bloodpressure , skinthickness , insulin , bmi ,diabetespedigree ,  age , patient_id)
                    st.success("Successfully updated!!!")

            elif option == 'Update glucose':
                with st.form(key="Update glucose", clear_on_submit=True):
                       
                        glucose_new = st.number_input("Glucose",placeholder="Enter",min_value=0,max_value=1000,step=1)
                        update_button = st.form_submit_button("Update")
                if update_button:
                    query = "update lab_data set glucose = %s where id = %s "
                    val = (glucose_new,patient_id)

                    mycursor.execute(query, val)
                    mydb.commit()
                    update_ml_value(pregnancies,glucose_new,bloodpressure , skinthickness , insulin , bmi ,diabetespedigree ,  age , patient_id)
                    st.success("Successfully updated!!!")

            elif option == 'Update bloodpressure':
                with st.form(key="Update bloodpressure", clear_on_submit=True):
                       
                        bloodpressure_new = st.number_input("bloodpressure",placeholder="Enter",min_value=0,max_value=1000,step=1)
                        update_button = st.form_submit_button("Update")
                if update_button:
                    query = "update lab_data set bloodpressure = %s where id = %s "
                    val = (bloodpressure_new,patient_id)

                    mycursor.execute(query, val)
                    mydb.commit()
                    update_ml_value(pregnancies,glucose,bloodpressure_new , skinthickness , insulin , bmi ,diabetespedigree ,  age , patient_id)
                    st.success("Successfully updated!!!")

            elif option == 'Update skinthickness':
                with st.form(key="Update skinthickness", clear_on_submit=True):
                        
                        skinthickness_new = st.number_input("skinthickness",placeholder="Enter",min_value=0,max_value=1000,step=1)
                        update_button = st.form_submit_button("Update")
                if update_button:
                    query = "update lab_data set skinthickness = %s where id = %s "
                    val = (skinthickness_new,patient_id)

                    mycursor.execute(query, val)
                    mydb.commit()
                    update_ml_value(pregnancies,glucose,bloodpressure , skinthickness_new , insulin , bmi ,diabetespedigree ,  age , patient_id)
                    st.success("Successfully updated!!!")
                    
            elif option == 'Update insulin':
                with st.form(key="Update insulin", clear_on_submit=True):
                       
                        insulin_new = st.number_input("insulin",placeholder="Enter",min_value=0,max_value=1000,step=1)
                        update_button = st.form_submit_button("Update")
                if update_button:
                    query = "update lab_data set insulin = %s where id = %s "
                    val = (insulin_new,patient_id)

                    mycursor.execute(query, val)
                    mydb.commit()
                    update_ml_value(pregnancies,glucose,bloodpressure , skinthickness , insulin_new , bmi ,diabetespedigree ,  age , patient_id)
                    st.success("Successfully updated!!!")

            elif option == 'Update bmi':
                with st.form(key="Update bmi", clear_on_submit=True):
                        
                        bmi_new = st.number_input("bmi",placeholder="bmi",min_value=0.000,format='%.3f')
                        update_button = st.form_submit_button("Update")
                if update_button:
                    query = "update lab_data set bmi = %s where id = %s "
                    val = (bmi_new,patient_id)

                    mycursor.execute(query, val)
                    mydb.commit()
                    update_ml_value(pregnancies,glucose,bloodpressure , skinthickness , insulin , bmi_new ,diabetespedigree ,  age , patient_id)
                    st.success("Successfully updated!!!")


            elif option == 'Update diabetespedigree':
                with st.form(key="Update diabetespedigree", clear_on_submit=True):
                        
                        diabetespedigree_new = st.number_input("bmi",placeholder="bmi",min_value=0.000,format='%.3f')
                        update_button = st.form_submit_button("Update")
                if update_button:
                    query = "update lab_data set diabetespedigree = %s where id = %s "
                    val = (diabetespedigree_new,patient_id)

                    mycursor.execute(query, val)
                    mydb.commit()
                    update_ml_value(pregnancies,glucose,bloodpressure , skinthickness , insulin , bmi ,diabetespedigree_new ,  age , patient_id)
                    st.success("Successfully updated!!!")



            
                

                

               

        elif option == "View Record":
            st.title("Records")
            sql = "select * from lab_data"
            mycursor.execute(sql)
            result = mycursor.fetchall()
            record = []
            for row in result:
                record.append(row)

            record_df = pd.DataFrame(
                record,
                columns=[
                    "ID",
                    "Pregnancies",
                    "Glucose",
                    "Blood Pressure",
                    "Skin Thickness",
                    "Insulin",
                    "BMI",
                    "DiabetesPedigree",
                    "Age",
                    "outcome",
                ],
                index=range(1, len(record) + 1),
            )
            st.write(record_df)

        

    with tab6:
        st.title("Lab Results")
        sql_select = "SELECT id FROM lab_data"

        mycursor.execute(sql_select)
        result = mycursor.fetchall()
        record = []
        for row in result:
            record.append(row)

        record_df = pd.DataFrame(
            record,
            columns=[
                "id",
            ],
            index=range(1, len(record) + 1),
        )

        option_inside = st.selectbox("Choose ids to view result", list(record_df["id"]),key='resultView')
        query = "SELECT * FROM lab_data WHERE id = %s"
        mycursor.execute(query, (option_inside,))

        try:
            result_from_id = np.array(list(mycursor.fetchone())).reshape(1, 10)

            st.write(mycursor.fetchone())

            record_df_results = pd.DataFrame(
                result_from_id,
                columns=[
                    "ID",
                    "Pregnancies",
                    "Glucose",
                    "Blood Pressure",
                    "Skin Thickness",
                    "Insulin",
                    "BMI",
                    "DiabetesPedigree",
                    "Age",
                    "outcome",
                ],
                index=range(1, 2),
            )
            st.write(record_df_results)

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            if record_df_results["Glucose"].values[0] >= 126:
                col1.metric(
                    ":violet[Glucose] :red[High] ↗ ",
                    f"{record_df_results['Glucose'].values[0]} mg/dL",
                )
            elif record_df_results["Glucose"].values[0] <= 70:
                col1.metric(
                    ":violet[Glucose] :red[low] ↙ ",
                    f"{record_df_results['Glucose'].values[0]}mg/dL",
                )
            elif (
                record_df_results["Glucose"].values[0] > 70
                and record_df_results["Glucose"].values[0] <= 126
            ):
                col1.metric(
                    ":violet[Glucose] :green[Normal] ✅ ",
                    f"{record_df_results['Glucose'].values[0]}mg/dL",
                )

            if record_df_results["Blood Pressure"].values[0] > 80:
                col2.metric(
                    ":violet[Blood Pressure] :red[High] ↗ ",
                    f"{record_df_results['Blood Pressure'].values[0]} mmHg",
                )
            elif record_df_results["Blood Pressure"].values[0] < 60:
                col2.metric(
                    ":violet[Blood Pressure] :red[low] ↙ ",
                    f"{record_df_results['Blood Pressure'].values[0]}mmHg",
                )
            elif (
                record_df_results["Blood Pressure"].values[0] >= 60
                and record_df_results["Blood Pressure"].values[0] <= 80
            ):
                col2.metric(
                    ":violet[Blood Pressure] :green[Normal] ✅ ",
                    f"{record_df_results['Blood Pressure'].values[0]} mmHg",
                )

            col3.metric(
                ":violet[Skin Thickness]",
                f"{record_df_results['Skin Thickness'].values[0]} mm",
            )

            col4.metric(
                ":violet[Insulin]", f"{record_df_results['Insulin'].values[0]} mm"
            )

            if record_df_results["BMI"].values[0] < 18.5:
                col5.metric(
                    ":violet[BMI] :red[Underweight]  ↙ ",
                    f"{record_df_results['BMI'].values[0]} Kg/m^2",
                )
            elif (
                record_df_results["BMI"].values[0] >= 25
                and record_df_results["BMI"].values[0] <= 29.9
            ):
                col5.metric(
                    ":violet[BMI] :red[Overweight] ↗ ",
                    f"{record_df_results['BMI'].values[0]}Kg/m^2",
                )
            elif record_df_results["BMI"].values[0] >= 30:
                col5.metric(
                    ":violet[BMI] :red[Obesity] ↗",
                    f"{record_df_results['BMI'].values[0]} Kg/m^2",
                )
            elif (
                record_df_results["BMI"].values[0] >= 18.5
                and record_df_results["BMI"].values[0] <= 24.9
            ):
                col5.metric(
                    ":violet[BMI] :green[Normal Weight] ✅ ",
                    f"{record_df_results['BMI'].values[0]} Kg/m^2",
                )

            col6.metric(
                ":violet[DiabetesPedigree]",
                f"{record_df_results['DiabetesPedigree'].values[0]} mm",
            )

            if record_df_results["outcome"].values[0] == 0:
                st.success("Patient has no Diabetes")
            else:
                st.warning("Patient has Diabetes")

            TestReport.generate(option_inside)

            st.subheader("Send Reports to :violet[the Patients]")
            ToMail(option_inside)

        except Exception:
            st.subheader("")

def update_ml_value(pregnancies,glucose,bloodpressure , skinthickness , insulin , bmi ,diabetespedigree ,  age , patient_id):  



    


    x_predict = predictor.detect_diabetes(
    [
        pregnancies,
        glucose,
        bloodpressure,
        skinthickness,
        insulin,
        bmi,
        diabetespedigree,
        age,
    ]
    )
      

    
    
    


    sql_record = "UPDATE lab_data SET outcome=%s WHERE id=%s"
    val_record = (
        
        x_predict,
        patient_id
    )
    mycursor.execute(sql_record, val_record)

    mydb.commit()
