import streamlit as st
import pandas as pd
import re

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูเที่ยง", layout="wide")

# แก้ไขจุดที่ทำให้เกิด Error สีแดง (เปลี่ยน index เป็น html)
st.markdown("""
    <style>
    .stMarkdown { font-size: 1.2rem !important; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 คลังข้อสอบฟิสิกส์ ครูเที่ยง")

# 2. ฟังก์ชันโหลดข้อมูล
@st.cache_data(ttl=1)
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"ไม่สามารถโหลดไฟล์ได้: {e}")
        return None

# ฟังก์ชัน "จอมซ่อม" เปลี่ยนข้อความธรรมดาให้เป็น LaTeX สวยๆ
def fix_latex(text):
    if pd.isna(text): return ""
    text = str(text)
    
    # ถ้าเจอตัวห้อย/ตัวยกแบบพิมพ์ดิบ (เช่น u_{2}, m_1) แต่ไม่มี $ ให้ใส่ครอบให้
    if any(c in text for c in ['_', '^', '\\', '/', '=']):
        if "$" not in text:
            # ครอบ $ ให้ทั้งข้อความเพื่อให้เรนเดอร์สัญลักษณ์ฟิสิกส์ได้
            return f"${text}$"
    return text

df = load_data()

if df is not None:
    # --- Sidebar ---
    st.sidebar.header("🔍 ค้นหาข้อสอบ")
    # คอลัมน์ TopicCode อยู่ที่ Index 1
    topics = ["ทั้งหมด"] + sorted(df.iloc[:, 1].dropna().unique().tolist())
    selected_topic = st.sidebar.selectbox("เลือกบทเรียน:", topics)

    filtered_df = df if selected_topic == "ทั้งหมด" else df[df.iloc[:, 1] == selected_topic]
    st.write(f"📊 พบข้อสอบทั้งหมด {len(filtered_df)} ข้อ")
    st.divider()

    # 3. แสดงผลข้อสอบ
    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1.6, 1])
            
            with col1:
                # รหัส (A - Index 0) | บทเรียน (B - Index 1)
                st.subheader(f"📌 รหัส: {row.iloc[0]}")
                st.caption(f"บทเรียน: {row.iloc[1]}")
                
                # โจทย์ (C - Index 2)
                st.markdown("**โจทย์:**")
                st.markdown(fix_latex(row.iloc[2]))
                
                # ตัวเลือก (D - Index 3)
                st.markdown("**ตัวเลือก:**")
                st.markdown(fix_latex(row.iloc[3]))
                
                with st.expander("ดูเฉลย"):
                    # เฉลย (E - Index 4)
                    st.success(f"คำตอบคือ: {row.iloc[4]}")
            
            with col2:
                # รูปภาพ (I - Index 8)
                img_id = str(row.iloc[8]).strip()
                if img_id and img_id not in ["nan", "ไม่พบรูปภาพ", "ไม่มีรูป"]:
                    img_url = f"https://drive.google.com/thumbnail?authuser=0&sz=w1000&id={img_id}"
                    st.image(img_url, use_container_width=True)
                else:
                    st.info("⚪ ไม่มีรูปประกอบ")
            
            st.divider()
