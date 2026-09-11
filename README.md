# BhuRakshak — Live Streamlit Prototype

This version adds:
- GPS location capture
- Interactive NER risk map
- Citizen incident reporting
- Geo-tagged reports with timestamp
- Authority console
- Report status workflow
- Browser notification attempt
- Optional Telegram alerts
- Optional Supabase cloud persistence
- Weather API helper
- Explainable demo risk score
- Ask BhuRakshak safety chatbot
- Analytics
- Safety guide

## 1. GitHub files

Put these files in your repository:
- app.py
- requirements.txt

The main Streamlit file must be named `app.py` unless you change the Streamlit deployment command.

## 2. Streamlit deployment

On Streamlit Community Cloud:
- Select your GitHub repository
- Main file: `app.py`
- Deploy

## 3. IMPORTANT: live multi-user reports

Without Supabase, the app uses Streamlit session memory. That is useful for a demo but is NOT a real shared database.

For real cross-user reporting, create a free Supabase project and create this table:

```sql
create table reports (
  id text primary key,
  incident_type text,
  severity text,
  description text,
  latitude double precision,
  longitude double precision,
  accuracy double precision,
  risk_score integer,
  status text,
  created_at text,
  photo_name text
);
```

Then in Streamlit Cloud > Settings > Secrets, add:

```toml
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
```

Do NOT put these secrets in GitHub.

## 4. Optional Telegram notifications

Create a Telegram bot using BotFather, obtain the bot token and the target chat ID, then add:

```toml
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
```

When a citizen submits a report, the app attempts to send an immediate Telegram message.

## 5. What is actually live?

- Browser GPS: live when the user grants location permission.
- Weather helper: uses Open-Meteo when called; the current prototype keeps the dashboard lightweight.
- Reports: live across users only when Supabase is configured.
- Telegram: live when configured.
- Risk zones: DEMO data in this version. Replace with official/live GIS and sensor feeds before presenting it as real operational data.

## 6. SIH demo flow

1. Open Citizen mode.
2. Get My Live Location.
3. Show location and nearest risk zone.
4. Open Report Incident.
5. Submit a High/Critical landslide report.
6. Open Authority Console.
7. Show the incoming incident.
8. Change status: Reported -> Verified -> Response Team Dispatched -> Resolved.
9. Open Alerts and Analytics.
10. Ask BhuRakshak: "What should I do during a landslide?"

## 7. Production upgrades

For a production system, connect:
- official rainfall/weather feeds
- official landslide inventory
- DEM/slope layers
- verified shelter/safe-zone database
- field sensors
- trained ML model
- authenticated authority accounts
- proper push/SMS/WhatsApp infrastructure
- PostGIS spatial queries
- audit logs and security controls

Never present demo risk zones as official real-time predictions.
