import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูเที่ยง", layout="wide")

st.title("🚀 คลังข้อสอบฟิสิกส์ ครูเที่ยง")

# 2. ฟังก์ชันโหลดข้อมูล
@st.cache_data(ttl=1) # ตั้งเป็น 1 วินาทีเพื่อให้เห็นผลการอัปเดตทันที
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        # อ่านไฟล์ CSV โดยระบุชื่อคอลัมน์ให้ตรงตามหัวตาราง
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"ไม่สามารถโหลดไฟล์ได้: {e}")
        return None

df = load_data()

if df is not None:
    # --- Sidebar สำหรับค้นหา ---
    st.sidebar.header("🔍 ค้นหาข้อสอบ")
    
    # ใช้คอลัมน์ที่ 2 (Index 1) เป็น TopicCode สำหรับเลือกบทเรียน
    topics = ["ทั้งหมด"] + sorted(df.iloc[:, 1].dropna().unique().tolist())
    selected_topic = st.sidebar.selectbox("เลือกบทเรียน:", topics)

    # กรองข้อมูล
    if selected_topic == "ทั้งหมด":
        filtered_df = df
    else:
        filtered_df = df[df.iloc[:, 1] == selected_topic]

    st.write(f"📊 พบข้อสอบทั้งหมด {len(filtered_df)} ข้อ")
    st.divider()

    # 3. วนลูปแสดงผลข้อสอบ
    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1.5, 1])
            
            with col1:
                # คอลัมน์ A (Index 0): รหัสข้อสอบ
                st.subheader(f"📌 รหัส: {row.iloc[0]}")
                
                # รายละเอียดคอลัมน์ B (Index 1)
                st.caption(f"บทเรียน: {row.iloc[1]}")
                
                # คอลัมน์ C (Index 2): โจทย์
                st.markdown("**โจทย์:**")
                st.write(row.iloc[2])
                
                # คอลัมน์ D (Index 3): ตัวเลือก
                st.markdown(f"**ตัวเลือก:** {row.iloc[3]}")
                
                # คอลัมน์ E (Index 4): เฉลย
                with st.expander("เฉลย"):
                    st.success(f"คำตอบคือ: {row.iloc[4]}")
            
            with col2:
                # คอลัมน์ I (Index 8): image_id
                # หมายเหตุ: .iloc[8] คือคอลัมน์ I ในตาราง
                img_id = str(row.iloc[8]).strip()
                
                if img_id and img_id not in ["nan", "ไม่พบรูปภาพ", "ไม่มีรูป"]:
                    img_url = f"https://drive.google.com/thumbnail?authuser=0&sz=w1000&id={img_id}"
                    st.image(img_url, use_container_width=True)
                else:
                    st.info("⚪ ไม่มีรูปประกอบ")
            
            st.divider()
