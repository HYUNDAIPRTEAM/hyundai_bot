import streamlit as st
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime
import re

# 1. 시스템 설정
st.set_page_config(page_title="현대 뉴스 브리핑", page_icon="🗞️", layout="wide")

# 매체명 매핑 딕셔너리 (도메인 포함 키워드 중심)
# 이미지에서 확인된 'v.daum.net' 등 모든 예외 사례를 반영했습니다.
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
    if not text: return ""
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(clean, '', text).strip()

def get_kor_media_name(link):
    link = link.lower()
    # 1순위: 지정된 딕셔너리에서 매핑
    for key, kor_name in KOR_MEDIA_DICT.items():
        if key in link:
            return kor_name
    
    # 2순위: 도메인 추출 후 첫 글자만 대문자로 하거나 '뉴스' 처리
    match = re.search(r'https?://(?:www\.)?([^/.]+)', link)
    if match:
        domain = match.group(1)
        # 영문 도메인이 너무 지저분하게 나오는 것을 방지
        if len(domain) > 2:
            return domain.upper()
    return "뉴스"

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

# 3. 디자인 스타일링 (미니멀리즘)
st.markdown("""
    <style>
    .stTitle { color: #002c5f; font-weight: 800; margin-bottom: 25px; }
    .news-item { padding: 12px 0; border-bottom: 1px solid #f2f2f2; display: flex; align-items: center; gap: 15px; }
    .media-tag { 
        font-size: 0.75rem; color: #002c5f; background-color: #f0f4f8; 
        padding: 4px 12px; border-radius: 4px; font-weight: 700; white-space: nowrap;
        min-width: 100px; text-align: center; border: 1px solid #dce6f0;
    }
    .title-link { font-size: 1.05rem; font-weight: 500; color: #333; text-decoration: none; line-height: 1.4; }
    .title-link:hover { color: #002c5f; text-decoration: underline; }
    </style>
    """, unsafe_allow_html=True)

st.title("📢 현대 뉴스 실시간 브리핑")
st.write(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 4. 키워드 모니터링
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    st.subheader(f"🔍 {kw}")
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("🔹 네이버 뉴스")
        items = get_naver_news(kw)
        for item in items:
            raw_title = clean_text(item['title'])
            kor_media = get_kor_media_name(item['originallink']) # 보강된 로직
            
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
