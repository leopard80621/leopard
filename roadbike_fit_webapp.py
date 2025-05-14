import streamlit as st

# 頁面設定
st.set_page_config(page_title="🚴‍♂️ Road Bike Fit Tool", layout="centered")

# 中英語言內容（含骨標記說明）
language_text = {
    "繁體中文": {
        "title": "公路車尺寸建議工具",
        "input_prompt": "請輸入以下身體數據：",
        "gender": "性別",
        "gender_options": ["男性", "女性"],
        "fields": {
            "inseam": ["跨下長（cm）", "腳跟到會陰的垂直距離"],
            "trunk": ["軀幹長（cm）", "從大椎（C7）到髂脊上緣"],
            "forearm": ["前臂長（cm）", "手肘外上髁到橈骨莖突"],
            "arm": ["手臂長（cm）", "肩峰到橈骨莖突"],
            "thigh": ["大腿長（cm）", "髂前上棘到髕骨上緣"],
            "leg": ["小腿長（cm）", "髕骨下緣到內踝"],
            "sacrum": ["胸骨凹口高（cm）", "腳跟到胸骨凹口"],
            "height": ["身高（cm）", "身體總長"],
            "shoulder": ["肩寬（cm）", "左右肩峰之間的距離"],
            "sitbone": ["坐骨寬（cm）", "坐骨之間最寬的距離"]
        },
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
        "input_prompt": "Please enter your body measurements:",
        "gender": "Gender",
        "gender_options": ["Male", "Female"],
        "fields": {
            "inseam": ["Inseam (cm)", "Vertical distance from heel to crotch"],
            "trunk": ["Trunk Length (cm)", "From C7 vertebra to iliac crest"],
            "forearm": ["Forearm Length (cm)", "From lateral epicondyle to radial styloid"],
            "arm": ["Arm Length (cm)", "From acromion to radial styloid"],
            "thigh": ["Thigh Length (cm)", "From ASIS to top of patella"],
            "leg": ["Lower Leg Length (cm)", "From bottom of patella to medial malleolus"],
            "sacrum": ["Sternal Notch Height (cm)", "From heel to sternal notch"],
            "height": ["Height (cm)", "Total body height"],
            "shoulder": ["Shoulder Width (cm)", "Distance between both acromions"],
            "sitbone": ["Ischial Width (cm)", "Widest distance between sit bones"]
        },
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
        "stack_comment": "✅ Matches. Recommend using {value} cm spacer",
        "stack_exceed": "❌ Too much difference. Suggest changing frame",
        "reach_fit": "✅ Matches. Recommend using {stem_length} cm stem",
        "reach_unfit": "❌ Mismatch. Consider switching to a {direction} size frame",
        "shoulder_suggest": "Recommended Handlebar Width:",
        "sitbone_suggest": "Recommended Saddle Width:",
        "crank_suggest": "Recommended Crank Length:",
        "unit_cm": "cm",
        "unit_mm": "mm"
    }
}

# 語言選擇與內容載入
language = st.selectbox("語言 / Language", list(language_text.keys()))
text = language_text[language]
fields = text["fields"]

st.markdown(f"<h1 style='text-align: center;'>🚴‍♂️ {text['title']}</h1>", unsafe_allow_html=True)
st.markdown(text["input_prompt"])

# 工具：安全轉 float
def parse_float(val): 
    try: return float(val)
    except: return None

# 性別
gender = st.radio(text["gender"], text["gender_options"], horizontal=True)

# 輸入欄位（帶有 ? 說明）
user_inputs = {}
for key, (label, tip) in fields.items():
    user_inputs[key] = parse_float(st.text_input(f"{label} ❓", help=tip))

# 車架幾何輸入
st.markdown(f"### {text['frame_stack_label']}")
input_stack = parse_float(st.text_input(text["frame_stack"]))
input_reach = parse_float(st.text_input(text["frame_reach"]))

# 計算建議
if st.button(text["submit"]):
    inputs = list(user_inputs.values()) + [input_stack, input_reach]
    if any(v is None for v in inputs):
        st.warning("請完整填寫所有欄位！" if language == "繁體中文" else "Please complete all fields!")
    else:
        st.markdown(f"### {text['result_title']}")

        inseam = user_inputs["inseam"]
        trunk = user_inputs["trunk"]
        arm = user_inputs["arm"]
        thigh = user_inputs["thigh"]
        leg = user_inputs["leg"]
        sacrum = user_inputs["sacrum"]
        height = user_inputs["height"]
        shoulder = user_inputs["shoulder"]
        sit_bone = user_inputs["sitbone"]

        # 建議座墊高度
        saddle_height = round(inseam * 0.883, 1)
        st.markdown(f"📏 {text['saddle_height']} {saddle_height} {text['unit_cm']}")

        # 建議 Stack 計算
        stack = round((sacrum + leg) * 2.8, 1)
        stack_diff = round(stack - input_stack, 1)
        if abs(stack_diff) <= 30:
            spacer_cm = 0.5 * round(abs(stack_diff) / 5 + 1)
            st.markdown(f"📐 {text['stack_suggest']} {stack} {text['unit_mm']}　{text['stack_diff']} {stack_diff} mm（{text['stack_comment'].format(value=spacer_cm)}）")
        else:
            st.markdown(f"📐 {text['stack_suggest']} {stack} {text['unit_mm']}　{text['stack_diff']} {stack_diff} mm（{text['stack_exceed']}）")

        # 建議 Reach 計算
        reach = round(trunk * 6.0, 1)  # trunk in cm, reach in mm via empirical ratio
        reach_diff = round(input_reach - reach, 1)
        stem_cm = round(reach_diff / 10)

        if 7 <= stem_cm <= 12:
            st.markdown(f"📏 {text['reach_suggest']} {reach} {text['unit_mm']}　{text['reach_diff']} {reach_diff} mm（{text['reach_fit'].format(stem_length=stem_cm)}）")
        else:
            direction = "小" if reach_diff < 0 else "大" if language == "繁體中文" else "smaller" if reach_diff < 0 else "larger"
            st.markdown(f"📏 {text['reach_suggest']} {reach} {text['unit_mm']}　{text['reach_diff']} {reach_diff} mm（{text['reach_unfit'].format(direction=direction)}）")

        # 把手寬度
        st.markdown(f"🤝 {text['shoulder_suggest']} {round(shoulder)} ±2 {text['unit_cm']}")

        # 坐墊寬度
        pad = 2.0 if gender in ["男性", "Male"] else 3.0
        sit_width = round(sit_bone + pad, 1)
        st.markdown(f"🍑 {text['sitbone_suggest']} {sit_width} {text['unit_cm']}")

        # 曲柄建議
        if gender in ["男性", "Male"]:
            crank = 175 if height >= 185 else 172.5 if height >= 175 else 170 if height >= 165 else 165 if height >= 155 else 160
        else:
            crank = 172.5 if height >= 175 else 170 if height >= 165 else 165 if height >= 155 else 160
        st.markdown(f"🦵 {text['crank_suggest']} {crank} mm")
