import streamlit as st
import requests
import base64
import os
from datetime import datetime
import re

# 1. 폰트 주입 및 UI 클리닝 (겹침 문제 해결)
def inject_final_style():
    base_path = os.path.dirname(__file__)
    font_b = os.path.join(base_path, "NeoHyundai_B.woff2")
    font_r = os.path.join(base_path, "NeoHyundai_R.woff2")
    
    css_content = ""
    if os.path.exists(font_b):
        with open(font_b, "rb") as f:
            b64_b = base64.b64encode(f.read()).decode()
        css_content += f"@font-face {{ font-family: 'NeoHyundaiBold'; src: url(data:font/woff2;base64,{b64_b}) format('woff2'); font-weight: bold; }}"
    if os.path.exists(font_r):
        with open(font_r, "rb") as f:
            b64_r = base64.b64encode(f.read()).decode()
        css_content += f"@font-face {{ font-family: 'NeoHyundaiReg'; src: url(data:font/woff2;base64,{b64_r}) format('woff2'); font-weight: normal; }}"

    return f"""
    <style>
    {css_content}

    /* 1. 폰트 강제 적용 */
    * {{ font-family: 'NeoHyundaiReg', sans-serif !important; }}
    h1, h2, h3, .stTitle, b, strong, .m-tag, .stButton>button {{ 
        font-family: 'NeoHyundaiBold', sans-serif !important; 
        letter-spacing: -0.03em !important; 
    }}

    /* 2. [중요] arrow_down 텍스트 겹침 해결 */
    /* 아이콘 이름이 텍스트로 출력되는 것을 방지합니다 */
    .st-emotion-cache-p5msec svg {{ display: none !important; }} 
    .st-emotion-cache-p5msec {{ 
        color: transparent !important; 
        font-size: 0px !important; 
        line-height: 0 !important;
    }}
    
    /* 3. Expander 제목 영역 여백 최적화 */
    .st-emotion-cache-1h9vtsh {{
        padding-left: 0.5rem !important;
    }}

    /* 4. 사용자 정보 및 시스템 타이틀 */
    .user-info {{ color: #666; font-size: 0.85rem; margin-bottom: 5px; }}
    .system-title {{ 
        color: #002c5f; font-size: 1.15rem; font-weight: bold; 
        margin-bottom: 25px; border-left: 5px solid #002c5f; padding-left: 15px; 
    }}
    
    /* 5. 뉴스 카드 및 태그 디자인 */
    .news-card {{ padding: 12px 5px; border-bottom: 1px solid #f2f2f2; display: flex; align-items: center; gap: 15px; }}
    .m-tag {{ 
        min-width: 95px; text-align: center; font-size: 0.72rem; 
        background: #f1f6fa; color: #002c5f; padding: 4px 10px; 
        border-radius: 3px; border: 1px solid #dce6f0;
    }}
    .n-link {{ font-size: 1.02rem; color: #333; text-decoration: none; word-break: keep-all; }}
    .n-link:hover {{ color: #002c5f; text-decoration: underline; }}
    </style>
    """

# 2. 메인 앱 설정 (기존과 동일)
st.set_page_config(page_title="현대 뉴스 브리핑", page_icon="🗞️", layout="wide")
st.markdown(inject_final_style(), unsafe_allow_html=True)

# 3. UI 및 버튼 영역 복원
col_title, col_btn = st.columns([4, 1])
with col_title:
    st.markdown('<p class="user-info">사용자: 현대그룹 커뮤니케이션실</p>', unsafe_allow_html=True)
    st.title("📢 현대 실시간 미디어 모니터링")
    st.markdown('<p class="system-title">네이버/구글 실시간 모니터링 시스템</p>', unsafe_allow_html=True)

with col_btn:
    st.write(" ")
    st.write(" ")
    if st.button("🔄 뉴스 모니터링"):
        st.rerun()

# 4. 뉴스 리스트 출력 (이하 로직 생략 - 기존과 동일)
# ...
