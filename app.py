import streamlit as st
import requests
from datetime import datetime
import re
import base64
import os

# 1. 시스템 및 스타일 설정
# 제목 변경 반영: 네이버/구글 실시간 모니터링
st.set_page_config(page_title="네이버/구글 실시간 모니터링", page_icon="🗞️", layout="wide")

# 매체명 매핑 사전 (기존 유지)
MEDIA_MAP = {
    'busan.com': '부산일보', 'etoday': '이투데이', 'biz.chosun': '조선비즈',
    'bizwn': '비즈니스포스트', 'businesspost': '비즈니스포스트', 'hankookilbo': '한국일보', 
    'woman.chosun': '여성조선', 'hankyung': '한국경제', 'mk.co.kr': '매일경제', 
    'yna.co.kr': '연합뉴스', 'sedaily': '서울경제', 'edaily': '이데일리', 
    'mt.co.kr': '머니투데이', 'heraldcorp': '헤럴드경제', 'news1.kr': '뉴스1', 
    'newsis': '뉴시스', 'pinpointnews': '핀포인트뉴스', 'topdaily': '톱데일리',
    'insight': '인사이트', 'labortoday': '매일노동뉴스', 'ccdaily': '충청일보',
    'ccdn': '충청매일', 'gukjenews': '국제뉴스', 'jeonmae': '전국매일신문',
    'queen': '퀸', 'v.daum': '다음뉴스'
}

def get_kor_media(link):
    link = link.lower()
    for domain, kor_name in MEDIA_MAP.items():
        if domain in link: return kor_name
    match = re.search(r'https?://(?:www\.)?([^/.]+)', link)
    if match:
        raw_name = match.group(1).upper()
        if "NEWS" in raw_name: return raw_name.replace("NEWS", "뉴스")
        return raw_name
    return "뉴스"

def clean_text(text):
    return re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6});', '', text).strip()

# 2. 뉴스 수집 로직
def get_naver_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=10&sort=date"
    headers = {
        "X-Naver-Client-Id": st.secrets.get("NAVER_ID", ""),
        "X-Naver-Client-Secret": st.secrets.get("NAVER_SECRET", "")
    }
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except: return []

# 3. 화면 UI 레이아웃 및 CSS
st.markdown("""
    <style>
    .custom-title { color: #002c5f !important; font-weight: 800; font-size: 2.2rem; margin-bottom: 5px; }
    
    /* arrow_down 텍스트 겹침 방지 */
    [data-testid="stExpander"] svg { display: none !important; }
    div[class*="st-emotion-cache"] span { color: transparent !important; font-size: 0px !important; line-height: 0 !important; }
    div[data-testid="stExpander"] summary p { color: #333 !important; font-weight: 700 !important; font-size: 1.1rem !important; }

    .news-card { padding: 10px; border-bottom: 1px solid #eee; display: flex; align-items: center; gap: 15px; min-height: 55px; }
    .m-tag { 
        min-width: 100px; text-align: center; font-size: 0.75rem; 
        font-weight: 700; color: #002c5f; background: #f1f6fa; 
        padding: 5px 8px; border-radius: 4px; border: 1px solid #dce6f0;
    }
    .n-link { font-size: 1rem; font-weight: 500; color: #333; text-decoration: none; line-height: 1.4; }
    .n-link:hover { color: #002c5f; text-decoration: underline; }
    
    .stButton>button { background-color: #002c5f !important; color: white !important; border-radius: 4px; border: none; height: 45px; width: 100%; }
    .stButton>button p { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 레이아웃 구성
st.markdown('<p style="color:#666; font-size:0.85rem; margin-bottom:0px;">사용자: 현대그룹 커뮤니케이션실</p>', unsafe_allow_html=True)
col_t, col_b = st.columns([4, 1])

with col_t:
    # 제목 수정: 네이버/구글 실시간 모니터링
    st.markdown('<h1 class="custom-title">📢 네이버/구글 실시간 모니터링</h1>', unsafe_allow_html=True)
    # 실시간 시간 반영: 뉴스를 불러오는 시점의 시간 표시
    fetch_time = datetime.now().strftime('%H:%M:%S')
    st.caption(f"최종 업데이트: {fetch_time}")

with col_b:
    st.write(" ")
    if st.button("🔄 뉴스 새로고침"):
        st.rerun()

# 현대 관련 주요 키워드
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    with st.expander(f"🔍 {kw} 실시간 뉴스", expanded=True):
        items = get_naver_news(kw) # 여기서 뉴스를 호출함과 동시에 위에서 fetch_time이 갱신됩니다.
        if items:
            col1, col2 = st.columns(2)
            for i, item in enumerate(items):
                target_col = col1 if i < 5 else col2
                media_name = get_kor_media(item['originallink'])
                with target_col:
                    st.markdown(f'''
                    <div class="news-card">
                        <div class="m-tag">{media_name}</div>
                        <a href="{item['link']}" target="_blank" class="n-link">{clean_text(item['title'])}</a>
                    </div>
                    ''', unsafe_allow_html=True)
