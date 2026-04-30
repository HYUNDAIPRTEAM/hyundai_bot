import streamlit as st
import requests
from datetime import datetime
import re

# 1. 시스템 및 스타일 설정
st.set_page_config(page_title="현대 실시간 뉴스", page_icon="🗞️", layout="wide")

# 매체명 강제 매핑 사전 (이미지 속 영문들을 한글로 모두 치환)
# 팀장님, BUSAN -> 부산일보, ETODAY -> 이투데이 식으로 모두 잡았습니다.
MEDIA_MAP = {
    'busan.com': '부산일보', 'etoday': '이투데이', 'biz.chosun': '조선비즈',
    'bizwn': '비즈니스포스트', 'hankookilbo': '한국일보', 'woman.chosun': '여성조선',
    'hankyung': '한국경제', 'mk.co.kr': '매일경제', 'yna.co.kr': '연합뉴스',
    'sedaily': '서울경제', 'edaily': '이데일리', 'mt.co.kr': '머니투데이',
    'heraldcorp': '헤럴드경제', 'news1.kr': '뉴스1', 'newsis': '뉴시스',
    'v.daum': '다음뉴스', 'jeonmae': '전국매일신문', 'fnnews': '파이낸셜뉴스'
}

def get_kor_media(link):
    link = link.lower()
    for domain, kor_name in MEDIA_MAP.items():
        if domain in link:
            return kor_name
    # 매핑되지 않은 경우 도메인 앞글자만 따서 깔끔하게 표시
    match = re.search(r'https?://(?:www\.)?([^/.]+)', link)
    return match.group(1).upper() if match else "뉴스"

def clean_text(text):
    return re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6});', '', text).strip()

# 2. 뉴스 수집 로직 (네이버 우선)
def get_naver_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=8&sort=date"
    headers = {
        "X-Naver-Client-Id": st.secrets.get("NAVER_ID", ""),
        "X-Naver-Client-Secret": st.secrets.get("NAVER_SECRET", "")
    }
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except: return []

# 3. 화면 UI 레이아웃
st.markdown("""
    <style>
    .stTitle { color: #002c5f; font-weight: 800; margin-bottom: 20px; }
    .news-card { padding: 12px; border-bottom: 1px solid #eee; display: flex; align-items: center; gap: 15px; }
    .m-tag { 
        min-width: 95px; text-align: center; font-size: 0.72rem; 
        font-weight: 700; color: #002c5f; background: #f1f6fa; 
        padding: 4px 8px; border-radius: 4px; border: 1px solid #dce6f0;
    }
    .n-link { font-size: 1.05rem; font-weight: 500; color: #333; text-decoration: none; }
    .n-link:hover { color: #002c5f; text-decoration: underline; }
    </style>
    """, unsafe_allow_html=True)

st.title("📢 현대 실시간 미디어 모니터링")
st.caption(f"최종 업데이트: {datetime.now().strftime('%H:%M:%S')} (네이버 뉴스 우선 검색)")

keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    with st.expander(f"🔍 {kw} 실시간 뉴스", expanded=True):
        items = get_naver_news(kw)
        if items:
            # 2열 배치로 시인성 확보
            col1, col2 = st.columns(2)
            for i, item in enumerate(items):
                target_col = col1 if i < 4 else col2
                media_name = get_kor_media(item['originallink'])
                with target_col:
                    st.markdown(f'''
                    <div class="news-card">
                        <div class="m-tag">{media_name}</div>
                        <a href="{item['link']}" target="_blank" class="n-link">{clean_text(item['title'])}</a>
                    </div>
                    ''', unsafe_allow_html=True)
        else:
            st.write("검색 결과가 없습니다.")
