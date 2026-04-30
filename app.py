import streamlit as st
import requests
import base64
import os
from datetime import datetime
import re

# 1. 시스템 설정 및 디자인 스타일 주입 (함수명 오타 수정: b64encode)
st.set_page_config(page_title="현대 실시간 미디어 모니터링", page_icon="🗞️", layout="wide")

def inject_style():
    base_path = os.path.dirname(os.path.abspath(__file__))
    font_b = os.path.join(base_path, "NeoHyundai_B.woff2")
    font_r = os.path.join(base_path, "NeoHyundai_R.woff2")
    
    css_content = ""
    # Bold 폰트 적용 (함수명 b64encode로 수정)
    if os.path.exists(font_b):
        with open(font_b, "rb") as f:
            b64_b = base64.b64encode(f.read()).decode()
        css_content += f"@font-face {{ font-family: 'NeoHyundaiBold'; src: url(data:font/woff2;base64,{b64_b}) format('woff2'); font-weight: bold; }}"
    
    # Regular 폰트 적용
    if os.path.exists(font_r):
        with open(font_r, "rb") as f:
            b64_r = base64.b64encode(f.read()).decode()
        css_content += f"@font-face {{ font-family: 'NeoHyundaiReg'; src: url(data:font/woff2;base64,{b64_r}) format('woff2'); font-weight: normal; }}"

    return f"""
    <style>
    {css_content}
    /* 전역 폰트 및 텍스트 설정 */
    * {{ font-family: 'NeoHyundaiReg', sans-serif !important; }}
    h1, h2, h3, .stTitle, b, strong, .m-tag, .stButton>button {{ 
        font-family: 'NeoHyundaiBold', sans-serif !important; 
        letter-spacing: -0.03em !important; 
    }}
    
    /* 겹침 문제 해결 (arrow_down 텍스트 제거) */
    .st-emotion-cache-p5msec {{ color: transparent !important; font-size: 0px !important; line-height: 0 !important; }}
    
    /* UI 디자인 요소 */
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

# 2. 뉴스 데이터 수집 로직 (네이버 API)
MEDIA_MAP = {
    'busan.com': '부산일보', 'etoday': '이투데이', 'biz.chosun': '조선비즈',
    'bizwn': '비즈니스포스트', 'businesspost': '비즈니스포스트', 'hankookilbo': '한국일보',
    'hankyung': '한국경제', 'mk.co.kr': '매일경제', 'yna.co.kr': '연합뉴스',
    'sedaily': '서울경제', 'edaily': '이데일리', 'mt.co.kr': '머니투데이',
    'heraldcorp': '헤럴드경제', 'news1.kr': '뉴스1', 'newsis': '뉴시스'
}

def get_kor_media(link):
    link = link.lower()
    for domain, kor_name in MEDIA_MAP.items():
        if domain in link: return kor_name
    match = re.search(r'https?://(?:www\.)?([^/.]+)', link)
    return match.group(1).upper() if match else "뉴스"

def clean_text(text):
    return re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6});', '', text).strip()

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

# 3. 메인 레이아웃 및 버튼
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

st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()

# 4. 키워드별 뉴스 출력
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    with st.expander(f"{kw} 실시간 뉴스", expanded=True):
        items = get_naver_news(kw)
        if items:
            c1, c2 = st.columns(2)
            for i, item in enumerate(items):
                target_col = c1 if i < 5 else c2
                m_name = get_kor_media(item['originallink'])
                with target_col:
                    st.markdown(f'''
                    <div class="news-card">
                        <div class="m-tag">{m_name}</div>
                        <a href="{item['link']}" target="_blank" class="n-link">{clean_text(item['title'])}</a>
                    </div>
                    ''', unsafe_allow_html=True)
