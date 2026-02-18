import streamlit as st
import pandas as pd

st.set_page_config(page_title="คลังข้อสอบฟิสิกส์", layout="wide")

# ดึงข้อมูลจาก GitHub
@st.cache_data(ttl=60) # ให้โหลดใหม่ทุก 60 วินาที
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

if df is not None:
    for _, row in df.iterrows():
        # แสดงโจทย์ (คอลัมน์ Index 2)
        # ถ้าใน Sheet มี $...$ อยู่แล้ว st.write จะเปลี่ยนเป็น LaTeX ให้เอง
        st.write(f"### 📌 รหัส: {row.iloc[0]}")
        st.write("**โจทย์:**")
        st.write(row.iloc[2]) 
        
        st.write("**ตัวเลือก:**")
        st.write(row.iloc[3])
        
        st.divider()
