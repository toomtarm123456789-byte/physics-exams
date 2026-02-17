import streamlit as st
import pandas as pd
import re

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูต้อม", layout="wide")
st.title("🚀 คลังข้อสอบฟิสิกส์ ครูต้อม")

# 2. ฟังก์ชันโหลดข้อมูล
@st.cache_data(ttl=60)
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        # อ่านไฟล์และล้างช่องว่างหัวคอลัมน์ทันที
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip() 
        return df
    except Exception as e:
        st.error(f"ไม่สามารถโหลดไฟล์ได้: {e}")
        return None

df = load_data()

if df is not None:
    # --- ส่วนการค้นหาด้านข้าง (Sidebar) ---
    st.sidebar.header("🔍 ค้นหาข้อสอบ")
    
    # ดึงรายชื่อบทเรียนจากคอลัมน์ 'topic'
    if 'topic' in df.columns:
        topic_list = ["ทั้งหมด"] + sorted(df['topic'].dropna().unique().tolist())
        selected_topic = st.sidebar.selectbox("เลือกบทเรียน:", topic_list)
        filtered_df = df if selected_topic == "ทั้งหมด" else df[df['topic'] == selected_topic]
    else:
        filtered_df = df

    st.write(f"📊 พบข้อสอบทั้งหมด {len(filtered_df)} ข้อ")
    st.divider()

    # 3. ส่วนแสดงผลข้อสอบ (ใช้ชื่อคอลัมน์ตามไฟล์ Excel ของครู)
    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1.5, 1]) # ปรับสัดส่วนให้โจทย์กว้างขึ้น
            
            with col1:
                # แสดงรหัสข้อสอบ
                st.subheader(f"📌 รหัส: {row.get('id', '-')}") 
                
                # แสดงโจทย์ (คอลัมน์ text)
                st.markdown(f"**โจทย์:**\n{row.get('text', '-')}")
                
                # แสดงตัวเลือก (คอลัมน์ choices)
                st.write(f"**ตัวเลือก:** {row.get('choices', '-')}")
                
                # แสดงชื่อบทเรียนกำกับ (คอลัมน์ topic)
                st.caption(f"บทเรียน: {row.get('topic', '-')}")
            
            with col2:
                # ดึงลิงก์จากคอลัมน์ image_url (คอลัมน์ I)
                raw_link = str(row.get('image_url', ''))
                
                # ค้นหารหัส ID จากลิงก์ Google Drive เพื่อทำเป็น Direct Link
                match = re.search(r'id=([a-zA-Z0-9_-]{25,})', raw_link)
                
                if match:
                    file_id = match.group(1)
                    # ใช้ระบบ Thumbnail ของ Google เพื่อความไวและเสถียร
                    direct_link = f"https://drive.google.com/thumbnail?authuser=0&sz=w1000&id={file_id}"
                    st.image(direct_link, use_container_width=True)
                else:
                    # ถ้าไม่มีรูป ให้เว้นว่างไว้สวยๆ
                    pass
            
            st.divider()
            
