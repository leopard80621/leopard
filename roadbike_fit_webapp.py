import streamlit as st

# ---------- 頁面設定 ----------
st.set_page_config(page_title="🚴‍♂️ Road Bike Fit Tool", layout="centered")

# ---------- 語言切換 ----------
language_text = {
    "繁體中文": {
        "title": "公路車尺寸建議工具",
        "input_prompt": "請輸入以下身體數據：",
        "gender": "性別",
        "gender_options": ["男性", "女性"],
        "frame_size_label": "📏 預計購買的車架尺寸",
        "fields": {
            "inseam": ["跨下長（cm）", "腳跟到會陰的垂直距離"],
            "trunk": ["軀幹長（cm）", "C7到髂脊上緣的距離"],
            "leg": ["小腿長（cm）", "髕骨下緣到內踝"],
            "sacrum": ["胸骨凹口高（cm）", "腳跟到胸骨凹口的高度"],
            "height": ["身高（cm）", "身體總長"],
            "shoulder": ["肩寬（cm）", "左右肩峰之間的距離"],
            "sitbone": ["坐骨寬（cm）", "坐骨之間最寬的距離"]
        },
        "stack": "車架 Stack (mm)",
        "reach": "車架 Reach (mm)",
        "submit": "計算建議",
        "result_title": "📋 建議結果",
        "stack_suggest": "建議 Stack：",
        "reach_suggest": "建議 Reach：",
        "stack_diff": "與車架 Stack 差值：",
        "reach_diff": "與車架 Reach 差值：",
        "stack_ok": "✅ 相符，建議使用 {value} cm 墊圈",
        "stack_fail": "❌ 差距太大，建議更換車架",
        "reach_fit": "✅ 可用 {required} mm 龍頭，與預設 {default} mm 龍頭差 {diff} mm → 可使用預設龍頭",
        "reach_unfit": "❌ 需要 {required} mm 龍頭，預設為 {default} mm → 建議使用{direction}龍頭或更換車架尺寸",
        "longer": "更長",
        "shorter": "更短",
        "shoulder_suggest": "建議把手寬度：{value} cm ±2 cm",
        "sitbone_suggest": "建議坐墊寬度：{value} cm",
        "support": "☕ 如果這個工具對你有幫助，歡迎請我喝杯咖啡：",
        "support_link": "https://paypal.me/leopardbikeadvice",
        "unit_mm": "mm"
    },
    "English": {
        "title": "Road Bike Fit Recommendation Tool",
        "input_prompt": "Please enter your body measurements:",
        "gender": "Gender",
        "gender_options": ["Male", "Female"],
        "frame_size_label": "📏 Target Frame Size",
        "fields": {
            "inseam": ["Inseam (cm)", "Vertical distance from heel to crotch"],
            "trunk": ["Trunk Length (cm)", "Distance from C7 to iliac crest"],
            "leg": ["Lower Leg Length (cm)", "From bottom of patella to medial malleolus"],
            "sacrum": ["Sternal Notch Height (cm)", "From heel to sternal notch"],
            "height": ["Height (cm)", "Total body height"],
            "shoulder": ["Shoulder Width (cm)", "Distance between both acromions"],
            "sitbone": ["Ischial Width (cm)", "Widest distance between sit bones"]
        },
        "stack": "Frame Stack (mm)",
        "reach": "Frame Reach (mm)",
        "submit": "Calculate Suggestion",
        "result_title": "📋 Recommendation Result",
        "stack_suggest": "Recommended Stack:",
        "reach_suggest": "Recommended Reach:",
        "stack_diff": "Stack difference from frame:",
        "reach_diff": "Reach difference from frame:",
        "stack_ok": "✅ Match. Use a {value} cm spacer",
        "stack_fail": "❌ Too far off. Consider changing frame",
        "reach_fit": "✅ Recommended {required} mm stem, difference from default {default} mm is {diff} mm → Default stem is acceptable",
        "reach_unfit": "❌ Needs {required} mm stem, default is {default} mm → Consider a {direction} stem or changing frame size",
        "longer": "longer",
        "shorter": "shorter",
        "shoulder_suggest": "Recommended handlebar width: {value} cm ±2 cm",
        "sitbone_suggest": "Recommended saddle width: {value} cm",
        "support": "☕ If this tool helps you, consider buying me a coffee:",
        "support_link": "https://paypal.me/leopardbikeadvice",
        "unit_mm": "mm"
    }
}

# ---------- 計算建議 ----------
# 最後部分加入：
# 把手與坐墊建議顯示
shoulder = user_inputs.get("shoulder")
sitbone = user_inputs.get("sitbone")
if shoulder:
    st.markdown(text["shoulder_suggest"].format(value=round(shoulder)))
if sitbone:
    pad = 2.0 if language_text[language]["gender_options"][0] in ["男性", "Male"] else 3.0
    st.markdown(text["sitbone_suggest"].format(value=round(sitbone + pad, 1)))

# 支援贊助連結
st.markdown("---")
st.markdown(f"{text['support']} [☕ Buy here]({text['support_link']})")
