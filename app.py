import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูต้อม", layout="wide")
st.title("🚀 คลังข้อสอบฟิสิกส์ (ฉบับแก้ไขด่วน)")

@st.cache_data(ttl=60)
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        df = pd.read_csv(url)
        # ล้างชื่อคอลัมน์ให้สะอาด (ตัดเว้นวรรคและทำให้เป็นตัวพิมพ์เล็ก)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        st.error(f"ไม่สามารถอ่านไฟล์ CSV ได้: {e}")
        return None

df = load_data()

if df is not None:
    # แสดงรายชื่อคอลัมน์ที่ระบบเห็น (เพื่อการตรวจสอบ)
    # st.write("คอลัมน์ที่พบ:", list(df.columns)) 

    # หาชื่อคอลัมน์ที่ใกล้เคียงที่สุด
    def get_col(options):
        for opt in options:
            if opt.lower() in df.columns: return opt.lower()
        return None

    col_topic = get_col(['topic', 'บทเรียน'])
    col_id = get_col(['id', 'รหัส'])
    col_img = get_col(['image_url', 'image', 'url', 'link'])

    # ส่วนกรองข้อมูล
    if col_topic:
        df[col_topic] = df[col_topic].fillna("ทั่วไป").astype(str)
        topics = ["ทั้งหมด"] + sorted(df[col_topic].unique().tolist())
        selected = st.sidebar.selectbox("เลือกบทเรียน", topics)
        filtered_df = df if selected == "ทั้งหมด" else df[df[col_topic] == selected]
    else:
        filtered_df = df

    # แสดงผล
    for _, row in filtered_df.iterrows():
        with st.container():
            c1, c2 = st.columns([2, 1])
            with c1:
                st.subheader(f"📌 {row.get(col_id, 'N/A')}")
                st.info(f"**โจทย์:** {row.get('text', row.get('โจทย์', '-'))}")
                st.write(f"**ตัวเลือก:** {row.get('choices', row.get('ตัวเลือก', '-'))}")
            with c2:
                img = str(row.get(col_img, '')).strip() if col_img else ""
                # แสดงรูปถ้าลิงก์ถูกต้องและมีรหัสรูป (รหัสรูป Google Drive มักจะยาวกว่า 20 ตัว)
                if "http" in img and len(img) > 50:
                    st.image(img, use_container_width=True)
                else:
                    st.warning("⚪ ไม่มีรูปประกอบ")
            st.divider()
