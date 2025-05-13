
import streamlit as st

st.set_page_config(page_title="Roadbike Fit Tool", layout="centered")

st.title("🚴 公路車尺寸建議工具")
st.markdown("請輸入下列身體尺寸資料：")

inseam = st.number_input("跨下長（cm）", min_value=60.0, max_value=100.0, step=0.5)
height = st.number_input("身高（cm）", min_value=140.0, max_value=200.0, step=0.5)
shoulder_width = st.number_input("肩寬（cm）", min_value=30.0, max_value=60.0, step=0.5)
saddle_width = st.number_input("坐骨寬（cm）", min_value=8.0, max_value=20.0, step=0.5)

if st.button("計算建議"):
    saddle_height = round(inseam * 0.883, 1)
    stack = round(height * 0.32 * 10, 1)
    reach = round((height * 0.22) * 10, 1)
    handlebar = f"{int(shoulder_width)}–{int(shoulder_width + 2)} cm"
    saddle_range = f"{round(saddle_width + 1.0, 1)}–{round(saddle_width + 3.0, 1)} cm"

    st.markdown("## 🧾 建議結果")
    st.write(f"📏 建議座墊高度：{saddle_height} cm")
    st.write(f"📐 建議 Stack：{stack} mm")
    st.write(f"📏 建議 Reach：{reach} mm")
    st.write(f"🤝 建議把手寬度：{handlebar}")
    st.write(f"🪑 建議坐墊寬度：{saddle_range}")
