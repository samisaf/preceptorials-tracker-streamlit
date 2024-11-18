import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from geopy.geocoders import Nominatim

@st.cache_data()
def get_students(access_token):
    return pd.read_csv(f'./data/students.csv') 

@st.cache_data()
def geolocate_institutions(students):
    """Add latitude and longitude based on the institution name if not available"""
    result = {}
    unique_institutions = students['institution'].dropna().unique().tolist()
    geolocator = Nominatim(user_agent="geoapiExercises")
    for inst in unique_institutions: 
        location = geolocator.geocode(inst)
        if location:
            result[inst] = (location.latitude, location.longitude)
    return result

# Set the layout to wide mode
st.set_page_config(layout="wide")

# Display Info page
st.title("Learners")

# Retrieve the entered data
access_token = st.session_state.get("access_token", "")

# Load CSV file into a pandas DataFrame
students = get_students(access_token)

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
geolocations = geolocate_institutions(students)
# Convert institution_data into a list of dictionaries with 'latitude', 'longitude', and 'name' keys
location_data = [
    {"name": name, "latitude": location[0], "longitude": location[1]}
    for name, location in geolocations.items()
]

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

st.write(geolocations)
# Ensure the user has provided a username, email, and password
if access_token:
    st.write(f"{access_token}")
else:
    st.warning("Please go to the Welcome Screen to enter your information.")

