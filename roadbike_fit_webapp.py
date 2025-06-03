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
# 4. Step 1：展示「所有量測欄位」＋說明 Expander（使用 text_input，預設為空）
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
    inseam_str      = st.text_input(text["inseam_label"],        "")
    torso_str       = st.text_input(text["torso_label"],         "")
    forearm_str     = st.text_input(text["forearm_label"],       "")
    arm_str         = st.text_input(text["arm_label"],           "")
    thigh_str       = st.text_input(text["thigh_label"],         "")
with col2:
    lower_leg_str   = st.text_input(text["lower_leg_label"],     "")
    sternal_str     = st.text_input(text["sternal_label"],       "")
    height_str      = st.text_input(text["height_label"],        "")
    shoulder_str    = st.text_input(text["shoulder_label"],      "")
    sitbone_str     = st.text_input(text["sitbone_label"],       "")

# ----------------------------
# 5. Step 2：自訂車架 Stack & Reach（也改用 text_input, 預設空白）
# ----------------------------
st.header(text["step2"])
default_stack_str = st.text_input(text["custom_stack_label"], "")
default_reach_str = st.text_input(text["custom_reach_label"], "")

# ----------------------------
# 輔助函式：將文字轉 float，若無法轉或為空，回傳 None
# ----------------------------
def to_float(val_str):
    try:
        return float(val_str)
    except:
        return None

# ----------------------------
# 6. Step 3：按鈕觸發計算（僅進階公式，全部欄位都用 to_float() 轉）
# ----------------------------
st.header(text["step3"])
if st.button(text["calculate_button"]):
    # 6.1 先把所有輸入轉成浮點數，若空白或格式錯誤，就得到 None
    inseam      = to_float(inseam_str)
    torso       = to_float(torso_str)
    forearm     = to_float(forearm_str)
    arm         = to_float(arm_str)
    thigh       = to_float(thigh_str)
    lower_leg   = to_float(lower_leg_str)
    sternal     = to_float(sternal_str)
    height      = to_float(height_str)
    shoulder    = to_float(shoulder_str)
    sitbone     = to_float(sitbone_str)

    default_stack = to_float(default_stack_str)
    default_reach = to_float(default_reach_str)

    # 6.2 檢查必要欄位：Inseam、Height、Shoulder、Default Stack、Default Reach
    missing = []
    if inseam is None:
        missing.append("跨下長")
    if height is None:
        missing.append("身高")
    if shoulder is None:
        missing.append("肩寬")
    if default_stack is None:
        missing.append("車架 Stack")
    if default_reach is None:
        missing.append("車架 Reach")

    if missing:
        st.error("❗ 請確認以下欄位已正確填寫（數字形式）：\n- " + "、".join(missing))
    else:
        # 若扔沒有至少 Inseam、Height、Shoulder、車架 Stack/Reach，就不繼續
        # 連續檢查後，開始進階計算

        # ----------------------------------
        # 6.3 Stack（進階公式）
        # ----------------------------------
        st.markdown("---")
        st.markdown(f"#### {text['stack_title']}")

        # (A) 計算座管到踏板中心(mm)：Inseam × 0.883 × 10
        seat_height_mm = round(inseam * 0.883 * 10)

        # (B) 計算胸骨到座管頂的垂直差： (Sternal - Inseam×0.883) × 10 × cos(lean_angle)
        lean_angle = 18
        if sternal is not None:
            s_b_diff_mm = (sternal - (inseam * 0.883)) * 10
            upper_vert_mm = round(s_b_diff_mm * math.cos(math.radians(lean_angle)))
        else:
            # 若沒填胸骨，就以 0 當作示範
            upper_vert_mm = 0

        # (C) 加權：alpha = 0.3
        alpha = 0.3
        raw_stack_mm = round(seat_height_mm * alpha + upper_vert_mm * (1 - alpha))

        # (D) 縮放：final_stack = round(raw_stack_mm × 0.82)
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

        # ----------------------------------
        # 6.4 Reach（進階公式）
        # ----------------------------------
        st.markdown(f"#### {text['reach_title']}")

        # (1) Torso 水平投影 (mm)：
        if torso is not None:
            torso_horiz_mm = round(torso * math.cos(math.radians(lean_angle)) * 10)
        else:
            torso_horiz_mm = 0

        # (2) Upper Arm 水平投影 (mm)：Arm × cos(60°) × 10
        if arm is not None:
            arm_horiz_mm = round(arm * math.cos(math.radians(60)) * 10)
        else:
            arm_horiz_mm = 0

        # (3) Forearm 水平投影 (mm)：Forearm × cos(75°) × 10
        if forearm is not None:
            forearm_horiz_mm = round(forearm * math.cos(math.radians(75)) * 10)
        else:
            forearm_horiz_mm = 0

        # (4) 座管前傾骨盆水平投影 (mm)：Inseam × sin(73°) × 0.883 × 10
        seat_angle = 73
        pelvis_proj_mm = round(inseam * math.sin(math.radians(seat_angle)) * 0.883 * 10)

        # (5) 坐骨寬補正 (mm)
        if sitbone is not None:
            sitbone_mm = round(sitbone * 10)
        else:
            sitbone_mm = 0

        raw_reach_mm = torso_horiz_mm + arm_horiz_mm + forearm_horiz_mm + sitbone_mm - pelvis_proj_mm

        # (6) 縮放：beta = 0.78
        beta = 0.78
        suggested_reach_adv = round(raw_reach_mm * beta)
        delta_reach_adv = suggested_reach_adv - default_reach

        st.success(
            text["reach_result"].format(
                suggested_adv=suggested_reach_adv,
                delta_adv=delta_reach_adv
            )
        )

        # ----------------------------------
        # 6.5 把手寬度建議
        # ----------------------------------
        st.markdown(f"#### {text['shoulder_result']}")
        st.info(text["shoulder_result"].format(value=round(shoulder)))

        # ----------------------------------
        # 6.6 曲柄長度建議（進階公式）
        # ----------------------------------
        st.markdown(f"#### {text['crank_title']}")
        if thigh is not None and lower_leg is not None:
            crank_adv = round((thigh * 0.45 + lower_leg * 0.45) * 10)
            crank_adv = max(155, min(180, crank_adv))
            st.info(text["crank_result"].format(value_adv=crank_adv))
        else:
            st.info("▶ 若要進階曲柄計算，請同時填寫「大腿長」和「小腿長」。")

        # ----------------------------------
        # 6.7 健康舒適小提醒
        # ----------------------------------
        st.markdown("---")
        st.markdown(f"#### {text['health_title']}")
        st.markdown(text["health_tip1"])
        st.markdown(text["health_tip2"])
        st.markdown(text["health_tip3"])
        st.markdown(text["health_tip4"])
