import os
import json
import uuid
import time
from datetime import datetime, timezone
from math import radians, sin, cos, asin, sqrt

import requests
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation

st.set_page_config(
    page_title="BhuRakshak | Live Landslide Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# CONFIG / SESSION STATE
# -----------------------------
APP_TITLE = "BhuRakshak"
NER_CENTER = [25.5, 91.3]  # North-East India demo center

DEMO_ZONES = [
    {"name": "Shillong Hills", "state": "Meghalaya", "lat": 25.5788, "lon": 91.8933, "risk": 82, "rain": 74, "slope": 36},
    {"name": "Aizawl Hills", "state": "Mizoram", "lat": 23.7271, "lon": 92.7176, "risk": 76, "rain": 68, "slope": 41},
    {"name": "Gangtok Slopes", "state": "Sikkim", "lat": 27.3389, "lon": 88.6065, "risk": 71, "rain": 59, "slope": 38},
    {"name": "Itanagar Hills", "state": "Arunachal Pradesh", "lat": 27.0844, "lon": 93.6053, "risk": 64, "rain": 53, "slope": 34},
    {"name": "Kohima Hills", "state": "Nagaland", "lat": 25.6751, "lon": 94.1086, "risk": 58, "rain": 46, "slope": 31},
    {"name": "Imphal Valley Edge", "state": "Manipur", "lat": 24.8170, "lon": 93.9368, "risk": 43, "rain": 39, "slope": 22},
]

if "reports" not in st.session_state:
    st.session_state.reports = []
if "last_report_count" not in st.session_state:
    st.session_state.last_report_count = 0
if "messages" not in st.session_state:
    st.session_state.messages = []
if "role" not in st.session_state:
    st.session_state.role = "Citizen"
if "weather" not in st.session_state:
    st.session_state.weather = None
if "location" not in st.session_state:
    st.session_state.location = None


# -----------------------------
# OPTIONAL SUPABASE
# -----------------------------
def supabase_configured():
    try:
        return bool(st.secrets["SUPABASE_URL"]) and bool(st.secrets["SUPABASE_KEY"])
    except Exception:
        return False


def supabase_headers():
    return {
        "apikey": st.secrets["SUPABASE_KEY"],
        "Authorization": f"Bearer {st.secrets['SUPABASE_KEY']}",
        "Content-Type": "application/json",
    }


def load_reports():
    if not supabase_configured():
        return st.session_state.reports

    try:
        url = st.secrets["SUPABASE_URL"].rstrip("/") + "/rest/v1/reports"
        params = {"select": "*", "order": "created_at.desc", "limit": "100"}
        r = requests.get(url, headers=supabase_headers(), params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        st.session_state.reports = data
        return data
    except Exception:
        return st.session_state.reports


def save_report(report):
    st.session_state.reports.insert(0, report)

    if supabase_configured():
        try:
            url = st.secrets["SUPABASE_URL"].rstrip("/") + "/rest/v1/reports"
            r = requests.post(
                url,
                headers={**supabase_headers(), "Prefer": "return=minimal"},
                json=report,
                timeout=8,
            )
            r.raise_for_status()
        except Exception as e:
            st.warning(f"Cloud database unavailable; report kept for this app session. ({e})")


def update_report_status(report_id, status):
    for r in st.session_state.reports:
        if r.get("id") == report_id:
            r["status"] = status

    if supabase_configured():
        try:
            url = st.secrets["SUPABASE_URL"].rstrip("/") + "/rest/v1/reports"
            params = {"id": f"eq.{report_id}"}
            requests.patch(
                url,
                headers={**supabase_headers(), "Prefer": "return=minimal"},
                params=params,
                json={"status": status},
                timeout=8,
            )
        except Exception:
            pass


# -----------------------------
# HELPERS
# -----------------------------
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))


def nearest_zone(lat, lon):
    return min(DEMO_ZONES, key=lambda z: haversine_km(lat, lon, z["lat"], z["lon"]))


def risk_label(score):
    if score >= 80:
        return "CRITICAL"
    if score >= 60:
        return "HIGH"
    if score >= 40:
        return "MODERATE"
    return "LOW"


def risk_emoji(score):
    if score >= 80:
        return "🔴"
    if score >= 60:
        return "🟠"
    if score >= 40:
        return "🟡"
    return "🟢"


def calculate_risk(rainfall, humidity, slope, history_factor=50):
    # Demo explainable scoring model. Replace with a trained ML model later.
    score = (
        0.40 * min(rainfall / 100, 1) * 100
        + 0.20 * min(humidity / 100, 1) * 100
        + 0.25 * min(slope / 45, 1) * 100
        + 0.15 * history_factor
    )
    return max(0, min(100, round(score)))


def send_telegram_message(text):
    try:
        token = st.secrets["TELEGRAM_BOT_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        r = requests.post(url, data={"chat_id": chat_id, "text": text}, timeout=8)
        return r.ok
    except Exception:
        return False


def browser_notification(title, body):
    safe_title = json.dumps(title)
    safe_body = json.dumps(body)
    components.html(
        f"""
        <script>
        try {{
            if ("Notification" in window) {{
                if (Notification.permission === "default") Notification.requestPermission();
                if (Notification.permission === "granted") {{
                    new Notification({safe_title}, {{body: {safe_body}}});
                }}
            }}
        }} catch(e) {{}}
        </script>
        """,
        height=0,
    )


def fetch_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,precipitation,rain,weather_code"
        "&hourly=precipitation,rain"
        "&forecast_days=1"
        "&timezone=auto"
    )
    r = requests.get(url, timeout=8)
    r.raise_for_status()
    return r.json()


def chatbot_answer(question, lat=None, lon=None):
    q = question.lower().strip()

    if any(x in q for x in ["emergency", "trapped", "landslide happening", "help me", "stuck"]):
        return (
            "🚨 ACTIVE EMERGENCY: Move away from the landslide path and unstable slopes. "
            "Do not cross a moving slope or blocked road. Call local emergency services "
            "and alert the nearest authority immediately."
        )

    if "risk" in q or "danger" in q:
        if lat is not None and lon is not None:
            z = nearest_zone(lat, lon)
            d = haversine_km(lat, lon, z["lat"], z["lon"])
            return f"{risk_emoji(z['risk'])} Nearest monitored zone: {z['name']} ({z['state']}). Demo risk: {z['risk']}/100 ({risk_label(z['risk'])}), about {d:.1f} km away."
        return "Share your location to calculate the nearest monitored risk zone."

    if "report" in q or "complaint" in q:
        return "Use 🆘 Report Incident in the sidebar. Your GPS position, timestamp, severity and description can be attached to the report."

    if "shelter" in q or "safe zone" in q:
        return "For this prototype, safe-zone data is represented on the map. In the production version, connect verified district shelter/safe-zone records and calculate the nearest facility from GPS."

    if "road" in q:
        return "Road status should be verified from the latest authority/field reports. BhuRakshak avoids claiming a road is safe when current data is unavailable."

    if "what should i do" in q or "what to do" in q or "safety" in q:
        return "Stay away from steep unstable slopes, cracks, falling rocks and flowing debris. If evacuation is advised, move to a designated safe area using an approved route."

    return "I can help with risk level, emergency guidance, reporting an incident, nearby monitored zones and safety steps. Try: 'What is my risk?' or 'How do I report a landslide?'"


# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {font-size: 2.5rem; font-weight: 800; margin-bottom: 0;}
    .subtitle {color:#667085; font-size:1rem;}
    .risk-card {padding:18px; border-radius:16px; border:1px solid #e5e7eb; background:#fff;}
    .alert-card {padding:16px; border-radius:14px; border-left:6px solid #ef4444; background:#fff5f5;}
    .small {font-size:.85rem; color:#667085;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">🛡️ BhuRakshak</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Based Landslide Early Warning & Risk Monitoring Platform — North Eastern Region</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Open",
        [
            "🏠 Live Dashboard",
            "🗺️ Risk Map",
            "🆘 Report Incident",
            "🚨 Alerts",
            "👮 Authority Console",
            "🤖 Ask BhuRakshak",
            "📊 Analytics",
            "🧭 Safety Guide",
        ],
    )

    st.divider()
    st.subheader("User mode")
    st.session_state.role = st.selectbox(
        "Role",
        ["Citizen", "Field Officer", "District Admin"],
        index=["Citizen", "Field Officer", "District Admin"].index(st.session_state.role),
    )

    st.divider()
    st.caption("Live location is requested only after you choose the location button.")


# -----------------------------
# LOCATION
# -----------------------------
location_data = streamlit_geolocation()

if location_data and location_data.get("latitude") is not None:
    st.session_state.location = {
        "lat": float(location_data["latitude"]),
        "lon": float(location_data["longitude"]),
        "accuracy": location_data.get("accuracy"),
    }

# -----------------------------
# LIVE DASHBOARD
# -----------------------------
if page == "🏠 Live Dashboard":
    st.subheader("Live situation overview")

    c1, c2, c3, c4 = st.columns(4)

    reports = load_reports()
    active_reports = [r for r in reports if r.get("status") != "Resolved"]

    c1.metric("🔴 Critical Zones", sum(z["risk"] >= 80 for z in DEMO_ZONES))
    c2.metric("🟠 High Risk Zones", sum(z["risk"] >= 60 for z in DEMO_ZONES))
    c3.metric("🚨 Active Reports", len(active_reports))
    c4.metric("📡 System", "LIVE" if supabase_configured() else "DEMO LIVE")

    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📍 My Location")
        if st.session_state.location:
            loc = st.session_state.location
            st.success("GPS location received")
            st.write(f"Latitude: `{loc['lat']:.5f}`")
            st.write(f"Longitude: `{loc['lon']:.5f}`")
            if loc.get("accuracy"):
                st.write(f"Accuracy: `{loc['accuracy']:.0f} m`")

            z = nearest_zone(loc["lat"], loc["lon"])
            distance = haversine_km(loc["lat"], loc["lon"], z["lat"], z["lon"])
            st.markdown(
                f"### {risk_emoji(z['risk'])} {risk_label(z['risk'])}"
            )
            st.write(f"Nearest monitored zone: **{z['name']}**")
            st.write(f"Distance: **{distance:.1f} km**")
            st.progress(z["risk"] / 100)
            st.caption(f"Demo risk score: {z['risk']}/100")
        else:
            st.info("Tap the button below and allow GPS access.")
            st.button("📍 Get My Live Location", type="primary")

    with col2:
        st.subheader("🗺️ Live Risk Snapshot")
        m = folium.Map(location=NER_CENTER, zoom_start=5, control_scale=True)
        for z in DEMO_ZONES:
            color = "red" if z["risk"] >= 80 else "orange" if z["risk"] >= 60 else "beige" if z["risk"] >= 40 else "green"
            folium.CircleMarker(
                [z["lat"], z["lon"]],
                radius=12,
                color=color,
                fill=True,
                fill_opacity=0.65,
                popup=f"{z['name']} — {risk_label(z['risk'])} ({z['risk']}/100)",
            ).add_to(m)

        if st.session_state.location:
            loc = st.session_state.location
            folium.Marker(
                [loc["lat"], loc["lon"]],
                tooltip="📍 Your current location",
                icon=folium.Icon(color="blue", icon="user"),
            ).add_to(m)

        st_folium(m, height=430, use_container_width=True)

    st.divider()
    st.subheader("🚨 Latest incidents")
    if reports:
        for r in reports[:5]:
            score = int(r.get("risk_score", 0))
            st.markdown(
                f"**{risk_emoji(score)} {r.get('incident_type','Incident')}** — "
                f"{r.get('severity','Medium')} — {r.get('status','Reported')} — "
                f"`{r.get('created_at','')}`"
            )
    else:
        st.info("No incidents reported yet.")


# -----------------------------
# RISK MAP
# -----------------------------
elif page == "🗺️ Risk Map":
    st.subheader("🗺️ GIS Risk Map")
    st.caption("Demo risk zones can later be replaced by live PostGIS/official GIS layers.")

    m = folium.Map(location=NER_CENTER, zoom_start=5, control_scale=True)

    for z in DEMO_ZONES:
        color = "red" if z["risk"] >= 80 else "orange" if z["risk"] >= 60 else "beige" if z["risk"] >= 40 else "green"
        folium.Circle(
            [z["lat"], z["lon"]],
            radius=30000,
            color=color,
            fill=True,
            fill_opacity=0.15,
        ).add_to(m)
        folium.Marker(
            [z["lat"], z["lon"]],
            popup=(
                f"<b>{z['name']}</b><br>"
                f"State: {z['state']}<br>"
                f"Risk: {z['risk']}/100<br>"
                f"Rainfall: {z['rain']} mm<br>"
                f"Slope: {z['slope']}°"
            ),
        ).add_to(m)

    reports = load_reports()
    for r in reports:
        try:
            lat = float(r["latitude"])
            lon = float(r["longitude"])
            score = int(r.get("risk_score", 50))
            folium.Marker(
                [lat, lon],
                tooltip=f"🚨 Report #{r.get('id','')}",
                popup=(
                    f"<b>{r.get('incident_type','Incident')}</b><br>"
                    f"Severity: {r.get('severity','Medium')}<br>"
                    f"Risk: {score}/100<br>"
                    f"Status: {r.get('status','Reported')}"
                ),
                icon=folium.Icon(color="red" if score >= 60 else "orange", icon="warning-sign"),
            ).add_to(m)
        except Exception:
            pass

    if st.session_state.location:
        folium.Marker(
            [st.session_state.location["lat"], st.session_state.location["lon"]],
            tooltip="📍 Live user location",
            icon=folium.Icon(color="blue", icon="user"),
        ).add_to(m)

    st_folium(m, height=620, use_container_width=True)


# -----------------------------
# REPORT INCIDENT
# -----------------------------
elif page == "🆘 Report Incident":
    st.subheader("🆘 Report a Landslide / Hazard")
    st.write("GPS, timestamp and report details are attached automatically.")

    if not st.session_state.location:
        st.warning("Please get your GPS location first.")
        streamlit_geolocation()
    else:
        loc = st.session_state.location
        st.success(f"Location locked: {loc['lat']:.5f}, {loc['lon']:.5f}")

        with st.form("incident_form"):
            incident_type = st.selectbox(
                "Problem type",
                ["Landslide", "Road blocked", "Slope crack", "Rockfall", "Flooding", "Other"],
            )
            severity = st.select_slider(
                "Severity",
                options=["Low", "Medium", "High", "Critical"],
                value="High",
            )
            description = st.text_area(
                "Describe the problem",
                placeholder="Example: Soil and rocks have fallen onto the road...",
            )
            photo = st.file_uploader(
                "📸 Upload photo (optional)",
                type=["jpg", "jpeg", "png", "webp"],
            )
            submit = st.form_submit_button("🚨 SUBMIT INCIDENT", type="primary")

        if submit:
            if not description.strip():
                st.error("Please add a short description.")
            else:
                severity_score = {"Low": 25, "Medium": 50, "High": 75, "Critical": 95}[severity]

                report = {
                    "id": "BR-" + uuid.uuid4().hex[:8].upper(),
                    "incident_type": incident_type,
                    "severity": severity,
                    "description": description.strip(),
                    "latitude": loc["lat"],
                    "longitude": loc["lon"],
                    "accuracy": loc.get("accuracy"),
                    "risk_score": severity_score,
                    "status": "Reported",
                    "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "photo_name": photo.name if photo else "",
                }

                save_report(report)

                telegram_text = (
                    f"🚨 NEW BHURAKSHAK INCIDENT\n"
                    f"ID: {report['id']}\n"
                    f"Type: {incident_type}\n"
                    f"Severity: {severity}\n"
                    f"Risk: {severity_score}/100\n"
                    f"Location: {loc['lat']:.5f}, {loc['lon']:.5f}\n"
                    f"Description: {description}"
                )
                telegram_sent = send_telegram_message(telegram_text)

                browser_notification(
                    "BhuRakshak — New Incident",
                    f"{incident_type} reported at {loc['lat']:.4f}, {loc['lon']:.4f}",
                )

                st.success(f"✅ Incident {report['id']} submitted successfully.")
                st.info("Authority dashboard has received the report." + (" Telegram alert sent." if telegram_sent else ""))


# -----------------------------
# ALERTS
# -----------------------------
elif page == "🚨 Alerts":
    st.subheader("🚨 Alerts & Advisories")

    reports = load_reports()
    critical = [r for r in reports if int(r.get("risk_score", 0)) >= 80 and r.get("status") != "Resolved"]

    if critical:
        for r in critical:
            st.markdown(
                f"""
                <div class="alert-card">
                <b>🔴 EMERGENCY / CRITICAL REPORT</b><br>
                <b>{r.get('incident_type','Incident')}</b> — {r.get('description','')}<br>
                Location: {r.get('latitude')}, {r.get('longitude')}<br>
                Report ID: {r.get('id')}<br>
                Status: {r.get('status')}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.success("No active critical citizen reports.")

    st.divider()
    st.subheader("⚠️ Regional risk advisories")

    for z in sorted(DEMO_ZONES, key=lambda x: x["risk"], reverse=True):
        if z["risk"] >= 60:
            st.warning(
                f"{risk_emoji(z['risk'])} **{risk_label(z['risk'])} — {z['name']} ({z['state']})** | "
                f"Risk {z['risk']}/100 | Rainfall indicator {z['rain']} mm | Slope {z['slope']}°"
            )


# -----------------------------
# AUTHORITY CONSOLE
# -----------------------------
elif page == "👮 Authority Console":
    st.subheader("👮 District Authority Command Console")

    reports = load_reports()

    if not reports:
        st.info("No citizen reports have arrived yet. Submit one from Report Incident.")
    else:
        st.metric("Incoming / Active Reports", len([r for r in reports if r.get("status") != "Resolved"]))

        for r in reports:
            score = int(r.get("risk_score", 0))
            with st.container(border=True):
                a, b = st.columns([3, 1])
                with a:
                    st.markdown(
                        f"### {risk_emoji(score)} {r.get('incident_type','Incident')} — {r.get('id')}"
                    )
                    st.write(r.get("description", ""))
                    st.write(
                        f"📍 `{r.get('latitude')}, {r.get('longitude')}`  | "
                        f"Severity: **{r.get('severity')}**  | "
                        f"Risk: **{score}/100**"
                    )
                    st.caption(f"Reported: {r.get('created_at','')}")

                with b:
                    status_options = ["Reported", "Verified", "Response Team Dispatched", "Resolved"]
                    current = r.get("status", "Reported")
                    new_status = st.selectbox(
                        "Status",
                        status_options,
                        index=status_options.index(current) if current in status_options else 0,
                        key=f"status_{r.get('id')}",
                    )
                    if st.button("Update", key=f"update_{r.get('id')}"):
                        update_report_status(r.get("id"), new_status)
                        st.success("Updated")
                        st.rerun()


# -----------------------------
# CHATBOT
# -----------------------------
elif page == "🤖 Ask BhuRakshak":
    st.subheader("🤖 Ask BhuRakshak AI")
    st.caption("Safety-focused assistant. Location-based answers use your current GPS when available.")

    if st.session_state.location:
        st.success("📍 Location available to the assistant.")
    else:
        st.info("Share your location on the dashboard for location-based answers.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask: What is my current risk? / What should I do during a landslide?")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        loc = st.session_state.location or {}
        answer = chatbot_answer(prompt, loc.get("lat"), loc.get("lon"))
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()


# -----------------------------
# ANALYTICS
# -----------------------------
elif page == "📊 Analytics":
    st.subheader("📊 Risk & Incident Analytics")

    reports = load_reports()

    if reports:
        df = pd.DataFrame(reports)
        st.dataframe(
            df[
                [c for c in [
                    "id", "incident_type", "severity", "risk_score",
                    "status", "latitude", "longitude", "created_at"
                ] if c in df.columns]
            ],
            use_container_width=True,
            hide_index=True,
        )

        if "risk_score" in df.columns:
            chart = df[["id", "risk_score"]].copy()
            chart["risk_score"] = pd.to_numeric(chart["risk_score"], errors="coerce")
            st.bar_chart(chart.set_index("id"))
    else:
        st.info("Incident analytics will appear after reports are submitted.")

    st.divider()
    st.subheader("Regional risk ranking")
    zdf = pd.DataFrame(DEMO_ZONES)[["name", "state", "risk", "rain", "slope"]].sort_values("risk", ascending=False)
    st.dataframe(zdf, use_container_width=True, hide_index=True)


# -----------------------------
# SAFETY
# -----------------------------
elif page == "🧭 Safety Guide":
    st.subheader("🧭 Landslide Safety & Preparedness")

    tabs = st.tabs(["Before", "During", "After", "Emergency"])

    with tabs[0]:
        st.markdown(
            """
            - Watch for new cracks in ground/walls and unusual sounds.
            - Follow official weather and evacuation advisories.
            - Keep emergency documents, medicines, water and a torch ready.
            - Know the designated safe area and evacuation route.
            """
        )

    with tabs[1]:
        st.markdown(
            """
            - Move away from the landslide path and unstable slopes.
            - Do not cross flowing debris or newly blocked roads.
            - Follow instructions from local authorities.
            - If indoors and evacuation is not yet possible, move to the safest available part of the building away from slope-facing walls/windows.
            """
        )

    with tabs[2]:
        st.markdown(
            """
            - Avoid returning until authorities declare the area safe.
            - Watch for secondary landslides and unstable ground.
            - Report fresh cracks, slope movement, damaged roads or bridges.
            """
        )

    with tabs[3]:
        st.error("If there is immediate danger, contact local emergency services and the responsible district authorities. Do not rely only on this prototype for emergency decisions.")


# -----------------------------
# FOOTER / AUTO REFRESH HINT
# -----------------------------
st.divider()
st.caption(
    f"BhuRakshak • Prototype • Last page refresh: {datetime.now().strftime('%H:%M:%S')} • "
    + ("Cloud sync enabled" if supabase_configured() else "Local demo storage — configure Supabase for multi-user persistence")
)
