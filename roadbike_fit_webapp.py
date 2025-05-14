import streamlit as st

# 頁面設定
st.set_page_config(page_title="公路車尺寸建議工具", layout="centered")

# 語言選擇
language = st.selectbox("語言 / Language", ["繁體中文", "English"])

# 多語言文字字典
text = {
    "繁體中文": {
        "title": "🚴‍♂️ 公路車尺寸建議工具",
        "input_prompt": "請輸入下列身體尺寸資料：",
        "inseam": "跨下長（cm）　（坐骨結節 ➝ 腳跟/地面）",
        "height": "身高（cm）　（頭頂 ➝ 地面）",
        "shoulder": "肩寬（cm）　（左右肩峰）",
        "ischial": "坐骨寬（cm）　（左右坐骨結節）",
        "forearm": "前臂長（cm）　（肘骨外上髁 ➝ 橈骨莖突）",
        "arm": "手臂長（cm）　（肩峰 ➝ 肘骨外上髁）",
        "trunk": "軀幹長（cm）　（胸骨凹口 ➝ 髖脊）",
        "thigh": "大腿長（cm）　（大轉子 ➝ 股骨外髁）",
        "lower_leg": "小腿長（cm）　（股骨外髁 ➝ 脛骨外踝）",
        "sternal": "胸骨凹口高（cm）　（胸骨凹口 ➝ 地面）",
        "gender": "性別",
        "male": "男性",
        "female": "女性",
        "bike_stack": "車架 Stack (mm)",
        "bike_reach": "車架 Reach (mm)",
        "calculate": "計算建議",
        "result": "📄 建議結果",
        "saddle_height": "📐 建議座墊高度：約 {:.1f} cm",
        "stack_recommend": "📏 建議 Stack：約 {:.1f} mm",
        "reach_recommend": "📏 建議 Reach：約 {:.1f} mm",
        "stack_diff": "📐 與車架 Stack 差值：{:.1f} mm（{} 建議使用{}公分墊圈）",
        "reach_diff": "📏 與車架 Reach 差值：{:.1f} mm（{} 建議使用龍頭長度：約 {} cm）",
        "handlebar_width": "🤲 建議把手寬度：約 {:.0f} ± 2 cm",
        "saddle_width": "🪑 建議坐墊寬度：約 {:.1f}–{:.1f} cm",
        "crank_length": "🚴 建議曲柄長度：約 {} mm（依 {} 建議）",
        "sponsor": "☕ 如果這個工具對你有幫助，歡迎[贊助我一杯咖啡](https://paypal.me/leopardbikeadvice)"
    },
    "English": {
        "title": "🚴 Road Bike Fit Recommendation Tool",
        # 可依需要補英文
    }
}[language]

st.title(text["title"])
st.markdown(text["input_prompt"])

# 輸入欄位
inseam = st.number_input(text["inseam"], min_value=0.0, value=0.0)
height = st.number_input(text["height"], min_value=0.0, value=0.0)
shoulder = st.number_input(text["shoulder"], min_value=0.0, value=0.0)
ischial = st.number_input(text["ischial"], min_value=0.0, value=0.0)
forearm = st.number_input(text["forearm"], min_value=0.0, value=0.0)
arm = st.number_input(text["arm"], min_value=0.0, value=0.0)
trunk = st.number_input(text["trunk"], min_value=0.0, value=0.0)
thigh = st.number_input(text["thigh"], min_value=0.0, value=0.0)
lower_leg = st.number_input(text["lower_leg"], min_value=0.0, value=0.0)
sternal = st.number_input(text["sternal"], min_value=0.0, value=0.0)
gender = st.selectbox(text["gender"], [text["male"], text["female"]])
bike_stack = st.number_input(text["bike_stack"], min_value=0.0, value=0.0)
bike_reach = st.number_input(text["bike_reach"], min_value=0.0, value=0.0)

# 計算邏輯（簡化示例）
if st.button(text["calculate"]):
    saddle_height = inseam * 0.883
    recommend_stack = height * 0.32
    recommend_reach = trunk * 2.5  # 修正為新係數
    diff_stack = recommend_stack - bike_stack
    diff_reach = recommend_reach - bike_reach
    spacer_cm = 0.5 if abs(diff_stack) <= 5 else 1.0 if abs(diff_stack) <= 15 else "需更換車架"
    
    # 龍頭建議
    stem_length = round(abs(diff_reach) / 10)
    stem_text = f"{stem_length}" if 7 <= stem_length <= 12 else "更換車架尺寸"

    # 曲柄建議邏輯
    if gender == text["male"]:
        if inseam >= 90:
            crank = 175
        elif inseam >= 85:
            crank = 172.5
        elif inseam >= 80:
            crank = 170
        elif inseam >= 75:
            crank = 165
        else:
            crank = 160
    else:
        if inseam >= 85:
            crank = 172.5
        elif inseam >= 80:
            crank = 170
        elif inseam >= 75:
            crank = 165
        else:
            crank = 160

    st.markdown("---")
    st.subheader(text["result"])
    st.markdown(text["saddle_height"].format(saddle_height))
    st.markdown(text["stack_recommend"].format(recommend_stack))
    st.markdown(text["reach_recommend"].format(recommend_reach))
    st.markdown(text["stack_diff"].format(diff_stack, "✅ 相符", spacer_cm))
    st.markdown(text["reach_diff"].format(diff_reach, "✅ 相符", stem_text))
    st.markdown(text["handlebar_width"].format(shoulder))
    st.markdown(text["saddle_width"].format(ischial + 1, ischial + 2))
    st.markdown(text["crank_length"].format(crank, gender))
    st.markdown("---")
    st.markdown(text["sponsor"])