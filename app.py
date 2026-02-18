import streamlit as st
import pandas as pd

st.set_page_config(page_title="คลังข้อสอบฟิสิกส์ ครูเที่ยง", layout="wide")

# เพิ่ม CSS เพื่อปรับขนาดฟอนต์ให้ใหญ่และอ่านง่ายขึ้น
st.markdown("""
    <style>
    .reportview-container .main .block-container { font-size: 1.2rem; }
    div[data-testid="stExpander"] p { font-size: 1.1rem; font-weight: bold; }
    </style>
    """, unsafe_allow_index=True)

st.title("🚀 คลังข้อสอบฟิสิกส์ ครูเที่ยง")

@st.cache_data(ttl=1)
def load_data():
    url = "https://raw.githubusercontent.com/toomtarm123456789-byte/physics-exams/main/physics_data.csv"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"ไม่สามารถโหลดไฟล์ได้: {e}")
        return None

df = load_data()

if df is not None:
    st.sidebar.header("🔍 ค้นหาข้อสอบ")
    topics = ["ทั้งหมด"] + sorted(df.iloc[:, 1].dropna().unique().tolist())
    selected_topic = st.sidebar.selectbox("เลือกบทเรียน:", topics)

    filtered_df = df if selected_topic == "ทั้งหมด" else df[df.iloc[:, 1] == selected_topic]

    st.write(f"📊 พบข้อสอบทั้งหมด {len(filtered_df)} ข้อ")
    st.divider()

    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1.6, 1])
            
            with col1:
                st.subheader(f"📌 รหัส: {row.iloc[0]}")
                st.caption(f"บทเรียน: {row.iloc[1]}")
                
                # --- ส่วนการแสดงผล LaTeX ---
                # ใช้ st.markdown เพราะรองรับทั้งข้อความปกติและ LaTeX ที่อยู่ในเครื่องหมาย $...$
                st.markdown("**โจทย์:**")
                st.markdown(row.iloc[2]) # คอลัมน์ C: โจทย์
                
                st.write("") # เว้นวรรคเล็กน้อย
                
                st.markdown("**ตัวเลือก:**")
                st.markdown(row.iloc[3]) # คอลัมน์ D: ตัวเลือก
                
                with st.expander("ดูเฉลย"):
                    # แสดงเฉลยแบบสวยๆ
                    st.success(f"คำตอบคือ: {row.iloc[4]}")
            
            with col2:
                img_id = str(row.iloc[8]).strip()
                if img_id and img_id not in ["nan", "ไม่พบรูปภาพ", "ไม่มีรูป"]:
                    img_url = f"https://drive.google.com/thumbnail?authuser=0&sz=w1000&id={img_id}"
                    st.image(img_url, use_container_width=True)
                else:
                    st.info("⚪ ไม่มีรูปประกอบ")
            
            st.divider()
