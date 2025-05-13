import streamlit as st

# 🛠️ 初始設定：需在最前面
st.set_page_config(page_title="公路車尺寸建議工具", layout="centered")

# 🌐 語言切換
lang = st.selectbox("語言 / Language", ["繁體中文", "English"])

# 🌐 文字包
text = {
    "繁體中文": {
        "title": "🚴‍♂️ 公路車尺寸建議工具",
        "instruction": "請輸入下列身體尺寸資料：",
        "inseam": "跨下長（cm）　（坐骨結節 ➜ 腳跟/地面）",
        "height": "身高（cm）　（頭頂 ➜ 地面）",
        "shoulder": "肩寬（cm）　（左右肩峰）",
        "ischial": "坐骨寬（cm）　（左右坐骨結節）",
        "trunk": "臀幹長（cm）　（胸骨凹口 ➜ 髖脊）",
        "arm": "手臂長（cm）　（肩峰 ➜ 肘骨外上髁）",
        "forearm": "前臂長（cm）　（肘骨外上髁 ➜ 橈骨莖突）",
        "thigh": "大腿長（cm）　（大轉子 ➜ 股骨外髁）",
        "lowerleg": "小腿長（cm）　（股骨外髁 ➜ 脛骨外踝）",
        "sternal": "胸骨凹口高（cm）　（胸骨凹口 ➜ 地面）",
        "section_purchase": "📦 預計購買的車架幾何（Stack / Reach）",
        "stack_input": "車架 Stack (mm)",
        "reach_input": "車架 Reach (mm)",
        "stem_length": "龍頭長度 (mm)",
        "calculate": "計算建議",
        "result": "🧾 建議結果",
        "saddle_height": "建議座墊高度：",
        "stack": "建議 Stack：",
        "reach": "建議 Reach：",
        "delta_stack": "與車架差值：",
        "delta_reach": "與車架差值：",
        "spacer": "（建議加墊圈：{:.1f} cm）",
        "ok": "✅ 相符",
        "ng": "❌ 有差距",
        "bar": "｜",
        "handlebar": "建議把手寬度：",
        "saddle_width": "建議坐墊寬度：",
        "donate": "☕️ 想支持這個工具？歡迎[贊助我一杯咖啡](https://paypal.me/leopardbikeadvice)",
    },
    "English": {
        "title": "🚴‍♂️ Road Bike Fit Recommendation Tool",
        "instruction": "Please enter the following body measurements:",
        "inseam": "Inseam (cm)　(Sit bone ➜ Heel/ground)",
        "height": "Height (cm)　(Top of head ➜ Ground)",
        "shoulder": "Shoulder width (cm)　(Left ➜ Right AC joint)",
        "ischial": "Ischial width (cm)　(Left ➜ Right sit bones)",
        "trunk": "Trunk length (cm)　(Sternal notch ➜ Iliac crest)",
        "arm": "Arm length (cm)　(Shoulder ➜ Lateral epicondyle)",
        "forearm": "Forearm length (cm)　(Epicondyle ➜ Styloid)",
        "thigh": "Thigh length (cm)　(Greater trochanter ➜ Femoral condyle)",
        "lowerleg": "Lower leg (cm)　(Condyle ➜ Malleolus)",
        "sternal": "Sternal height (cm)　(Sternal notch ➜ Ground)",
        "section_purchase": "📦 Geometry of Bike You Plan to Purchase (Stack / Reach)",
        "stack_input": "Frame Stack (mm)",
        "reach_input": "Frame Reach (mm)",
        "stem_length": "Stem length (mm)",
        "calculate": "Get Recommendation",
        "result": "🧾 Fit Result",
        "saddle_height": "Recommended Saddle Height:",
        "stack": "Recommended Stack:",
        "reach": "Recommended Reach:",
        "delta_stack": "Difference from Frame:",
        "delta_reach": "Difference from Frame:",
        "spacer": "(Add spacer: {:.1f} cm)",
        "ok": "✅ Matched",
        "ng": "❌ Mismatch",
        "bar": "｜",
        "handlebar": "Recommended Handlebar Width:",
        "saddle_width": "Recommended Saddle Width:",
        "donate": "☕️ Like this tool? [Buy me a coffee](https://paypal.me/leopardbikeadvice)",
    }
}[lang]

st.title(text["title"])
st.markdown(text["instruction"])

# ✏️ 基本量測欄位
inseam = st.number_input(text["inseam"], 50.0, 100.0, 80.0)
height = st.number_input(text["height"], 140.0, 200.0, 175.0)
shoulder = st.number_input(text["shoulder"], 30.0, 60.0, 42.0)
ischial = st.number_input(text["ischial"], 8.0, 16.0, 13.0)
trunk = st.number_input(text["trunk"], 50.0, 80.0, 64.0)
arm = st.number_input(text["arm"], 50.0, 80.0, 66.0)
forearm = st.number_input(text["forearm"], 25.0, 40.0, 33.5)
thigh = st.number_input(text["thigh"], 50.0, 70.0, 62.0)
lower_leg = st.number_input(text["lowerleg"], 40.0, 65.0, 55.0)
sternal = st.number_input(text["sternal"], 120.0, 160.0, 145.0)

# 📦 預計購買資訊
st.markdown("---")
st.subheader(text["section_purchase"])
stack_input = st.number_input(text["stack_input"], 400, 650, 570)
reach_input = st.number_input(text["reach_input"], 350, 450, 390)

# 🧮 按鈕
if st.button(text["calculate"]):
    saddle_height = round(inseam * 0.883, 1)
    rec_stack = round(height * 0.32 * 10, 1)
    rec_reach = round((trunk + arm) * 0.26 * 10, 1)
    delta_stack = round(stack_input - rec_stack, 1)
    delta_reach = round(reach_input - rec_reach, 1)
    spacer_cm = max(0, -delta_stack / 10)

    st.subheader(text["result"])
    st.write(f"📐 {text['saddle_height']} {saddle_height} cm")
    st.write(f"📏 {text['stack']} {rec_stack} mm {text['bar']} {text['delta_stack']} {delta_stack} mm", text["ok"] if abs(delta_stack) <= 10 else text["ng"], (text["spacer"].format(spacer_cm) if delta_stack < -5 else ""))
    st.write(f"📐 {text['reach']} {rec_reach} mm {text['bar']} {text['delta_reach']} {delta_reach} mm", text["ok"] if abs(delta_reach) <= 10 else text["ng"])
    st.write(f"🤝 {text['handlebar']} {shoulder} ± 2 cm")
    st.write(f"🪑 {text['saddle_width']} {ischial + 2.0:.1f}–{ischial + 2.5:.1f} cm")

    # ☕ 贊助區
    st.markdown("---")
    st.markdown(text["donate"])
