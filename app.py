import streamlit as st
import feedparser
from urllib.parse import quote
from datetime import datetime
import re

# 1. 시스템 설정 (현대 블루 컬러 테마)
st.set_page_config(page_title="현대 뉴스 실시간 브리핑", page_icon="🗞️", layout="wide")

def clean_text(text):
    if not text: return ""
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(clean, '', text).strip()

def get_google_news(query, count=10):
    try:
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
        d = feedparser.parse(url)
        return d.entries[:count]
    except: return []

# 2. 디자인 스타일링 (팀장님 취향의 미니멀 화이트)
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

# 3. 키워드 모니터링 (현정은, 현대엘리베이터, 현대무벡스)
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    st.subheader(f"🔍 {kw}")
    
    # 10개의 뉴스를 가져와서 좌우 5개씩 나눕니다.
    all_news = get_google_news(kw, count=10)
    col1, col2 = st.columns(2)
    
    # 좌측 열 (1~5번 뉴스)
    with col1:
        for entry in all_news[:5]:
            raw_t = clean_text(entry.title)
            title_part, media_part = raw_t.rsplit(" - ", 1) if " - " in raw_t else (raw_t, "뉴스")
            st.markdown(f'''
            <div class="news-item">
                <span class="media-tag">{media_part}</span>
                <a href="{entry.link}" target="_blank" class="title-link">{title_part}</a>
            </div>
            ''', unsafe_allow_html=True)

    # 우측 열 (6~10번 뉴스)
    with col2:
        for entry in all_news[5:]:
            raw_t = clean_text(entry.title)
            title_part, media_part = raw_t.rsplit(" - ", 1) if " - " in raw_t else (raw_t, "뉴스")
            st.markdown(f'''
            <div class="news-item">
                <span class="media-tag">{media_part}</span>
                <a href="{entry.link}" target="_blank" class="title-link">{title_part}</a>
            </div>
            ''', unsafe_allow_html=True)
    st.divider()

# 4. 사이드바
st.sidebar.info("사용자: 현대그룹 커뮤니케이션실")
st.sidebar.caption("실시간 미디어 모니터링 v4.0")
