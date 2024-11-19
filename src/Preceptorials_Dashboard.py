import streamlit as st
from util.backend import authenticate, get_students, get_teachers, get_chapters

# Create State Variables
if "access_token" not in st.session_state: st.session_state["access_token"] = ""
if "students" not in st.session_state: st.session_state["students"] = ""
if "teachers" not in st.session_state: st.session_state["teachers"] = ""
if "chapters" not in st.session_state: st.session_state["chapters"] = ""

st.write(
"""
# Preceptorials Dashboard

Welcome to our new dashboard. Please enter your email and password to access learner information. 
Once authenticated, you may navigate the available pages using the menu on the left.
"""
)

email = st.text_input("Enter Email")
password = st.text_input("Enter Password", type="password")

# Create a Submit button when clicked, it calls the authenticate function
if st.button("Submit") and (email and password):
    try:
        access_token = authenticate(email, password)
        st.success(f"You have been successfully authenticated.")
        st.session_state["access_token"] = access_token
        st.session_state["students"] = get_students(access_token)
        st.session_state["teachers"] = get_teachers(access_token)
        st.session_state["chapters"] = get_chapters(access_token)
    except Exception as err:
            st.error(err)

