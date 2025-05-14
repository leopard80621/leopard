
import streamlit as st

# 頁面設定
st.set_page_config(page_title="公路車尺寸建議工具", layout="centered")

# 語言切換
lang = st.selectbox("語言 / Language", ["繁體中文", "English"])
zh = lang == "繁體中文"

T = {
    "title": "🚴‍♂️ 公路車尺寸建議工具" if zh else "🚴‍♂️ Road Bike Fit Recommendation Tool",
    "input": "請輸入身體數據：" if zh else "Enter your body measurements:",
    "trunk": "臀幹長（cm）", "arm": "手臂長（cm）", "forearm": "前臂長（cm）",
    "stack": "預計購買車架 Stack（mm）", "reach": "預計購買車架 Reach（mm）",
    "calc": "計算建議" if zh else "Calculate",
    "result": "🧾 建議結果" if zh else "🧾 Recommended Fit",
    "rec_stack": "建議 Stack：約 {:.1f} mm", "rec_reach": "建議 Reach：約 {:.1f} mm",
    "delta_stack": "與車架 Stack 差值：{} mm（{}）", "delta_reach": "與車架 Reach 差值：{} mm（{}）",
    "stem_suggest": "建議使用龍頭長度：約 {:.1f} mm",
    "ok": "✅ 相符", "bad": "❌ 明顯不符",
    "donate": "☕️ 喜歡這個工具？[贊助我一杯咖啡](https://paypal.me/leopardbikeadvice)" if zh else "☕️ Like this tool? [Buy me a coffee](https://paypal.me/leopardbikeadvice)"
}

st.title(T["title"])
st.markdown(T["input"])

trunk = st.number_input(T["trunk"], min_value=50.0, max_value=75.0, step=0.1)
arm = st.number_input(T["arm"], min_value=50.0, max_value=80.0, step=0.1)
forearm = st.number_input(T["forearm"], min_value=30.0, max_value=45.0, step=0.1)
frame_stack = st.number_input(T["stack"], min_value=450.0, max_value=650.0, step=1.0)
frame_reach = st.number_input(T["reach"], min_value=350.0, max_value=500.0, step=1.0)

if st.button(T["calc"]):
    rider_reach = (trunk + arm + forearm) * 2.96
    suggested_stack = 580.0  # 固定預估 stack，可後續擴充
    stem_suggest = rider_reach - frame_reach

    st.subheader(T["result"])
    st.write(T["rec_stack"].format(suggested_stack))
    st.write(T["rec_reach"].format(rider_reach))

    # Stack 差異提示
    stack_diff = round(suggested_stack - frame_stack, 1)
    st.write(T["delta_stack"].format(stack_diff, T["ok"] if abs(stack_diff) <= 10 else T["bad"]))

    # Reach 差異提示
    reach_diff = round(rider_reach - frame_reach, 1)
    st.write(T["delta_reach"].format(reach_diff, T["ok"] if abs(reach_diff) <= 10 else T["bad"]))

    # 顯示建議龍頭長度
    st.write(T["stem_suggest"].format(stem_suggest))

st.markdown("---")
st.markdown(T["donate"])
