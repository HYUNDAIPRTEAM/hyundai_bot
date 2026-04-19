import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 30분마다 자동 새로고침 (화면 업데이트용)
st_autorefresh(interval=30 * 60 * 1000, key="news_check")

st.title("🚀 현대그룹 뉴스 대시보드 (알람 중단 모드)")

# 보안 정보
NAVER_ID = st.secrets["NAVER_ID"]
NAVER_SECRET = st.secrets["NAVER_SECRET"]

def get_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=5&sort=date"
    headers = {"X-Naver-Client-Id": NAVER_ID, "X-Naver-Client-Secret": NAVER_SECRET}
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except:
        return []

# 감시 키워드
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

st.success("✅ 현재 텔레그램 알람이 꺼져 있습니다. 앱 화면에서만 뉴스를 확인하세요.")
st.info(f"⏱️ 마지막 확인 시각: {datetime.now().strftime('%H:%M:%S')}")

for kw in keywords:
    st.subheader(f"🔍 {kw}")
    items = get_news(kw)
    if items:
        for item in items:
            title = item['title'].replace('<b>','').replace('</b>','').replace('&quot;', '"')
            st.markdown(f"• [{title}]({item['link']})")
    else:
        st.write("최신 뉴스가 없습니다.")
    st.divider()
