import streamlit as st
from util.backend import get_learners, get_teachers
from util.directus_connector import authenticate
# Create State Variables
if "access_token" not in st.session_state: st.session_state["access_token"] = ""
if "learners" not in st.session_state: st.session_state["learners"] = ""
if "teachers" not in st.session_state: st.session_state["teachers"] = ""

# Set the layout to wide mode
st.set_page_config(layout="wide")

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
        st.session_state["access_token"] = access_token

    except Exception as err:
            st.error(err)

if st.session_state["access_token"]:
     st.success(f"You have been successfully authenticated.")