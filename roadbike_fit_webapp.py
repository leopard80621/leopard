import json
import streamlit as st

# 1. 讀取語系文字
with open("language_text_options.json", "r", encoding="utf-8") as f:
    language_text_options = json.load(f)

# 2. 選擇語系
st.set_page_config(page_title="🚴‍♂️ Road Bike Fit Tool", layout="centered")
language = st.sidebar.selectbox(
    "Language / 語言", ["繁體中文", "English"]
)
text = language_text_options[language]

# 3. 頁面標題與步驟提示
st.title(f"🚴‍♂️ {text['page_title']}")
st.markdown("---")
st.markdown(
    f"**{text['step_indicator']} 1**：{text['step1']}  \n"
    f"**{text['step_indicator']} 2**：{text['step2']}  \n"
    f"**{text['step_indicator']} 3**：{text['step3']}"
)

# 4. Step 1：量測說明區
with st.expander(text["expander_title"], expanded=False):
    st.write(text["expander_instructions"])

# 5. 輸入：跨下長、軀幹長
col1, col2 = st.columns(2)
with col1:
    inseam = st.number_input(
        text["inseam_label"],
        min_value=50.0,
        max_value=100.0,
        step=0.5,
        format="%.1f"
    )
with col2:
    torso = st.number_input(
        text["torso_label"],
        min_value=40.0,
        max_value=80.0,
        step=0.5,
        format="%.1f"
    )

# 6. Step 2：選擇熱門車架或自訂輸入
st.subheader(text["step2"])
# 預設熱門車架與幾何
frame_list = {
    "Liv Avail S": (535, 390),
    "Specialized Allez S": (530, 385),
    "Canyon Endurace S": (535, 388),
    "Trek Domane S": (540, 392),
    "Giant TCR S": (532, 382)
}

selected_frame = st.selectbox(
    text["select_frame_label"],
    [text["custom_option"]] + list(frame_list.keys())
)

if selected_frame != text["custom_option"]:
    default_stack, default_reach = frame_list[selected_frame]
    st.write(
        f"📐 Stack = {default_stack} mm、📏 Reach = {default_reach} mm"
    )
else:
    default_stack = st.number_input(
        text["custom_stack_label"],
        min_value=400,
        max_value=700,
        step=1,
        value=550
    )
    default_reach = st.number_input(
        text["custom_reach_label"],
        min_value=300,
        max_value=450,
        step=1,
        value=380
    )

# 7. Step 3：按鈕觸發計算
if st.button(text["calculate_button"]):
    # 先檢查「跨下長」與「軀幹長」是否都大於0
    if inseam <= 0 or torso <= 0:
        st.warning("❗ 請先輸入跨下長與軀幹長！")
    else:
        # 7.1 計算建議 Stack
        suggested_stack = round(inseam * 22)  # mm
        delta_stack = suggested_stack - default_stack

        # 7.2 計算建議 Reach
        suggested_reach = round(torso * 5.5)  # mm
        delta_reach = suggested_reach - default_reach

        # 7.3 顯示 Stack 結果
        st.markdown("---")
        st.markdown(f"#### {text['stack_title']}")
        if delta_stack < 0:
            # 車架過高
            st.error(
                text["stack_result_high"].format(
                    input=default_stack,
                    suggested=suggested_stack
                )
            )
        else:
            # 車架 Stack 可用墊圈補足
            # 計算最接近的 0.5 cm 墊圈（四捨五入到 0.5 cm）
            spacer_cm = max(0.5, round(delta_stack / 10 * 2) / 2)
            st.success(
                text["stack_result_ok"].format(
                    suggested=suggested_stack,
                    delta=delta_stack,
                    spacer=spacer_cm
                )
            )

        # 7.4 顯示 Reach 結果
        st.markdown(f"#### {text['reach_title']}")
        if delta_reach < -20:
            st.error(
                text["reach_result_too_long"].format(
                    input=default_reach,
                    suggested=suggested_reach
                )
            )
        elif delta_reach > 20:
            st.error(
                text["reach_result_too_short"].format(
                    input=default_reach,
                    suggested=suggested_reach
                )
            )
        else:
            st.success(
                text["reach_result_ok"].format(
                    suggested=suggested_reach,
                    delta=delta_reach
                )
            )

        # 7.5 額外：把手寬度建議（選填肩寬）
        st.markdown(f"#### {text['shoulder_label']}")
        shoulder = st.number_input(
            text["shoulder_label"],
            min_value=30.0,
            max_value=60.0,
            step=0.5,
            format="%.1f"
        )
        if shoulder and shoulder > 0:
            st.info(
                text["shoulder_result"].format(
                    value=round(shoulder)
                )
            )

        # 7.6 額外：曲柄長度建議（選填身高）
        st.markdown(f"#### {text['height_label']}")
        height = st.number_input(
            text["height_label"],
            min_value=140.0,
            max_value=210.0,
            step=0.5,
            format="%.1f"
        )
        if height and height > 0:
            if height < 165:
                crank = 165
            elif height < 175:
                crank = 170
            elif height < 185:
                crank = 172.5
            else:
                crank = 175
            st.info(
                text["crank_result"].format(
                    value=crank
                )
            )

        # 7.7 健康舒適小提醒（物理治療師視角）
        st.markdown("---")
        st.markdown(f"#### {text['health_title']}")
        st.markdown(text["health_tip1"])
        st.markdown(text["health_tip2"])
        st.markdown(text["health_tip3"])
