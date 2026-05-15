import streamlit as st
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime
import re
import base64
import os

# 1. 시스템 설정
st.set_page_config(page_title="HYUNDAI NEWS MONITORING", page_icon="🗞️", layout="wide")

# 🔹 폰트 로드 함수
def load_font(font_file):
    if os.path.exists(font_file):
        with open(font_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 🔹 폰트 데이터 로딩
font_bold = "NeoHyundai_B.woff2"
font_reg = "NeoHyundai_R.woff2"
data_b = load_font(font_bold)
data_r = load_font(font_reg)

# 🔹 CSS 적용
if data_b and data_r:
    st.markdown(f"""
    <style>
    @font-face {{ font-family: 'NeoHyundaiBold'; src: url(data:font/woff2;base64,{data_b}) format('woff2'); }}
    @font-face {{ font-family: 'NeoHyundaiReg'; src: url(data:font/woff2;base64,{data_r}) format('woff2'); }}
    * {{ font-family: 'NeoHyundaiReg', sans-serif !important; }}
    .custom-title {{ font-family: 'NeoHyundaiBold', sans-serif !important; font-size: 2.2rem; color: #002c5f; margin-bottom: 10px; }}
    .news-item {{ padding: 10px 0; border-bottom: 1px solid #f2f2f2; display: flex; align-items: center; gap: 15px; }}
    .media-tag {{ font-family: 'NeoHyundaiBold', sans-serif !important; font-size: 0.75rem; color: #002c5f; background-color: #f0f4f8; padding: 4px 12px; border-radius: 4px; min-width: 100px; text-align: center; border: 1px solid #dce6f0; }}
    .blog-tag {{ font-family: 'NeoHyundaiBold', sans-serif !important; font-size: 0.75rem; color: #2db400; background-color: #f0fff0; padding: 4px 12px; border-radius: 4px; min-width: 100px; text-align: center; border: 1px solid #2db400; }}
    .title-link {{ font-size: 1.05rem; color: #333; text-decoration: none; line-height: 1.4; }}
    .title-link:hover {{ color: #002c5f; text-decoration: underline; }}
    </style>
    """, unsafe_allow_html=True)

# 2. 유틸리티 함수
def clean_text(text):
    return re.sub(r'<.*?>|&[a-z0-9]+;', '', text).strip()

def get_kor_media_name(link):
    # ✅ 국문 매칭 딕셔너리
    KOR_MEDIA_DICT = {
        'hankyung': '한국경제', 'mk.co.kr': '매일경제', 'chosun': '조선일보', 'donga': '동아일보', 'joins': '중앙일보',
        'hani': '한겨레', 'khan': '경향신문', 'segye': '세계일보', 'kmib': '국민일보', 'hankookilbo': '한국일보',
        'seoul.co.kr': '서울신문', 'heraldcorp': '헤럴드경제', 'fnnews': '파이낸셜뉴스', 'asiae': '아시아경제',
        'ajunews': '아주경제', 'etnews': '전자신문', 'dt.co.kr': '디지털타임스', 'bizwatch': '비즈워치',
        'newspim': '뉴스핌', 'newsis': '뉴시스', 'news1': '뉴스1', 'yna': '연합뉴스', 'ytn': 'YTN',
        'nocutnews': '노컷뉴스', 'ohmynews': '오마이뉴스', 'edaily': '이데일리', 'mt.co.kr': '머니투데이',
        'sedaily': '서울경제', 'bizwn': '비즈니스포스트', 'kbs': 'KBS', 'mbc': 'MBC', 'sbs': 'SBS'
    }
    link_lower = link.lower()
    # 1. 국문이 있으면 국문 반환
    for key, kor_name in KOR_MEDIA_DICT.items():
        if key in link_lower: return kor_name
    
    # 2. 국문이 없으면 영문(도메인) 추출하여 반환
    try:
        # www. 빼고 도메인 첫 단어 추출 (예: news.v.daum.net -> daum)
        domain_part = link.split('//')[-1].split('/')[0].replace('www.', '')
        parts = domain_part.split('.')
        return parts[-2] if len(parts) > 1 else parts[0]
    except:
        return "News"

# 3. 데이터 수집 함수
def get_naver_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=5&sort=date"
    headers = {"X-Naver-Client-Id": st.secrets.get("NAVER_ID", ""), "X-Naver-Client-Secret": st.secrets.get("NAVER_SECRET", "")}
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except: return []

def get_google_news(query):
    try:
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
        return feedparser.parse(url).entries[:5]
    except: return []

def get_naver_blog(query):
    url = f"https://openapi.naver.com/v1/search/blog.json?query={query}&display=5&sort=date"
    headers = {"X-Naver-Client-Id": st.secrets.get("NAVER_ID", ""), "X-Naver-Client-Secret": st.secrets.get("NAVER_SECRET", "")}
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except: return []

# 4. 화면 구성
if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

col_title, col_btn = st.columns([6, 1])
with col_title:
    st.markdown('<div class="custom-title">📢 HYUNDAI NEWS MONITORING</div>', unsafe_allow_html=True)
    st.write(f"최종 업데이트: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
with col_btn:
    if st.button("🔄 뉴스 새로고침", use_container_width=True):
        st.session_state.last_update = datetime.now()

# 5. 키워드별 출력
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    st.subheader(f"🔍 {kw}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.caption("🔹 네이버 뉴스")
        for item in get_naver_news(kw):
            # ✅ 네이버 매체명 로직 적용 (국문 없으면 영문)
            target_link = item.get('originallink') if item.get('originallink') else item.get('link', '')
            m_name = get_kor_media_name(target_link)
            st.markdown(f'''<div class="news-item"><span class="media-tag">{m_name}</span><a href="{item["link"]}" target="_blank" class="title-link">{clean_text(item['title'])}</a></div>''', unsafe_allow_html=True)
            
    with col2:
        st.caption("🔹 구글 뉴스")
        for entry in get_google_news(kw):
            raw_t = clean_text(entry.title)
            if " - " in raw_t:
                t_part, m_name = raw_t.rsplit(" - ", 1)
            else:
                t_part, m_name = raw_t, get_kor_media_name(entry.link)
            st.markdown(f'''<div class="news-item"><span class="media-tag">{m_name}</span><a href="{entry.link}" target="_blank" class="title-link">{t_part}</a></div>''', unsafe_allow_html=True)

    if kw == "현정은":
        st.write("")
        st.caption("📝 네이버 블로그(최신순)")
        blogs = get_naver_blog(kw)
        if blogs:
            for blog in blogs:
                b_name = blog.get('bloggername', 'BLOG')
                st.markdown(f'''<div class="news-item"><span class="blog-tag">{b_name}</span><a href="{blog["link"]}" target="_blank" class="title-link">{clean_text(blog['title'])}</a></div>''', unsafe_allow_html=True)
    
    st.divider()
