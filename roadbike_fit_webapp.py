
import streamlit as st

# ======================
# ⚙️ 1. 頁面基本設定
# ======================
st.set_page_config(page_title="公路車尺寸建議工具", layout="centered")

# ======================
# 🌐 2. 中英文語系切換
# ======================
lang = st.selectbox("語言 / Language", ["繁體中文", "English"])
is_tw = lang == "繁體中文"

# ======================
# 📄 3. 多語言文字定義
# ======================
text = {
    "title": "公路車尺寸建議工具" if is_tw else "Road Bike Fit Recommendation Tool",
    "instruction": "請輸入下列身體尺寸資料：" if is_tw else "Please enter the following body measurements:",
    "gender": "性別" if is_tw else "Gender",
    "male": "男性" if is_tw else "Male",
    "female": "女性" if is_tw else "Female",
    "inseam": "跨下長（cm）" if is_tw else "Inseam (cm)",
    "height": "身高（cm）" if is_tw else "Height (cm)",
    "shoulder": "肩寬（cm）" if is_tw else "Shoulder Width (cm)",
    "ischial": "坐骨寬（cm）" if is_tw else "Ischial Width (cm)",
    "stack": "車架 Stack (mm)",
    "reach": "車架 Reach (mm)",
    "calculate": "計算建議" if is_tw else "Get Recommendation",
    "result": "📄 建議結果" if is_tw else "📄 Recommended Fit",
    "saddle_height": "建議座墊高度",
    "stack_result": "建議 Stack",
    "reach_result": "建議 Reach",
    "spacer": "與車架 Stack 差值",
    "stem": "與車架 Reach 差值",
    "handlebar": "建議把手寬度",
    "saddle_width": "建議坐墊寬度",
    "crank": "建議曲柄長度",
    "donate": "☕️ 歡迎贊助我一杯咖啡：" if is_tw else "☕️ Buy me a coffee:",
}

# ======================
# 🧮 4. 使用者輸入
# ======================
st.title(text["title"])
st.markdown(f"### {text['instruction']}")

gender = st.selectbox(text["gender"], [text["male"], text["female"]])

col1, col2 = st.columns(2)
with col1:
    inseam = st.number_input(text["inseam"], min_value=50.0, max_value=120.0, step=0.5)
    shoulder = st.number_input(text["shoulder"], min_value=30.0, max_value=60.0, step=0.5)
with col2:
    height = st.number_input(text["height"], min_value=140.0, max_value=200.0, step=0.5)
    ischial = st.number_input(text["ischial"], min_value=8.0, max_value=20.0, step=0.5)

st.markdown("---")
st.markdown("📦 **預計購買的車架幾何（Stack / Reach）**")
col3, col4 = st.columns(2)
with col3:
    input_stack = st.number_input(text["stack"], min_value=400.0, max_value=700.0, step=1.0)
with col4:
    input_reach = st.number_input(text["reach"], min_value=300.0, max_value=500.0, step=1.0)

if st.button(text["calculate"]):
    st.markdown(f"## {text['result']}")

    # 建議值計算
    saddle_height = round(inseam * 0.883, 1)
    stack = round(height * 0.32, 1)
    reach = round((height + inseam) / 2.5, 1)

    spacer_diff = round(stack - input_stack, 1)
    reach_diff = round(input_reach - reach, 1)

    # 龍頭長度建議（只在合理範圍）
    stem_cm = None
    if abs(reach_diff) <= 40:
        stem_cm = round(reach_diff / 10)

    # 曲柄長度建議
    if gender == text["male"]:
        if inseam >= 88: crank = "175 mm"
        elif inseam >= 83: crank = "172.5 mm"
        elif inseam >= 78: crank = "170 mm"
        elif inseam >= 73: crank = "165 mm"
        else: crank = "160 mm"
    else:
        if inseam >= 85: crank = "172.5 mm"
        elif inseam >= 80: crank = "170 mm"
        elif inseam >= 75: crank = "165 mm"
        else: crank = "160 mm"

    # 顯示建議結果
    st.write(f"📐 {text['saddle_height']}：{saddle_height} cm")
    st.write(f"📏 {text['stack_result']}：{stack} mm　({text['spacer']}：{stack - input_stack:+.1f} mm{' ✅ 相符建議使用1公分墊圈' if abs(spacer_diff) <= 10 else ' ❌ 差距過大建議更換車架'})")
    if stem_cm:
        st.write(f"📏 {text['reach_result']}：{reach} mm　({text['stem']}：{reach_diff:+.1f} mm，建議龍頭長度：約 {stem_cm} cm)")
    else:
        st.write(f"📏 {text['reach_result']}：{reach} mm　({text['stem']}：{reach_diff:+.1f} mm ❌ 差距過大建議更換車架）")

    st.write(f"👐 {text['handlebar']}：{shoulder} ± 2 cm")
    st.write(f"🍑 {text['saddle_width']}：{ischial + 2}–{ischial + 4} cm")
    st.write(f"🔧 {text['crank']}：{crank}")

    st.markdown(f"---
{text['donate']} [paypal.me/leopardbikeadvice](https://paypal.me/leopardbikeadvice)")
