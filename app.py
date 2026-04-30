import streamlit as st
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime
import re
import base64
import os

# 1. 시스템 설정
st.set_page_config(page_title="현대 뉴스 브리핑", page_icon="🗞️", layout="wide")

# 🔹 폰트 로드 함수
def load_font(font_file):
    if os.path.exists(font_file):
        with open(font_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 🔹 폰트 파일명
font_bold = "NeoHyundai_B.woff2"
font_reg = "NeoHyundai_R.woff2"

# 🔹 폰트 데이터 로딩
data_b = load_font(font_bold)
data_r = load_font(font_reg)

# 🔹 CSS 적용
if data_b and data_r:
    st.markdown(f"""
    <style>
    @font-face {{
        font-family: 'NeoHyundaiBold';
        src: url(data:font/woff2;base64,{data_b}) format('woff2');
        font-weight: 700;
    }}

    @font-face {{
        font-family: 'NeoHyundaiReg';
        src: url(data:font/woff2;base64,{data_r}) format('woff2');
        font-weight: 400;
    }}

    /* 전체 기본 = Regular */
    * {{
        font-family: 'NeoHyundaiReg', sans-serif !important;
    }}

    /* 제목만 Bold */
    .custom-title {{
        font-family: 'NeoHyundaiBold', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em;
        font-size: 2.2rem;
        margin-bottom: 10px;
    }}

    /* 뉴스 UI */
    .news-item {{
        padding: 12px 0;
        border-bottom: 1px solid #f2f2f2;
        display: flex;
        align-items: center;
        gap: 15px;
    }}

    .media-tag {{
        font-family: 'NeoHyundaiBold', sans-serif !important;
        font-size: 0.75rem;
        color: #002c5f;
        background-color: #f0f4f8;
        padding: 4px 12px;
        border-radius: 4px;
        min-width: 100px;
        text-align: center;
        border: 1px solid #dce6f0;
    }}

    .title-link {{
        font-family: 'NeoHyundaiReg', sans-serif !important;
        font-size: 1.05rem;
        font-weight: 400;
        color: #333;
        text-decoration: none;
        line-height: 1.4;
    }}

    .title-link:hover {{
        color: #002c5f;
        text-decoration: underline;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ 폰트 파일(NeoHyundai_B.woff2, NeoHyundai_R.woff2) 경로 확인 필요")

# 🔥 최초 실행 시 업데이트 시간 저장
if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

# 2. 매체명 매핑
KOR_MEDIA_DICT = {
    'bizwn': '비즈니스포스트', 'hankookilbo': '한국일보', 'woman.chosun': '여성조선',
    'hankyung': '한국경제', 'mk.co.kr': '매일경제', 'yna.co.kr': '연합뉴스',
    'chosun.com': '조선일보', 'donga.com': '동아일보', 'joins.com': '중앙일보',
    'sedaily': '서울경제', 'edaily': '이데일리', 'mt.co.kr': '머니투데이',
    'heraldcorp': '헤럴드경제', 'newsis': '뉴시스', 'news1': '뉴스1',
    'etnews': '전자신문', 'fnnews': '파이낸셜뉴스', 'bizwatch': '비즈워치',
    'v.daum.net': '다음뉴스', 'daum.net': '다음뉴스', 'naver.com': '네이버뉴스'
}

def clean_text(text):
    if not text:
        return ""
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(clean, '', text).strip()

def get_kor_media_name(link):
    link = link.lower()
    for key, kor_name in KOR_MEDIA_DICT.items():
        if key in link:
            return kor_name
    
    match = re.search(r'https?://(?:www\.)?([^/.]+)', link)
    if match:
        domain = match.group(1)
        if len(domain) > 2:
            return domain.upper()
    return "뉴스"

# 3. 뉴스 수집
def get_naver_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=5&sort=date"
    headers = {
        "X-Naver-Client-Id": st.secrets.get("NAVER_ID", ""),
        "X-Naver-Client-Secret": st.secrets.get("NAVER_SECRET", "")
    }
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except:
        return []

def get_google_news(query):
    try:
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
        d = feedparser.parse(url)
        return d.entries[:5]
    except:
        return []

# 🔹 제목 + 새로고침 버튼
col_title, col_btn = st.columns([6, 1])

with col_title:
    st.markdown('<div class="custom-title">📢 현대 뉴스 실시간 브리핑</div>', unsafe_allow_html=True)
    st.write(f"최종 업데이트: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

with col_btn:
    st.write("")
    if st.button("🔄 뉴스 새로고침", use_container_width=True):
        st.session_state.last_update = datetime.now()
        st.rerun()

# 4. 키워드
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    st.subheader(f"🔍 {kw}")
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("🔹 네이버 뉴스")
        items = get_naver_news(kw)
        for item in items:
            raw_title = clean_text(item['title'])
            kor_media = get_kor_media_name(item['originallink'])
            
            st.markdown(f'''
            <div class="news-item">
                <span class="media-tag">{kor_media}</span>
                <a href="{item["link"]}" target="_blank" class="title-link">{raw_title}</a>
            </div>
            ''', unsafe_allow_html=True)

    with col2:
        st.caption("🔹 구글 뉴스")
        entries = get_google_news(kw)
        for entry in entries:
            raw_t = clean_text(entry.title)
            title_part, media_part = raw_t.rsplit(" - ", 1) if " - " in raw_t else (raw_t, "구글")
            
            st.markdown(f'''
            <div class="news-item">
                <span class="media-tag">{media_part}</span>
                <a href="{entry.link}" target="_blank" class="title-link">{title_part}</a>
            </div>
            ''', unsafe_allow_html=True)

    st.divider()
