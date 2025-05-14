import streamlit as st
import json

# ---------- 頁面設定 ----------
st.set_page_config(page_title="🚴‍♂️ Road Bike Fit Tool", layout="centered")

# ---------- 載入語言選項 ----------
with open("language_text_options.json", "r", encoding="utf-8") as f:
    language_text = json.load(f)

# ---------- 語言與欄位 ----------
language = st.selectbox("Language / 語言", list(language_text.keys()))
text = language_text[language]
fields = text["fields"]

st.markdown(f"<h1 style='text-align: center;'>🚴‍♂️ {text['title']}</h1>", unsafe_allow_html=True)
st.markdown(text["input_prompt"])

# ---------- 安全轉換函數 ----------
def parse_float(val):
    try:
        return float(val)
    except:
        return None

# ---------- 性別與車架尺寸 ----------
gender = st.radio(text["gender"], text["gender_options"], horizontal=True)
frame_size = st.selectbox(text["frame_size_label"], ["XS", "S", "M", "L", "XL"])
default_stem_dict = {"XS": 80, "S": 90, "M": 100, "L": 110, "XL": 120}
default_stem = default_stem_dict[frame_size]

# ---------- 身體資料輸入 ----------
user_inputs = {}
for key, (label, tip) in fields.items():
    user_inputs[key] = parse_float(st.text_input(f"{label} ❓", help=tip))

input_stack = parse_float(st.text_input(text["stack"]))
input_reach = parse_float(st.text_input(text["reach"]))

# ---------- 計算建議 ----------
if st.button(text["submit"]):
    inputs = list(user_inputs.values()) + [input_stack, input_reach]
    if any(v is None for v in inputs):
        st.warning("請完整填寫所有欄位！" if language == "繁體中文" else "Please complete all fields!")
    else:
        st.markdown(f"### {text['result_title']}")

        trunk = user_inputs["trunk"]
        sacrum = user_inputs["sacrum"]
        leg = user_inputs["leg"]

        # Stack 計算
        stack = round((sacrum + leg) * 2.8, 1)
        stack_diff = round(stack - input_stack, 1)
        if abs(stack_diff) <= 30:
            spacer = 0.5 * round(abs(stack_diff) / 5 + 1)
            st.markdown(f"📐 {text['stack_suggest']} {stack} mm　{text['stack_diff']} {stack_diff} mm（{text['stack_ok'].format(value=spacer)}）")
        else:
            st.markdown(f"📐 {text['stack_suggest']} {stack} mm　{text['stack_diff']} {stack_diff} mm（{text['stack_fail']}）")

        # Reach 計算
        reach = round(trunk * 6.0, 1)
        reach_diff = round(reach - input_reach, 1)
        st.markdown(f"📏 {text['reach_suggest']} {reach} mm　{text['reach_diff']} {reach_diff} mm（預設龍頭長度為 {default_stem} mm）")

        # 額外建議：把手與坐墊寬度
        shoulder = user_inputs.get("shoulder")
        if shoulder is not None:
            st.markdown(text["shoulder_suggest"].format(value=round(shoulder)))

        sitbone = user_inputs.get("sitbone")
        if sitbone is not None:
            pad = 2.0 if gender in ["男性", "Male"] else 3.0
            st.markdown(text["sitbone_suggest"].format(value=round(sitbone + pad, 1)))

        # 贊助連結
        st.markdown("---")
        st.markdown(f"{text['support']} [☕ Buy here]({text['support_link']})")
