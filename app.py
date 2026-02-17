import streamlit as st
import pandas as pd
import re

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูเที่ยง", layout="wide")
st.title("🚀 คลังข้อสอบฟิสิกส์ ครูเที่ยง (ฉบับล็อคคอลัมน์)")

# 2. ฟังก์ชันโหลดข้อมูล
@st.cache_data(ttl=1)
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        # อ่านไฟล์โดยไม่ใช้ชื่อหัวตาราง (header=0 เพื่อข้ามแถวแรกที่เป็นชื่อคอลัมน์ไป)
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"ไม่สามารถโหลดไฟล์ได้: {e}")
        return None

df = load_data()

if df is not None:
    # --- ส่วนการค้นหาด้านข้าง (ใช้คอลัมน์ B หรือ Index 1 สำหรับ Topic) ---
    st.sidebar.header("🔍 ค้นหาข้อสอบ")
    # คอลัมน์ B คือ Topic (Index 1)
    topic_list = ["ทั้งหมด"] + sorted(df.iloc[:, 1].dropna().unique().tolist())
    selected_topic = st.sidebar.selectbox("เลือกบทเรียน:", topic_list)
    
    # กรองข้อมูลตามคอลัมน์ B
    filtered_df = df if selected_topic == "ทั้งหมด" else df[df.iloc[:, 1] == selected_topic]

    st.write(f"📊 พบข้อสอบทั้งหมด {len(filtered_df)} ข้อ")
    st.divider()

    # 3. ส่วนแสดงผลข้อสอบ (ระบุคอลัมน์ A=0, B=1, C=2, D=3, E=4, F=5, I=8)
    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1.5, 1])
            
            with col1:
                # คอลัมน์ A (Index 0) = id
                st.subheader(f"📌 รหัส: {row.iloc[0]}") 
                
                # คอลัมน์ B (Index 1) = topic, C (Index 2) = year, D (Index 3) = exam
                st.caption(f"บทเรียน: {row.iloc[1]} | ปี: {row.iloc[2]} | แหล่งที่มา: {row.iloc[3]}")
                
                # คอลัมน์ E (Index 4) = text (โจทย์)
                st.markdown(f"**โจทย์:**\n{row.iloc[4]}")
                
                # คอลัมน์ F (Index 5) = choices (ตัวเลือก)
                st.write(f"**ตัวเลือก:** {row.iloc[5]}")
            
            with col2:
                # --- คอลัมน์ I (Index 8) = รูปภาพ ---
                try:
                    raw_link = str(row.iloc[8]) 
                    # ค้นหารหัส ID จากลิงก์ Google Drive
                    match = re.search(r'id=([a-zA-Z0-9_-]{25,})', raw_link)
                    
                    if match:
                        file_id = match.group(1)
                        # ใช้ลิงก์แสดงผลแบบ thumbnail เพื่อความเสถียร
                        direct_link = f"https://drive.google.com/thumbnail?authuser=0&sz=w1000&id={file_id}"
                        st.image(direct_link, use_container_width=True)
                    else:
                        st.info("⚪ ไม่มีรูปประกอบ")
                except:
                    st.warning("⚠️ ไม่พบข้อมูลรูปในคอลัมน์ I")
            
            st.divider()
