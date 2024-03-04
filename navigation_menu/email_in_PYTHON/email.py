import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

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

if __name__ == '__main__':
    st.write("this is the base structure")

    with st.form("Email form"):
        subject = st.text_input(label='Subject', placeholder='Please enter subject of your mail')
        fullName = st.text_input(label='Full Name', placeholder='Enter name')
        email = st.text_input(label='Email', placeholder='Enter email')
        message_body = st.text_area(label='Message', placeholder='Enter message')
        uploaded_file = st.file_uploader('Attachment')
        submit_res = st.form_submit_button(label='Send')

        if submit_res:
            send_email(sender="adityacodesf1502@gmail.com", password="lwbl xrcx jlqf wnlh", receiver=email,
                       smtp_server="smtp.gmail.com", smtp_port=587, email_message=message_body,
                       subject=subject, attachment=uploaded_file)
