import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import sys
import os
# adding parent directory to path in order to convert relative import to absolute import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.geolocations import get_student_locations

access_token = st.session_state.get("access_token", "")
students = st.session_state.get("students", "")

# Set the layout to wide mode
st.set_page_config(layout="wide")

# Display Info page
st.title("Learners")

# Create tabs based on the year field
unique_years = students['year'].unique().tolist()
unique_years = [str(int(u)) for u in unique_years if not np.isnan(u)]
year_tabs = st.tabs(unique_years)

# Display students based on the selected year tab
for tab, year in zip(year_tabs, unique_years):
    with tab:
        year_students = students[students['year'] == int(year)][['first_name', 'last_name', 'institution']]
        st.dataframe(year_students, hide_index=True, column_config={"first_name": "First Name", "last_name": "Last Name",  "institution": "Institution",} )

# Display a map of the US with dots representing each institution
st.subheader("Institutions Map")

# Display a map of the US with dots representing each institution
location_data = get_student_locations()

# Convert institution_data into a list of dictionaries with 'latitude', 'longitude', and 'name' keys
# location_data = [
#     {"name": name, "latitude": location[0], "longitude": location[1]}
#     for name, location in geolocations.items()
# ]

# Pydeck chart with tooltip showing institution name on hover
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=37.0902,  # Centered on the USA
        longitude=-95.7129,
        zoom=3,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=location_data,  # Pass the data with institution names
            get_position='[longitude, latitude]',
            get_radius=50000,
            get_color='[200, 30, 0, 160]',
            pickable=True,  # Enables the hover
        ),
    ],
    tooltip={
        "html": "<b>Institution:</b> {name}",  # Format the tooltip to display the institution name
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
))

st.write(location_data)
# Ensure the user has provided a username, email, and password
if access_token:
    st.write(f"{access_token}")
else:
    st.warning("Please go to the Welcome Screen to enter your information.")

