import streamlit as st
import time, threading, datetime, requests, folium
from streamlit_folium import st_folium
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ====== APP CONFIG =======
st.set_page_config(page_title="CyberSentinel", layout="wide")

# ====== DATABASE SETUP =======
engine = create_engine('sqlite:///cybersentinel.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class LogHistory(Base):
    __tablename__ = 'log_history'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    log_line = Column(String)

class IPHistory(Base):
    __tablename__ = 'ip_history'
    id = Column(Integer, primary_key=True)
    ip = Column(String)
    city = Column(String)
    region = Column(String)
    country = Column(String)
    org = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ====== AI Setup =======
TOGETHER_API_KEY = "f09eb9d2bd068fbbe9fc3043bbb9f35ddb1c0303e9eb9766d3adf5332be94a54"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

def get_together_explanation(threat_description):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You are a cybersecurity assistant. Explain threats clearly and concisely."},
            {"role": "user", "content": f"Explain the following cybersecurity threat:\n{threat_description}"}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# ====== Real-Time Log Monitor =======
def tail_f(file_path, stop_event, log_buffer):
    try:
        with open(file_path, "r") as f:
            f.seek(0, 2)
            while not stop_event.is_set():
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                clean_line = line.strip()
                log_buffer.append(clean_line)
                session.add(LogHistory(log_line=clean_line))
                session.commit()
    except FileNotFoundError:
        log_buffer.append(f"File not found: {file_path}")
        stop_event.set()

# ====== Main Streamlit App =======
def main():
    st.title("🛡️ CyberSentinel — AI Cybersecurity Toolkit")
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Dashboard", "Threat Detector", "Live Monitor", "Threat Classifier", "IP Tracker"
    ])

    # Dashboard
    with tab1:
        st.header("📊 Dashboard")
        st.success("Real-time Monitoring, AI Threat Analysis, and IP Intelligence — all in one toolkit!")

    # Threat Detector
    with tab2:
        st.header("🧠 Threat Detector (AI-Powered)")
        user_input = st.text_input("Enter suspicious IP, file hash, or threat description:")
        if st.button("Analyze Threat"):
            if user_input:
                explanation = get_together_explanation(user_input)
                st.markdown(f"### 🔍 AI Explanation:\n\n{explanation}")
            else:
                st.warning("Please enter something to analyze.")

    # Log Monitor
    with tab3:
        st.header("📡 Real-Time Log Monitor")
        log_file = st.text_input("Enter log file path", "/var/log/syslog")
        if 'logs' not in st.session_state:
            st.session_state.logs = []
        if 'stop_event' not in st.session_state:
            st.session_state.stop_event = threading.Event()
        if 'thread' not in st.session_state:
            st.session_state.thread = None

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Monitoring"):
                if log_file:
                    if st.session_state.thread is None or not st.session_state.thread.is_alive():
                        st.session_state.stop_event.clear()
                        st.session_state.logs = []
                        st.session_state.thread = threading.Thread(
                            target=tail_f,
                            args=(log_file, st.session_state.stop_event, st.session_state.logs),
                            daemon=True
                        )
                        st.session_state.thread.start()
                        st.success("Started monitoring log file.")
        with col2:
            if st.button("Stop Monitoring"):
                if st.session_state.thread and st.session_state.thread.is_alive():
                    st.session_state.stop_event.set()
                    st.session_state.thread = None
                    st.success("Stopped monitoring.")
        st.subheader("Latest Log Entries")
        st.text("\n".join(st.session_state.logs[-20:]))

    # Threat Classifier
    with tab4:
        st.header("⚠️ Threat Classifier")
        sample_threat = st.text_area("Paste suspicious log or behavior for classification:")
        if st.button("Classify Threat"):
            if sample_threat:
                classification = get_together_explanation(f"Classify this threat: {sample_threat}")
                st.markdown(f"### 🧠 Classification:\n{classification}")

    # IP Tracker with Visualization + Local DB
    with tab5:
        st.header("🌐 IP Tracker with Geo Visualization")
        if "ip_data" not in st.session_state:
            st.session_state.ip_data = None  # Store IP lookup result persistently

        ip_input = st.text_input("Enter IP address to track:")

        if st.button("Lookup IP"):
            if ip_input:
                try:
                    response = requests.get(f"https://ipinfo.io/{ip_input}/json")
                    data = response.json()
                    if "bogon" in data:
                        st.warning("Bogon IP address (private/internal). No info available.")
                        st.session_state.ip_data = None
                    else:
                        st.session_state.ip_data = data
                        session.add(IPHistory(
                            ip=data.get("ip", "N/A"),
                            city=data.get("city", "N/A"),
                            region=data.get("region", "N/A"),
                            country=data.get("country", "N/A"),
                            org=data.get("org", "N/A"),
                        ))
                        session.commit()
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.session_state.ip_data = None
            else:
                st.warning("Please enter a valid IP.")
                st.session_state.ip_data = None

        # Render IP info and map if data exists
        if st.session_state.ip_data:
            data = st.session_state.ip_data
            ip = data.get("ip", "N/A")
            city = data.get("city", "N/A")
            region = data.get("region", "N/A")
            country = data.get("country", "N/A")
            org = data.get("org", "N/A")
            loc = data.get("loc", "")

            st.write(f"**IP**: {ip}")
            st.write(f"**City**: {city}")
            st.write(f"**Region**: {region}")
            st.write(f"**Country**: {country}")
            st.write(f"**Organization**: {org}")

            if loc:
                lat, lon = map(float, loc.split(','))
                m = folium.Map(location=[lat, lon], zoom_start=10)
                folium.Marker([lat, lon], tooltip=f"{ip} - {city}").add_to(m)
                st_folium(m, width=700, height=500)
        else:
            st.info("Lookup an IP address to see location and info.")

        with st.expander("📁 View IP Lookup History"):
            history = session.query(IPHistory).order_by(IPHistory.timestamp.desc()).limit(10).all()
            for item in history:
                st.write(f"{item.timestamp} | {item.ip} - {item.city}, {item.region}, {item.country} | {item.org}")

if __name__ == "__main__":
    main()
