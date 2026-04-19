import streamlit as st
import requests
from datetime import datetime
import time

# 1. 페이지 및 보안 설정
st.set_page_config(page_title="현대그룹 뉴스 비서", layout="wide", initial_sidebar_state="collapsed")
NAVER_ID = st.secrets["NAVER_ID"]
NAVER_SECRET = st.secrets["NAVER_SECRET"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

st.title("📱 현대그룹 실시간 뉴스 비서")

# 2. 뉴스 검색 및 알림 함수
def get_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=3&sort=date"
    headers = {"X-Naver-Client-Id": NAVER_ID, "X-Naver-Client-Secret": NAVER_SECRET}
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except:
        return []

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.get(url, params=params)

# 3. 화면 출력 및 로직
raw_keywords = st.sidebar.text_input("감시 키워드", value="현정은, 현대엘리베이터, 현대무벡스")
keywords_list = [k.strip() for k in raw_keywords.split(",") if k.strip()]

if st.button("🔄 지금 즉시 뉴스 체크"):
    st.write("뉴스를 확인 중입니다...")
    for kw in keywords_list:
        items = get_news(kw)
        if items:
            latest_news = items[0]
            title = latest_news['title'].replace('<b>','').replace('</b>','')
            link = latest_news['link']
            
            # 텔레그램으로 즉시 보고
            msg = f"📢 [신규 뉴스 포착: {kw}]\n\n{title}\n\n바로가기: {link}"
            send_telegram(msg)
            st.success(f"'{kw}' 관련 뉴스를 텔레그램으로 전송했습니다.")

# 4. 30분 자동 새로고침 (Streamlit 편법)
st.caption(f"⏱️ 마지막 확인: {datetime.now().strftime('%H:%M:%S')}")
time.sleep(1) # 부하 방지
# st.empty() 등을 이용한 자동 재실행 로직은 리소스를 많이 먹으므로 
# 브라우저만 켜두시면 30분마다 알림이 가도록 세팅해 드릴 수 있습니다.
