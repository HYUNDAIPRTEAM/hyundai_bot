import streamlit as st
import requests
import base64
import os
from datetime import datetime
import re

# 1. 시스템 설정 및 디자인 스타일 (가시성 확보 최우선)
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
    
    /* [긴급] 전역 텍스트 가시성 설정 */
    * {{ font-family: 'NeoHyundaiReg', sans-serif !important; }}
    
    /* 1. 메인 제목 컬러 강제 고정 */
    h1, .stTitle {{ 
        color: #002c5f !important; 
        font-family: 'NeoHyundaiBold' !important;
        font-size: 2.2rem !important;
        visibility: visible !important;
        display: block !important;
    }}

    /* 2. 버튼 내부 텍스트 컬러 강제 고정 (흰색으로 명시) */
    .stButton>button div p {{
        color: white !important;
        font-family: 'NeoHyundaiBold' !important;
    }}
    .stButton>button {{ 
        background-color: #002c5f !important;
        border: 1px solid #002c5f !important;
        min-width: 150px !important;
    }}

    /* 3. 시스템 서브 타이틀 및 잔상 제거 */
    .system-sub-title {{ 
        color: #002c5f !important; font-size: 1.15rem; font-weight: bold; 
        border-left: 5px solid #002c5f; padding-left: 15px; margin-top: 10px;
    }}
    [data-testid="stExpander"] svg {{ display: none !important; }}
    div[class*="st-emotion-cache"] span {{ color: transparent !important; font-size: 0px !important; }}
    
    /* 4. 뉴스 카드 가독성 강화 */
    .n-link {{ color: #333 !important; font-size: 1.05rem !important; text-decoration: none !important; }}
    .n-link:hover {{ color: #002c5f !important; text-decoration: underline !important; }}
    </style>
    """

st.markdown(inject_style(), unsafe_allow_html=True)

# 2. 뉴스 데이터 로직 (기존 유지)
def get_naver_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=10&sort=date"
    headers = {"X-Naver-Client-Id": st.secrets.get("NAVER_ID", ""), "X-Naver-Client-Secret": st.secrets.get("NAVER_SECRET", "")}
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except: return []

# 3. 레이아웃 (제목과 버튼 재배치)
st.markdown('<p style="color:#666; font-size:0.9rem;">사용자: 현대그룹 커뮤니케이션실</p>', unsafe_allow_html=True)

col_title, col_btn = st.columns([4, 1])
with col_title:
    st.markdown('<h1 class="stTitle">📢 현대그룹 미디어 모니터링</h1>', unsafe_allow_html=True)
    st.markdown('<p class="system-sub-title">네이버/구글 실시간 모니터링 시스템</p>', unsafe_allow_html=True)

with col_btn:
    st.write(" ")
    st.write(" ")
    if st.button("🔄 뉴스 새로고침"):
        st.rerun()

st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()

# 4. 뉴스 출력부
for kw in ["현정은", "현대엘리베이터", "현대무벡스"]:
    with st.expander(f"{kw} 실시간 뉴스", expanded=True):
        items = get_naver_news(kw)
        if items:
            for item in items[:5]:
                t = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6});', '', item['title'])
                st.markdown(f'''<div style="padding:10px 0; border-bottom:1px solid #eee;"><a href="{item['link']}" target="_blank" class="n-link"><b>[뉴스]</b> {t}</a></div>''', unsafe_allow_html=True)
