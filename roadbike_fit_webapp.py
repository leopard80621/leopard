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
            "trunk": ["軀幹長（cm）", "從大椎（C7）到髂脊上緣"],
            "frame_reach": ["車架 Reach（mm）", "車架幾何圖標示的 Reach 數值"]
        },
        "submit": "計算建議",
        "result_title": "📋 建議結果",
        "reach_suggest": "建議 Reach：",
        "reach_diff": "與車架 Reach 差值：",
        "reach_fit": "✅ 符合，建議使用 {stem_length} 公分龍頭",
        "reach_unfit": "❌ 差距過大，建議更換車架"
    },
    "English": {
        "title": "Road Bike Fit Recommendation Tool",
        "input_prompt": "Please enter your body measurements:",
        "gender": "Gender",
        "gender_options": ["Male", "Female"],
        "fields": {
            "trunk": ["Trunk Length (cm)", "From C7 to iliac crest"],
            "frame_reach": ["Frame Reach (mm)", "Reach value shown on geometry chart"]
        },
        "submit": "Calculate Suggestion",
        "result_title": "📋 Recommendation Result",
        "reach_suggest": "Recommended Reach:",
        "reach_diff": "Reach difference from frame:",
        "reach_fit": "✅ Match. Recommend using {stem_length} cm stem",
        "reach_unfit": "❌ Too far off. Recommend switching frame"
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

# 使用者輸入
data = {}
for key, (label, tip) in fields.items():
    data[key] = parse_float(st.text_input(f"{label} ❓", help=tip))

# 提交按鈕
if st.button(text["submit"]):
    trunk = data.get("trunk")
    frame_reach = data.get("frame_reach")

    if trunk is None or frame_reach is None:
        st.warning("請完整填寫所有欄位！" if language == "繁體中文" else "Please complete all fields!")
    else:
        st.markdown(f"### {text['result_title']}")
        recommended_reach = round(trunk * 6.0, 1)
        reach_diff = round(recommended_reach - frame_reach, 1)

        st.write(f"{text['reach_suggest']} {recommended_reach} mm")
        st.write(f"{text['reach_diff']} {reach_diff} mm")

        stem_cm = round(reach_diff / 10)
        if 7 <= stem_cm <= 12:
            st.write(text["reach_fit"].format(stem_length=stem_cm))
        else:
            st.write(text["reach_unfit"])
