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
# 4. Step 1：量測欄位（使用 text_input，預設空白）
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
    inseam_str    = st.text_input(text["inseam_label"], "")
    torso_str     = st.text_input(text["torso_label"], "")
    forearm_str   = st.text_input(text["forearm_label"], "")
    arm_str       = st.text_input(text["arm_label"], "")
    thigh_str     = st.text_input(text["thigh_label"], "")
with col2:
    lower_leg_str = st.text_input(text["lower_leg_label"], "")
    sternal_str   = st.text_input(text["sternal_label"], "")
    height_str    = st.text_input(text["height_label"], "")
    shoulder_str  = st.text_input(text["shoulder_label"], "")
    sitbone_str   = st.text_input(text["sitbone_label"], "")

# ----------------------------
# 5. Step 2：輸入車架 Reach
# ----------------------------
st.header(text["step2"])
frame_reach_str = st.text_input(text["custom_reach_label"], "")

# ----------------------------
# 輔助函式：文字轉 float
# ----------------------------
def to_float(val_str):
    try:
        return float(val_str)
    except:
        return None

# ----------------------------
# 6. Step 3：按鈕觸發計算
# ----------------------------
st.header(text["step3"])
if st.button(text["calculate_button"]):
    # 6.1 讀取並轉型
    inseam    = to_float(inseam_str)
    torso     = to_float(torso_str)
    forearm   = to_float(forearm_str)
    arm       = to_float(arm_str)
    thigh     = to_float(thigh_str)
    lower_leg = to_float(lower_leg_str)
    sternal   = to_float(sternal_str)
    height    = to_float(height_str)
    shoulder  = to_float(shoulder_str)
    sitbone   = to_float(sitbone_str)

    frame_reach = to_float(frame_reach_str)

    # 檢查必要欄位：Inseam、Height、Shoulder、Frame Reach
    missing = []
    if inseam is None:
        missing.append("跨下長")
    if height is None:
        missing.append("身高")
    if shoulder is None:
        missing.append("肩寬")
    if frame_reach is None:
        missing.append("車架 Reach")

    if missing:
        st.error("❗ 請確認以下欄位已正確填寫（數字格式）：\n- " + "、".join(missing))
    else:
        # ----------------------------
        # 計算「建議身體 Reach」
        # ----------------------------
        st.markdown("---")
        st.markdown(f"#### {text['reach_title']}")

        # (1) Torso 水平投影 (mm)
        lean_angle = 18
        if torso is not None:
            torso_horiz_mm = round(torso * math.cos(math.radians(lean_angle)) * 10)
        else:
            torso_horiz_mm = 0

        # (2) 上臂水平投影 (mm)
        if arm is not None:
            arm_horiz_mm = round(arm * math.cos(math.radians(60)) * 10)
        else:
            arm_horiz_mm = 0

        # (3) 前臂水平投影 (mm)
        if forearm is not None:
            forearm_horiz_mm = round(forearm * math.cos(math.radians(75)) * 10)
        else:
            forearm_horiz_mm = 0

        # (4) 骨盆前傾後水平投影 (mm)
        seat_angle = 73
        pelvis_proj_mm = round(inseam * math.sin(math.radians(seat_angle)) * 0.883 * 10)

        # (5) 坐骨寬度水平加成 (mm)
        if sitbone is not None:
            sitbone_mm = round(sitbone * 10)
        else:
            sitbone_mm = 0

        # (6) Raw Reach
        raw_reach_mm = torso_horiz_mm + arm_horiz_mm + forearm_horiz_mm + sitbone_mm - pelvis_proj_mm

        # (7) 建議身體 Reach：β = 0.95
        beta = 0.95
        suggested_body_reach = round(raw_reach_mm * beta)

        # 顯示建議身體 Reach
        st.markdown(f"▶ 建議身體 Reach：{suggested_body_reach} mm")

        # ----------------------------
        # 只比對「車架 Reach」與「建議身體 Reach」
        # ----------------------------
        tolerance = 10  # ±10 mm

        delta = frame_reach - suggested_body_reach

        if delta > tolerance:
            # 車架 Reach 過長
            st.error(
                f"▶ 你的車架 Reach = {frame_reach:.0f} mm，比建議身體 Reach {suggested_body_reach} mm 長 {delta} mm，"
                "建議選擇較短 Reach 的車架。"
            )
        elif delta < -tolerance:
            # 車架 Reach 過短
            needed = abs(delta)
            st.success(
                f"▶ 你的車架 Reach = {frame_reach:.0f} mm，比建議身體 Reach {suggested_body_reach} mm 短 {needed} mm，"
                "建議選擇較長 Reach 的車架。"
            )
        else:
            # 在 ±10 mm 內
            st.success(
                f"▶ 你的車架 Reach = {frame_reach:.0f} mm，與建議身體 Reach {suggested_body_reach} mm 相差 {delta} mm，"
                "可接受。"
            )

        # ----------------------------
        # 6.5 把手寬度建議
        # ----------------------------
        st.markdown(f"#### {text['shoulder_result']}")
        st.info(text["shoulder_result"].format(value=round(shoulder)))

        # ----------------------------
        # 6.6 曲柄長度建議（依身高分段）
        # ----------------------------
        st.markdown(f"#### {text['crank_title']}")
        if height is not None:
            if height < 165:
                crank = 165
            elif height < 175:
                crank = 170
            elif height < 185:
                crank = 172.5
            else:
                crank = 175
            st.info(text["crank_result"].format(value_adv=crank))
        else:
            st.info("▶ 若要計算曲柄長度，請填寫「身高」。")

        # ----------------------------
        # 6.7 健康舒適小提醒
        # ----------------------------
        st.markdown("---")
        st.markdown(f"#### {text['health_title']}")
        st.markdown(text["health_tip1"])
        st.markdown(text["health_tip2"])
        st.markdown(text["health_tip3"])
        st.markdown(text["health_tip4"])
