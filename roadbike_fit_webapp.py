import streamlit as st
import json

# Load language options
with open("language_text_options.json", "r", encoding="utf-8") as f:
    language_options = json.load(f)

language = st.selectbox("語言 / Language", options=list(language_options.keys()))
text = language_options[language]

st.set_page_config(page_title=text["title"], layout="centered")

# Title
st.markdown(f"<h1 style='text-align: center;'>🚴 {text['title']}</h1>", unsafe_allow_html=True)
st.markdown(text["input_prompt"])

# Gender input
gender = st.radio(text["gender"], ["男", "女"], horizontal=True)

# Body measurements
inputs = {}
fields = ["inseam", "height", "shoulder", "ischial", "trunk", "arm", "forearm", "thigh", "lower_leg", "sternal"]
for field in fields:
    inputs[field] = st.number_input(text[field], min_value=0.0, format="%.2f")

# Expected bike stack and reach
st.markdown(f"📦 {text['expected_frame_label']}")
expected_stack = st.number_input(text["expected_stack"], min_value=0.0, format="%.1f")
expected_reach = st.number_input(text["expected_reach"], min_value=0.0, format="%.1f")

# Submit button
if st.button(text["submit"]):
    # Simple estimation formulas (example only)
    saddle_height = round(inputs["inseam"] * 0.885, 1)
    recommended_stack = round(inputs["height"] * 0.33 + inputs["sternal"] * 0.27, 1)
    reach_factor = 2.5 if gender == "男" else 2.35
    recommended_reach = round(inputs["trunk"] * reach_factor, 1)
    handlebar_width = round(inputs["shoulder"], 1)
    saddle_width = round(inputs["ischial"] + 5.5, 1)

    stack_diff = round(recommended_stack - expected_stack, 1)
    reach_diff = round(expected_reach - recommended_reach, 1)
    
    st.markdown(f"🧾 {text['result']}")
    st.markdown(f"📐 {text['saddle_height']}: {saddle_height} cm")
    st.markdown(f"📐 {text['recommended_stack']}: {recommended_stack} mm")
    st.markdown(f"📐 {text['recommended_reach']}: {recommended_reach} mm")
    st.markdown(f"📐 {text['recommended_handlebar']}: {handlebar_width} ±2 cm")
    st.markdown(f"🪑 {text['recommended_saddle']}: {saddle_width} cm")

    # Stack result
    if abs(stack_diff) <= 10:
        spacer = "0.5" if abs(stack_diff) <= 5 else "1"
        st.markdown(f"📐 {text['stack_diff']}: {stack_diff} mm ✅ {text['matched']}（{spacer} 公分{ text['spacer'] }）")
    else:
        st.markdown(f"📐 {text['stack_diff']}: {stack_diff} mm ❌ {text['mismatch']}")

    # Reach result
    stem_length = round(reach_diff / 10) * 10
    stem_cm = round(stem_length / 10)
    if 7 <= stem_cm <= 12:
        st.markdown(f"📐 {text['reach_diff']}: {reach_diff} mm ✅ {text['recommend_stem']}：{stem_cm} cm")
    else:
        size_note = text['recommend_resize_bigger'] if stem_cm > 12 else text['recommend_resize_smaller']
        st.markdown(f"📐 {text['reach_diff']}: {reach_diff} mm ❌ {size_note}")
