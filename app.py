import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูเที่ยง", layout="wide")

# แก้ไขจุดที่ทำให้เกิด Error สีแดง (เปลี่ยน index เป็น html)
st.markdown("""
    <style>
    .reportview-container .main .block-container { font-size: 1.2rem; }
    div[data-testid="stExpander"] p { font-size: 1.1rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 คลังข้อสอบฟิสิกส์ ครูเที่ยง")

# 2. ฟังก์ชันโหลดข้อมูล
@st.cache_data(ttl=1)
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        # ใช้ header=0 และเช็คให้แน่ใจว่าไม่มีช่องว่างเกินมา
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"ไม่สามารถโหลดไฟล์ได้: {e}")
        return None

df = load_data()

# ฟังก์ชันเสริมสำหรับทำให้ LaTeX แสดงผลได้ชัวร์ขึ้น
def format_latex(text):
    text = str(text)
    # ถ้าในข้อความมีสัญลักษณ์ทางคณิตศาสตร์แต่ไม่มี $ ให้ลองใส่ครอบให้
    if "\\" in text and "$" not in text:
        return f"${text}$"
    return text

if df is not None:
    st.sidebar.header("🔍 ค้นหาข้อสอบ")
    # คอลัมน์ TopicCode อยู่ที่ Index 1
    topics = ["ทั้งหมด"] + sorted(df.iloc[:, 1].dropna().unique().tolist())
    selected_topic = st.sidebar.selectbox("เลือกบทเรียน:", topics)

    filtered_df = df if selected_topic == "ทั้งหมด" else df[df.iloc[:, 1] == selected_topic]

    st.write(f"📊 พบข้อสอบทั้งหมด {len(filtered_df)} ข้อ")
    st.divider()

    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1.6, 1])
            
            with col1:
                # แสดงรหัสข้อสอบ (Index 0)
                st.subheader(f"📌 รหัส: {row.iloc[0]}")
                st.caption(f"บทเรียน: {row.iloc[1]}")
                
                # โจทย์ (Index 2) - ใช้ฟังก์ชัน format_latex ช่วย
                st.markdown("**โจทย์:**")
                st.markdown(format_latex(row.iloc[2]))
                
                st.write("") 
                
                # ตัวเลือก (Index 3)
                st.markdown("**ตัวเลือก:**")
                st.markdown(format_latex(row.iloc[3]))
                
                with st.expander("ดูเฉลย"):
                    st.success(f"คำตอบคือ: {row.iloc[4]}")
            
            with col2:
                # รูปภาพ (Index 8)
                img_id = str(row.iloc[8]).strip()
                if img_id and img_id not in ["nan", "ไม่พบรูปภาพ", "ไม่มีรูป"]:
                    img_url = f"https://drive.google.com/thumbnail?authuser=0&sz=w1000&id={img_id}"
                    st.image(img_url, use_container_width=True)
                else:
                    st.info("⚪ ไม่มีรูปประกอบ")
            
            st.divider()
