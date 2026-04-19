import streamlit as st
import requests
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="현대그룹 뉴스 모니터링", layout="wide")

st.title("🚀 현대그룹 실시간 뉴스 대시보드")

# API 정보 (Secrets에서 가져오기)
NAVER_ID = st.secrets["NAVER_ID"]
NAVER_SECRET = st.secrets["NAVER_SECRET"]

# 사이드바 설정
with st.sidebar:
    st.header("모니터링 설정")
    keyword = st.text_input("검색 키워드", value="현대엘리베이터")
    num_news = st.slider("가져올 뉴스 개수", 10, 50, 20)

# 뉴스 가져오기 함수
def get_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={num_news}&sort=sim"
    headers = {"X-Naver-Client-Id": NAVER_ID, "X-Naver-Client-Secret": NAVER_SECRET}
    res = requests.get(url, headers=headers)
    return res.json().get('items', [])

# 실행 버튼 없이 바로 보여주기
if keyword:
    news_items = get_news(keyword)
    st.success(f"✅ 업데이트 시각: {datetime.now().strftime('%H:%M:%S')}")
    
    if not news_items:
        st.warning("현재 검색된 뉴스가 없습니다. 키워드를 확인해 주세요.")
    else:
        for item in news_items:
            # HTML 태그 제거 및 출력
            title = item['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
            st.markdown(f"### [{title}]({item['link']})")
            st.caption(f"게시일: {item['pubDate']}")
            st.write(item['description'].replace('<b>', '').replace('</b>', ''))
            st.divider()
