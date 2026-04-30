import streamlit as st
import requests
import base64
import os
from datetime import datetime
import re

# 1. 시스템 설정 및 디자인 스타일 (가시성 강제 고정)
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
    
    /* 1. 메인 제목 가시성 확보 (안 보일 수 없게 설정) */
    .header-container {{
        margin-top: -30px;
        margin-bottom: 20px;
    }}
    .main-title {{
        font-family: 'NeoHyundaiBold', sans-serif !important;
        color: #002c5f !important; /* 현대 블루 */
        font-size: 2.4rem !important;
        font-weight: bold !important;
        line-height: 1.2 !important;
        margin: 0 !important;
    }}
    
    /* 2. 버튼 텍스트 가시성 확보 (검은색/남색 배경 무관하게 흰색 고정) */
    .stButton>button {{
        background-color: #002c5f !important;
        border: none !important;
        border-radius: 4px !important;
        height: 48px !important;
        width: 100% !important;
    }}
    .stButton>button p {{
        color: #ffffff !important; /* 새로고침 글자색 강제 */
        font-family: 'NeoHyundaiBold' !important;
        font-size: 1rem !important;
        font-weight: bold !important;
    }}

    /* 3. 불필요한 잔상 제거 (arrow_down 등) */
    [data-testid="stExpander"] svg {{ display: none !important; }}
    div[class*="st-emotion-cache"] span {{ color: transparent !important; font-size: 0px !important; }}
    
    /* 4. 기타 요소 */
    .system-sub-title {{ 
        color: #002c5f !important; font-size: 1.15rem; 
        border-left: 5px solid #002c5f; padding-left: 15px; margin-top: 10px;
    }}
    .user-info {{ color: #666 !important; font-size: 0.85rem; margin-bottom: 5px; }}
    </style>
    """

st.markdown(inject_style(), unsafe_allow_html=True)

# 2. 뉴스 데이터 로직 (네이버 API)
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

# 3. 레이아웃 (제목과 버튼 한 줄 배치)
st.markdown('<p class="user-info">사용자: 현대그룹 커뮤니케이션실</p>', unsafe_allow_html=True)

col_title, col_btn = st.columns([4, 1])

with col_title:
    # st.title 대신 마크다운으로 직접 제목 주입 (가시성 보장)
    st.markdown('<div class="header-container"><h1 class="main-title">📢 현대그룹 미디어 모니터링</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="system-sub-title">네이버/구글 실시간 모니터링 시스템</p>', unsafe_allow_html=True)

with col_btn:
    st.write("##") # 정렬용 공백
    if st.button("🔄 뉴스 새로고침"):
        st.rerun()

st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()

# 4. 출력 영역 (키워드 루프)
for kw in ["현정은", "현대엘리베이터", "현대무벡스"]:
    with st.expander(f"{kw} 실시간 뉴스", expanded=True):
        items = get_naver_news(kw)
        if items:
            for item in items[:5]:
                clean_title = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6});', '', item['title'])
                st.markdown(f'''
                <div style="padding:12px 0; border-bottom:1px solid #f2f2f2;">
                    <a href="{item['link']}" target="_blank" style="color:#333; text-decoration:none; font-size:1.05rem;">
                        <b>[뉴스]</b> {clean_title}
                    </a>
                </div>
                ''', unsafe_allow_html=True)
