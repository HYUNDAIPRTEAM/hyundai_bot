import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="현대그룹 뉴스 모니터링", layout="wide")
st.title("🚀 현대그룹 실시간 뉴스 대시보드")

NAVER_ID = st.secrets["NAVER_ID"]
NAVER_SECRET = st.secrets["NAVER_SECRET"]

with st.sidebar:
    st.header("모니터링 설정")
    # 여러 키워드를 쉼표로 입력받게 합니다.
    raw_keywords = st.text_input("검색 키워드 (쉼표로 구분)", value="현정은, 현대엘리베이터, 현대무벡스")
    num_news = st.slider("키워드당 가져올 뉴스 개수", 5, 30, 10)

def get_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={num_news}&sort=date"
    headers = {"X-Naver-Client-Id": NAVER_ID, "X-Naver-Client-Secret": NAVER_SECRET}
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except:
        return []

if raw_keywords:
    # 쉼표를 기준으로 키워드를 분리합니다.
    keywords_list = [k.strip() for k in raw_keywords.split(",") if k.strip()]
    
    all_news = []
    for kw in keywords_list:
        all_news.extend(get_news(kw))
    
    # 중복 뉴스 제거 및 날짜순 정렬
    unique_news = {item['link']: item for item in all_news}.values()
    sorted_news = sorted(unique_news, key=lambda x: x['pubDate'], reverse=True)

    st.success(f"✅ 업데이트 시각: {datetime.now().strftime('%H:%M:%S')} (키워드 {len(keywords_list)}개 모니터링 중)")
    
    if not sorted_news:
        st.warning("현재 검색된 뉴스가 없습니다.")
    else:
        for item in sorted_news:
            title = item['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
            st.markdown(f"### [{title}]({item['link']})")
            # 날짜 형식 예쁘게 출력
            st.caption(f"📅 {item['pubDate']} | 🔍 검색어 관련 뉴스")
            st.write(item['description'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"'))
            st.divider()
