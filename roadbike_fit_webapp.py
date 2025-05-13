
import streamlit as st

# 多語言切換
lang = st.selectbox("語言 / Language", ["繁體中文", "English"])

text = {
    "繁體中文": {
        "title": "🚴‍♂️ 公路車尺寸建議工具",
        "input_prompt": "請輸入下列身體尺寸資料：",
        "inseam": "跨下長（cm）",
        "height": "身高（cm）",
        "shoulder": "肩寬（cm）",
        "ischial": "坐骨寬（cm）",
        "calculate": "計算建議",
        "result": "📄 建議結果",
        "saddle": "建議座墊高度",
        "stack": "建議 Stack",
        "reach": "建議 Reach",
        "stem": "使用龍頭長度",
        "seatwidth": "建議坐墊寬度",
        "compare": "🚲 預計購買的車架幾何",
        "bike_stack": "車架 Stack（mm）",
        "bike_reach": "車架 Reach（mm）",
        "diff_stack": "與建議 Stack 差值",
        "diff_reach": "與建議 Reach 差值",
        "donate": "☕ 贊助一杯咖啡",
        "donate_link": "https://paypal.me/leopardbikeadvice"
    },
    "English": {
        "title": "🚴‍♂️ Roadbike Fit Recommendation Tool",
        "input_prompt": "Please enter your body measurements:",
        "inseam": "Inseam (cm)",
        "height": "Height (cm)",
        "shoulder": "Shoulder width (cm)",
        "ischial": "Ischial width (cm)",
        "calculate": "Get Recommendation",
        "result": "📄 Recommendation Result",
        "saddle": "Recommended Saddle Height",
        "stack": "Recommended Stack",
        "reach": "Recommended Reach",
        "stem": "Stem Length Used",
        "seatwidth": "Recommended Saddle Width",
        "compare": "🚲 Geometry of Bike You Plan to Purchase",
        "bike_stack": "Bike Stack (mm)",
        "bike_reach": "Bike Reach (mm)",
        "diff_stack": "Stack Difference",
        "diff_reach": "Reach Difference",
        "donate": "☕ Buy me a coffee",
        "donate_link": "https://paypal.me/leopardbikeadvice"
    }
}[lang]

st.set_page_config(page_title=text["title"], layout="centered")
st.title(text["title"])
st.write(text["input_prompt"])

inseam = st.number_input(text["inseam"], 60.0, 100.0, step=0.5)
height = st.number_input(text["height"], 140.0, 200.0, step=0.5)
shoulder = st.number_input(text["shoulder"], 30.0, 50.0, step=0.5)
ischial = st.number_input(text["ischial"], 8.0, 20.0, step=0.5)

st.write("---")
st.subheader(text["compare"])
bike_stack = st.number_input(text["bike_stack"], 400.0, 650.0, step=1.0)
bike_reach = st.number_input(text["bike_reach"], 350.0, 450.0, step=1.0)
stem_length = st.slider(text["stem"], 80, 120, 100, step=10)

if st.button(text["calculate"]):
    saddle_height = round(inseam * 0.883, 1)
    recommended_stack = round(height * 0.32 * 10, 1)
    recommended_reach = round((height * 0.26 * 10) + (stem_length - 100), 1)
    seat_width = f"{ischial + 2.0:.1f}–{ischial + 4.0:.1f}"

    stack_diff = round(bike_stack - recommended_stack, 1)
    reach_diff = round(bike_reach - recommended_reach, 1)

    st.subheader(text["result"])
    st.write(f"📐 {text['saddle']}：{saddle_height} cm")
    st.write(f"📐 {text['stack']}：{recommended_stack} mm")
    st.write(f"📐 {text['reach']}：{recommended_reach} mm （{text['stem']} {stem_length} mm）")
    st.write(f"📏 {text['diff_stack']}：{stack_diff} mm")
    st.write(f"📏 {text['diff_reach']}：{reach_diff} mm")
    st.write(f"🪑 {text['seatwidth']}：{seat_width} cm")

st.markdown(f"<br><a href='{text['donate_link']}' target='_blank'>{text['donate']}</a>", unsafe_allow_html=True)
