import streamlit as st
import json
import math

# 頁面設定
st.set_page_config(page_title="🚴‍♂️ 公路車尺寸建議工具", layout="centered")

# 語言文字內容
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
    }
}

# 語言切換
language = st.selectbox("語言 / Language", list(language_text.keys()))
text = language_text[language]

# 顯示標題與說明
st.markdown(f"<h1 style='text-align: center;'>🚴‍♂️ {text['title']}</h1>", unsafe_allow_html=True)
st.markdown(text["input_prompt"])

# 輸入資料
gender = st.radio(text["gender"], text["gender_options"], horizontal=True)
inseam = st.number_input(text["inseam"], min_value=50.0, max_value=100.0, step=0.1)
trunk = st.number_input(text["trunk"], min_value=30.0, max_value=80.0, step=0.1)
forearm = st.number_input(text["forearm"], min_value=20.0, max_value=60.0, step=0.1)
arm = st.number_input(text["arm"], min_value=30.0, max_value=80.0, step=0.1)
thigh = st.number_input(text["thigh"], min_value=30.0, max_value=80.0, step=0.1)
leg = st.number_input(text["leg"], min_value=30.0, max_value=70.0, step=0.1)
sacrum = st.number_input(text["sacrum"], min_value=100.0, max_value=180.0, step=0.1)
height = st.number_input(text["height"], min_value=140.0, max_value=200.0, step=0.1)
shoulder = st.number_input(text["shoulder_width"], min_value=30.0, max_value=60.0, step=0.1)
sit_bone = st.number_input(text["sit_bone_width"], min_value=7.0, max_value=20.0, step=0.1)

st.markdown(f"### {text['frame_stack_label']}")
input_stack = st.number_input(text["frame_stack"], min_value=400.0, max_value=650.0, step=1.0)
input_reach = st.number_input(text["frame_reach"], min_value=300.0, max_value=450.0, step=1.0)

if st.button(text["submit"]):
    st.markdown(f"### {text['result_title']}")

    # 座墊高度估算：Inseam * 0.883（經典公式）
    saddle_height = round(inseam * 0.883, 1)
    st.markdown(f"📏 {text['saddle_height']} {saddle_height} {text['unit_cm']}")

    # Stack 建議：使用 sacrum 高度與身高比例簡化推估
    stack = round(sacrum * 0.4 + leg * 1.3, 1)
    stack_diff = round(stack - input_stack, 1)

    # 根據差值給建議：範圍 +/-15 mm 內視為合理，搭配墊圈調整
    if abs(stack_diff) <= 30:
        spacer_cm = 0.5 * round(abs(stack_diff) / 5 + 1)
        st.markdown(f"📐 {text['stack_suggest']} {stack} {text['unit_mm']}　{text['stack_diff']} {stack_diff} mm（{text['stack_comment'].format(value=spacer_cm)}）")
    else:
        st.markdown(f"📐 {text['stack_suggest']} {stack} {text['unit_mm']}　{text['stack_diff']} {stack_diff} mm（{text['stack_exceed']}）")

    # Reach 建議算法（修正後 2.5 倍軀幹長）
    reach = round(trunk * 2.5, 1)
    reach_diff = round(input_reach - reach, 1)

    # 判斷龍頭長度（標準長度 7~12 cm），每 10 mm 差距對應 1 cm 龍頭
    stem_cm = round(reach_diff / 10)
    if 7 <= stem_cm <= 12:
        st.markdown(f"📏 {text['reach_suggest']} {reach} {text['unit_mm']}　{text['reach_diff']} {reach_diff} mm（{text['reach_fit'].format(stem_length=stem_cm)}）")
    else:
        direction = "小" if reach_diff < 0 else "大"
        st.markdown(f"📏 {text['reach_suggest']} {reach} {text['unit_mm']}　{text['reach_diff']} {reach_diff} mm（{text['reach_unfit'].format(direction=direction)}）")

    # 建議把手寬度：依肩寬取整數（四捨五入）
    st.markdown(f"🤝 {text['shoulder_suggest']} {round(shoulder)} ±2 {text['unit_cm']}")

    # 建議坐墊寬度（依性別取 buffer）
    pad = 2.0 if gender == "男性" else 3.0
    sit_width = round(sit_bone + pad, 1)
    st.markdown(f"🍑 {text['sitbone_suggest']} {sit_width} {text['unit_cm']}")

    # 建議曲柄長度（依身高與性別調整）
    if gender == "男性":
        if height >= 185:
            crank = 175
        elif height >= 175:
            crank = 172.5
        elif height >= 165:
            crank = 170
        elif height >= 155:
            crank = 165
        else:
            crank = 160
    else:
        if height >= 175:
            crank = 172.5
        elif height >= 165:
            crank = 170
        elif height >= 155:
            crank = 165
        else:
            crank = 160

    st.markdown(f"🦵 {text['crank_suggest']} {crank} mm")
