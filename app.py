import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูเที่ยง", layout="wide")

st.title("🚀 คลังข้อสอบฟิสิกส์ ครูเที่ยง")

# ฟังก์ชัน "จอมซ่อม" (ช่วยเปลี่ยนข้อความธรรมดาให้เป็น LaTeX)
def super_clean_latex(text):
    if pd.isna(text): return ""
    text = str(text)
    
    # 1. จัดการตัวห้อยและตัวยกที่พบบ่อย (mO -> m_O, mHe -> m_{He})
    text = text.replace("mO", "m_{O}").replace("mHe", "m_{He}")
    text = re.sub(r'([a-zA-Z])(\d)', r'\1_{\2}', text) # เปลี่ยนอักษรตามด้วยเลขให้เป็นตัวห้อย เช่น v1 -> v_{1}
    
    # 2. จัดการเศษส่วนเบื้องต้น (ถ้ามีเครื่องหมาย / ให้พยายามจัดรูป)
    if "/" in text and "=" in text and "$" not in text:
        parts = text.split("=")
        if len(parts) == 2:
            left = parts[0].strip()
            right = parts[1].strip()
            if "/" in right:
                num_den = right.split("/")
                text = f"{left} = \\frac{{{num_den[0]}}}{{{num_den[1]}}}"

    # 3. ถ้าเป็นสูตรแต่ไม่มี $ ครอบ ให้ใส่ให้เลย
    if any(c in text for c in ['=', '\\', '_', '^', '/']):
        if "$" not in text:
            text = f"$ {text} $"
            
    return text

@st.cache_data(ttl=1)
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"โหลดไฟล์ไม่สำเร็จ: {e}")
        return None

df = load_data()

if df is not None:
    # --- ส่วนการแสดงผล (ใช้ฟังก์ชันซ่อมข้อความ) ---
    for _, row in df.iterrows():
        with st.container():
            col1, col2 = st.columns([1.6, 1])
            with col1:
                st.subheader(f"📌 {row.iloc[0]}")
                st.markdown("**โจทย์:**")
                # ใช้ฟังก์ชันซ่อมข้อความก่อนแสดงผล
                st.markdown(super_clean_latex(row.iloc[2])) 
                
                st.markdown("**ตัวเลือก:**")
                st.markdown(super_clean_latex(row.iloc[3]))
            # ... (ส่วนรูปภาพด้านขวาเหมือนเดิม) ...
            st.divider()
