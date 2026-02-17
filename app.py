import streamlit as st
import pandas as pd

st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูต้อม", layout="wide")

st.title("🚀 คลังข้อสอบฟิสิกส์ (ระบบตรวจสอบรูปภาพ)")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        df = pd.read_csv(url)
        # ล้างช่องว่างที่หัวคอลัมน์ทั้งหมด
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        st.error(f"โหลดไฟล์ไม่ได้: {e}")
        return None

df = load_data()

if df is not None:
    # ค้นหาคอลัมน์ที่มีคำว่า 'image' หรือ 'url'
    img_col = next((c for c in df.columns if 'image' in c or 'url' in c), None)
    
    # ส่วนกรองข้อมูล
    topic_col = next((c for c in df.columns if 'topic' in c), 'topic')
    df[topic_col] = df[topic_col].fillna("ทั่วไป").astype(str)
    topics = ["ทั้งหมด"] + sorted(df[topic_col].unique().tolist())
    selected = st.sidebar.selectbox("เลือกบทเรียน", topics)

    filtered_df = df if selected == "ทั้งหมด" else df[df[topic_col] == selected]

    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(f"📌 รหัส: {row.get('id', 'N/A')}")
                st.info(f"**โจทย์:** {row.get('text', '-')}")
                st.write(f"**ตัวเลือก:** {row.get('choices', '-')}")
            
            with col2:
                # พยายามดึงลิงก์จากคอลัมน์ที่เจอ
                link = str(row.get(img_col, ''))
                if "http" in link:
                    st.image(link.strip(), use_container_width=True)
                else:
                    st.warning(f"❌ ไม่พบลิงก์ (ข้อมูลที่พบ: {link})")
            st.divider()
