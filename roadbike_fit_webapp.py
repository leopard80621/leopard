import streamlit as st
import json

# 讀取語言包
with open("language_text_options.json", "r", encoding="utf-8") as f:
    language_text_options = json.load(f)

# 頁面設定
st.set_page_config(page_title="Roadbike Fit Recommendation Tool", layout="centered")

# 語言選擇
language = st.selectbox("語言 / Language", ["繁體中文", "English"])
text = language_text_options[language]

# 標題
st.markdown(f"<h1 style='text-align: center;'>🚴‍♂️ {text['title']}</h1>", unsafe_allow_html=True)

# 輸入資料區
st.markdown(text["input_prompt"])
gender = st.radio(text["gender"], ["男", "女"], horizontal=True)

inseam = st.number_input(text["inseam"], 60.0, 100.0, format="%.2f")
height = st.number_input(text["height"], 140.0, 210.0, format="%.2f")
shoulder = st.number_input(text["shoulder"], 30.0, 60.0, format="%.2f")
ischial = st.number_input(text["ischial"], 8.0, 20.0, format="%.2f")

# 預計購買車架資訊
st.markdown("---")
st.markdown(f"📦 {text['expected_frame_label']}")
input_stack = st.number_input(text["input_stack"], 480, 650)
input_reach = st.number_input(text["input_reach"], 350, 450)

# 計算建議
if st.button(text["calculate"]):
    st.markdown(f"### {text['results']}")

    saddle_height = round(inseam * 0.883, 1)
    suggested_stack = round((height + inseam) / 3.2, 1)
    if gender == "男":
        suggested_reach = round((height + shoulder) / 2.5, 1)
        crank = "172.5 mm" if inseam >= 85 else "170 mm" if inseam >= 80 else "165 mm"
    else:
        suggested_reach = round((height + shoulder) / 2.65, 1)
        crank = "170 mm" if inseam >= 80 else "165 mm" if inseam >= 75 else "160 mm"

    # 墊圈計算
    stack_diff = round(suggested_stack - input_stack, 1)
    if stack_diff >= 0:
        if stack_diff < 0.5:
            spacer = "0.5 cm"
        elif stack_diff < 1.5:
            spacer = "1 cm"
        else:
            spacer = "1.5 cm"
        stack_result = f"{text['diff']}{stack_diff} mm（✅ {text['matched']}，{text['spacer_note']} {spacer}）"
    else:
        stack_result = f"{text['diff']}{stack_diff} mm（❌ {text['not_matched']}）"

    # reach 計算
    reach_diff = round(input_reach - suggested_reach, 1)
    if 70 <= reach_diff <= 130:
        stem_length = round(reach_diff / 10)  # 四捨五入至整數
        if stem_length > 12:
            reach_result = f"{text['diff']}{reach_diff} mm（❌ {text['not_matched']}，{text['change_frame']}）"
        else:
            reach_result = f"{text['diff']}{reach_diff} mm（✅ {text['matched']}，{text['recommend_stem']}：{stem_length} cm）"
    else:
        reach_result = f"{text['diff']}{reach_diff} mm（❌ {text['not_matched']}，{text['change_frame']}）"

    st.markdown(f"📏 {text['saddle_height']}：{saddle_height} cm")
    st.markdown(f"🪜 {text['stack']}：{suggested_stack} mm　{stack_result}")
    st.markdown(f"📐 {text['reach']}：{suggested_reach} mm　{reach_result}")
    st.markdown(f"🤝 {text['handlebar']}：{shoulder} ± 2 cm")
    st.markdown(f"🪑 {text['ischial']}：{ischial + 2.5}-{ischial + 3.0} cm")
    st.markdown(f"🔁 {text['crank_length']}：{crank}")

# 贊助連結
st.markdown("---")
st.markdown(text["donate_note"], unsafe_allow_html=True)