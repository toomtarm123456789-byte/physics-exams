import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูเที่ยง", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_index=True)

st.title("🚀 คลังข้อสอบฟิสิกส์ ครูเที่ยง")

# 2. ฟังก์ชันโหลดข้อมูล
@st.cache_data(ttl=60)
def load_data():
    # เปลี่ยน URL เป็นลิงก์ Raw ของไฟล์ CSV ใน GitHub ของคุณ
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        # กำหนด header=0 เพื่อใช้แถวแรกเป็นหัวตาราง
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"ไม่สามารถโหลดไฟล์ได้: {e}")
        return None

df = load_data()

if df is not None:
    # --- Sidebar สำหรับค้นหา ---
    st.sidebar.header("🔍 ค้นหาข้อสอบ")
    
    # ดึงรายชื่อบทเรียนจากคอลัมน์ TopicCode (Index 1)
    topics = ["ทั้งหมด"] + sorted(df.iloc[:, 1].dropna().unique().tolist())
    selected_topic = st.sidebar.selectbox("เลือกบทเรียน (TopicCode):", topics)

    # กรองข้อมูล
    if selected_topic == "ทั้งหมด":
        filtered_df = df
    else:
        filtered_df = df[df.iloc[:, 1] == selected_topic]

    st.write(f"📊 พบข้อสอบทั้งหมด {len(filtered_df)} ข้อ")
    st.divider()

    # 3. วนลูปแสดงผลข้อสอบ
    for index, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1.5, 1])
            
            with col1:
                # คอลัมน์ A (Index 0): รหัสข้อสอบ
                st.subheader(f"📌 รหัส: {row.iloc[0]}")
                
                # คอลัมน์ B (Index 1): บทเรียน
                st.caption(f"บทเรียน: {row.iloc[1]}")
                
                # คอลัมน์ C (Index 2): โจทย์ (ใช้ Markdown เพื่อรองรับ LaTeX)
                st.markdown("**โจทย์:**")
                st.markdown(row.iloc[2])
                
                # คอลัมน์ D (Index 3): ตัวเลือก
                st.info(f"**ตัวเลือก:** {row.iloc[3]}")
                
                # คอลัมน์ E (Index 4): เฉลย (ซ่อนไว้ให้กดดู)
                with st.expander("คลิกเพื่อดูเฉลย"):
                    st.success(f"คำตอบคือ: {row.iloc[4]}")
            
            with col2:
                # คอลัมน์ I (Index 8): image_id
                img_id = str(row.iloc[8]).strip()
                
                # ตรวจสอบว่ามี ID รูปภาพที่ใช้งานได้จริงหรือไม่
                if img_id and img_id not in ["nan", "ไม่พบรูปภาพ", "ไม่มีรูป"]:
                    # ใช้ URL Thumbnail ของ Google Drive (ให้ภาพชัดและโหลดไว)
                    img_url = f"https://drive.google.com/thumbnail?authuser=0&sz=w1000&id={img_id}"
                    st.image(img_url, use_container_width=True, caption=f"รูปประกอบ {row.iloc[0]}")
                else:
                    st.text("— ไม่มีรูปภาพประกอบ —")
            
            st.divider()
