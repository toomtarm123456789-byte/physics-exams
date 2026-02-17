import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บให้ดูทันสมัย
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูต้อม", layout="wide")
st.title("🚀 คลังข้อสอบฟิสิกส์ (ระบบอัตโนมัติ)")

# 2. ฟังก์ชันโหลดข้อมูลและทำความสะอาด (Clean Data)
@st.cache_data(ttl=60) # ตั้งค่าให้รีเฟรชข้อมูลทุก 1 นาที
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        df = pd.read_csv(url)
        # ล้างช่องว่างหัวตาราง
        df.columns = df.columns.str.strip()
        # แปลงเลข 0 หรือช่องว่างใน image_url ให้เป็นค่าว่างจริงๆ
        df['image_url'] = df['image_url'].astype(str).replace(['0', '0.0', 'nan', 'None'], '')
        return df
    except Exception as e:
        st.error(f"โหลดข้อมูลไม่ได้: {e}")
        return None

df = load_data()

if df is not None:
    # ส่วน Sidebar สำหรับกรองบทเรียน
    topic_list = ["ทั้งหมด"] + sorted(df['topic'].dropna().unique().tolist())
    selected_topic = st.sidebar.selectbox("เลือกบทเรียน", topic_list)
    
    filtered_df = df if selected_topic == "ทั้งหมด" else df[df['topic'] == selected_topic]

    # 3. ส่วนแสดงผลข้อสอบ
    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(f"📌 รหัส: {row.get('id', 'N/A')}")
                st.info(f"**โจทย์:** {row.get('text', '-')}")
                st.write(f"**ตัวเลือก:** {row.get('choices', '-')}")
            
            with col2:
                img_link = str(row.get('image_url', '')).strip()
                
                # เงื่อนไขสำคัญ: ต้องมีลิงก์ และมีรหัสไฟล์ต่อท้าย (ยาวกว่า 60 ตัวอักษร)
                if "http" in img_link and len(img_link) > 60:
                    st.image(img_link, use_container_width=True)
                else:
                    st.warning("⚪ ไม่มีรูปประกอบ")
            st.divider()
