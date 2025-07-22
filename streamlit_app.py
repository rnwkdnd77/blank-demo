import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# ✅ 한글 폰트 설정
font_path = "./fonts/NanumGothic-Regular.ttf"
nanum_font = font_manager.FontProperties(fname=font_path)

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# 앱 기본 설정
st.set_page_config(layout="wide")
st.title("1학기 기말 수학1 답지응답률 분석")

# 좌우 레이아웃
left_col, right_col = st.columns(2)

# --- 좌측: 이미지 업로드 ---
with left_col:
    st.header("기출문제")
    image_file = st.file_uploader("문제 이미지 업로드 (PNG)", type=["png"])
    if image_file:
        st.image(image_file, use_container_width=True)

# --- 우측: CSV 업로드 및 정답률 차트 --
with right_col:
    st.header("답지응답률")

    csv_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
    if csv_file:
        df = pd.read_csv(csv_file, header=None)

        if len(df) < 19:
            st.warning("CSV 파일에 최소 19행이 필요합니다.")
        else:
            if 'show_chart' not in st.session_state:
                st.session_state.show_chart = False
                st.session_state.selected_row = None

            button_cols = st.columns(6)
            for i in range(1, 19):
                if button_cols[(i - 1) % 6].button(f"{i}번 보기"):
                    st.session_state.show_chart = True
                    st.session_state.selected_row = i

            if st.session_state.show_chart and st.session_state.selected_row:
                row_index = st.session_state.selected_row

                labels = df.iloc[0, :].astype(str)
                data = df.iloc[row_index, :].astype(float)

                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(labels, data, color='skyblue')

                ax.set_ylim(0, 100)
                ax.set_ylabel("정답률 (%)", fontproperties=nanum_font)
                ax.set_title(f"{row_index}번 문항 정답률", fontproperties=nanum_font)
                ax.set_xticklabels(labels, fontproperties=nanum_font)

                # 축 레이블 폰트도 설정
                for label in ax.get_xticklabels() + ax.get_yticklabels():
                    label.set_fontproperties(nanum_font)

                st.pyplot(fig)

               
