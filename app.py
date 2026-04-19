import streamlit as st
import requests
from datetime import datetime

# 1. 페이지 설정 (사이드바 숨김, 넓은 화면)
st.set_page_config(page_title="현대그룹 뉴스 요약", layout="wide", initial_sidebar_state="collapsed")

# 앱 제목
st.title("📱 현대그룹 핵심 뉴스 (TOP 3)")

# 2. 보안 설정 (Secrets에서 API 키 불러오기)
NAVER_ID = st.secrets["NAVER_ID"]
NAVER_SECRET = st.secrets["NAVER_SECRET"]

# 3. 사이드바 - 키워드 설정
with st.sidebar:
    st.header("설정")
    # 쉼표로 키워드 구분 (기본값 설정)
    raw_keywords = st.text_input("모니터링 키워드", value="현정은, 현대엘리베이터, 현대무벡스, 현대경제연구원")
    # 키워드별 뉴스 개수를 3개로 고정
    show_count = 3 

# 4. 네이버 뉴스 검색 함수
def get_news(query):
    # sort=date: 최신순 정렬
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={show_count}&sort=date"
    headers = {
        "X-Naver-Client-Id": NAVER_ID, 
        "X-Naver-Client-Secret": NAVER_SECRET
    }
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except:
        return []

# 5. 화면 출력 로직
if raw_keywords:
    # 입력받은 키워드를 리스트로 변환
    keywords_list = [k.strip() for k in raw_keywords.split(",") if k.strip()]
    
    # 상단에 업데이트 시각 표시
    st.info(f"⏱️ 업데이트: {datetime.now().strftime('%m/%d %H:%M')}")

    # 키워드별로 루프를 돌며 뉴스 출력
    for kw in keywords_list:
        st.subheader(f"🔍 {kw}")
        items = get_news(kw)
        
        if not items:
            st.write(" 최근 올라온 소식이 없습니다.")
        else:
            for item in items:
                # 제목에서 HTML 태그 및 특수문자 제거
                title = item['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
                # 게시일 날짜 형식 정리 (네이버 제공 형식에서 필요한 부분만 추출)
                pub_date = item['pubDate'][5:16] 
                
                # 리스트 형태로 출력 (제목 클릭 시 링크 이동)
                st.markdown(f"• **[{title}]({item['link']})**")
                st.caption(f"  └ {pub_date}")
        
        # 섹션 간 구분선 대신 여백 추가
        st.write("")
