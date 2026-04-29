import streamlit as st
import requests
import feedparser
from urllib.parse import quote

st.title("📢 현대 뉴스 실시간 브리핑")

# 1. 뉴스 가져오기 함수 (기존 로직 활용)
def fetch_all_news(kw):
    # 네이버 뉴스
    n_url = f"https://openapi.naver.com/v1/search/news.json?query={kw}&display=3&sort=date"
    headers = {"X-Naver-Client-Id": st.secrets["NAVER_ID"], "X-Naver-Client-Secret": st.secrets["NAVER_SECRET"]}
    n_res = requests.get(n_url, headers=headers).json().get('items', [])
    
    # 구글 뉴스
    g_url = f"https://news.google.com/rss/search?q={quote(kw)}&hl=ko&gl=KR&ceid=KR:ko"
    g_res = feedparser.parse(g_url).entries[:5]
    
    return n_res, g_res

# 2. 새로고침 버튼 만들기
if st.button('🔄 지금 뉴스 새로고침'):
    keywords = ["현정은", "현대엘리베이터", "현대무벡스"] #
    
    for kw in keywords:
        st.subheader(f"📍 {kw} 관련 소식")
        n_news, g_news = fetch_all_news(kw)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔹 네이버 뉴스**")
            for n in n_news:
                title = n['title'].replace('<b>','').replace('</b>','').replace('&quot;', '"')
                st.caption(f"• [{title}]({n['link']})")
        
        with col2:
            st.markdown("**🔹 구글 뉴스**")
            for g in g_news:
                st.caption(f"• [{g.title}]({g.link})")
        st.divider()
else:
    st.info("위의 버튼을 누르면 실시간 뉴스를 가져옵니다.")
