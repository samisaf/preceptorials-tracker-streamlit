import streamlit as st
import sys
import os
# adding parent directory to path in order to convert relative import to absolute import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.backend import get_teacher_users

def get_preceptors(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    users = get_teacher_users(headers)
    return users

if "preceptors" not in st.session_state:
    st.session_state["preceptors"] = ""

# Set the layout to wide mode
# st.set_page_config(layout="wide")
# Retrieve the entered data
access_token = st.session_state.get("access_token", "")
# Display Info page
st.title("Our Preceptors")

# Ensure the user has provided a username, email, and password
if access_token:
    preceptors = get_preceptors(access_token)
    st.dataframe(preceptors, 
                     column_config={"first_name": "First Name", 
                                    "last_name": "Last Name", 
                                    "email": "Email", 
                                    "location": "Location",} )  
else:
    st.warning("Please go to the Welcome Screen to enter your information.")
