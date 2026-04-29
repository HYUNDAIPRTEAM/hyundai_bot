import streamlit as st
import requests
import feedparser
import os
from urllib.parse import quote

st.set_page_config(page_title="현대 뉴스 비서", layout="wide")
st.title("📢 현대 뉴스 실시간 브리핑")

# 뉴스 가져오기 함수
def fetch_all_news(kw):
    # 네이버 (Secrets 설정 필요)
    n_url = f"https://openapi.naver.com/v1/search/news.json?query={kw}&display=10&sort=date"
    headers = {
        "X-Naver-Client-Id": st.secrets["NAVER_ID"], 
        "X-Naver-Client-Secret": st.secrets["NAVER_SECRET"]
    }
    n_res = requests.get(n_url, headers=headers).json().get('items', [])
    
    # 구글
    g_url = f"https://news.google.com/rss/search?q={quote(kw)}&hl=ko&gl=KR&ceid=KR:ko"
    g_res = feedparser.parse(g_url).entries[:10]
    
    return n_res, g_res

# 버튼 디자인
if st.button('🔄 지금 최신 뉴스 새로고침'):
    keywords = ["현정은 회장", "현대엘리베이터", "현대무벡스"]
    
    for kw in keywords:
        st.header(f"📍 {kw}")
        n_news, g_news = fetch_all_news(kw)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔹 네이버 뉴스")
            for n in n_news:
                title = n['title'].replace('<b>','').replace('</b>','').replace('&quot;', '"')
                st.write(f"• [{title}]({n['link']})")
        
        with col2:
            st.subheader("🔹 구글 뉴스")
            for g in g_news:
                st.write(f"• [{g.title}]({g.link})")
        st.divider()
else:
    st.info("버튼을 누르면 '현정은 회장', '현대엘리베이터', '현대무벡스' 관련 최신 뉴스를 10개씩 가져옵니다.")
