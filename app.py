import streamlit as st
import pandas as pd

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="BhuRakshak",
    page_icon="🌧️",
    layout="wide"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.hero {
    padding: 30px;
    border-radius: 18px;
    background: linear-gradient(135deg, #12372A, #436850);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 5px;
}

.card {
    padding: 22px;
    border-radius: 16px;
    background: white;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

.risk-low {
    padding: 18px;
    border-radius: 14px;
    background: #e8f5e9;
    font-size: 22px;
    font-weight: bold;
}

.risk-moderate {
    padding: 18px;
    border-radius: 14px;
    background: #fff8e1;
    font-size: 22px;
    font-weight: bold;
}

.risk-high {
    padding: 18px;
    border-radius: 14px;
    background: #fff3e0;
    font-size: 22px;
    font-weight: bold;
}

.risk-critical {
    padding: 18px;
    border-radius: 14px;
    background: #ffebee;
    font-size: 22px;
    font-weight: bold;
}

.small {
    color: #667085;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

def go_to(page):
    st.session_state.page = page

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>🌧️ BhuRakshak</h1>
    <h3>AI-Based Landslide Early Warning & Risk Monitoring System</h3>
    <p>Predict. Prepare. Protect.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------
nav = st.columns(6)

with nav[0]:
    if st.button("🏠 Home", use_container_width=True):
        go_to("Home")

with nav[1]:
    if st.button("🗺️ Risk Map", use_container_width=True):
        go_to("Risk Map")

with nav[2]:
    if st.button("🤖 Risk Prediction", use_container_width=True):
        go_to("Risk Prediction")

with nav[3]:
    if st.button("🚨 Alerts", use_container_width=True):
        go_to("Alerts")

with nav[4]:
    if st.button("🏥 Safe Zones", use_container_width=True):
        go_to("Safe Zones")

with nav[5]:
    if st.button("📊 Dashboard", use_container_width=True):
        go_to("Dashboard")

st.divider()

# =====================================================
# HOME
# =====================================================

if st.session_state.page == "Home":

    st.subheader("Know the Risk. Get Warned. Stay Safe.")

    st.write(
        "BhuRakshak combines rainfall, terrain, historical landslide "
        "information and other risk factors to provide location-based "
        "landslide risk information."
    )

    st.markdown("### 🚀 Quick Actions")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
        <h3>🗺️ Live Risk Map</h3>
        <p>Explore landslide-prone locations across the North Eastern Region.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Risk Map →", key="map_home",
                     use_container_width=True):
            go_to("Risk Map")

    with c2:
        st.markdown("""
        <div class="card">
        <h3>🤖 Check My Risk</h3>
        <p>Enter environmental conditions and calculate a prototype risk score.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Check Risk →", key="risk_home",
                     use_container_width=True):
            go_to("Risk Prediction")

    with c3:
        st.markdown("""
        <div class="card">
        <h3>🚨 Emergency Alerts</h3>
        <p>View high-risk locations and recommended safety actions.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View Alerts →", key="alert_home",
                     use_container_width=True):
            go_to("Alerts")

    st.markdown("### 📊 System Overview")

    a, b, c, d = st.columns(4)

    a.metric("Monitored Zones", "24")
    b.metric("High Risk Zones", "7")
    c.metric("Active Alerts", "3")
    d.metric("Safe Zones", "18")

    st.markdown("### ⚙️ How BhuRakshak Works")

    p1, p2, p3, p4 = st.columns(4)

    p1.info("1️⃣ DATA\n\nRainfall, terrain and historical data")
    p2.info("2️⃣ AI ENGINE\n\nAnalyse multiple risk factors")
    p3.warning("3️⃣ RISK SCORE\n\nLOW → MODERATE → HIGH → CRITICAL")
    p4.success("4️⃣ EARLY WARNING\n\nAlert communities and authorities")

# =====================================================
# RISK MAP
# =====================================================

elif st.session_state.page == "Risk Map":

    st.subheader("🗺️ Live Landslide Risk Map")

    st.write("Prototype demonstration data for North Eastern Region.")

    locations = pd.DataFrame({
        "Location": [
            "Shillong",
            "Cherrapunji",
            "Aizawl",
            "Gangtok",
            "Itanagar",
            "Kohima",
            "Imphal",
            "Agartala"
        ],
        "lat": [
            25.5788, 25.2841, 23.7271, 27.3389,
            27.0844, 25.6751, 24.8170, 23.8315
        ],
        "lon": [
            91.8933, 91.7210, 92.7176, 88.6065,
            93.6053, 94.1086, 93.9368, 91.2868
        ],
        "Risk Score": [72, 84, 67, 78, 55, 81, 48, 32],
        "Risk": [
            "HIGH",
            "CRITICAL",
            "HIGH",
            "HIGH",
            "MODERATE",
            "CRITICAL",
            "MODERATE",
            "LOW"
        ]
    })

    st.dataframe(
        locations[["Location", "Risk", "Risk Score"]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 📍 Geographic View")

    st.map(
        locations.rename(columns={"lat": "latitude", "lon": "longitude"}),
        latitude="latitude",
        longitude="longitude",
        size=100
    )

    st.caption(
        "⚠️ Prototype/demo data. Real-time GIS and satellite integrations "
        "can be connected in the next development stage."
    )

# =====================================================
# RISK PREDICTION
# =====================================================

elif st.session_state.page == "Risk Prediction":

    st.subheader("🤖 AI Risk Prediction")

    st.write(
        "Adjust the environmental conditions below to simulate "
        "landslide-risk assessment."
    )

    col1, col2 = st.columns(2)

    with col1:

        rainfall = st.slider(
            "🌧️ Rainfall intensity (mm)",
            0, 250, 60
        )

        soil = st.slider(
            "💧 Soil moisture (%)",
            0, 100, 40
        )

        slope = st.slider(
            "⛰️ Slope angle (°)",
            0, 60, 25
        )

    with col2:

        historical = st.slider(
            "📚 Historical landslide risk (%)",
            0, 100, 30
        )

        terrain = st.slider(
            "🛰️ Terrain / satellite indicator (%)",
            0, 100, 30
        )

    # Weighted prototype algorithm
    rainfall_score = min(rainfall / 250 * 100, 100)
    soil_score = soil
    slope_score = min(slope / 60 * 100, 100)

    risk_score = (
        rainfall_score * 0.30 +
        soil_score * 0.25 +
        slope_score * 0.20 +
        historical * 0.15 +
        terrain * 0.10
    )

    risk_score = round(risk_score, 1)

    if risk_score < 30:
        risk = "LOW"
        st.markdown(
            f'<div class="risk-low">🟢 LOW RISK — {risk_score}%</div>',
            unsafe_allow_html=True
        )

    elif risk_score < 50:
        risk = "MODERATE"
        st.markdown(
            f'<div class="risk-moderate">🟡 MODERATE RISK — {risk_score}%</div>',
            unsafe_allow_html=True
        )

    elif risk_score < 75:
        risk = "HIGH"
        st.markdown(
            f'<div class="risk-high">🟠 HIGH RISK — {risk_score}%</div>',
            unsafe_allow_html=True
        )

    else:
        risk = "CRITICAL"
        st.markdown(
            f'<div class="risk-critical">🔴 CRITICAL RISK — {risk_score}%</div>',
            unsafe_allow_html=True
        )

    st.markdown("### 📊 Risk Factors")

    f1, f2, f3, f4, f5 = st.columns(5)

    f1.metric("Rainfall", f"{rainfall} mm")
    f2.metric("Soil Moisture", f"{soil}%")
    f3.metric("Slope", f"{slope}°")
    f4.metric("Historical", f"{historical}%")
    f5.metric("Terrain", f"{terrain}%")

    st.markdown("### 🧠 Why this risk level?")

    if rainfall > 150:
        st.write("🌧️ Heavy rainfall is significantly increasing the risk.")

    if soil > 70:
        st.write("💧 High soil moisture may reduce slope stability.")

    if slope > 40:
        st.write("⛰️ Steep terrain increases landslide susceptibility.")

    if historical > 60:
        st.write("📚 Historical landslide activity increases the risk.")

    if risk_score < 50:
        st.success("Current conditions indicate comparatively lower risk.")

    elif risk_score < 75:
        st.warning("Precaution and monitoring are recommended.")

    else:
        st.error(
            "🚨 Critical conditions detected. Early warning action is recommended."
        )

    st.caption(
        "Prototype: weighted risk algorithm used for demonstration. "
        "A trained ML model can replace this module in future."
    )

# =====================================================
# ALERTS
# =====================================================

elif st.session_state.page == "Alerts":

    st.subheader("🚨 Early Warning Alerts")

    st.error(
        "🔴 CRITICAL — Cherrapunji\n\n"
        "Heavy rainfall + steep terrain + historical landslide risk."
    )

    st.warning(
        "🟠 HIGH — Shillong\n\n"
        "Rainfall conditions are increasing landslide risk."
    )

    st.warning(
        "🟠 HIGH — Gangtok\n\n"
        "Slope and historical risk indicators are elevated."
    )

    st.markdown("### 🛡️ Recommended Actions")

    st.info(
        "• Avoid unnecessary travel through high-risk slopes.\n"
        "• Follow official evacuation instructions.\n"
        "• Move towards designated safe zones if instructed.\n"
        "• Report new cracks, debris flow or slope movement."
    )

# =====================================================
# SAFE ZONES
# =====================================================

elif st.session_state.page == "Safe Zones":

    st.subheader("🏥 Safe Zones & Emergency Centres")

    safezones = pd.DataFrame({
        "Place": [
            "Shillong Emergency Shelter",
            "Cherrapunji Community Centre",
            "Aizawl Safe Shelter",
            "Gangtok Emergency Centre"
        ],
        "Type": [
            "Shelter",
            "Community Centre",
            "Shelter",
            "Emergency Centre"
        ],
        "Capacity": [
            "250 people",
            "180 people",
            "220 people",
            "150 people"
        ],
        "Status": [
            "Open",
            "Open",
            "Available",
            "Open"
        ]
    })

    st.dataframe(
        safezones,
        use_container_width=True,
        hide_index=True
    )

    st.success(
        "📍 In a real deployment, the nearest safe zone would be "
        "recommended using the user's approximate location."
    )

# =====================================================
# AUTHORITY DASHBOARD
# =====================================================

elif st.session_state.page == "Dashboard":

    st.subheader("👨‍💼 Authority Dashboard")

    a, b, c, d = st.columns(4)

    a.metric("Critical Zones", "3")
    b.metric("High Risk Zones", "7")
    c.metric("Active Alerts", "3")
    d.metric("Incident Reports", "12")

    st.markdown("### 📈 Risk Monitoring")

    chart = pd.DataFrame({
        "Risk Level": ["Low", "Moderate", "High", "Critical"],
        "Zones": [8, 6, 7, 3]
    })

    st.bar_chart(
        chart.set_index("Risk Level")
    )

    st.markdown("### 🚧 Road Status")

    roads = pd.DataFrame({
        "Road": [
            "Shillong–Cherrapunji Road",
            "Aizawl–Lunglei Road",
            "Gangtok–North Sikkim Road",
            "Kohima–Dimapur Road"
        ],
        "Status": [
            "⚠️ Caution",
            "🟢 Open",
            "🔴 Blocked",
            "🟢 Open"
        ]
    })

    st.dataframe(
        roads,
        use_container_width=True,
        hide_index=True
    )

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "BhuRakshak • Predict. Prepare. Protect. • SIH 2026 Prototype"
)
