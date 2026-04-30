import streamlit as st
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime
import re

# 1. 시스템 설정 및 브랜딩
st.set_page_config(page_title="현대 뉴스 브리핑", page_icon="🗞️", layout="wide")

# 텍스트 정제 및 AI 요약 시뮬레이션 함수
def clean_and_summarize(title, raw_content):
    # 1. 태그 제거
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    text = re.sub(clean, '', raw_content)
    
    # 2. 제목 중복 제거 및 지능형 요약 로직
    if not text or len(text) < 20 or title[:20] in text[:50]:
        # 요약이 부실하거나 제목과 중복될 경우 제목 기반으로 핵심 키워드 추출 시뮬레이션
        summary = f"본 기사는 '{title[:30]}...' 관련 주요 소식을 다루고 있습니다. 상세 내용은 링크를 참조해 주세요."
    else:
        summary = text[:120].strip() + "..."
    
    return summary

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
    .news-box { padding: 12px; margin-bottom: 12px; border-bottom: 1px solid #eee; background-color: #ffffff; border-radius: 5px; }
    .summary-text { font-size: 0.85rem; color: #555; line-height: 1.5; margin-top: 6px; background: #f1f3f5; padding: 8px; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📢 현대 뉴스 실시간 브리핑")
st.write(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 4. 모니터링 키워드
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    st.subheader(f"🔍 {kw} 실시간 분석")
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("🔹 네이버 뉴스 분석")
        items = get_naver_news(kw)
        for item in items:
            t = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '', item['title'])
            d = clean_and_summarize(t, item['description'])
            st.markdown(f'<div class="news-box"><a href="{item["link"]}" target="_blank" style="text-decoration:none; color:#111; font-weight:bold;">{t}</a><div class="summary-text">{d}</div></div>', unsafe_allow_html=True)

    with col2:
        st.caption("🔹 구글 뉴스 분석")
        entries = get_google_news(kw)
        for entry in entries:
            gt = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '', entry.title)
            gd = clean_and_summarize(gt, entry.summary if 'summary' in entry else "")
            st.markdown(f'<div class="news-box"><a href="{entry.link}" target="_blank" style="text-decoration:none; color:#111; font-weight:bold;">{gt}</a><div class="summary-text">{gd}</div></div>', unsafe_allow_html=True)
    st.divider()

# 5. 사이드바
st.sidebar.info("사용자: 현대그룹 커뮤니케이션실")
if st.sidebar.button("지금 새로고침"): st.rerun()
st.sidebar.caption("AI 기반 실시간 뉴스 분석 시스템 v2.0")
