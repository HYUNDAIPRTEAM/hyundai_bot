import streamlit as st
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime
import re

# 1. 시스템 설정
st.set_page_config(page_title="현대 뉴스 브리핑", page_icon="🗞️", layout="wide")

# 텍스트 정제 및 첫 문단 추출 함수
def get_first_paragraph(raw_html):
    if not raw_html: return ""
    # HTML 태그 제거
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    text = re.sub(clean, '', raw_html).strip()
    
    # 첫 번째 문장 혹은 적절한 길이의 첫 단락만 추출 (약 150자 내외)
    sentences = text.split('.')
    if len(sentences) > 0:
        first_part = sentences[0] + '.'
        if len(first_part) < 30 and len(sentences) > 1: # 너무 짧으면 다음 문장까지
            first_part += " " + sentences[1] + "."
        return first_part[:150]
    return text[:150]

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
    .news-box { padding: 12px; margin-bottom: 12px; border-bottom: 1px solid #eee; }
    .first-para { font-size: 0.88rem; color: #444; line-height: 1.6; margin-top: 8px; border-left: 3px solid #002c5f; padding-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📢 현대 뉴스 실시간 브리핑")
st.write(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 4. 모니터링 키워드
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    st.subheader(f"🔍 {kw} 실시간 동향")
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("🔹 네이버 뉴스 (첫 문단)")
        items = get_naver_news(kw)
        for item in items:
            t = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '', item['title'])
            p = get_first_paragraph(item['description'])
            st.markdown(f'<div class="news-box"><a href="{item["link"]}" target="_blank" style="text-decoration:none; color:#111; font-weight:bold;">{t}</a><div class="first-para">{p}</div></div>', unsafe_allow_html=True)

    with col2:
        st.caption("🔹 구글 뉴스 (첫 문단)")
        entries = get_google_news(kw)
        for entry in entries:
            gt = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '', entry.title)
            # 구글 뉴스 요약에서 제목과 겹치지 않는 본문 시작점 추출
            gp = get_first_paragraph(entry.summary if 'summary' in entry else "")
            
            # 제목과 내용이 거의 같다면 표시하지 않음
            display_p = f'<div class="first-para">{gp}</div>' if len(gp) > len(gt) + 10 else ""
            
            st.markdown(f'<div class="news-box"><a href="{entry.link}" target="_blank" style="text-decoration:none; color:#111; font-weight:bold;">{gt}</a>{display_p}</div>', unsafe_allow_html=True)
    st.divider()

# 5. 사이드바
st.sidebar.info("사용자: 현대그룹 커뮤니케이션실")
if st.sidebar.button("지금 새로고침"): st.rerun()
st.sidebar.divider()
st.sidebar.caption("네이버/구글 뉴스 실시간 모니터링 시스템")
