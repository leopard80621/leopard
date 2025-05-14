
import streamlit as st
import json

# 頁面設定應在所有 Streamlit 呼叫之前
st.set_page_config(page_title="🚴‍♂️ 公路車尺寸建議工具", layout="centered")

# 載入語言選項
with open("language_text_options.json", "r", encoding="utf-8") as f:
    language_text = json.load(f)

language = st.selectbox("語言 / Language", list(language_text.keys()))
text = language_text[language]

# 顯示標題與說明
st.markdown(f"<h1 style='text-align: center;'>🚴‍♂️ {text['title']}</h1>", unsafe_allow_html=True)
st.markdown(text["input_prompt"])

# 性別選擇
gender = st.radio(text["gender"], ["男", "女"], horizontal=True)

# 10項輸入資料
input_fields = [
    ("inseam", text["inseam"]),
    ("height", text["height"]),
    ("shoulder", text["shoulder"]),
    ("ischial", text["ischial"]),
    ("trunk", text["trunk"]),
    ("arm", text["arm"]),
    ("thigh", text["thigh"]),
    ("lower_leg", text["lower_leg"]),
    ("sternal_notch", text["sternal_notch"]),
    ("forearm", text["forearm"]),
]
inputs = {}
cols = st.columns(2)
for i, (key, label) in enumerate(input_fields):
    col = cols[i % 2]
    with col:
        inputs[key] = st.number_input(f"{label} (cm)", min_value=0.0, step=0.1, key=key)

# 車架幾何輸入
st.markdown(f"📦 {text['expected_frame_label']}")
frame_stack = st.number_input("車架 Stack (mm)", min_value=0.0, step=1.0)
frame_reach = st.number_input("車架 Reach (mm)", min_value=0.0, step=1.0)

if st.button(text["calculate"]):
    st.markdown(f"🧾 {text['result_title']}")

    inseam = inputs["inseam"]
    height = inputs["height"]
    shoulder = inputs["shoulder"]
    ischial = inputs["ischial"]
    trunk = inputs["trunk"]
    arm = inputs["arm"]
    thigh = inputs["thigh"]
    lower_leg = inputs["lower_leg"]
    sternal_notch = inputs["sternal_notch"]
    forearm = inputs["forearm"]

    saddle_height = round(inseam * 0.955, 1)
    reach_estimate = round(trunk + arm - (2.5 if gender == "女" else 2.96), 1)
    stack_estimate = round(sternal_notch - (0.76 * inseam), 1)
    handlebar_width = round(shoulder, 1)
    saddle_width = round(ischial, 1)

    leg_length = thigh + lower_leg
    crank_suggestion = ""
    if gender == "女":
        if leg_length < 68:
            crank_suggestion = "160 mm"
        elif leg_length <= 72:
            crank_suggestion = "165 mm"
        elif leg_length <= 76:
            crank_suggestion = "170 mm"
        else:
            crank_suggestion = "172.5 mm"
    else:
        if leg_length < 70:
            crank_suggestion = "165 mm"
        elif leg_length <= 75:
            crank_suggestion = "170 mm"
        elif leg_length <= 80:
            crank_suggestion = "172.5 mm"
        else:
            crank_suggestion = "175 mm"

    # 輸出建議
    st.write(f"📏 建議座墊高度：約 {saddle_height} cm")
    st.write(f"📏 建議 Stack：約 {stack_estimate} mm")
    st.write(f"📏 建議 Reach：約 {reach_estimate} mm")
    st.write(f"📏 建議把手寬度：約 {handlebar_width} cm")
    st.write(f"📏 建議坐墊寬度：約 {saddle_width} cm")
    st.write(f"📏 建議曲柄長度：{crank_suggestion}")

    # Stack 比較
    stack_diff = round(stack_estimate - frame_stack, 1)
    if abs(stack_diff) <= 15:
        spacer = 1.5 if abs(stack_diff) >= 1.0 else 0.5
        st.write(f"📐 與車架 Stack 差值：{stack_diff} mm（✅ 相符建議使用 {spacer} 公分墊圈）")
    else:
        st.write(f"📐 與車架 Stack 差值：{stack_diff} mm（⚠️ 建議考慮其他幾何）")

    # Reach 比較與龍頭建議
    reach_diff = round(frame_reach - reach_estimate, 1)
    if abs(reach_diff) > 40:
        st.write(f"📐 與車架 Reach 差值：{reach_diff} mm（❌ 龍頭難以補足，建議更換車架）")
    else:
        stem_length = round(reach_diff / 10) + 10
        if 7 <= stem_length <= 12:
            st.write(f"📐 與車架 Reach 差值：{reach_diff} mm（✅ 建議使用 {stem_length} cm 龍頭）")
        else:
            st.write(f"📐 與車架 Reach 差值：{reach_diff} mm（⚠️ 龍頭長度 {stem_length} cm 不建議使用）")

    # 支援贊助
    st.markdown("---")
    st.markdown("[☕ 請我喝杯咖啡](https://paypal.me/leopardbikeadvice)")
