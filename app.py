import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูต้อม", layout="wide")

st.title("🚀 คลังข้อสอบฟิสิกส์ (ฉบับสมบูรณ์)")

@st.cache_data
def load_data():
    # ดึงไฟล์โดยตรงจาก GitHub
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        df = pd.read_csv(url)
        # ล้างช่องว่างที่หัวคอลัมน์
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"โหลดข้อมูลไม่ได้: {e}")
        return None

df = load_data()

if df is not None:
    # ส่วนกรองข้อมูล (Topic)
    topic_col = 'topic' if 'topic' in df.columns else df.columns[0]
    df[topic_col] = df[topic_col].fillna("ทั่วไป").astype(str)
    topics = ["ทั้งหมด"] + sorted(df[topic_col].unique().tolist())
    selected = st.sidebar.selectbox("เลือกบทเรียน", topics)

    filtered_df = df if selected == "ทั้งหมด" else df[df[topic_col] == selected]

    # วนลูปแสดงข้อสอบ
    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(f"📌 รหัส: {row.get('id', 'N/A')}")
                st.info(f"**โจทย์:** {row.get('text', '-')}")
                st.write(f"**ตัวเลือก:** {row.get('choices', '-')}")
            
            with col2:
                # บังคับดึงจากคอลัมน์ image_url เท่านั้น
                link = str(row.get('image_url', ''))
                
                # เช็คว่ามีลิงก์และต้องมีรหัส ID ต่อท้าย (ความยาว > 40 ตัวอักษร)
                if "http" in link and len(link) > 40:
                    st.image(link.strip(), use_container_width=True)
                else:
                    st.warning("⚪ ข้อนี้ไม่มีรูปประกอบ")
            st.divider()
