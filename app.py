import streamlit as st

# ---------- PAGE SETTINGS ----------
st.set_page_config(
    page_title="BhuRakshak",
    page_icon="⛰️",
    layout="wide"
)

# ---------- CUSTOM DESIGN ----------
st.markdown("""
<style>
.main {
    background-color: #f5f8f7;
}

.hero {
    padding: 35px;
    border-radius: 20px;
    background: linear-gradient(135deg, #063b35, #0b6658);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 48px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 20px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 15px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

.risk {
    background: #fff3cd;
    padding: 25px;
    border-radius: 16px;
    text-align: center;
}

.footer {
    text-align: center;
    padding: 25px;
    color: #666;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("⛰️ BhuRakshak")
st.sidebar.caption("Predict. Prepare. Protect.")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🗺️ Live Risk Map",
        "🤖 Risk Prediction",
        "🚨 Alerts",
        "📍 Check My Risk",
        "🟢 Safe Zones",
        "📝 Report Incident",
        "🤖 BhuRakshak AI",
        "👨‍💼 Authority Dashboard",
        "ℹ️ About"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Prototype Mode\n\n"
    "Data shown in this version is demonstration data."
)

# ---------- HOME ----------
if page == "🏠 Home":

    st.markdown("""
    <div class="hero">
        <h1>⛰️ BhuRakshak</h1>
        <h3>Predict. Prepare. Protect.</h3>
        <p>
        AI-Based Early Warning & Landslide Risk Monitoring
        System for the North Eastern Region of India.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗺️ View Live Risk Map", use_container_width=True):
            st.info("Use the Live Risk Map section from the sidebar.")

    with col2:
        if st.button("📍 Check My Area Risk", use_container_width=True):
            st.info("Use the Check My Risk section from the sidebar.")

    st.subheader("📊 BhuRakshak at a Glance")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Monitoring", "24/7")
    c2.metric("AI Risk Analysis", "Active")
    c3.metric("Active Alerts", "7")
    c4.metric("Reports", "143")

    st.subheader("🛡️ How BhuRakshak Protects Communities")

    a, b, c, d = st.columns(4)

    with a:
        st.markdown("""
        <div class="card">
        <h3>1. 📡 Collect</h3>
        Rainfall, soil moisture, terrain, satellite and historical data.
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="card">
        <h3>2. 🧠 Analyse</h3>
        AI/ML models analyse environmental conditions.
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="card">
        <h3>3. 📊 Predict</h3>
        Generate location-based landslide risk scores.
        </div>
        """, unsafe_allow_html=True)

    with d:
        st.markdown("""
        <div class="card">
        <h3>4. 🚨 Alert</h3>
        Provide early warnings when risk becomes critical.
        </div>
        """, unsafe_allow_html=True)

    st.subheader("🌏 North Eastern Region")

    st.write(
        "BhuRakshak is designed to support landslide risk monitoring "
        "across the North Eastern Region of India."
    )

# ---------- LIVE RISK MAP ----------
elif page == "🗺️ Live Risk Map":

    st.title("🗺️ Live Risk Map")
    st.caption("Prototype GIS visualization using demonstration data.")

    location = st.selectbox(
        "Select Region",
        [
            "Meghalaya",
            "Sikkim",
            "Arunachal Pradesh",
            "Assam",
            "Nagaland",
            "Manipur",
            "Mizoram",
            "Tripura"
        ]
    )

    st.map(
        {
            "lat": [25.4670],
            "lon": [91.3662]
        },
        zoom=6
    )

    st.subheader(f"📍 Risk Information — {location}")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Risk Score", "78/100")
    c2.metric("Risk Level", "HIGH")
    c3.metric("Rainfall", "112 mm")
    c4.metric("Slope", "38°")

    st.warning(
        "⚠️ Prototype warning: Heavy rainfall combined with "
        "steep terrain may increase landslide risk."
    )

    st.info(
        "Demo data only. Production deployment will integrate "
        "verified geographical and environmental datasets."
    )

# ---------- RISK PREDICTION ----------
elif page == "🤖 Risk Prediction":

    st.title("🤖 AI Risk Prediction Engine")

    st.write(
        "BhuRakshak estimates landslide risk by combining "
        "environmental and geographical indicators."
    )

    st.divider()

    rainfall = st.slider(
        "🌧️ Rainfall",
        0, 300, 120
    )

    soil = st.slider(
        "💧 Soil Moisture",
        0, 100, 70
    )

    slope = st.slider(
        "⛰️ Slope Angle",
        0, 60, 30
    )

    historical = st.slider(
        "📚 Historical Landslide Risk",
        0, 100, 65
    )

    terrain = st.slider(
        "🪨 Terrain Instability",
        0, 100, 60
    )

    # Prototype weighted risk calculation
    rainfall_score = min(rainfall / 3, 100)

    risk = (
        rainfall_score * 0.30
        + soil * 0.25
        + (slope / 60 * 100) * 0.20
        + historical * 0.15
        + terrain * 0.10
    )

    risk = round(risk)

    st.divider()

    if risk < 30:
        level = "LOW"
        st.success(f"🟢 RISK LEVEL: {level}")
    elif risk < 50:
        level = "MODERATE"
        st.warning(f"🟡 RISK LEVEL: {level}")
    elif risk < 75:
        level = "HIGH"
        st.warning(f"🟠 RISK LEVEL: {level}")
    else:
        level = "CRITICAL"
        st.error(f"🔴 RISK LEVEL: {level}")

    st.metric("AI Risk Score", f"{risk}/100")

    st.subheader("Risk Factors")

    st.progress(min(rainfall_score / 100, 1.0))
    st.write(f"Rainfall: {round(rainfall_score)}%")

    st.progress(soil / 100)
    st.write(f"Soil Moisture: {soil}%")

    st.progress(slope / 60)
    st.write(f"Slope: {slope}°")

    st.progress(historical / 100)
    st.write(f"Historical Risk: {historical}%")

    st.progress(terrain / 100)
    st.write(f"Terrain Instability: {terrain}%")

    if risk >= 75:
        st.error(
            "🚨 EARLY WARNING: Critical landslide risk detected. "
            "Follow official safety instructions and move away "
            "from unstable slopes."
        )

    st.caption(
        "Prototype/Simulation: This demonstration uses a transparent "
        "weighted-risk algorithm. It is not a production prediction model."
    )

# ---------- ALERTS ----------
elif page == "🚨 Alerts":

    st.title("🚨 Early Warning & Alerts")

    st.error(
        "🔴 CRITICAL ALERT\n\n"
        "High landslide risk detected in a monitored zone."
    )

    st.subheader("Active Alerts")

    st.markdown("""
    **🔴 Critical — Meghalaya**  
    Heavy rainfall + high soil moisture + steep terrain.

    **🟠 High — Sikkim**  
    Elevated rainfall and historical landslide susceptibility.

    **🟡 Moderate — Arunachal Pradesh**  
    Increased rainfall conditions being monitored.
    """)

    st.subheader("📢 Alert Channels")

    c1, c2, c3, c4 = st.columns(4)

    c1.info("📱 SMS")
    c2.info("🔔 Mobile Notification")
    c3.info("🌐 Web Notification")
    c4.info("🏢 Authority Dashboard")

# ---------- CHECK MY RISK ----------
elif page == "📍 Check My Risk":

    st.title("📍 Check My Area Risk")

    st.write(
        "Enter your area information to view the prototype risk assessment."
    )

    location = st.selectbox(
        "Select your location",
        ["Meghalaya", "Sikkim", "Assam", "Arunachal Pradesh"]
    )

    if st.button("🔍 Check Risk", use_container_width=True):

        st.error("🔴 HIGH RISK")

        st.metric("Risk Score", "78/100")

        st.subheader("Why is the risk high?")

        st.write("🌧️ Heavy rainfall")
        st.write("💧 High soil moisture")
        st.write("⛰️ Steep slope")
        st.write("📚 Historical landslide activity")

        st.warning(
            "Stay away from steep slopes and drainage channels. "
            "Keep emergency supplies ready and follow official "
            "evacuation instructions."
        )

        c1, c2 = st.columns(2)

        c1.button("🟢 Find Safe Zone")
        c2.button("🗺️ View Full Analysis")

# ---------- SAFE ZONES ----------
elif page == "🟢 Safe Zones":

    st.title("🟢 Find Safe Places")

    st.write("Prototype safe-zone database.")

    places = [
        ("🏫 Relief Shelter — Meghalaya", "Capacity: 250", "OPEN"),
        ("🏥 District Hospital", "Emergency services available", "OPEN"),
        ("🏢 Emergency Centre", "Capacity: 100", "OPEN"),
        ("🚓 Police Station", "Emergency assistance", "OPEN")
    ]

    for name, info, status in places:
        st.markdown(
            f"""
            <div class="card">
            <h3>{name}</h3>
            <p>{info}</p>
            <b>Status: 🟢 {status}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.button("📍 Find Nearest Safe Zone")

# ---------- REPORT INCIDENT ----------
elif page == "📝 Report Incident":

    st.title("📝 Report an Incident")

    incident = st.selectbox(
        "Incident Type",
        [
            "Landslide",
            "Road blockage",
            "Slope crack",
            "Soil movement",
            "Flash flood",
            "Fallen trees",
            "Infrastructure damage"
        ]
    )

    description = st.text_area("Describe the incident")

    severity = st.select_slider(
        "Severity",
        options=["Low", "Moderate", "High", "Critical"]
    )

    uploaded = st.file_uploader(
        "📷 Upload Photograph",
        type=["jpg", "jpeg", "png"]
    )

    if st.button("🚨 Submit Report", use_container_width=True):

        st.success("✅ Report Successfully Submitted")

        st.info(
            "Incident ID: BRK-2026-00421\n\n"
            "The report has been added to the prototype incident system."
        )

# ---------- AI ASSISTANT ----------
elif page == "🤖 BhuRakshak AI":

    st.title("🤖 BhuRakshak AI")

    st.caption("Your disaster safety assistant")

    question = st.text_input(
        "Ask a disaster-safety question"
    )

    if st.button("Ask BhuRakshak AI"):

        if question:
            st.info(
                "For immediate safety: move away from steep or unstable "
                "slopes, avoid flowing water and follow instructions "
                "from local emergency authorities."
            )

            st.caption(
                "Prototype AI Assistant. Location-specific live "
                "information requires verified emergency databases."
            )
        else:
            st.warning("Please enter a question.")

# ---------- AUTHORITY DASHBOARD ----------
elif page == "👨‍💼 Authority Dashboard":

    st.title("👨‍💼 Authority Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Critical Zones", "12")
    c2.metric("High-Risk Zones", "28")
    c3.metric("Active Alerts", "7")

    c4, c5, c6 = st.columns(3)

    c4.metric("Reported Incidents", "143")
    c5.metric("Blocked Roads", "9")
    c6.metric("People Potentially Affected", "18,450")

    st.subheader("Priority Monitoring")

    st.dataframe(
        {
            "Location": [
                "Meghalaya Zone A",
                "Sikkim Zone B",
                "Arunachal Zone C"
            ],
            "Risk": [
                "CRITICAL",
                "HIGH",
                "MODERATE"
            ],
            "Population": [
                "4,200",
                "2,800",
                "1,900"
            ],
            "Road Status": [
                "Blocked",
                "Caution",
                "Open"
            ]
        },
        use_container_width=True
    )

# ---------- ABOUT ----------
elif page == "ℹ️ About":

    st.title("ℹ️ About BhuRakshak")

    st.markdown("""
    ### BhuRakshak
    **Predict. Prepare. Protect.**

    BhuRakshak is a prototype AI-based early warning and
    landslide risk monitoring platform designed for the
    North Eastern Region of India.

    ### System Architecture

    🌧️ Rainfall  
    ↓  
    💧 Soil Moisture  
    ↓  
    🛰️ Satellite Information  
    ↓  
    ⛰️ Terrain & Slope  
    ↓  
    📚 Historical Landslide Data  
    ↓  
    🤖 AI/ML Risk Engine  
    ↓  
    📊 Risk Score  
    ↓  
    🗺️ GIS Visualization  
    ↓  
    🚨 Early Warning  
    ↓  
    👨‍💼 Authorities + 👥 Communities
    """)

    st.info(
        "This is an SIH prototype. Demonstration data and "
        "simulated predictions are clearly separated from "
        "future verified live-data integrations."
    )

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
BhuRakshak • Predict. Prepare. Protect. • SIH 2026 Prototype
</div>
""", unsafe_allow_html=True)
