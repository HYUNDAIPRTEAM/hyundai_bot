import streamlit as st
import requests
import base64
import os
from datetime import datetime
import re

# 1. 시스템 설정 및 디자인 스타일 (가시성 및 겹침 방지 CSS)
st.set_page_config(page_title="네이버/구글 실시간 모니터링 시스템", page_icon="🗞️", layout="wide")

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
    
    /* [1] 제목 가시성 강제 확보 */
    .main-title {{
        font-family: 'NeoHyundaiBold', sans-serif !important;
        color: #002c5f !important;
        font-size: 2.3rem !important;
        margin: 0 !important;
        display: block !important;
    }}

    /* [2] 'arrow_down' 글자 겹침 완전 제거 */
    [data-testid="stExpander"] svg {{ display: none !important; }}
    div[class*="st-emotion-cache"] span {{ 
        color: transparent !important; 
        font-size: 0px !important; 
        line-height: 0 !important;
    }}
    div[data-testid="stExpander"] summary p {{
        color: #333 !important;
        font-family: 'NeoHyundaiBold' !important;
        font-size: 1.1rem !important;
    }}

    /* [3] 버튼 텍스트 가시성 확보 */
    .stButton>button {{
        background-color: #002c5f !important;
        border: none !important;
        height: 48px !important;
        width: 100% !important;
    }}
    .stButton>button div p {{
        color: #ffffff !important; 
        font-family: 'NeoHyundaiBold' !important;
        font-size: 1rem !important;
    }}

    .system-sub-title {{ color: #002c5f !important; border-left: 5px solid #002c5f; padding-left: 15px; margin-top: 10px; font-weight: bold; }}
    .user-info {{ color: #666 !important; font-size: 0.85rem; }}
    </style>
    """

st.markdown(inject_style(), unsafe_allow_html=True)

# 2. 뉴스 데이터 로직 (수정 없음)
def get_naver_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=10&sort=date"
    headers = {"X-Naver-Client-Id": st.secrets.get("NAVER_ID", ""), "X-Naver-Client-Secret": st.secrets.get("NAVER_SECRET", "")}
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except: return []

# 3. 레이아웃
st.markdown('<p class="user-info">사용자: 현대그룹 커뮤니케이션실</p>', unsafe_allow_html=True)

col_title, col_btn = st.columns([4, 1])
with col_title:
    st.markdown('<h1 class="main-title">📢 네이버/구글 실시간 모니터링 시스템</h1>', unsafe_allow_html=True)
    st.markdown('<p class="system-sub-title">현대그룹 실시간 뉴스룸</p>', unsafe_allow_html=True)

with col_btn:
    st.write("##")
    # 버튼 명칭 변경: 뉴스 새로고침
    if st.button("🔄 뉴스 새로고침"):
        st.rerun()

st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()

# 4. 출력부
for kw in ["현정은", "현대엘리베이터", "현대무벡스"]:
    with st.expander(f"{kw} 실시간 뉴스", expanded=True):
        items = get_naver_news(kw)
        if items:
            for item in items[:5]:
                t = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6});', '', item['title'])
                st.markdown(f'''<div style="padding:10px 0; border-bottom:1px solid #f2f2f2;"><a href="{item['link']}" target="_blank" style="color:#333; text-decoration:none;"><b>[NEWS]</b> {t}</a></div>''', unsafe_allow_html=True)
