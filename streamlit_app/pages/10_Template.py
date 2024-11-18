import streamlit as st
# Set the layout to wide mode
st.set_page_config(layout="wide")

# Display Info page
st.title("Display User Information")

# Retrieve the entered data
access_token = st.session_state.get("access_token", "")

# Ensure the user has provided a username, email, and password
if access_token:
    st.write(f"{access_token}")
else:
    st.warning("Please go to the Welcome Screen to enter your information.")