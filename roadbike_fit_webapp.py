import streamlit as st
import json

# 頁面設定
st.set_page_config(page_title="🚴‍♂️ 公路車尺寸建議工具", layout="centered")

# 載入語言設定
with open("language_text_options.json", "r", encoding="utf-8") as f:
    language_text = json.load(f)

language = st.selectbox("語言 / Language", list(language_text.keys()))
text = language_text[language]

# 標題與提示文字
st.markdown(f"<h1 style='text-align: center;'>🚴‍♂️ {text['title']}</h1>", unsafe_allow_html=True)
st.markdown(text["input_prompt"])

# 性別
gender = st.radio(text["gender"], ["男", "女"], horizontal=True)

# 10 項量測輸入與 Tooltip 顯示
cols = st.columns(2)
with cols[0]:
    inseam = st.number_input(f"{text['inseam']} ❓", help=text["inseam_tooltip"], min_value=40.0, max_value=110.0, step=0.5)
    height = st.number_input(f"{text['height']} ❓", help=text["height_tooltip"], min_value=130.0, max_value=220.0, step=0.5)
    shoulder = st.number_input(f"{text['shoulder_width']} ❓", help=text["shoulder_width_tooltip"], min_value=30.0, max_value=60.0, step=0.5)
    sitbone = st.number_input(f"{text['ischial_width']} ❓", help=text["ischial_width_tooltip"], min_value=7.0, max_value=20.0, step=0.5)
    trunk = st.number_input(f"{text['trunk_length']} ❓", help=text["trunk_length_tooltip"], min_value=30.0, max_value=70.0, step=0.5)
with cols[1]:
    arm = st.number_input(f"{text['arm_length']} ❓", help=text["arm_length_tooltip"], min_value=30.0, max_value=80.0, step=0.5)
    forearm = st.number_input(f"{text['forearm_length']} ❓", help=text["forearm_length_tooltip"], min_value=20.0, max_value=60.0, step=0.5)
    thigh = st.number_input(f"{text['thigh_length']} ❓", help=text["thigh_length_tooltip"], min_value=30.0, max_value=80.0, step=0.5)
    lower_leg = st.number_input(f"{text['lower_leg_length']} ❓", help=text["lower_leg_length_tooltip"], min_value=30.0, max_value=80.0, step=0.5)
    sternal = st.number_input(f"{text['sternal_notch']} ❓", help=text["sternal_notch_tooltip"], min_value=100.0, max_value=180.0, step=0.5)

# 預計購買的車架 Stack / Reach
st.markdown(f"📦 {text['expected_frame_label']}")
expected_stack = st.number_input(f"{text['expected_stack']} (mm)", min_value=400.0, max_value=700.0, step=1.0)
expected_reach = st.number_input(f"{text['expected_reach']} (mm)", min_value=300.0, max_value=500.0, step=1.0)

# 計算按鈕
if st.button(text["submit"]):
    st.markdown(f"📄 {text['result_title']}")

    # 計算建議值
    saddle_height = round(inseam * 0.883, 1)
    stack = round(sternal, 1)
    reach = round((trunk + arm) / 2.5, 1)  # ✅ 固定使用 2.5
    bar_width = round(shoulder, 1)
    saddle_width = round(sitbone + (2.0 if gender == "女" else 1.0), 1)

    # 曲柄長度建議
    leg_length = thigh + lower_leg
    if leg_length < 68:
        crank = 160
    elif leg_length < 73:
        crank = 165
    elif leg_length < 78:
        crank = 170
    elif leg_length < 83:
        crank = 172.5
    else:
        crank = 175

    # Stack 差值與建議
    stack_diff = round(stack - expected_stack, 1)
    if abs(stack_diff) <= 10:
        spacer = 0.5 if abs(stack_diff) <= 5 else 1.5
        stack_result = f"{stack} mm，與車架差值：{stack_diff} mm ✅ {text['match']}，建議使用 {spacer} 公分墊圈"
    else:
        stack_result = f"{stack} mm，與車架差值：{stack_diff} mm ❌ {text['mismatch']}"

    # Reach 差值與建議
    reach_diff = round(expected_reach - reach, 1)
    if 70 <= reach_diff <= 130:
        stem = round(reach_diff / 10)
        reach_result = f"{reach} mm，與車架差值：{reach_diff} mm ✅ {text['match']}，建議使用 {stem} 公分龍頭"
    else:
        reach_result = f"{reach} mm，與車架差值：{reach_diff} mm ❌ {text['mismatch']}，{text['suggest_frame_change']}"

    # 顯示建議
    st.markdown(f"🔧 {text['saddle_height']}: {saddle_height} cm")
    st.markdown(f"🔧 {text['stack']}: {stack_result}")
    st.markdown(f"🔧 {text['reach']}: {reach_result}")
    st.markdown(f"🔧 {text['bar_width']}: {bar_width} ±2 cm")
    st.markdown(f"🔧 {text['saddle_width']}: {saddle_width} ±1 cm")
    st.markdown(f"🔧 {text['crank_length']}: {crank} mm")

    # 贊助按鈕
    st.markdown("---")
    st.markdown(f"[{text['sponsor_text']}](https://paypal.me/leopardbikeadvice)")
