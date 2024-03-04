import streamlit as st
st.header(":mailbox: Get In Touch with Me!")
contact_form = """
<form action="https://formsubmit.co/adityakshatriya2002@gmail.com" method="GET">
     <input type="text" name="name" required>
     <input type="email" name="email" required>
     <button type="submit">Send</button>
</form>


"""
st.markdown(contact_form , unsafe_allow_html=True)