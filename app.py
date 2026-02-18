import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูเที่ยง", layout="wide")

# แก้ไขจุดที่ทำให้เกิด Error สีแดง (เปลี่ยนจาก unsafe_allow_index เป็น unsafe_allow_html)
st.markdown("""
    <style>
    .stMarkdown p { font-size: 1.2rem !important; line-height: 1.6; }
    .katex { font-size: 1.1em !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 คลังข้อสอบฟิสิกส์ ครูเที่ยง")

# 2. ฟังก์ชันโหลดข้อมูล
@st.cache_data(ttl=1)
def load_data():
    # ลิงก์ไฟล์ CSV ของคุณครู
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        # อ่านไฟล์และลบช่องว่างหัวท้ายของชื่อคอลัมน์
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"ไม่สามารถโหลดไฟล์ได้: {e}")
        return None

df = load_data()

if df is not None:
    # --- Sidebar สำหรับกรองบทเรียน ---
    st.sidebar.header("🔍 ค้นหาข้อสอบ")
    topics = ["ทั้งหมด"] + sorted(df.iloc[:, 1].dropna().unique().tolist())
    selected_topic = st.sidebar.selectbox("เลือกบทเรียน:", topics)

    filtered_df = df if selected_topic == "ทั้งหมด" else df[df.iloc[:, 1] == selected_topic]
    
    st.write(f"📊 พบข้อสอบทั้งหมด {len(filtered_df)} ข้อ")
    st.divider()

    # 3. วนลูปแสดงผลข้อสอบ
    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1.6, 1])
            
            with col1:
                # แสดงรหัสและบทเรียน
                st.subheader(f"📌 รหัส: {row.iloc[0]}")
                st.caption(f"บทเรียน: {row.iloc[1]}")
                
                # แสดงโจทย์ (รองรับ LaTeX ที่มี $ ครอบมาจาก Sheet แล้ว)
                st.markdown("**โจทย์:**")
                st.write(row.iloc[2]) 
                
                st.write("")
                
                # แสดงตัวเลือก
                st.markdown("**ตัวเลือก:**")
                st.write(row.iloc[3])
                
                with st.expander("ดูเฉลย"):
                    st.success(f"คำตอบคือ: {row.iloc[4]}")
            
            with col2:
                # ส่วนแสดงรูปภาพ (คอลัมน์ I)
                img_id = str(row.iloc[8]).strip()
                if img_id and img_id not in ["nan", "ไม่พบรูปภาพ", "ไม่มีรูป"]:
                    img_url = f"https://drive.google.com/thumbnail?authuser=0&sz=w1000&id={img_id}"
                    st.image(img_url, use_container_width=True)
                else:
                    st.info("⚪ ไม่มีรูปประกอบ")
            
            st.divider()
