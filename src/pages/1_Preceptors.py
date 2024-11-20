import streamlit as st
import sys
import os
# adding parent directory to path in order to convert relative import to absolute import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Retrieve global state data
access_token = st.session_state.get("access_token", "")
teachers = st.session_state.get("teachers", "")

# st.set_page_config(layout="wide")
st.title("Our Preceptors")

# Ensure the user has provided a username, email, and password
if access_token:
    st.dataframe(teachers,
                 column_config={"first_name": "First Name", "last_name": "Last Name", "email": "Email",
                                "location": "Location", })
else:
    st.warning("Please go to the Welcome Screen to enter your information.")
