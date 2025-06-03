import json
import streamlit as st


# ----------------------------
# 1. 讀取語系 JSON
# ----------------------------
with open("language_text_options.json", "r", encoding="utf-8") as f:
    language_text_options = json.load(f)

# ----------------------------
# 2. 選擇語系
# ----------------------------
st.set_page_config(page_title="🚴‍♂️ Road Bike Fit", layout="centered")
language = st.sidebar.selectbox(
    "Language / 語言",
    list(language_text_options.keys())
)
text = language_text_options[language]

# ----------------------------
# 3. 網頁標題與步驟提示
# ----------------------------
st.title(f"🚴‍♂️ {text['page_title']}")
st.markdown("---")
st.markdown(
    f"**{text['step_indicator']} 1**：{text['step1']}  \n"
    f"**{text['step_indicator']} 2**：{text['step2']}  \n"
    f"**{text['step_indicator']} 3**：{text['step3']}"
)

# ----------------------------
# 4. Step 1：新手必填欄位
# ----------------------------
st.header(text["step1"])
col1, col2 = st.columns(2)

with col1:
    height = st.number_input(
        text["height_label"],
        min_value=140.0,
        max_value=210.0,
        step=0.5,
        format="%.1f"
    )

with col2:
    gender = st.selectbox(
        text["gender_label"],
        text["gender_options"]
    )

col3, col4 = st.columns(2)
with col3:
    inseam = st.number_input(
        text["inseam_label"],
        min_value=50.0,
        max_value=100.0,
        step=0.5,
        format="%.1f"
    )
with col4:
    shoulder = st.number_input(
        text["shoulder_label"],
        min_value=30.0,
        max_value=60.0,
        step=0.5,
        format="%.1f"
    )

# ----------------------------
# 5. 進階選項（預設隱藏）
# ----------------------------
st.markdown("---")
with st.expander(text["expander_advanced"], expanded=False):
    st.write(text["expander_advanced_instructions"])
    st.write(text["#advanced_fields_header"])
    adv_col1, adv_col2 = st.columns(2)
    with adv_col1:
        torso = st.number_input(
            text["torso_label"],
            min_value=35.0,
            max_value=80.0,
            step=0.5,
            format="%.1f",
            help="從 C7 量到髂骨頂端的垂直距離（cm）"
        )
        sitbone = st.number_input(
            text["sitbone_label"],
            min_value=8.0,
            max_value=20.0,
            step=0.5,
            format="%.1f",
            help="坐在硬物上時，左右坐骨最寬距離（cm）"
        )
        sitbone_height = st.number_input(
            text["sitbone_height_label"],
            min_value=20.0,
            max_value=60.0,
            step=0.5,
            format="%.1f",
            help="坐在硬物上時，坐骨最低點到地面的垂直距離（cm）"
        )
    with adv_col2:
        hip_flex = st.number_input(
            text["hip_flex_label"],
            min_value=60.0,
            max_value=120.0,
            step=1.0,
            format="%.0f",
            help="躺平屈髖角度（°），可由 PT 協助測"
        )
        knee_angle_low = st.number_input(
            text["knee_angle_low_label"],
            min_value=10.0,
            max_value=60.0,
            step=1.0,
            format="%.0f",
            help="在最低踩踏點（6 點鐘位置）膝蓋彎曲角度（°）"
        )
        sternal = st.number_input(
            text["sternal_label"],
            min_value=50.0,
            max_value=120.0,
            step=0.5,
            format="%.1f",
            help="從地面量到胸骨凹口的垂直距離（cm）"
        )
    st.write(text["#end_advanced_fields"])

# ----------------------------
# 6. Step 2：選車架（熱門或自訂）
# ----------------------------
st.header(text["step2"])
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
    default_stack = frame_list[selected_frame][0]
    default_reach = frame_list[selected_frame][1]
    st.write(f"📐 Stack = {default_stack} mm、📏 Reach = {default_reach} mm")
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

# ----------------------------
# 7. Step 3：觸發計算
# ----------------------------
st.header(text["step3"])
if st.button(text["calculate_button"]):
    # 7.1 基本檢核：新手必填是否都有填
    if height <= 0 or inseam <= 0 or shoulder <= 0:
        st.warning("❗ 請先完整填寫：身高、性別、跨下長、肩寬，才能計算！")
    else:
        # 7.2 判斷是否使用進階公式：以「torso 或 sitbone_height 或 hip_flex 任一 > 0」為條件
        use_advanced = False
        if (
            "torso" in locals() and torso and torso > 0
        ) or (
            "sitbone_height" in locals() and sitbone_height and sitbone_height > 0
        ) or (
            "hip_flex" in locals() and hip_flex and hip_flex > 0
        ) or (
            "knee_angle_low" in locals() and knee_angle_low and knee_angle_low > 0
        ) or (
            "sternal" in locals() and sternal and sternal > 0
        ):
            use_advanced = True

        # ------------------------
        # 7.3 Stack 計算
        # ------------------------
        st.markdown("---")
        st.markdown(f"#### {text['stack_title']}")

        # 7.3.1 新手公式：Stack ≈ 跨下 × 22
        suggested_stack = round(inseam * 22)  # mm
        delta_stack = suggested_stack - default_stack

        # 7.3.2 進階公式：使用「坐骨高度 + (髖屈曲或膝角度)」推演座管高度
        if use_advanced:
            # a) 需要有 sitbone_height（cm）→ 換算為 mm，再考慮膝角度或 hip_flex 微調
            sbh_mm = sitbone_height * 10  # 坐骨高度 mm
            # 假設進階建議 Stack = 坐骨高度 mm + (腿部在最低點延伸距離)
            #   下腿長 = 跨下 - 坐骨到地 (cm)
            lower_leg_len = (inseam - sitbone_height)  # cm
            #   最低點膝彎角度控制下，腿部延伸為 lower_leg_len * cos(膝彎角度)
            import math

            leg_extension_mm = lower_leg_len * 10 * math.cos(
                math.radians(knee_angle_low)
            )
            suggested_stack_adv = round(sbh_mm + leg_extension_mm)
            delta_stack_adv = suggested_stack_adv - default_stack

            # 計算需要墊圈（四捨五入到 0.5 cm）
            spacer_adv = max(0.5, round(delta_stack_adv / 10 * 2) / 2)

            st.success(
                text["stack_result_adv"].format(
                    suggested_adv=suggested_stack_adv,
                    delta_adv=delta_stack_adv,
                    spacer_adv=spacer_adv,
                )
            )
        else:
            # 僅顯示新手公式
            if delta_stack < 0:
                st.error(
                    text["stack_result_high"].format(
                        input=default_stack,
                        suggested=suggested_stack
                    )
                )
            else:
                spacer = max(0.5, round(delta_stack / 10 * 2) / 2)
                st.success(
                    text["stack_result_ok"].format(
                        suggested=suggested_stack,
                        delta=delta_stack,
                        spacer=spacer
                    )
                )

        # ------------------------
        # 7.4 Reach 計算
        # ------------------------
        st.markdown(f"#### {text['reach_title']}")

        if use_advanced and "torso" in locals() and torso and torso > 0:
            # 進階公式：Reach ≈ Torso × 5.5，再考慮肩胛活動度與胸骨高度差
            suggested_reach_adv = round(torso * 5.5)
            # 若有胸骨凹口高與坐骨高度，就要確保腰背傾斜度合乎安全
            #   假設腰背容許最大前傾 = (sternal - sitbone_height) cm -> mm
            if "sternal" in locals() and "sitbone_height" in locals() and sternal and sitbone_height:
                body_drop_mm = (sternal - sitbone_height) * 10
                # 若 body_drop_mm < 建議 Reach，則需減少 Reach 10% 確保舒適
                if suggested_reach_adv > body_drop_mm * 0.85:
                    suggested_reach_adv = round(body_drop_mm * 0.85)
            delta_reach_adv = suggested_reach_adv - default_reach

            if delta_reach_adv > 20 or delta_reach_adv < -20:
                # 過長或過短
                if delta_reach_adv < -20:
                    st.error(
                        text["reach_result_too_long"].format(
                            input=default_reach,
                            suggested=suggested_reach_adv
                        )
                    )
                else:
                    st.error(
                        text["reach_result_too_short"].format(
                            input=default_reach,
                            suggested=suggested_reach_adv
                        )
                    )
            else:
                st.success(
                    text["reach_result_adv"].format(
                        suggested_adv=suggested_reach_adv,
                        delta_adv=delta_reach_adv
                    )
                )
        else:
            # 新手公式：估算 Torso ≈ Height × 0.5，然後 Reach = Torso × 5.5
            estimated_torso = height * 0.5
            suggested_reach = round(estimated_torso * 5.5)
            delta_reach = suggested_reach - default_reach

            if delta_reach > 20 or delta_reach < -20:
                if delta_reach < -20:
                    st.error(
                        text["reach_result_too_long"].format(
                            input=default_reach,
                            suggested=suggested_reach
                        )
                    )
                else:
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

        # ------------------------
        # 7.5 把手寬度建議
        # ------------------------
        st.markdown(f"#### {text['shoulder_result']}")
        if shoulder > 0:
            st.info(
                text["shoulder_result"].format(value=round(shoulder))
            )

        # ------------------------
        # 7.6 曲柄長度建議
        # ------------------------
        st.markdown(f"#### {text['crank_title']}")
        # 先顯示新手版曲柄參考
        if gender == text["gender_options"][0] or gender == "Male":
            # 男性
            if height < 165:
                crank = 165
            elif height < 175:
                crank = 170
            elif height < 185:
                crank = 172.5
            else:
                crank = 175
        else:
            # 女性
            if height < 165:
                crank = 162.5
            elif height < 175:
                crank = 167.5
            else:
                crank = 170

        if use_advanced and "sitbone" in locals() and "hip_flex" in locals() and hip_flex:
            # 進階公式：以坐骨寬 & 大腿/小腿分段計算
            # 假設：大腿長 ≈ torso - 下背骨段 (此處簡化)
            thigh_length = torso - (sitbone_height) if "sitbone_height" in locals() else torso * 0.4
            lower_leg_length = inseam - (sitbone_height) if "sitbone_height" in locals() else inseam * 0.4
            # 簡單分段：曲柄 ≈ (大腿長 × 0.45 ＋ 小腿長 × 0.45) × 10 mm
            crank_adv = round((thigh_length * 0.45 + lower_leg_length * 0.45) * 10)
            # 限制在 155–180 mm
            crank_adv = max(155, min(180, crank_adv))
            st.info(
                text["crank_result_adv"].format(value_adv=crank_adv)
            )
        else:
            st.info(
                text["crank_result"].format(value=crank)
            )

        # ------------------------
        # 7.7 健康舒適小提醒
        # ------------------------
        st.markdown("---")
        st.markdown(f"#### {text['health_title']}")
        st.markdown(text["health_tip1"])
        st.markdown(text["health_tip2"])
        st.markdown(text["health_tip3"])
        st.markdown(text["health_tip4"])
