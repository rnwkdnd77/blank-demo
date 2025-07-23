import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# ✅ 한글 폰트 설정
font_path = "./fonts/NanumGothic-Regular.ttf"
nanum_font = font_manager.FontProperties(fname=font_path)
plt.rcParams['axes.unicode_minus'] = False

# 앱 기본 설정
st.set_page_config(layout="wide")
st.title("1학기 기말 수학1 답지응답률 분석")

# ✅ 사용자 정의 CSS (선택된 버튼 강조 + hover 효과)
st.markdown("""
<style>
.stButton>button {
    width: 100%;
    height: 60px;
    font-size: 18px;
    transition: all 0.2s ease-in-out;
}
.stButton>button:hover {
    background-color: #f0f0f0;
    color: black;
}
.selected-button > button {
    border: 3px solid red !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# ✅ session state 초기화
if 'selected_row' not in st.session_state:
    st.session_state.selected_row = None

# 좌우 레이아웃
left_col, right_col = st.columns(2)

# --- 좌측: 이미지 업로드 ---
with left_col:
    st.header("기출문제")
    image_file = st.file_uploader("문제 이미지 업로드 (PNG)", type=["png"])
    if image_file:
        st.image(image_file, use_container_width=True)

# --- 우측: CSV 업로드 및 버튼 표시 ---
with right_col:
    st.header("답지응답률")
    csv_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

    if csv_file:
        df = pd.read_csv(csv_file, header=None)

        if len(df) < 2:
            st.warning("CSV 파일에 최소 2행이 필요합니다.")
        else:
            st.markdown("#### 문항 선택")

            # ✅ 버튼을 6열 × 3행 (18개까지)로 고정 정렬
            total_buttons = min(18, len(df) - 1)
            cols = st.columns(6)

            for i in range(1, total_buttons + 1):
                col = cols[(i - 1) % 6]
                with col:
                    btn_class = "selected-button" if st.session_state.selected_row == i else ""
                    st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
                    if st.button(f"{i}번\n보기", key=f"btn_{i}"):
                        st.session_state.selected_row = i
                    st.markdown("</div>", unsafe_allow_html=True)

# ✅ 버튼과 같은 레벨에서 차트를 바로 표시
if csv_file and st.session_state.selected_row:
    row_index = st.session_state.selected_row

    if row_index >= len(df):
        st.warning(f"{row_index}번 데이터가 없습니다.")
    else:
        labels = df.iloc[0, :].astype(str)
        data = df.iloc[row_index, :].astype(float)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(labels, data, color='skyblue')
        ax.set_ylim(0, 100)
        ax.set_ylabel("정답률 (%)", fontproperties=nanum_font)
        ax.set_title(f"{row_index}번 문항 정답률", fontproperties=nanum_font)
        ax.set_xticklabels(labels, fontproperties=nanum_font)

        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(nanum_font)

        st.pyplot(fig)
