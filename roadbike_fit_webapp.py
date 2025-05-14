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

# 其餘頁面邏輯可在這裡繼續...
