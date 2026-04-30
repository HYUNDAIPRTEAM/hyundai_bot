import streamlit as st
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime
import re

# 1. 시스템 설정 및 홈 화면 이름 정의
st.set_page_config(
    page_title="현대 뉴스 브리핑", 
    page_icon="🗞️", 
    layout="wide"
)

# 텍스트 정제 함수 (HTML 태그 및 특수문자 제거)
def clean_text(text):
    if not text: return ""
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(clean, '', text)

# 2. 뉴스 수집 로직 (네이버/구글 API)
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

# 3. 디자인 스타일링 (현대 블루 적용)
st.markdown("""
    <style>
    .stTitle { color: #002c5f; font-weight: 800; }
    .news-box { padding: 12px; margin-bottom: 12px; border-bottom: 1px solid #eee; }
    .summary-text { font-size: 0.85rem; color: #555; line-height: 1.5; margin-top: 6px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📢 현대 뉴스 실시간 브리핑")
st.write(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 4. 모니터링 키워드 리스트
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    st.subheader(f"🔍 {kw} 실시간 동향")
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("🔹 네이버 뉴스")
        items = get_naver_news(kw)
        if items:
            for item in items:
                title = clean_text(item['title'])
                desc = clean_text(item['description'])
                st.markdown(f'<div class="news-box"><a href="{item["link"]}" target="_blank" style="text-decoration:none; color:#111; font-weight:bold;">{title}</a><div class="summary-text">{desc[:110]}...</div></div>', unsafe_allow_html=True)
        else: st.write("최신 뉴스가 없습니다.")

    with col2:
        st.caption("🔹 구글 뉴스")
        entries = get_google_news(kw)
        if entries:
            for entry in entries:
                g_title = clean_text(entry.title)
                g_desc = clean_text(entry.summary if 'summary' in entry else "")
                st.markdown(f'<div class="news-box"><a href="{entry.link}" target="_blank" style="text-decoration:none; color:#111; font-weight:bold;">{g_title}</a><div class="summary-text">{g_desc[:110]}...</div></div>', unsafe_allow_html=True)
        else: st.write("최신 뉴스가 없습니다.")
    st.divider()

# 5. 사이드바 관리 설정
st.sidebar.info("사용자: 현대그룹 커뮤니케이션실")
if st.sidebar.button("지금 새로고침"): st.rerun()
st.sidebar.divider()
st.sidebar.caption("네이버/구글 뉴스 실시간 모니터링 시스템")
