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
# 4. Step 1：所有量測欄位＋說明 Expander（使用 text_input，預設空白）
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
# 5. Step 2：自訂車架 Stack & Reach ＋ 車架尺寸選擇＆固定龍頭長度/角度
# ----------------------------
st.header(text["step2"])
default_stack_str = st.text_input(text["custom_stack_label"], "")
frame_reach_str   = st.text_input(text["custom_reach_label"], "")

# 車架尺寸下拉選單：XS/S/M/L/XL
frame_size = st.selectbox(
    "選擇 車架尺寸 Frame Size",
    options=["XS", "S", "M", "L", "XL"],
    index=2  # 預設 M
)

# 定義「車架尺寸 → 建議龍頭長度」映射
stem_map = {
    "XS": 70,
    "S": 80,
    "M": 90,
    "L": 100,
    "XL": 110
}
# 依據所選 frame_size，取得對應 stem_length
stem_length = stem_map[frame_size]

# 固定龍頭角度 -6°
stem_angle = -6  # 度

st.markdown(
    f"**依照你選的車架尺寸 {frame_size}，系統建議使用 龍頭長度：{stem_length} mm，角度固定 {stem_angle}°。**"
)

# 讓使用者如果想自己微調，也可以在此輸入「自訂龍頭長度」
custom_stem_str = st.text_input("若要自訂龍頭長度，請輸入數值 (mm)，否則留空套用建議", "")

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
    # 將所有 text_input 嘗試轉成 float
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

    default_stack = to_float(default_stack_str)
    frame_reach   = to_float(frame_reach_str)

    custom_stem = to_float(custom_stem_str)
    if custom_stem is not None:
        stem_length = custom_stem

    # 檢查必要欄位
    missing = []
    if inseam is None:
        missing.append("跨下長")
    if height is None:
        missing.append("身高")
    if shoulder is None:
        missing.append("肩寬")
    if default_stack is None:
        missing.append("車架 Stack")
    if frame_reach is None:
        missing.append("車架 Reach")

    if missing:
        st.error("❗ 請確認以下欄位已正確填寫（輸入數字格式）：\n- " + "、".join(missing))
    else:
        # ----------------------------
        # 6.3 Stack 計算（進階公式）
        # ----------------------------
        st.markdown("---")
        st.markdown(f"#### {text['stack_title']}")

        # (A) 座管到踏板中心 (mm)
        seat_height_mm = round(inseam * 0.883 * 10)

        # (B) 胸骨到座管頂垂直差 (mm)
        lean_angle = 18
        if sternal is not None:
            s_b_diff_mm = (sternal - (inseam * 0.883)) * 10
            upper_vert_mm = round(s_b_diff_mm * math.cos(math.radians(lean_angle)))
        else:
            upper_vert_mm = 0

        # (C) 加權 α = 0.3
        alpha = 0.3
        raw_stack_mm = round(seat_height_mm * alpha + upper_vert_mm * (1 - alpha))

        # (D) 縮放 ×0.82
        suggested_stack_adv = round(raw_stack_mm * 0.82)
        delta_stack_adv = suggested_stack_adv - default_stack

        # 判斷若需要的墊圈超過 4 cm，建議換大一號車架
        spacer_adv = max(0.5, round(delta_stack_adv / 10 * 2) / 2)
        if spacer_adv > 4.0:
            st.error(
                f"▶ 建議 Stack：{suggested_stack_adv} mm  \n"
                f"  → 你輸入的車架 Stack = {default_stack:.0f} mm，比建議低 {delta_stack_adv} mm，"
                f"需要墊圈 {spacer_adv} cm，已超過 4 cm 上限，建議選擇大一號車架。"
            )
        else:
            if delta_stack_adv > 20:
                st.success(
                    f"▶ 建議 Stack：{suggested_stack_adv} mm  \n"
                    f"  → 你輸入的車架 Stack = {default_stack:.0f} mm，比建議低 {delta_stack_adv} mm，"
                    f"可使用墊圈 {spacer_adv} cm。"
                )
            elif delta_stack_adv < -20:
                st.error(
                    f"▶ 建議 Stack：{suggested_stack_adv} mm  \n"
                    f"  → 你輸入的車架 Stack = {default_stack:.0f} mm，比建議高 {abs(delta_stack_adv)} mm，"
                    f"不建議此車架，或考慮降低座管／使用低把高度。"
                )
            else:
                st.success(
                    f"▶ 建議 Stack：{suggested_stack_adv} mm  \n"
                    f"  → 你輸入的車架 Stack = {default_stack:.0f} mm，與建議相差 {delta_stack_adv} mm，可接受。"
                )

        # ----------------------------
        # 6.4 Reach 計算（優化演算法 + 固定龍頭角度 -6° + β = 0.95）
        # ----------------------------
        st.markdown(f"#### {text['reach_title']}")

        # (1) Torso 水平投影 (mm)
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

        # (6) Raw Reach = 各段投影 + 坐骨寬 - 骨盆投影
        raw_reach_mm = torso_horiz_mm + arm_horiz_mm + forearm_horiz_mm + sitbone_mm - pelvis_proj_mm

        # (7) 建議 Reach：β = 0.95
        beta = 0.95
        suggested_reach_adv = round(raw_reach_mm * beta)

        # (8) 計算龍頭水平投影 = stem_length × cos(6°)
        stem_horizontal = round(stem_length * math.cos(math.radians(abs(stem_angle))))

        # (9) 計算有效 Reach = 車架 Reach + 龍頭水平投影
        effective_reach = frame_reach + stem_horizontal
        delta_reach_adv = suggested_reach_adv - effective_reach

        if delta_reach_adv > 20:
            needed = delta_reach_adv
            st.success(
                f"▶ 建議 Reach：{suggested_reach_adv} mm  \n"
                f"  → 你輸入的車架 Reach = {frame_reach:.0f} mm + 龍頭水平 {stem_horizontal:.0f} mm "
                f"(長度 {stem_length:.0f} mm，角度 {stem_angle}°) = {effective_reach:.0f} mm，"
                f"比建議短 {needed} mm，可更換更長龍頭或角度調整 +{needed} mm。"
            )
        elif delta_reach_adv < -20:
            over = abs(delta_reach_adv)
            st.error(
                f"▶ 建議 Reach：{suggested_reach_adv} mm  \n"
                f"  → 你輸入的車架 Reach = {frame_reach:.0f} mm + 龍頭水平 {stem_horizontal:.0f} mm "
                f"(長度 {stem_length:.0f} mm，角度 {stem_angle}°) = {effective_reach:.0f} mm，"
                f"比建議長 {over} mm，可更換更短龍頭或角度調整 −{over} mm。"
            )
        else:
            st.success(
                f"▶ 建議 Reach：{suggested_reach_adv} mm  \n"
                f"  → 你輸入的車架 Reach = {frame_reach:.0f} mm + 龍頭水平 {stem_horizontal:.0f} mm "
                f"(長度 {stem_length:.0f} mm，角度 {stem_angle}°) = {effective_reach:.0f} mm，"
                f"與建議相差 {delta_reach_adv} mm，可接受。"
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
