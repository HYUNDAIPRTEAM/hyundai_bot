import streamlit as st
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime
import re

# 1. 시스템 설정
st.set_page_config(page_title="현대 뉴스 브리핑", page_icon="🗞️", layout="wide")

# 매체명 매핑 사전 (포함 여부 확인용)
# 팀장님, 자주 노출되는 매체들을 우선적으로 배치했습니다.
KOR_MEDIA_LIST = [
    ('yna', '연합뉴스'), ('hankyung', '한국경제'), ('mk.co.kr', '매일경제'), 
    ('chosun', '조선일보'), ('donga', '동아일보'), ('joins', '중앙일보'), 
    ('hani', '한겨레'), ('khan', '경향신문'), ('sedaily', '서울경제'), 
    ('edaily', '이데일리'), ('mt.co.kr', '머니투데이'), ('heraldcorp', '헤럴드경제'),
    ('newsis', '뉴시스'), ('news1', '뉴스1'), ('sbs', 'SBS'), ('kbs', 'KBS'), 
    ('mbc', 'MBC'), ('ytn', 'YTN'), ('etnews', '전자신문'), ('segye', '세계일보'), 
    ('seoul', '서울신문'), ('munhwa', '문화일보'), ('fnnews', '파이낸셜뉴스'), 
    ('ajunews', '아주경제'), ('kmib', '국민일보'), ('moneyis', '머니S'),
    ('bizwatch', '비즈워치'), ('digitaltimes', '디지털타임스')
]

def clean_text(text):
    if not text: return ""
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(clean, '', text).strip()

# 링크 주소를 분석해 한글 매체명을 반환하는 함수
def get_kor_media_name(link):
    link = link.lower()
    for eng, kor in KOR_MEDIA_LIST:
        if eng in link:
            return kor
    return "뉴스" # 매핑되지 않은 경우 기본값

# 2. 뉴스 수집 로직
def get_naver_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=5&sort=date"
    headers = {
        "X-Naver-Client-Id": st.secrets.get("NAVER_ID", ""),
        "X-Naver-Client-Secret": st.secrets.get("NAVER_SECRET", "")
    }
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except: return []

def get_google_news(query):
    try:
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
        d = feedparser.parse(url)
        return d.entries[:5]
    except: return []

# 3. 디자인 스타일링 (미니멀 화이트)
st.markdown("""
    <style>
    .stTitle { color: #002c5f; font-weight: 800; margin-bottom: 25px; }
    .news-item { padding: 10px 0; border-bottom: 1px solid #f2f2f2; display: flex; align-items: center; gap: 12px; }
    .media-tag { 
        font-size: 0.75rem; color: #002c5f; background-color: #f0f4f8; 
        padding: 3px 10px; border-radius: 4px; font-weight: 700; white-space: nowrap;
        min-width: 90px; text-align: center;
    }
    .title-link { font-size: 1.05rem; font-weight: 500; color: #333; text-decoration: none; line-height: 1.4; }
    .title-link:hover { color: #002c5f; text-decoration: underline; }
    </style>
    """, unsafe_allow_html=True)

st.title("📢 현대 뉴스 실시간 브리핑")
st.write(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 4. 키워드 모니터링 (현정은, 현대엘리베이터, 현대무벡스)
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    st.subheader(f"🔍 {kw}")
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("🔹 네이버 뉴스")
        items = get_naver_news(kw)
        for item in items:
            raw_title = clean_text(item['title'])
            # 보강된 한글 추출 로직 적용
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

# 5. 사이드바
st.sidebar.info("사용자: 현대그룹 커뮤니케이션실")
if st.sidebar.button("지금 새로고침"): st.rerun()
st.sidebar.caption("실시간 미디어 모니터링 v3.2")
