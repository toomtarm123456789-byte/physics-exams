import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูต้อม", layout="wide")
st.title("🚀 คลังข้อสอบฟิสิกส์ (ระบบดึงรูปอัตโนมัติ)")

@st.cache_data(ttl=1)
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

df = load_data()

if df is not None:
    # ค้นหาคอลัมน์
    col_img = next((c for c in df.columns if 'url' in c or 'image' in c), None)
    
    for _, row in df.iterrows():
        with st.container():
            c1, c2 = st.columns([2, 1])
            with c1:
                st.subheader(f"📌 {row.get('id', 'N/A')}")
                st.info(f"**โจทย์:** {row.get('text', '-')}")
            
            with c2:
                raw_link = str(row.get(col_img, ''))
                
                # --- ส่วนผ่าตัดลิงก์ (Magic Logic) ---
                # ค้นหา File ID จากลิงก์ Google Drive (รหัส 33 ตัว)
                match = re.search(r'id=([a-zA-Z0-9_-]{25,})', raw_link)
                
                if match:
                    file_id = match.group(1)
                    # แปลงเป็นลิงก์ดึงรูปโดยตรง (Direct Link)
                    direct_link = f"https://lh3.googleusercontent.com/u/0/d/{file_id}"
                    st.image(direct_link, use_container_width=True)
                elif "http" in raw_link and len(raw_link) > 20:
                    # ถ้ามีลิงก์แต่หารหัสไม่เจอ ลองแสดงตรงๆ
                    st.image(raw_link, use_container_width=True)
                else:
                    st.warning("⚪ ไม่มีรูปประกอบ")
            st.divider()
