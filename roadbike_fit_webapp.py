import streamlit as st

# 頁面設定
st.set_page_config(page_title="🚴‍♂️ 公路車尺寸建議工具", layout="centered")

# 多語言字典
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
    }
}

# 語言選擇
language = st.selectbox("語言 / Language", list(language_text.keys()))
text = language_text[language]
fields = text["fields"]

# 顯示標題與說明
st.markdown(f"<h1 style='text-align: center;'>🚴‍♂️ {text['title']}</h1>", unsafe_allow_html=True)
st.markdown(text["input_prompt"])

# 工具：轉為 float，容錯空白輸入
def parse_float(val): 
    try: return float(val)
    except: return None

# 性別
gender = st.radio(text["gender"], text["gender_options"], horizontal=True)

# 動態欄位（含 tooltip）
user_inputs = {}
for key, (label, tip) in fields.items():
    user_inputs[key] = parse_float(st.text_input(f"{label} ❓", help=tip))

# 車架幾何輸入
st.markdown(f"### {text['frame_stack_label']}")
input_stack = parse_float(st.text_input(text["frame_stack"]))
input_reach = parse_float(st.text_input(text["frame_reach"]))

if st.button(text["submit"]):
    inputs = list(user_inputs.values()) + [input_stack, input_reach]
    if any(v is None for v in inputs):
        st.warning("請完整填寫所有欄位！")
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
        pad = 2.0 if gender in ["男性", "Male"] else 3.0
        sit_width = round(sit_bone + pad, 1)
        st.markdown(f"🍑 {text['sitbone_suggest']} {sit_width} {text['unit_cm']}")

        if gender in ["男性", "Male"]:
            crank = 175 if height >= 185 else 172.5 if height >= 175 else 170 if height >= 165 else 165 if height >= 155 else 160
        else:
            crank = 172.5 if height >= 175 else 170 if height >= 165 else 165 if height >= 155 else 160
        st.markdown(f"🦵 {text['crank_suggest']} {crank} mm")
