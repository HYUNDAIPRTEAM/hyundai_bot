import streamlit as st
import requests
import base64
import os
from datetime import datetime
import re

# 1. 시스템 설정 및 디자인 스타일 (가시성 100% 보장 CSS)
st.set_page_config(page_title="현대그룹 미디어 모니터링", page_icon="🗞️", layout="wide")

def inject_style():
    base_path = os.path.dirname(os.path.abspath(__file__))
    font_b = os.path.join(base_path, "NeoHyundai_B.woff2")
    
    css_content = ""
    if os.path.exists(font_b):
        with open(font_b, "rb") as f:
            b64_b = base64.b64encode(f.read()).decode()
        css_content += f"@font-face {{ font-family: 'NeoHyundaiBold'; src: url(data:font/woff2;base64,{b64_b}) format('woff2'); font-weight: bold; }}"

    return f"""
    <style>
    {css_content}
    
    /* [중요] 제목 가시성 확보: 배경색과 상관없이 현대 블루로 고정 */
    .custom-title {{
        font-family: 'NeoHyundaiBold', sans-serif !important;
        color: #002c5f !important;
        font-size: 2.2rem !important;
        font-weight: bold !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.2 !important;
    }}

    /* 버튼 내 텍스트(새로고침) 가시성 확보 */
    .stButton>button {{
        background-color: #002c5f !important;
        border: none !important;
        border-radius: 4px !important;
        height: 45px !important;
        width: 100% !important;
    }}
    .stButton>button p {{
        color: #ffffff !important; /* 버튼 글자를 흰색으로 강제 */
        font-family: 'NeoHyundaiBold' !important;
        font-size: 1rem !important;
        margin: 0 !important;
    }}

    /* 서브 타이틀 및 잔상 제거 */
    .system-sub-title {{ 
        color: #002c5f !important; font-size: 1.1rem; 
        border-left: 5px solid #002c5f; padding-left: 15px; margin-top: 15px;
    }}
    [data-testid="stExpander"] svg {{ display: none !important; }}
    div[class*="st-emotion-cache"] span {{ color: transparent !important; font-size: 0px !important; }}
    </style>
    """

st.markdown(inject_style(), unsafe_allow_html=True)

# 2. 레이아웃 구성 (제목과 버튼을 한 줄에 배치)
st.markdown('<p style="color:#666; font-size:0.85rem; margin-bottom:10px;">사용자: 현대그룹 커뮤니케이션실</p>', unsafe_allow_html=True)

# 제목과 버튼을 가로로 정렬
col_title, col_empty, col_btn = st.columns([3.5, 0.5, 1])

with col_title:
    # st.title 대신 커스텀 클래스 사용으로 가시성 확보
    st.markdown('<h1 class="custom-title">📢 현대그룹 미디어 모니터링</h1>', unsafe_allow_html=True)

with col_btn:
    st.write("") # 상단 여백 조절용
    if st.button("🔄 뉴스 새로고침"):
        st.rerun()

st.markdown('<p class="system-sub-title">네이버/구글 실시간 모니터링 시스템</p>', unsafe_allow_html=True)
st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()

# 3. 뉴스 데이터 로직 및 출력 (이하 기존과 동일)
# ... (뉴스 수집 함수 생략) ...
