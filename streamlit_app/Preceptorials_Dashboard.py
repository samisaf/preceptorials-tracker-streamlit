import streamlit as st
from util.backend import authenticate

st.write(
"""
# Preceptorials Dashboard

Welcome to our new dashboard. Please enter your email and password to access learner information. 
Once authenticated, you may navigate the available pages using the menu on the left.
"""
)

# if "email" not in st.session_state:
#     st.session_state["email"] = ""
# if "password" not in st.session_state:
#     st.session_state["password"] = ""
if "access_token" not in st.session_state:
    st.session_state["access_token"] = ""

email = st.text_input("Enter Email")
password = st.text_input("Enter Password", type="password")

# Create a Submit button when clicked, it calls the authenticate function
if st.button("Submit") and (email and password):
    try:
        st.session_state["access_token"] = authenticate(email, password)
        st.success(f"You have been successfully authenticated.")
    except Exception as err:
            st.error(err)

