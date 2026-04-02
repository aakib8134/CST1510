import streamlit as st
import pandas as pd
from app_model.cyber_incident import get_all_cyber_incidents
from app_model.db import check_connection

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)
conn = check_connection()
data = get_all_cyber_incidents(conn)


st.title("Welcome to Home Page")
with st.sidebar:
    st.header("Navigation")
    severity_level = st.selectbox("severity Level", data["severity"].unique())

data["timestamp"] = pd.to_datetime(data["timestamp"])
filtered_data = data[data["severity"] == severity_level]

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Cyber Incidents with severity level: {severity_level}")
    st.bar_chart(filtered_data["category"].value_counts())

with col2:
    st.subheader("Trend of Incidents Over Time")
    st.line_chart(filtered_data, x="timestamp", y="category")

st.subheader("Filtered Data")
st.dataframe(filtered_data)
