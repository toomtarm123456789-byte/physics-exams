import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูต้อม", layout="wide")

st.title("🚀 คลังข้อสอบฟิสิกส์ (แบบมีรูปประกอบ)")
st.write("เลือกหัวข้อที่ต้องการทบทวนได้เลยครับ")

# 2. ฟังก์ชันโหลดข้อมูลจาก GitHub
@st.cache_data
def load_data():
    # ดึงไฟล์โดยตรงจาก GitHub (Raw URL)
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        df = pd.read_csv(url)
        # ล้างช่องว่างที่อาจติดมากับหัวตาราง
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"ไม่สามารถดึงไฟล์ CSV ได้: {e}")
        return None

df = load_data()

if df is not None:
    # 3. ส่วนตัวกรองบทเรียน (Sidebar)
    try:
        # กำจัดค่าว่างในคอลัมน์ topic ก่อนสร้างรายการ
        df['topic'] = df['topic'].fillna("ไม่ระบุหัวข้อ").astype(str)
        topic_list = ["ทั้งหมด"] + sorted(df['topic'].unique().tolist())
        selected_topic = st.sidebar.selectbox("เลือกบทเรียน (Topic):", topic_list)

        # กรองข้อมูลตามที่เลือก
        if selected_topic == "ทั้งหมด":
            filtered_df = df
        else:
            filtered_df = df[df['topic'] == selected_topic]

        st.write(f"📊 พบข้อสอบทั้งหมด {len(filtered_df)} ข้อ")
        st.divider()

        # 4. แสดงผลข้อสอบแต่ละข้อ
        for index, row in filtered_df.iterrows():
            with st.container():
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # แสดงรหัสข้อสอบและโจทย์
                    exam_id = str(row.get('id', 'N/A'))
                    st.subheader(f"📌 รหัส: {exam_id}")
                    st.info(f"**โจทย์:** {row.get('text', '-')}")
                    st.write(f"**ตัวเลือก:** {row.get('choices', '-')}")
                
                with col2:
                    # ดึงลิงก์รูปภาพ
                    image_link = row.get('image_url')
                    
                    # ตรวจสอบว่าลิงกยูปภาพใช้ได้หรือไม่ (ต้องเป็น string และมี http)
                    if isinstance(image_link, str) and "http" in image_link:
                        # ลองแสดงรูปภาพ
                        st.image(image_link, use_container_width=True)
                    else:
                        st.warning("❌ ไม่มีรูปประกอบ")
                
                st.divider()
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการแสดงผล: {e}")
else:
    st.info("กรุณาตรวจสอบว่าอัปโหลดไฟล์ physics_data.csv ขึ้น GitHub หรือยัง")
