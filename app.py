import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูต้อม", layout="wide")

st.title("🚀 คลังข้อสอบฟิสิกส์ (แบบมีรูปประกอบ)")
st.write("เลือกหัวข้อที่ต้องการทบทวนได้เลยครับ")

# 1. ดึงข้อมูลจาก GitHub
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    df = pd.read_csv(url)
    # ล้างช่องว่างในชื่อคอลัมน์ (ถ้ามี)
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

    # 2. ส่วนตัวกรอง (Filter)
    topics = ["ทั้งหมด"] + sorted(df['topic'].unique().tolist())
    selected_topic = st.sidebar.selectbox("เลือกบทเรียน", topics)

    if selected_topic != "ทั้งหมด":
        display_df = df[df['topic'] == selected_topic]
    else:
        display_df = df

    # 3. การแสดงผลข้อสอบ
    for index, row in display_df.iterrows():
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader(f"📌 รหัส: {row['id']} ({row['exam']})")
                st.info(f"**โจทย์:** {row['text']}")
                st.write(f"**ตัวเลือก:** {row['choices']}")
            
            with col2:
                # ดึงลิงก์จากคอลัมน์ image_url
                image_link = row.get('image_url')
                
                # ตรวจสอบเงื่อนไขการแสดงรูป
                if isinstance(image_link, str) and "http" in image_link and len(image_link) > 50:
                    st.image(image_link, caption=f"รูปประกอบข้อ {row['id']}", use_container_width=True)
                else:
                    st.write("⚪ *ข้อนี้ไม่มีรูปประกอบ*")
            
            st.divider()

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
    st.info("คำแนะนำ: ตรวจสอบว่าชื่อไฟล์ใน GitHub ตรงกับในโค้ด (physics_data.csv) หรือไม่")
