import streamlit as st
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime
import re

# 1. 시스템 설정
st.set_page_config(page_title="현대 뉴스 브리핑", page_icon="🗞️", layout="wide")

# 텍스트 및 첫 문장 정제 함수
def clean_text(text):
    if not text: return ""
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(clean, '', text).strip()

def get_first_sentence(text):
    text = clean_text(text)
    if not text: return ""
    sentence = text.split('.')[0]
    return sentence + "." if len(sentence) > 5 else ""

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

# 3. 디자인 스타일링
st.markdown("""
    <style>
    .stTitle { color: #002c5f; font-weight: 800; }
    .news-item { padding: 10px 0; border-bottom: 1px solid #f0f0f0; }
    .header-line { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
    .media-tag { 
        font-size: 0.72rem; 
        color: #ffffff; 
        background-color: #002c5f; 
        padding: 2px 8px; 
        border-radius: 3px; 
        font-weight: 600;
        white-space: nowrap;
        text-transform: uppercase;
    }
    .title-link { 
        font-size: 1.02rem; 
        font-weight: 700; 
        color: #111; 
        text-decoration: none; 
        line-height: 1.3;
    }
    .first-sentence { 
        font-size: 0.88rem; 
        color: #666; 
        line-height: 1.5; 
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📢 현대 뉴스 실시간 브리핑")
st.write(f"업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 4. 키워드 모니터링
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    st.subheader(f"🔍 {kw} 동향")
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("🔹 네이버 뉴스")
        items = get_naver_news(kw)
        for item in items:
            raw_title = clean_text(item['title'])
            # 링크에서 매체사 도메인 추출 시도 (예: naver.com, yna.co.kr 등)
            media_match = re.search(r'https?://(?:www\.)?([^/]+)', item['originallink'])
            media_name = media_match.group(1).split('.')[0] if media_match else "NAVER"
            
            first_s = get_first_sentence(item['description'])
            
            st.markdown(f'''
            <div class="news-item">
                <div class="header-line">
                    <span class="media-tag">{media_name}</span>
                    <a href="{item["link"]}" target="_blank" class="title-link">{raw_title}</a>
                </div>
                <div class="first-sentence">{first_s}</div>
            </div>
            ''', unsafe_allow_html=True)

    with col2:
        st.caption("🔹 구글 뉴스")
        entries = get_google_news(kw)
        for entry in entries:
            raw_t = clean_text(entry.title)
            if " - " in raw_t:
                title_part, media_part = raw_t.rsplit(" - ", 1)
            else:
                title_part, media_part = raw_t, "GOOGLE"
            
            first_s = get_first_sentence(entry.summary if 'summary' in entry else "")
            display_s = first_s if len(first_s) > 10 and title_part[:10] not in first_s else ""
            
            st.markdown(f'''
            <div class="news-item">
                <div class="header-line">
                    <span class="media-tag">{media_part}</span>
                    <a href="{entry.link}" target="_blank" class="title-link">{title_part}</a>
                </div>
                <div class="first-sentence">{display_s}</div>
            </div>
            ''', unsafe_allow_html=True)
    st.divider()

# 5. 사이드바
st.sidebar.info("사용자: 현대그룹 커뮤니케이션실")
if st.sidebar.button("지금 새로고침"): st.rerun()
st.sidebar.caption("네이버/구글 뉴스 모니터링 시스템 v2.1")
