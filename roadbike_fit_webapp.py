
import streamlit as st

# ⚙️ 頁面設定
st.set_page_config(page_title="公路車尺寸建議工具", layout="centered")

# 🌐 語言切換
lang = st.selectbox("語言 / Language", ["繁體中文", "English"])

# 📚 多語系文字包
text = {
    "繁體中文": {
        "title": "🚴‍♂️ 公路車尺寸建議工具",
        "instruction": "請輸入下列身體尺寸資料：",
        "inseam": "跨下長（cm） ？",
        "height": "身高（cm） ？",
        "shoulder": "肩寬（cm） ？",
        "ischial": "坐骨寬（cm） ？",
        "trunk": "臀幹長（cm） ？",
        "arm": "手臂長（cm） ？",
        "forearm": "前臂長（cm） ？",
        "thigh": "大腿長（cm） ？",
        "lowerleg": "小腿長（cm） ？",
        "sternal": "胸骨凹口高（cm） ？",
        "frame_stack": "車架 Stack（mm）",
        "frame_reach": "車架 Reach（mm）",
        "calculate": "計算建議",
        "result": "🧾 建議結果",
        "saddle_height": "建議座墊高度：約 {:.1f} cm",
        "stack": "建議 Stack：約 {:.1f} mm",
        "reach": "建議 Reach：約 {:.1f} mm",
        "stem_suggestion": "建議龍頭長度：約 {:.1f} mm（依據龍頭補償距離推算）",
        "handlebar": "建議把手寬度：約 {}–{} cm",
        "saddle_width": "建議坐墊寬度：約 {:.1f}–{:.1f} cm",
        "donate": "☕️ 想支持這個工具？歡迎[贊助我一杯咖啡](https://paypal.me/leopardbikeadvice)"
    },
    "English": {
        "title": "🚴‍♂️ Road Bike Fit Recommendation Tool",
        "instruction": "Please enter the following body measurements:",
        "inseam": "Inseam (cm) ？",
        "height": "Height (cm) ？",
        "shoulder": "Shoulder Width (cm) ？",
        "ischial": "Ischial Width (cm) ？",
        "trunk": "Trunk Length (cm) ？",
        "arm": "Arm Length (cm) ？",
        "forearm": "Forearm Length (cm) ？",
        "thigh": "Thigh Length (cm) ？",
        "lowerleg": "Lower Leg Length (cm) ？",
        "sternal": "Sternal Notch Height (cm) ？",
        "frame_stack": "Frame Stack (mm)",
        "frame_reach": "Frame Reach (mm)",
        "calculate": "Get Recommendation",
        "result": "🧾 Fit Result",
        "saddle_height": "Recommended Saddle Height: {:.1f} cm",
        "stack": "Recommended Stack: {:.1f} mm",
        "reach": "Recommended Reach: {:.1f} mm",
        "stem_suggestion": "Suggested Stem Length: {:.1f} mm (based on reach delta)",
        "handlebar": "Recommended Handlebar Width: {}–{} cm",
        "saddle_width": "Recommended Saddle Width: {:.1f}–{:.1f} cm",
        "donate": "☕️ Want to support this tool? [Buy me a coffee](https://paypal.me/leopardbikeadvice)"
    }
}

st.title(text[lang]["title"])
st.markdown(text[lang]["instruction"])

# ✍️ 使用者輸入
cols = st.columns(2)
with cols[0]:
    inseam = st.number_input(text[lang]["inseam"], 60.0, 100.0, step=0.1)
    height = st.number_input(text[lang]["height"], 140.0, 200.0, step=0.1)
    shoulder = st.number_input(text[lang]["shoulder"], 30.0, 50.0, step=0.1)
    ischial = st.number_input(text[lang]["ischial"], 8.0, 16.0, step=0.1)
    trunk = st.number_input(text[lang]["trunk"], 50.0, 70.0, step=0.1)
with cols[1]:
    arm = st.number_input(text[lang]["arm"], 60.0, 80.0, step=0.1)
    forearm = st.number_input(text[lang]["forearm"], 25.0, 45.0, step=0.1)
    thigh = st.number_input(text[lang]["thigh"], 50.0, 70.0, step=0.1)
    lowerleg = st.number_input(text[lang]["lowerleg"], 40.0, 65.0, step=0.1)
    sternal = st.number_input(text[lang]["sternal"], 120.0, 170.0, step=0.1)

st.markdown("### 📦 " + text[lang]["frame_stack"])
frame_stack = st.number_input(text[lang]["frame_stack"], 450, 650, step=1)
frame_reach = st.number_input(text[lang]["frame_reach"], 350, 450, step=1)

# 🔢 計算邏輯
if st.button(text[lang]["calculate"]):
    saddle_height = inseam * 0.883
    stack = height * 0.32
    reach = (arm + forearm + trunk) * 10 / 3  # 三段合併比例值，較為貼合

    # 預估龍頭長度建議：假設標準龍頭 100 mm
    reach_delta = frame_reach - reach
    suggested_stem = 100 + reach_delta

    # 顯示結果
    st.markdown("### " + text[lang]["result"])
    st.write(text[lang]["saddle_height"].format(saddle_height))
    st.write(text[lang]["stack"].format(stack))
    st.write(text[lang]["reach"].format(reach))
    st.write(text[lang]["stem_suggestion"].format(suggested_stem))
    st.write(text[lang]["handlebar"].format(int(shoulder), int(shoulder+2)))
    st.write(text[lang]["saddle_width"].format(ischial+0.6, ischial+2.6))

# ☕️ 贊助我一杯咖啡
st.markdown("---")
st.markdown(text[lang]["donate"])
