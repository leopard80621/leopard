import streamlit as st
import json

# 頁面設定（一定要最上面）
st.set_page_config(page_title="🚴‍♂️ 公路車尺寸建議工具", layout="centered")

# 載入語言檔
with open("language_text_options.json", "r", encoding="utf-8") as f:
    language_text = json.load(f)

language = st.selectbox("語言 / Language", list(language_text.keys()))
text = language_text[language]

# 標題與說明
st.markdown(f"<h1 style='text-align: center;'>🚴‍♂️ {text['title']}</h1>", unsafe_allow_html=True)
st.markdown(text["input_prompt"])

# 性別
gender = st.radio(text["gender"], ["男", "女"], horizontal=True)

# 收集 10 項身體數據
cols = st.columns(2)
with cols[0]:
    inseam = st.number_input(text["inseam"], min_value=40.0, max_value=110.0, step=0.5)
    height = st.number_input(text["height"], min_value=130.0, max_value=220.0, step=0.5)
    shoulder = st.number_input(text["shoulder_width"], min_value=30.0, max_value=60.0, step=0.5)
    sitbone = st.number_input(text["ischial_width"], min_value=7.0, max_value=20.0, step=0.5)
    trunk = st.number_input(text["trunk_length"], min_value=30.0, max_value=70.0, step=0.5)
with cols[1]:
    arm = st.number_input(text["arm_length"], min_value=30.0, max_value=80.0, step=0.5)
    forearm = st.number_input(text["forearm_length"], min_value=20.0, max_value=60.0, step=0.5)
    thigh = st.number_input(text["thigh_length"], min_value=30.0, max_value=80.0, step=0.5)
    lower_leg = st.number_input(text["lower_leg_length"], min_value=30.0, max_value=80.0, step=0.5)
    sternal = st.number_input(text["sternal_notch"], min_value=100.0, max_value=180.0, step=0.5)

# 車架幾何輸入
st.markdown(f"📦 {text['expected_frame_label']}")
expected_stack = st.number_input(text["expected_stack"], min_value=400.0, max_value=700.0, step=1.0)
expected_reach = st.number_input(text["expected_reach"], min_value=300.0, max_value=500.0, step=1.0)

# 計算按鈕
if st.button(text["submit"]):
    st.markdown(f"📄 {text['result_title']}")

    # 建議值計算
    saddle_height = round(inseam * 0.883, 1)
    stack = round(sternal * 1.0, 1)
    reach_factor = 2.5  # ✅ 固定值，不分性別
    reach = round(trunk / reach_factor + arm / reach_factor, 1)
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

    # Stack 差值
    stack_diff = round(stack - expected_stack, 1)
    if abs(stack_diff) <= 10:
        spacer = 0.5 if abs(stack_diff) <= 5 else 1.5
        stack_result = f"{stack} mm，與車架差值：{stack_diff} mm ✅ 相符，建議使用 {spacer} 公分墊圈"
    else:
        stack_result = f"{stack} mm，與車架差值：{stack_diff} mm ❌ 不建議，請選擇其他尺寸"

    # Reach 差值與龍頭建議
    reach_diff = round(expected_reach - reach, 1)
    if 70 <= reach_diff <= 130:
        stem = round(reach_diff / 10)
        reach_result = f"{reach} mm，與車架差值：{reach_diff} mm ✅ 建議使用 {stem} 公分龍頭"
    else:
        reach_result = f"{reach} mm，與車架差值：{reach_diff} mm ❌ 龍頭無法調整，建議更換車架"

    # 顯示建議
    st.markdown(f"🔧 {text['saddle_height']}: {saddle_height} cm")
    st.markdown(f"🔧 {text['stack']}: {stack_result}")
    st.markdown(f"🔧 {text['reach']}: {reach_result}")
    st.markdown(f"🔧 {text['bar_width']}: {bar_width} ±2 cm")
    st.markdown(f"🔧 {text['saddle_width']}: {saddle_width} ±1 cm")
    st.markdown(f"🔧 {text['crank_length']}: {crank} mm")

    # 贊助區塊
    st.markdown("---")
    st.markdown("[☕ 請我喝杯咖啡](https://paypal.me/leopardbikeadvice)")
