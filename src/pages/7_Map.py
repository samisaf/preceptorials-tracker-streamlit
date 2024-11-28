import streamlit as st
import pydeck as pdk
from util.geolocations import get_student_locations

access_token = st.session_state.get("access_token", "")

st.title("Where do our Learners Come From?")
st.write("Zoom out to see our learners from across the world.")
# Display a map of the US with dots representing each institution
location_data = get_student_locations()

# Pydeck chart with tooltip showing institution name on hover
deck = pdk.Deck(
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
)

if access_token:
    st.pydeck_chart(deck)
else:
    st.warning("Please go to the Welcome Screen to enter your information.")

