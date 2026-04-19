import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 30분마다 자동 새로고침
st_autorefresh(interval=30 * 60 * 1000, key="news_check")

st.title("🚀 현대그룹 지능형 뉴스 비서")

# 보안 정보
NAVER_ID = st.secrets["NAVER_ID"]
NAVER_SECRET = st.secrets["NAVER_SECRET"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

def get_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=3&sort=date"
    headers = {"X-Naver-Client-Id": NAVER_ID, "X-Naver-Client-Secret": NAVER_SECRET}
    res = requests.get(url, headers=headers)
    return res.json().get('items', [])

def send_telegram(kw, item):
    title = item['title'].replace('<b>','').replace('</b>','').replace('&quot;', '"')
    msg = f"📢 [신규 뉴스 포착: {kw}]\n\n{title}\n\n{item['link']}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": msg})

# 감시 키워드
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

st.info(f"⏱️ 마지막 확인: {datetime.now().strftime('%H:%M:%S')} (새로운 뉴스가 있을 때만 알림을 보냅니다)")

# 핵심: '세션 상태'를 이용해 이전에 보낸 뉴스 제목을 기억합니다.
if "last_news" not in st.session_state:
    st.session_state.last_news = {}

for kw in keywords:
    st.subheader(f"🔍 {kw}")
    items = get_news(kw)
    
    if items:
        latest_item = items[0]
        latest_title = latest_item['title']
        
        # 앱 화면에는 항상 리스트 출력
        for item in items:
            title = item['title'].replace('<b>','').replace('</b>','').replace('&quot;', '"')
            st.markdown(f"• [{title}]({item['link']})")
        
        # [알림 로직] 이전에 보낸 제목과 다를 때만 텔레그램 전송
        if st.session_state.last_news.get(kw) != latest_title:
            send_telegram(kw, latest_item)
            st.session_state.last_news[kw] = latest_title # 새 제목을 기억 장치에 저장
            st.toast(f"{kw} 새로운 알림 전송 완료!")
    st.divider()
