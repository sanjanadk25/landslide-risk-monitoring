import streamlit as st

st.set_page_config(
    page_title="Landslide Risk Monitoring",
    page_icon="⛰️",
    layout="wide"
)

st.title("⛰️ Landslide Risk Monitoring System")
st.subheader("AI-Based Early Warning System for North Eastern Region")

st.write("Welcome to our prototype!")

st.info("🚧 Prototype under development")

st.header("📊 Risk Monitoring")

location = st.selectbox(
    "Select Location",
    ["Meghalaya", "Sikkim", "Arunachal Pradesh", "Assam"]
)

rainfall = st.slider(
    "🌧️ Rainfall (mm)",
    0, 300, 100
)

slope = st.slider(
    "⛰️ Slope (degrees)",
    0, 60, 20
)

st.write("### Selected Location")
st.write(location)

st.write("### Current Conditions")
st.write(f"Rainfall: {rainfall} mm")
st.write(f"Slope: {slope}°")

st.success("✅ Basic prototype is working!")
