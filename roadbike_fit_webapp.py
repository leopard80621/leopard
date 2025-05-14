
import streamlit as st

# Set page config
st.set_page_config(page_title="公路車尺寸建議工具", layout="centered")

# Language options
lang = st.radio("語言 / Language", ["繁體中文", "English"])
is_chinese = lang == "繁體中文"

# Define translation dictionary
text = {
    "title": "公路車尺寸建議工具" if is_chinese else "Road Bike Fit Recommendation Tool",
    "inseam": "跨下長（cm）（坐骨結節 ➝ 腳跟/地面）" if is_chinese else "Inseam (cm)",
    "height": "身高（cm）（頭頂 ➝ 地面）" if is_chinese else "Height (cm)",
    "shoulder": "肩寬（cm）（左右肩峰）" if is_chinese else "Shoulder Width (cm)",
    "ischial": "坐骨寬（cm）（左右坐骨結節）" if is_chinese else "Ischial Width (cm)",
    "trunk": "軀幹長（cm）（胸骨凹口 ➝ 髖骨）" if is_chinese else "Trunk Length (cm)",
    "arm": "手臂長（cm）（肩峰 ➝ 肘關節外上髁）" if is_chinese else "Arm Length (cm)",
    "stack_input": "預計購買的車架幾何（Stack / Reach）" if is_chinese else "Planned Frame Geometry (Stack / Reach)",
    "frame_stack": "車架 Stack (mm)",
    "frame_reach": "車架 Reach (mm)",
    "calculate": "計算建議" if is_chinese else "Calculate",
    "recommend": "建議結果" if is_chinese else "Recommended Fit",
    "saddle_height": "建議座墊高度",
    "stack_result": "建議 Stack",
    "reach_result": "建議 Reach",
    "handlebar_width": "建議把手寬度",
    "saddle_width": "建議坐墊寬度",
    "stem_length": "建議龍頭長度",
    "donate": "☕ 如果這個工具對你有幫助，歡迎[贊助一杯咖啡](https://paypal.me/leopardbikeadvice)" if is_chinese else "☕ Like this tool? [Buy me a coffee](https://paypal.me/leopardbikeadvice)"
}

# Input area
st.title(text["title"])
inseam = st.number_input(text["inseam"], min_value=60.0, max_value=100.0, value=80.0, step=0.1)
height = st.number_input(text["height"], min_value=140.0, max_value=200.0, value=175.0, step=0.1)
shoulder = st.number_input(text["shoulder"], min_value=30.0, max_value=50.0, value=42.0, step=0.1)
ischial = st.number_input(text["ischial"], min_value=9.0, max_value=15.0, value=13.0, step=0.1)
trunk = st.number_input(text["trunk"], min_value=40.0, max_value=70.0, value=60.0, step=0.1)
arm = st.number_input(text["arm"], min_value=50.0, max_value=80.0, value=66.0, step=0.1)

st.markdown("---")
st.subheader(text["stack_input"])
frame_stack = st.number_input(text["frame_stack"], min_value=480, max_value=650, value=576, step=1)
frame_reach = st.number_input(text["frame_reach"], min_value=350, max_value=450, value=390, step=1)

if st.button(text["calculate"]):
    saddle_height = round(inseam * 0.883, 1)
    suggested_stack = round(height * 0.32 * 10, 1)
    suggested_reach = round((trunk + arm) * 0.26 * 10, 1)
    handlebar_width = f"{int(shoulder)}.0 ± 2 cm"
    saddle_width = f"{ischial + 0.6:.1f}–{ischial + 2.1:.1f} cm"
    stem_diff = suggested_reach - frame_reach
    suggested_stem = round(100 + stem_diff, 1)

    st.markdown("### " + text["recommend"])
    st.write(f"📐 {text['saddle_height']}：{saddle_height} cm")
    st.write(f"📏 {text['stack_result']}：{suggested_stack} mm（與車架差值：{round(suggested_stack - frame_stack, 1)} mm）")
    st.write(f"📏 {text['reach_result']}：{suggested_reach} mm（與車架差值：{round(suggested_reach - frame_reach, 1)} mm）")
    st.write(f"🤝 {text['stem_length']}：{suggested_stem} mm")
    st.write(f"👐 {text['handlebar_width']}：{handlebar_width}")
    st.write(f"🪑 {text['saddle_width']}：{saddle_width}")

st.markdown("---")
st.markdown(text["donate"])
