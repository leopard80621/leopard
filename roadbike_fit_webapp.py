import streamlit as st

# 頁面設定必須為第一個 st 指令
st.set_page_config(page_title="公路車尺寸建議工具 | Roadbike Fit Tool", layout="centered")

# 多語言支援文字
TEXT = {
    "繁體中文": {
        "title": "🚴‍♂️ 公路車尺寸建議工具",
        "intro": "請輸入下列身體尺寸資料：",
        "inseam": "跨下長（cm）",
        "height": "身高（cm）",
        "shoulder": "肩寬（cm）",
        "ischial": "坐骨寬（cm）",
        "predict": "計算建議",
        "result": "📄 建議結果",
        "saddle_height": "建議座墊高度",
        "stack": "建議 Stack",
        "reach": "建議 Reach",
        "bar_width": "建議把手寬度",
        "saddle_width": "建議坐墊寬度",
        "bike_input": "📦 預計購買的車架幾何（Stack / Reach）",
        "stack_input": "車架 Stack",
        "reach_input": "車架 Reach",
        "compare_result": "✅ 幾何比對結果",
        "sponsor": "☕ 喜歡這個工具嗎？[贊助一杯咖啡](https://paypal.me/leopardbikeadvice)",
        "?_inseam": "（坐骨結節 → 腳跟/地面）",
        "?_height": "（頭頂 → 地面）",
        "?_shoulder": "（左右肩峰）",
        "?_ischial": "（左右坐骨結節）",
    },
    "English": {
        "title": "🚴‍♂️ Roadbike Fit Suggestion Tool",
        "intro": "Please enter your body measurements below:",
        "inseam": "Inseam (cm)",
        "height": "Height (cm)",
        "shoulder": "Shoulder Width (cm)",
        "ischial": "Ischial Width (cm)",
        "predict": "Calculate Suggestion",
        "result": "📄 Suggested Fit",
        "saddle_height": "Recommended Saddle Height",
        "stack": "Recommended Stack",
        "reach": "Recommended Reach",
        "bar_width": "Recommended Handlebar Width",
        "saddle_width": "Recommended Saddle Width",
        "bike_input": "📦 Geometry of Frame You Plan to Buy (Stack / Reach)",
        "stack_input": "Frame Stack",
        "reach_input": "Frame Reach",
        "compare_result": "✅ Geometry Comparison",
        "sponsor": "☕ Like this tool? [Buy me a coffee](https://paypal.me/leopardbikeadvice)",
        "?_inseam": "(Ischial Tuberosity → Floor)",
        "?_height": "(Top of Head → Floor)",
        "?_shoulder": "(Acromion to Acromion)",
        "?_ischial": "(Between Ischial Tuberosities)",
    }
}

# 語言選擇
lang = st.selectbox("語言 / Language", options=["繁體中文", "English"])
text = TEXT[lang]

st.title(text["title"])
st.markdown(text["intro"])

# 使用者輸入欄位
inseam = st.number_input(f"{text['inseam']} {text['?_inseam']}", min_value=40.0, max_value=120.0, value=80.0)
height = st.number_input(f"{text['height']} {text['?_height']}", min_value=140.0, max_value=210.0, value=175.0)
shoulder = st.number_input(f"{text['shoulder']} {text['?_shoulder']}", min_value=30.0, max_value=60.0, value=42.0)
ischial = st.number_input(f"{text['ischial']} {text['?_ischial']}", min_value=8.0, max_value=20.0, value=13.0)

st.markdown("---")

# 車架幾何輸入
st.markdown(text["bike_input"])
input_stack = st.number_input(f"{text['stack_input']} (mm)", min_value=400, max_value=700, value=570)
input_reach = st.number_input(f"{text['reach_input']} (mm)", min_value=350, max_value=450, value=390)

if st.button(text["predict"]):
    st.markdown("## " + text["result"])
    saddle_height = round(inseam * 0.883, 1)
    stack = round(height * 0.32 * 10, 1)
    reach = round((height * 0.22) * 10, 1)
    bar_width = f"{shoulder - 1}–{shoulder + 1}"
    saddle_width = f"{ischial + 1.0}–{ischial + 1.5}"

    st.write(f"📐 {text['saddle_height']}：{saddle_height} cm")
    st.write(f"📐 {text['stack']}：{stack} mm")
    st.write(f"📐 {text['reach']}：{reach} mm")
    st.write(f"📐 {text['bar_width']}：{bar_width} cm")
    st.write(f"🪑 {text['saddle_width']}：{saddle_width} cm")

    st.markdown("---")
    st.subheader(text["compare_result"])
    st.write(f"🔼 {text['stack']} 差值：{round(input_stack - stack, 1)} mm")
    st.write(f"🔼 {text['reach']} 差值：{round(input_reach - reach, 1)} mm")

    st.markdown("---")
    st.markdown(text["sponsor"])