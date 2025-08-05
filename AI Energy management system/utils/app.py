import streamlit as st
import pandas as pd
import plotly.express as px
import os#cCheck if file exists, create folders, get file paths.
import sys#Dynamically add directories to Python path (especially useful for custom module imports).

# Add current directory to sys.path
sys.path.append(os.path.dirname(__file__))

# Custom modules
from login import show_login
from forecast_model import forecast_energy
from inefficiency_detector import detect_inefficiencies
from recommendation_engine import generate_recommendations
from utils.report_generator import generate_energy_report

# ✅ Set page config once
st.set_page_config(page_title="AI Energy Management", layout="wide")

# Session defaults
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user"] = None

# Login screen
if not st.session_state["logged_in"]:
    show_login()
    st.stop()

# User info
USER = st.session_state["user"]["name"]
USER_ID = st.session_state["user"]["username"]
USER_DIR = f"data/user_data/{USER_ID}"
os.makedirs(USER_DIR, exist_ok=True)

# Sidebar
st.sidebar.title(f"Welcome, {USER} 👋")
st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False, "user": None}))

# Title
st.title("⚡ AI-Powered Energy Management Platform")

# File upload
uploaded_file = st.file_uploader("Upload your energy dataset (CSV)", type=["csv"])

if uploaded_file:
    user_file_path = f"{USER_DIR}/uploaded.csv"
    with open(user_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    df = pd.read_csv(user_file_path)
    # Inspect columns
    st.write("Uploaded Data Columns:", df.columns.tolist())

# Ensure datetime parsing
    if 'datetime' in df.columns:
       df['datetime'] = pd.to_datetime(df['datetime'])
       df['date'] = df['datetime'].dt.date
       df['hour'] = df['datetime'].dt.hour
    else:
       st.error("❌ Your CSV must contain a 'datetime' column.")
       st.stop()

    # ✅ Define tabs BEFORE using them
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "💸 Estimator", "⚠️ Alerts", "💡 Recommendations"])

    # 📊 TAB 1: DASHBOARD
    with tab1:
        st.subheader("📄 Data Preview")
        st.dataframe(df.head())

        st.subheader("📈 Daily Energy Usage")
        st.write(df.columns)
        print(df.columns)

        daily = df.groupby('date')['total_energy'].sum().reset_index()
        fig1 = px.line(daily, x='date', y='total_energy', title="Daily Energy Usage")
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("🕒 Hourly Energy Usage")
        hourly = df.groupby('hour')['total_energy'].mean().reset_index()
        fig2 = px.bar(hourly, x='hour', y='total_energy', title="Average Hourly Usage")
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("🔮 Weekly Usage Forecast")
        forecast = forecast_energy(df)
        st.line_chart(forecast, use_container_width=True)

    # 💸 TAB 2: BILL ESTIMATOR + PDF REPORT
    with tab2:
        st.subheader("Energy Bill Estimator")
        unit_rate = st.number_input("Enter cost per kWh (₹)", value=7.0)
        total_kWh = df['total_energy'].sum() / 1000
        estimated_bill = total_kWh * unit_rate

        st.metric("Total Consumption (kWh)", f"{total_kWh:.2f}")
        st.metric("Estimated Bill (₹)", f"{estimated_bill:.2f}")

        if st.button("📄 Generate PDF Report"):
            generate_energy_report(df, estimated_bill)
            with open("energy_report.pdf", "rb") as f:
                st.download_button("📥 Download Report", f, file_name="energy_summary.pdf")

    # ⚠️ TAB 3: ALERT SYSTEM
    with tab3:
        st.subheader("Unusual Consumption Alerts")
        threshold = st.slider("High Usage Threshold (Wh)", min_value=100, max_value=int(df['total_energy'].max()), value=500)
        high_usage = df[df['total_energy'] > threshold]
        st.warning(f"{len(high_usage)} high-usage records found")
        st.dataframe(high_usage[['datetime', 'total_energy']])
        
        ineffs = detect_inefficiencies(df)
        for i in ineffs:
            st.error(f"Inefficiency Detected: {i}")

    # 💡 TAB 4: SMART RECOMMENDATIONS
    with tab4:
        st.subheader("Smart Energy-Saving Recommendations")
        tips = generate_recommendations(df)
        for tip in tips:
            st.success(tip)

# ✅ If user has previously uploaded a file
elif os.path.exists(f"{USER_DIR}/uploaded.csv"):
    st.sidebar.success("📂 Last uploaded file loaded.")
