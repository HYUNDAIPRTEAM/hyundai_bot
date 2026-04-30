import streamlit as st
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime

# 1. 홈 화면 이름 및 브랜딩 설정
st.set_page_config(
    page_title="현대 뉴스 브리핑", 
    page_icon="🗞️", 
    layout="wide"
)

# 2. 뉴스 수집 함수 (네이버/구글 API 활용)
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

# 3. 화면 디자인 설정
st.markdown("""
    <style>
    .stTitle { color: #002c5f; font-weight: 800; }
    .news-card { padding: 15px; border-radius: 10px; background-color: #f8f9fa; margin-bottom: 10px; border-left: 5px solid #002c5f; }
    </style>
    """, unsafe_allow_html=True)

st.title("📢 현대 뉴스 실시간 브리핑")
st.write(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 4. [업데이트] 키워드 리스트: 현정은 회장님 추가
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    st.subheader(f"🔍 {kw} 관련 소식")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("🔹 네이버 뉴스")
        items = get_naver_news(kw)
        if items:
            for item in items:
                # 검색어 강조 태그 제거 후 깔끔하게 제목 표시
                title = item['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
                st.markdown(f"**[{title}]({item['link']})**")
        else:
            st.write("최신 뉴스가 없습니다.")

    with col2:
        st.caption("🔹 구글 뉴스")
        entries = get_google_news(kw)
        if entries:
            for entry in entries:
                st.markdown(f"**[{entry.title}]({entry.link})**")
        else:
            st.write("최신 뉴스가 없습니다.")
    st.divider()

# 5. 사이드바 관리
st.sidebar.header("관리 메뉴")
st.sidebar.info("사용자: 현대 PR 팀장님")
if st.sidebar.button("지금 새로고침"):
    st.rerun()
