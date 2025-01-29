import folium as fl
# m = fl.Map(location=[1.286389, 36.817223], zoom_start=7)

# st_map = st_folium(m, width=700, height=450)

# st.markdown("![Foo](https://www.google.com/maps/search/financial+institutions,+banks,+saccos/@-1.2996977,36.7871538,15z?entry=ttu&g_ep=EgoyMDI0MTIwMi4wIKXMDSoASAFQAw%3D%3D)(http://google.com.au/)")

import streamlit as st
import folium as fl
from streamlit_folium import st_folium
import requests

# Function to fetch financial institutions using Overpass API
def fetch_osm_data(query, bounding_box):
    url = "https://overpass-api.de/api/interpreter"
    osm_query = f"""
    [out:json];
    node["amenity"="{query}"]({bounding_box});
    out;
    """
    response = requests.get(url, params={"data": osm_query})
    if response.status_code == 200:
        return response.json()["elements"]
    else:
        st.error("Error fetching data from OpenStreetMap API.")
        return []

# Streamlit App
st.title("Gym, Trainers & Wellness institutes near me..")

# Define bounding box for Nairobi (latitude_min, longitude_min, latitude_max, longitude_max)
nairobi_bbox = "-1.406108,36.641423,-1.145753,37.010971"

# Fetch data for Gymn and  Health & Wellness
st.write("Fetching fitness centers in Nairobi...")
gym_data = fetch_osm_data("hospital", nairobi_bbox)
# wellness_data = fetch_osm_data("wellness institutions", nairobi_bbox)


# Initialize Folium Map
m = fl.Map(location=[-1.286389, 36.817223], zoom_start=13)

# Add markers for banks and ATMs
for gym in gym_data:
    fl.Marker(
        location=[gym["lat"], gym["lon"]],
        popup=gym.get("tags", {}).get("name", "Unnamed Gym"),
        tooltip="Gym",
        icon=fl.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

# for wellness in wellness_data:
#     fl.Marker(
#         location=[wellness["lat"], wellness["lon"]],
#         popup=wellness.get("tags", {}).get("name", "Unnamed Wellness Institute"),
#         tooltip="Wellness",
#         icon=fl.Icon(color="red", icon="info-sign"),
#     ).add_to(m)


# Display the map
st_map = st_folium(m, width=1000, height=800)