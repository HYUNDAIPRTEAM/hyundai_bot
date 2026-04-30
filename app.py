import streamlit as st
import requests
import base64
import os
from datetime import datetime
import re

# 1. 시스템 설정 및 디자인 스타일 (강력한 겹침 방지 로직 포함)
st.set_page_config(page_title="현대 실시간 미디어 모니터링", page_icon="🗞️", layout="wide")

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
    
    /* 전역 폰트 설정 */
    * {{ font-family: 'NeoHyundaiReg', sans-serif !important; }}
    h1, h2, h3, .stTitle, b, strong, .m-tag, .stButton>button {{ 
        font-family: 'NeoHyundaiBold', sans-serif !important; 
        letter-spacing: -0.03em !important; 
    }}

    /* [핵심] arrow_down 겹침 해결: 모든 아이콘 관련 텍스트 강제 제거 */
    [data-testid="stExpander"] svg {{ display: none !important; }}
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {{ margin-bottom: 0; }}
    
    /* 아이콘이 들어가는 span 영역의 텍스트를 완전히 숨깁니다 */
    div[class*="st-emotion-cache"] span {{
        color: transparent !important;
        font-size: 0px !important;
        line-height: 0 !important;
    }}
    
    /* Expander 제목 텍스트만 다시 보이게 설정 */
    div[data-testid="stExpander"] summary p {{
        color: #333 !important;
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
        font-family: 'NeoHyundaiBold' !important;
    }}

    /* UI 요소 스타일 */
    .user-info {{ color: #666; font-size: 0.85rem; margin-bottom: 5px; }}
    .system-title {{ 
        color: #002c5f; font-size: 1.15rem; font-weight: bold; 
        margin-bottom: 25px; border-left: 5px solid #002c5f; padding-left: 15px; 
    }}
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

st.markdown(inject_style(), unsafe_allow_html=True)

# 2. 뉴스 데이터 로직 (기존과 동일)
def get_naver_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=10&sort=date"
    headers = {"X-Naver-Client-Id": st.secrets.get("NAVER_ID", ""), "X-Naver-Client-Secret": st.secrets.get("NAVER_SECRET", "")}
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except: return []

# 3. 레이아웃
col_t, col_b = st.columns([4, 1])
with col_t:
    st.markdown('<p class="user-info">사용자: 현대그룹 커뮤니케이션실</p>', unsafe_allow_html=True)
    st.title("📢 현대 실시간 미디어 모니터링")
    st.markdown('<p class="system-title">네이버/구글 실시간 모니터링 시스템</p>', unsafe_allow_html=True)

with col_b:
    st.write(" ")
    st.write(" ")
    if st.button("🔄 뉴스 모니터링"):
        st.rerun()

# 4. 출력
for kw in ["현정은", "현대엘리베이터", "현대무벡스"]:
    with st.expander(f"{kw} 실시간 뉴스", expanded=True):
        items = get_naver_news(kw)
        if items:
            for item in items[:5]: # 예시로 5개만 출력
                st.markdown(f'''<div class="news-card"><div class="m-tag">뉴스</div><a href="{item['link']}" target="_blank" class="n-link">{item['title']}</a></div>''', unsafe_allow_html=True)
