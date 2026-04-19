import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="현대그룹 뉴스 모니터링", layout="wide")
st.title("🚀 현대그룹 키워드별 뉴스 대시보드")

NAVER_ID = st.secrets["NAVER_ID"]
NAVER_SECRET = st.secrets["NAVER_SECRET"]

with st.sidebar:
    st.header("모니터링 설정")
    # 쉼표로 키워드를 입력받습니다.
    raw_keywords = st.text_input("검색 키워드 (쉼표 구분)", value="현정은, 현대엘리베이터, 현대무벡스, 현대경제연구원")
    num_news = st.sidebar.number_input("키워드당 뉴스 개수", 1, 20, 5)

def get_news(query):
    # 최신순(date)으로 가져오도록 설정
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={num_news}&sort=date"
    headers = {"X-Naver-Client-Id": NAVER_ID, "X-Naver-Client-Secret": NAVER_SECRET}
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except:
        return []

if raw_keywords:
    keywords_list = [k.strip() for k in raw_keywords.split(",") if k.strip()]
    st.success(f"✅ 업데이트 시각: {datetime.now().strftime('%H:%M:%S')}")

    # 키워드별로 루프를 돌며 섹션을 생성합니다.
    for kw in keywords_list:
        with st.expander(f"🔍 '{kw}' 관련 최신 뉴스", expanded=True):
            items = get_news(kw)
            if not items:
                st.write("최근 관련 뉴스가 없습니다.")
            else:
                for item in items:
                    title = item['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
                    # 제목과 링크
                    st.markdown(f"**[{title}]({item['link']})**")
                    # 날짜만 추출해서 표시
                    st.caption(f"📅 {item['pubDate']}")
                    st.divider()
