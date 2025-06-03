import json
import math
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
# 3. 頁面標題與步驟指引
# ----------------------------
st.title(f"🚴‍♂️ {text['page_title']}")
st.markdown("---")
st.markdown(
    f"**{text['step_indicator']} 1**：{text['step1']}   \n"
    f"**{text['step_indicator']} 2**：{text['step2']}   \n"
    f"**{text['step_indicator']} 3**：{text['step3']}"
)

# ----------------------------
# 4. Step 1：展示「所有量測欄位」＋說明 Expander
# ----------------------------
st.header(text["step1"])
with st.expander(text["expander_help"], expanded=False):
    st.write(text["expander_help_instructions"])
    st.write(f"▶ {text['#help_instructions_1']}")
    st.write(f" {text['#help_instructions_1_content']}")
    st.write(f"▶ {text['#help_instructions_2']}")
    st.write(f" {text['#help_instructions_2_content']}")
    st.write(f"▶ {text['#help_instructions_3']}")
    st.write(f" {text['#help_instructions_3_content']}")
    st.write(f"▶ {text['#help_instructions_4']}")
    st.write(f" {text['#help_instructions_4_content']}")
    st.write(f"▶ {text['#help_instructions_5']}")
    st.write(f" {text['#help_instructions_5_content']}")
    st.write(f"▶ {text['#help_instructions_6']}")
    st.write(f" {text['#help_instructions_6_content']}")
    st.write(f"▶ {text['#help_instructions_7']}")
    st.write(f" {text['#help_instructions_7_content']}")
    st.write(f"▶ {text['#help_instructions_8']}")
    st.write(f" {text['#help_instructions_8_content']}")
    st.write(f"▶ {text['#help_instructions_9']}")
    st.write(f" {text['#help_instructions_9_content']}")
    st.write(f"▶ {text['#help_instructions_10']}")
    st.write(f" {text['#help_instructions_10_content']}")

col1, col2 = st.columns(2)
with col1:
    inseam      = st.number_input(text["inseam_label"],      min_value=50.0,   max_value=100.0,  step=0.5, format="%.1f")
    torso       = st.number_input(text["torso_label"],       min_value=35.0,   max_value=80.0,   step=0.5, format="%.1f")
    forearm     = st.number_input(text["forearm_label"],     min_value=20.0,   max_value=50.0,   step=0.5, format="%.1f")
    arm         = st.number_input(text["arm_label"],         min_value=40.0,   max_value=80.0,   step=0.5, format="%.1f")
    thigh       = st.number_input(text["thigh_label"],       min_value=40.0,   max_value=80.0,   step=0.5, format="%.1f")
with col2:
    lower_leg   = st.number_input(text["lower_leg_label"],   min_value=30.0,   max_value=70.0,   step=0.5, format="%.1f")
    sternal     = st.number_input(text["sternal_label"],     min_value=50.0,   max_value=200.0,  step=0.5, format="%.1f")
    height      = st.number_input(text["height_label"],      min_value=140.0,  max_value=210.0,  step=0.5, format="%.1f")
    shoulder    = st.number_input(text["shoulder_label"],    min_value=30.0,   max_value=60.0,   step=0.5, format="%.1f")
    sitbone     = st.number_input(text["sitbone_label"],     min_value=8.0,    max_value=20.0,   step=0.5, format="%.1f")

# ----------------------------
# 5. Step 2：自訂車架 Stack & Reach
# ----------------------------
st.header(text["step2"])
default_stack = st.number_input(text["custom_stack_label"], min_value=400, max_value=700, step=1, value=550)
default_reach = st.number_input(text["custom_reach_label"], min_value=300, max_value=450, step=1, value=380)

# ----------------------------
# 6. Step 3：按鈕觸發計算（僅進階公式）
# ----------------------------
st.header(text["step3"])
if st.button(text["calculate_button"]):
    # 6.1 基本檢核：至少要填 Inseam、Height、Shoulder 才能做計算
    if inseam <= 0 or height <= 0 or shoulder <= 0:
        st.warning("❗ 請先至少填寫「跨下、身高、肩寬」，才能開始進階計算！")
    else:
        # 下面我們假定只要有 Inseam、Torso、Forearm、Arm、Thigh、Lower Leg、SitBone、Sternal、Height、Shoulder，都可使用進階公式
        # --------------------------------------------------------------------------
        # 6.2 Stack（進階公式）
        # --------------------------------------------------------------------------
        st.markdown("---")
        st.markdown(f"#### {text['stack_title']}")

        # （A）計算座管到踏板中心(mm)：Inseam × 0.883 × 10
        seat_height_mm = round(inseam * 0.883 * 10)

        # （B）計算胸骨到座管頂的垂直差： (Sternal - Inseam×0.883) × 10 × cos(lean_angle)
        lean_angle = 18  # 前傾角度示範用
        s_b_diff_mm = (sternal - (inseam * 0.883)) * 10
        upper_vert_mm = round(s_b_diff_mm * math.cos(math.radians(lean_angle)))

        # （C）加權：假設 α = 0.3，raw_stack = seat_height_mm × α + upper_vert_mm × (1−α)
        alpha = 0.3
        raw_stack_mm = round(seat_height_mm * alpha + upper_vert_mm * (1 - alpha))

        # （D）縮放：final_stack = round(raw_stack_mm × 0.82)，使結果約 570 mm
        suggested_stack_adv = round(raw_stack_mm * 0.82)
        delta_stack_adv = suggested_stack_adv - default_stack
        spacer_adv = max(0.5, round(delta_stack_adv / 10 * 2) / 2)

        st.success(
            text["stack_result"].format(
                suggested_adv=suggested_stack_adv,
                delta_adv=delta_stack_adv,
                spacer_adv=spacer_adv
            )
        )

        # --------------------------------------------------------------------------
        # 6.3 Reach（進階公式）
        # --------------------------------------------------------------------------
        st.markdown(f"#### {text['reach_title']}")

        # （1）Torso 水平投影 (mm)：Torso × cos(lean_angle) × 10
        lean_angle = 18
        torso_horiz_mm = round(torso * math.cos(math.radians(lean_angle)) * 10) if torso > 0 else 0

        # （2）Upper Arm 水平投影 (mm)：Arm × cos(60°) × 10
        arm_horiz_mm = round(arm * math.cos(math.radians(60)) * 10) if arm > 0 else 0

        # （3）Forearm 水平投影 (mm)：Forearm × cos(75°) × 10
        forearm_horiz_mm = round(forearm * math.cos(math.radians(75)) * 10) if forearm > 0 else 0

        # （4）座管前傾骨盆水平投影 (mm)：Inseam × sin(73°) × 0.883 × 10
        seat_angle = 73
        pelvis_proj_mm = round(inseam * math.sin(math.radians(seat_angle)) * 0.883 * 10)

        # （5）坐骨寬補正 (mm)：SitBone × 10
        sitbone_mm = round(sitbone * 10) if sitbone > 0 else 0

        # （6）raw_reach = (1)+(2)+(3)+(5) − (4)
        raw_reach_mm = torso_horiz_mm + arm_horiz_mm + forearm_horiz_mm + sitbone_mm - pelvis_proj_mm

        # （7）縮放：final_reach = round(raw_reach_mm × β)，示範用 β = 0.78，使結果約 390 mm
        beta = 0.78
        suggested_reach_adv = round(raw_reach_mm * beta)
        delta_reach_adv = suggested_reach_adv - default_reach

        if delta_reach_adv > 20 or delta_reach_adv < -20:
            # 如果超過 ±20 mm，顯示錯誤提示
            if delta_reach_adv < -20:
                st.error(
                    text["reach_result"].format(
                        input=default_reach,
                        suggested_adv=suggested_reach_adv,
                        delta_adv=delta_reach_adv
                    )
                )
            else:
                st.error(
                    text["reach_result"].format(
                        input=default_reach,
                        suggested_adv=suggested_reach_adv,
                        delta_adv=delta_reach_adv
                    )
                )
        else:
            st.success(
                text["reach_result"].format(
                    suggested_adv=suggested_reach_adv,
                    delta_adv=delta_reach_adv
                )
            )

        # --------------------------------------------------------------------------
        # 6.4 把手寬度建議
        # --------------------------------------------------------------------------
        st.markdown(f"#### {text['shoulder_result']}")
        if shoulder > 0:
            st.info(text["shoulder_result"].format(value=round(shoulder)))

        # --------------------------------------------------------------------------
        # 6.5 曲柄長度建議（進階公式）
        # --------------------------------------------------------------------------
        st.markdown(f"#### {text['crank_title']}")
        if thigh > 0 and lower_leg > 0:
            crank_adv = round((thigh * 0.45 + lower_leg * 0.45) * 10)
            crank_adv = max(155, min(180, crank_adv))
            st.info(text["crank_result"].format(value_adv=crank_adv))
        else:
            st.info("▶ 若要進階曲柄計算，請同時填寫「大腿長」和「小腿長」。")

        # --------------------------------------------------------------------------
        # 6.6 健康舒適小提醒
        # --------------------------------------------------------------------------
        st.markdown("---")
        st.markdown(f"#### {text['health_title']}")
        st.markdown(text["health_tip1"])
        st.markdown(text["health_tip2"])
        st.markdown(text["health_tip3"])
        st.markdown(text["health_tip4"])
