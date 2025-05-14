
import streamlit as st

# 頁面設定
st.set_page_config(page_title="公路車尺寸建議工具", layout="centered")

# 語言選擇
lang = st.selectbox("語言 / Language", ["繁體中文", "English"])
zh = lang == "繁體中文"

# 文字包
T = {
    "title": "🚴‍♂️ 公路車尺寸建議工具" if zh else "🚴‍♂️ Road Bike Fit Recommendation Tool",
    "input": "請輸入身體數據：" if zh else "Enter your body measurements:",
    "inseam": "跨下長（cm）" if zh else "Inseam (cm)",
    "height": "身高（cm）" if zh else "Height (cm)",
    "shoulder": "肩寬（cm）" if zh else "Shoulder Width (cm)",
    "ischial": "坐骨寬（cm）" if zh else "Ischial Width (cm)",
    "trunk": "臀幹長（cm）" if zh else "Trunk Length (cm)",
    "arm": "手臂長（cm）" if zh else "Arm Length (cm)",
    "forearm": "前臂長（cm）" if zh else "Forearm Length (cm)",
    "thigh": "大腿長（cm）" if zh else "Thigh Length (cm)",
    "lowerleg": "小腿長（cm）" if zh else "Lower Leg Length (cm)",
    "sternal": "胸骨凹口高（cm）" if zh else "Sternal Height (cm)",
    "stack": "預計購買車架 Stack（mm）" if zh else "Planned Frame Stack (mm)",
    "reach": "預計購買車架 Reach（mm）" if zh else "Planned Frame Reach (mm)",
    "calc": "計算建議" if zh else "Calculate",
    "result": "🧾 建議結果" if zh else "🧾 Recommended Fit",
    "saddle": "建議座墊高度：約 {:.1f} cm" if zh else "Recommended Saddle Height: {:.1f} cm",
    "rec_stack": "建議 Stack：約 {:.1f} mm" if zh else "Recommended Stack: {:.1f} mm",
    "rec_reach": "建議 Reach：約 {:.1f} mm" if zh else "Recommended Reach: {:.1f} mm",
    "delta_stack": "與車架 Stack 差值：{} mm（{}）" if zh else "Stack difference: {} mm ({})",
    "delta_reach": "與車架 Reach 差值：{} mm（{}）" if zh else "Reach difference: {} mm ({})",
    "spacer": "建議加 {} cm 墊圈" if zh else "Suggest adding {} cm spacer",
    "ok": "✅ 相符" if zh else "✅ Matched",
    "bad": "❌ 明顯不符" if zh else "❌ Mismatch",
    "donate": "☕️ 喜歡這個工具？[贊助我一杯咖啡](https://paypal.me/leopardbikeadvice)" if zh else "☕️ Like this tool? [Buy me a coffee](https://paypal.me/leopardbikeadvice)"
}

st.title(T["title"])
st.markdown(T["input"])

# 分欄輸入 + tooltip hover
col1, col2 = st.columns(2)
with col1:
    inseam = st.number_input(f"{T['inseam']} ❔", help="坐骨結節 ➝ 腳跟", value=None)
    height = st.number_input(f"{T['height']} ❔", help="頭頂 ➝ 地面", value=None)
    shoulder = st.number_input(f"{T['shoulder']} ❔", help="左右肩峰", value=None)
    ischial = st.number_input(f"{T['ischial']} ❔", help="左右坐骨結節", value=None)
    trunk = st.number_input(f"{T['trunk']} ❔", help="胸骨凹口 ➝ 髖骨", value=None)

with col2:
    arm = st.number_input(f"{T['arm']} ❔", help="肩峰 ➝ 肘部", value=None)
    forearm = st.number_input(f"{T['forearm']} ❔", help="肘部 ➝ 橈骨莖突", value=None)
    thigh = st.number_input(f"{T['thigh']} ❔", help="大轉子 ➝ 股骨外髁", value=None)
    lowerleg = st.number_input(f"{T['lowerleg']} ❔", help="股骨外髁 ➝ 脛骨內踝", value=None)
    sternal = st.number_input(f"{T['sternal']} ❔", help="胸骨凹口 ➝ 地面", value=None)

st.markdown("### 📦 " + ("預計購買的車架幾何" if zh else "Planned Frame Geometry"))
input_stack = st.number_input(T["stack"], min_value=450.0, max_value=650.0, step=1.0, value=None)
input_reach = st.number_input(T["reach"], min_value=350.0, max_value=500.0, step=1.0, value=None)

# 避免尚未填寫時就顯示錯誤
if st.button(T["calc"]):
    if None in [inseam, height, shoulder, ischial, trunk, arm, forearm, thigh, lowerleg, sternal]:
        st.warning("請填寫所有欄位" if zh else "Please fill in all fields.")
    else:
        saddle_height = inseam * 0.883
        stack = height * 0.32 * 10
        reach = (trunk + arm + forearm) * 2.96  # 依據 fitting 報告推導

        st.subheader(T["result"])
        st.write(T["saddle"].format(saddle_height))
        st.write(T["rec_stack"].format(stack))
        st.write(T["rec_reach"].format(reach))

        if input_stack:
            diff_stack = round(stack - input_stack, 1)
            spacer = ""
            if diff_stack > 10:
                spacer = T["spacer"].format(round(diff_stack / 10, 1))
                st.write(T["delta_stack"].format(diff_stack, T["bad"]) + f" ｜ {spacer}")
            else:
                st.write(T["delta_stack"].format(diff_stack, T["ok"]))
        if input_reach:
            reach_diff = round(reach - input_reach, 1)
            st.write(T["delta_reach"].format(reach_diff, T["ok"] if abs(reach_diff) <= 10 else T["bad"]))
            stem = round(reach - input_reach)
            stem_rounded = min(max(round(stem / 10), 7), 12)
            if stem_rounded > 13:
                st.warning("❌ 建議龍頭長度已超過常見尺寸範圍（>130mm），請考慮換小一號車架")
            else:
                st.write(f"🛠️ 建議使用龍頭長度：約 {stem_rounded} cm")
            diff_reach = round(reach - input_reach, 1)
            st.write(T["delta_reach"].format(diff_reach, T["ok"] if abs(diff_reach) <= 10 else T["bad"]))

st.markdown("---")
st.markdown(T["donate"])
