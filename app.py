import streamlit as st
import requests
from datetime import datetime
import re

# 1. 시스템 및 스타일 설정
st.set_page_config(page_title="현대 실시간 뉴스", page_icon="🗞️", layout="wide")

# 매체명 매핑 사전 (이미지의 영문들을 한글로 모두 업데이트)
# 팀장님, 새로 발견된 영문들을 꼼꼼하게 다 집어넣었습니다.
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
    # 1. 사전 등록된 매체인지 확인
    for domain, kor_name in MEDIA_MAP.items():
        if domain in link:
            return kor_name
    
    # 2. 사전에는 없지만 'news'가 포함된 경우 처리 (자동 보정)
    match = re.search(r'https?://(?:www\.)?([^/.]+)', link)
    if match:
        raw_name = match.group(1).upper()
        # NEWS가 뒤에 붙은 경우 한글로 변환 시도
        if "NEWS" in raw_name:
            return raw_name.replace("NEWS", "뉴스")
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

# 3. 화면 UI 레이아웃
st.markdown("""
    <style>
    .stTitle { color: #002c5f; font-weight: 800; margin-bottom: 20px; }
    .news-card { padding: 10px; border-bottom: 1px solid #eee; display: flex; align-items: center; gap: 15px; min-height: 55px; }
    .m-tag { 
        min-width: 100px; text-align: center; font-size: 0.75rem; 
        font-weight: 700; color: #002c5f; background: #f1f6fa; 
        padding: 5px 8px; border-radius: 4px; border: 1px solid #dce6f0;
    }
    .n-link { font-size: 1rem; font-weight: 500; color: #333; text-decoration: none; line-height: 1.4; }
    .n-link:hover { color: #002c5f; text-decoration: underline; }
    </style>
    """, unsafe_allow_html=True)

st.title("📢 현대 실시간 미디어 모니터링")
st.caption(f"최종 업데이트: {datetime.now().strftime('%H:%M:%S')} (네이버 뉴스 기반 한글 최적화)")

# 현대 관련 주요 키워드
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    with st.expander(f"🔍 {kw} 실시간 뉴스", expanded=True):
        items = get_naver_news(kw)
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
