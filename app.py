import streamlit as st
import requests
from datetime import datetime
# 자동 새로고침을 위한 도구
from streamlit_autorefresh import st_autorefresh

# 1. 페이지 설정 및 자동 새로고침 (1800초 = 30분마다 자동 실행)
st.set_page_config(page_title="현대그룹 뉴스 비서", layout="wide")
st_autorefresh(interval=30 * 60 * 1000, key="news_check")

st.title("🚀 현대그룹 실시간 뉴스 비서 (30분 자동 감시)")

# 2. 보안 정보
NAVER_ID = st.secrets["NAVER_ID"]
NAVER_SECRET = st.secrets["NAVER_SECRET"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

# 3. 뉴스 검색 및 알림 로직
def get_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=3&sort=date"
    headers = {"X-Naver-Client-Id": NAVER_ID, "X-Naver-Client-Secret": NAVER_SECRET}
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except: return []

def send_telegram(kw, item):
    title = item['title'].replace('<b>','').replace('</b>','').replace('&quot;', '"')
    link = item['link']
    msg = f"📢 [신규 뉴스 포착: {kw}]\n\n{title}\n\n바로가기: {link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": msg})

# 4. 화면 출력
raw_keywords = "현정은, 현대엘리베이터, 현대무벡스" # 상시 감시용 고정
keywords_list = [k.strip() for k in raw_keywords.split(",")]

st.info(f"⏱️ 마지막 자동 확인 시각: {datetime.now().strftime('%H:%M:%S')} (30분 후 자동 갱신)")

for kw in keywords_list:
    st.subheader(f"🔍 {kw}")
    items = get_news(kw)
    if items:
        # 앱 화면에는 3개 출력
        for i, item in enumerate(items):
            title = item['title'].replace('<b>','').replace('</b>','').replace('&quot;', '"')
            st.markdown(f"• **[{title}]({item['link']})**")
            
            # 자동 새로고침될 때마다 각 키워드 '1등 기사'를 알림으로 전송
            # (중복 알림 방지 로직은 추후 고도화 가능합니다)
            if i == 0:
                send_telegram(kw, item)
    st.divider()
