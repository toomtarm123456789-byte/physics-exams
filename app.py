import streamlit as st
import pandas as pd

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์", layout="wide")
st.title("📚 ระบบคลังข้อสอบฟิสิกส์ออนไลน์ (2567)")

@st.cache_data
def load_data():
    # โหลดไฟล์ CSV
    df = pd.read_csv("physics_data.csv")
    return df

try:
    df = load_data()
    
    # --- ตัวกรองด้านข้าง ---
    st.sidebar.header("🔍 ค้นหาข้อสอบ")
    topic_list = ["ทั้งหมด"] + sorted(df['topic'].unique().astype(str).tolist())
    selected_topic = st.sidebar.selectbox("เลือกบทเรียน (Topic):", topic_list)
    
    filtered_df = df if selected_topic == "ทั้งหมด" else df[df['topic'] == selected_topic]

    # --- ส่วนแสดงผล ---
    st.write(f"พบข้อสอบทั้งหมด {len(filtered_df)} ข้อ")
    st.divider()

    for index, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1.5, 1]) 
            with col1:
                st.subheader(f"📌 รหัส: {row['id']} ({row['exam']})")
                st.info(f"**โจทย์:** {row['text']}")
                st.write(f"**ตัวเลือก:** {row['choices']}")
            with col2:
                image_link = str(row['image_url'])
                if "http" in image_link:
                    st.image(image_link, use_container_width=True)
                else:
                    st.warning("❌ ไม่มีรูปประกอบ")
            st.divider()

except Exception as e:
    st.error(f"กรุณาอัปโหลดไฟล์ physics_data.csv ขึ้น GitHub ก่อนครับ")
