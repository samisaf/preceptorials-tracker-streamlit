import streamlit as st
import sys
import os
from util.backend import get_teachers

# Retrieve global state data
access_token = st.session_state.get("access_token", "")

# st.set_page_config(layout="wide")
st.title("Our Preceptors")
st.write("Thanks to all of our preceptors for their dedication.")
# Ensure the user has provided a username, email, and password
if access_token:
    teachers = get_teachers(access_token)
    for _, row in teachers.iterrows():
        st.write(f"- {row['first_name']} {row['last_name']}, {row['location']}")

else:
    st.warning("Please go to the Welcome Screen to enter your information.")
