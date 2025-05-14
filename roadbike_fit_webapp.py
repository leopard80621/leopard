import streamlit as st
import json

# 頁面設定
st.set_page_config(page_title="🚴‍♂️ 公路車尺寸建議工具", layout="centered")

# 載入語言設定
language_text = {
    "繁體中文": {
        "title": "公路車尺寸建議工具",
        "input_prompt": "請輸入以下身體數據：",
        "gender": "性別",
        "gender_options": ["男性", "女性"],
        "inseam": "跨下長（cm）",
        "trunk": "軀幹長（cm）",
        "forearm": "前臂長（cm）",
        "arm": "手臂長（cm）",
        "thigh": "大腿長（cm）",
        "leg": "小腿長（cm）",
        "sacrum": "胸骨凹口高（cm）",
        "height": "身高（cm）",
        "shoulder_width": "肩寬（cm）",
        "sit_bone_width": "坐骨寬（cm）",
        "frame_stack_label": "📦 預計購買的車架幾何（Stack / Reach）",
        "frame_stack": "車架 Stack (mm)",
        "frame_reach": "車架 Reach (mm)",
        "submit": "計算建議",
        "result_title": "📋 建議結果",
        "saddle_height": "建議座墊高度：",
        "stack_suggest": "建議 Stack：",
        "reach_suggest": "建議 Reach：",
        "stack_diff": "與車架 Stack 差值：",
        "reach_diff": "與車架 Reach 差值：",
        "stem_suggest": "建議使用龍頭長度：約",
        "stack_comment": "✅ 相符建議使用 {value} 公分墊圈",
        "stack_exceed": "❌ 差距過大，建議更換車架",
        "reach_fit": "✅ 符合，建議使用 {stem_length} 公分龍頭",
        "reach_unfit": "❌ 不符，建議更換更 {direction} 尺寸車架",
        "shoulder_suggest": "建議把手寬度：",
        "sitbone_suggest": "建議坐墊寬度：",
        "crank_suggest": "建議曲柄長度：",
        "unit_cm": "cm",
        "unit_mm": "mm"
    },
    "English": {
        "title": "Road Bike Fit Recommendation Tool",
        "input_prompt": "Please enter the following body measurements:",
        "gender": "Gender",
        "gender_options": ["Male", "Female"],
        "inseam": "Inseam (cm)",
        "trunk": "Trunk Length (cm)",
        "forearm": "Forearm Length (cm)",
        "arm": "Arm Length (cm)",
        "thigh": "Thigh Length (cm)",
        "leg": "Lower Leg Length (cm)",
        "sacrum": "Sternal Notch Height (cm)",
        "height": "Height (cm)",
        "shoulder_width": "Shoulder Width (cm)",
        "sit_bone_width": "Ischial Width (cm)",
        "frame_stack_label": "📦 Target Frame Geometry (Stack / Reach)",
        "frame_stack": "Frame Stack (mm)",
        "frame_reach": "Frame Reach (mm)",
        "submit": "Calculate Suggestion",
        "result_title": "📋 Recommendation Result",
        "saddle_height": "Recommended Saddle Height:",
        "stack_suggest": "Recommended Stack:",
        "reach_suggest": "Recommended Reach:",
        "stack_diff": "Stack difference from frame:",
        "reach_diff": "Reach difference from frame:",
        "stem_suggest": "Suggested Stem Length:",
        "stack_comment": "✅ Matches. Recommend using {value} cm spacer",
        "stack_exceed": "❌ Too large. Suggest changing frame",
        "reach_fit": "✅ Matches. Recommend using {stem_length} cm stem",
        "reach_unfit": "❌ Mismatch. Recommend switching to a {direction} frame size",
        "shoulder_suggest": "Recommended Handlebar Width:",
        "sitbone_suggest": "Recommended Saddle Width:",
        "crank_suggest": "Recommended Crank Length:",
        "unit_cm": "cm",
        "unit_mm": "mm"
    }
}

# 語言切換
language = st.selectbox("語言 / Language", list(language_text.keys()))
text = language_text[language]

st.markdown(f"<h1 style='text-align: center;'>🚴‍♂️ {text['title']}</h1>", unsafe_allow_html=True)
st.markdown(text["input_prompt"])

# 工具：轉為 float，容錯空白輸入
def parse_float(val):
    try:
        return float(val)
    except:
        return None

gender = st.radio(text["gender"], text["gender_options"], horizontal=True)
inseam = parse_float(st.text_input(text["inseam"]))
trunk = parse_float(st.text_input(text["trunk"]))
forearm = parse_float(st.text_input(text["forearm"]))
arm = parse_float(st.text_input(text["arm"]))
thigh = parse_float(st.text_input(text["thigh"]))
leg = parse_float(st.text_input(text["leg"]))
sacrum = parse_float(st.text_input(text["sacrum"]))
height = parse_float(st.text_input(text["height"]))
shoulder = parse_float(st.text_input(text["shoulder_width"]))
sit_bone = parse_float(st.text_input(text["sit_bone_width"]))
input_stack = parse_float(st.text_input(text["frame_stack"]))
input_reach = parse_float(st.text_input(text["frame_reach"]))

if st.button(text["submit"]):
    inputs = [inseam, trunk, arm, thigh, leg, sacrum, height, shoulder, sit_bone, input_stack, input_reach]
    if any(v is None for v in inputs):
        st.warning("請完整填寫所有欄位！")
    else:
        st.markdown(f"### {text['result_title']}")

        saddle_height = round(inseam * 0.883, 1)
        st.markdown(f"📏 {text['saddle_height']} {saddle_height} {text['unit_cm']}")

        stack = round(sacrum * 0.4 + leg * 1.3, 1)
        stack_diff = round(stack - input_stack, 1)
        if abs(stack_diff) <= 30:
            spacer_cm = 0.5 * round(abs(stack_diff) / 5 + 1)
            st.markdown(f"📐 {text['stack_suggest']} {stack} {text['unit_mm']}　{text['stack_diff']} {stack_diff} mm（{text['stack_comment'].format(value=spacer_cm)}）")
        else:
            st.markdown(f"📐 {text['stack_suggest']} {stack} {text['unit_mm']}　{text['stack_diff']} {stack_diff} mm（{text['stack_exceed']}）")

        reach = round(trunk * 2.5, 1)
        reach_diff = round(input_reach - reach, 1)
        stem_cm = round(reach_diff / 10)
        if 7 <= stem_cm <= 12:
            st.markdown(f"📏 {text['reach_suggest']} {reach} {text['unit_mm']}　{text['reach_diff']} {reach_diff} mm（{text['reach_fit'].format(stem_length=stem_cm)}）")
        else:
            direction = "小" if reach_diff < 0 else "大"
            st.markdown(f"📏 {text['reach_suggest']} {reach} {text['unit_mm']}　{text['reach_diff']} {reach_diff} mm（{text['reach_unfit'].format(direction=direction)}）")

        st.markdown(f"🤝 {text['shoulder_suggest']} {round(shoulder)} ±2 {text['unit_cm']}")
        pad = 2.0 if gender == "男性" or gender == "Male" else 3.0
        sit_width = round(sit_bone + pad, 1)
        st.markdown(f"🍑 {text['sitbone_suggest']} {sit_width} {text['unit_cm']}")

        if gender in ["男性", "Male"]:
            crank = 175 if height >= 185 else 172.5 if height >= 175 else 170 if height >= 165 else 165 if height >= 155 else 160
        else:
            crank = 172.5 if height >= 175 else 170 if height >= 165 else 165 if height >= 155 else 160
        st.markdown(f"🦵 {text['crank_suggest']} {crank} mm")
