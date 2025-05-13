import streamlit as st
import math

st.set_page_config(page_title='公路車尺寸建議工具', page_icon='🚴', layout='centered')
st.title('🚴 公路車尺寸建議工具')

st.write('請輸入下列身體尺寸資料：')
inseam = st.number_input('跨下長（cm）', min_value=40.0, max_value=120.0, value=80.0, step=0.1)
height = st.number_input('身高（cm）', min_value=100.0, max_value=220.0, value=176.5, step=0.1)
shoulder_width = st.number_input('肩寬（cm）', min_value=30.0, max_value=60.0, value=42.0, step=0.1)
ischial_width = st.number_input('坐骨寬（cm）', min_value=8.0, max_value=20.0, value=12.7, step=0.1)
trunk = st.number_input('軀幹長（cm）', min_value=40.0, max_value=80.0, value=67.0, step=0.1)
arm = st.number_input('手臂長（cm）', min_value=40.0, max_value=80.0, value=65.0, step=0.1)
stem_length = st.slider('龍頭長度（mm）', min_value=60, max_value=140, value=100, step=10)

if st.button('計算建議'):
    saddle_height = round(inseam * 0.883, 1)
    stack = round(height * 0.32 * 10, 1)
    reach = round((trunk + arm) * 0.26 * 10, 1)
    base_reach = reach - stem_length
    saddle_width_range = (round(ischial_width + 1.0, 1), round(ischial_width + 3.0, 1))

    st.subheader('🧾 建議結果')
    st.markdown(f'📐 建議座墊高度：**{saddle_height} cm**')
    st.markdown(f'📐 建議 Stack：**{stack} mm**')
    st.markdown(f'📐 建議 Reach：**{reach} mm**（選用 {stem_length} mm 龍頭）')
    st.markdown(f'📐 建議車架 Reach 差值：**{base_reach:.1f} mm**')
    st.markdown(f'🪑 建議坐墊寬度：**{saddle_width_range[0]}–{saddle_width_range[1]} cm**')