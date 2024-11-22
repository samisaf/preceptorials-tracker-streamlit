import streamlit as st
import pandas as pd
import numpy as np
from util.backend import get_learners

columns_to_display = [
    "first_name", "last_name", "institution", "year",
    "date_created_a", "a_average",
    "date_created_b", "b_average",
    "date_created_c", "c_average",
    "date_created_d", "d_average",
    "date_created_e", "e_average",
    "date_created_f", "f_average",
    "date_created_g", "g_average",
    "date_created_h", "h_average",
    "total_score"
]

column_config = {
    "first_name": "First Name", "last_name": "Last Name",  "institution": "Institution", "year": "Year",
    "date_created_a": "Date A",
    "date_created_b": "Date B",
    "date_created_c": "Date C",
    "date_created_d": "Date D",
    "date_created_e": "Date E",
    "date_created_f": "Date F",
    "date_created_g": "Date G",
    "date_created_h": "Date H",
    "a_average": "Score A",
    "b_average": "Score B",
    "c_average": "Score C",
    "d_average": "Score D",
    "e_average": "Score E",
    "f_average": "Score F",
    "g_average": "Score G",
    "h_average": "Score H",
    "total_score": "Total Score"
}   

access_token = st.session_state.get("access_token", "")
learners = get_learners(access_token)

st.title("Progress")

if access_token:
    # Subset the DataFrame
    filtered_learners = learners[columns_to_display]
    # Create tabs based on the year field
    unique_years = filtered_learners['year'].unique().tolist()
    unique_years = [str(int(u)) for u in unique_years if not np.isnan(u)]
    year_tabs = st.tabs(unique_years)

    # Display students based on the selected year tab
    for tab, year in zip(year_tabs, unique_years):
        with tab:
            year_students = filtered_learners[filtered_learners['year'] == int(year)]
            year_students = year_students.drop(columns=["year"])
            st.dataframe(year_students, hide_index=True, column_config=column_config, height=600 )
            

else:
    st.warning("Please go to the Welcome Screen to enter your information.")

