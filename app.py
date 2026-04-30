import streamlit as st
import requests
import base64
import os
from datetime import datetime
import re

# 1. 시스템 설정 및 디자인 스타일 (폰트 컬러 명시적 지정)
st.set_page_config(page_title="현대그룹 미디어 모니터링", page_icon="🗞️", layout="wide")

def inject_style():
    base_path = os.path.dirname(os.path.abspath(__file__))
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
    
    /* 전역 폰트 및 가시성 설정 */
    * {{ font-family: 'NeoHyundaiReg', sans-serif !important; }}
    
    /* 제목 컬러 강제 지정 (Dark Blue) */
    h1, .stTitle {{ 
        font-family: 'NeoHyundaiBold', sans-serif !important; 
        color: #002c5f !important; 
        margin-bottom: 5px !important;
    }}

    /* 버튼 텍스트 컬러 및 스타일 강제 지정 */
    .stButton>button {{ 
        font-family: 'NeoHyundaiBold', sans-serif !important; 
        color: #ffffff !important; 
        background-color: #002c5f !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
    }}
    .stButton>button:hover {{ background-color: #004080 !important; color: white !important; }}

    /* arrow_down 잔상 제거 */
    [data-testid="stExpander"] svg {{ display: none !important; }}
    div[class*="st-emotion-cache"] span {{ color: transparent !important; font-size: 0px !important; }}
    
    /* UI 요소 디자인 */
    .user-info {{ color: #444 !important; font-size: 0.9rem !important; margin-bottom: 5px; }}
    .system-sub-title {{ 
        color: #002c5f !important; font-size: 1.1rem; font-weight: bold; 
        border-left: 5px solid #002c5f; padding-left: 15px; margin-bottom: 20px;
    }}
    
    .news-card {{ padding: 10px 5px; border-bottom: 1px solid #f2f2f2; display: flex; align-items: center; gap: 12px; }}
    .m-tag {{ 
        min-width: 90px; text-align: center; font-size: 0.75rem; font-family: 'NeoHyundaiBold' !important;
        background: #f1f6fa; color: #002c5f; padding: 4px 8px; border-radius: 2px;
    }}
    .n-link {{ font-size: 1.05rem; color: #333 !important; text-decoration: none; }}
    </style>
    """

st.markdown(inject_style(), unsafe_allow_html=True)

# 2. 뉴스 수집 로직 (기존 유지)
def get_naver_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=10&sort=date"
    headers = {
        "X-Naver-Client-Id": st.secrets.get("NAVER_ID", ""),
        "X-Naver-Client-Secret": st.secrets.get("NAVER_SECRET", "")
    }
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except: return []

# 3. 레이아웃 (제목 및 버튼 한 줄 구성)
st.markdown('<p class="user-info">사용자: 현대그룹 커뮤니케이션실</p>', unsafe_allow_html=True)

col_main, col_refresh = st.columns([5, 1])
with col_main:
    st.title("📢 현대그룹 미디어 모니터링")
    st.markdown('<p class="system-sub-title">네이버/구글 실시간 모니터링 시스템</p>', unsafe_allow_html=True)

with col_refresh:
    st.write("##") # 간격 조절
    if st.button("🔄 뉴스 새로고침"):
        st.rerun()

st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()

# 4. 키워드 출력 (현정은 회장님 등 주요 키워드)
for kw in ["현정은", "현대엘리베이터", "현대무벡스"]:
    with st.expander(f"{kw} 실시간 뉴스", expanded=True):
        items = get_naver_news(kw)
        if items:
            for item in items[:5]:
                title_clean = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6});', '', item['title'])
                st.markdown(f'''
                <div class="news-card">
                    <div class="m-tag">NEWS</div>
                    <a href="{item['link']}" target="_blank" class="n-link">{title_clean}</a>
                </div>
                ''', unsafe_allow_html=True)
