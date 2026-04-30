import streamlit as st
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime
import re

# 1. 시스템 설정
st.set_page_config(page_title="현대 뉴스 브리핑", page_icon="🗞️", layout="wide")

# 매체명 한글 변환 사전 (더 촘촘하게 보강)
MEDIA_MAP = {
    'yna': '연합뉴스', 'hankyung': '한국경제', 'mk': '매일경제', 'chosun': '조선일보',
    'donga': '동아일보', 'joins': '중앙일보', 'hani': '한겨레', 'khan': '경향신문',
    'sedaily': '서울경제', 'edaily': '이데일리', 'mt': '머니투데이', 'heraldcorp': '헤럴드경제',
    'bizwatch': '비즈워치', 'newsis': '뉴시스', 'news1': '뉴스1', 'sbs': 'SBS',
    'kbs': 'KBS', 'mbc': 'MBC', 'ytn': 'YTN', 'digitaltimes': '디지털타임스',
    'etnews': '전자신문', 'segye': '세계일보', 'seoul': '서울신문', 'munhwa': '문화일보',
    'fnnews': '파이낸셜뉴스', 'ajunews': '아주경제', 'kmib': '국민일보', 'busan': '부산일보',
    'kyeonggi': '경기일보', 'dailyian': '데일리에안', 'vop': '민중의소리', 'moneyis': '머니S'
}

def clean_text(text):
    if not text: return ""
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(clean, '', text).strip()

def get_first_sentence(text):
    text = clean_text(text)
    if not text: return ""
    sentence = text.split('.')[0]
    return sentence + "." if len(sentence) > 5 else ""

# 2. 뉴스 수집 로직
def get_naver_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=5&sort=date"
    headers = {
        "X-Naver-Client-Id": st.secrets.get("NAVER_ID", ""),
        "X-Naver-Client-Secret": st.secrets.get("NAVER_SECRET", "")
    }
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except: return []

def get_google_news(query):
    try:
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
        d = feedparser.parse(url)
        return d.entries[:5]
    except: return []

# 3. 디자인 스타일링
st.markdown("""
    <style>
    .stTitle { color: #002c5f; font-weight: 800; }
    .news-item { padding: 12px 0; border-bottom: 1px solid #f0f0f0; }
    .header-line { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
    .media-tag { 
        font-size: 0.75rem; color: #ffffff; background-color: #002c5f; 
        padding: 3px 10px; border-radius: 4px; font-weight: 600; white-space: nowrap;
    }
    .title-link { font-size: 1.05rem; font-weight: 700; color: #111; text-decoration: none; line-height: 1.4; }
    .first-sentence { font-size: 0.92rem; color: #555; line-height: 1.6; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📢 현대 뉴스 실시간 브리핑")
st.write(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 4. 모니터링 키워드 (현정은, 현대엘리베이터, 현대무벡스)
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    st.subheader(f"🔍 {kw} 동향")
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("🔹 네이버 뉴스")
        items = get_naver_news(kw)
        for item in items:
            raw_title = clean_text(item['title'])
            # 링크 주소에서 매체 식별 코드 추출
            media_match = re.search(r'https?://(?:www\.)?([^/]+)', item['originallink'])
            eng_id = media_match.group(1).split('.')[0] if media_match else ""
            
            # 매핑 사전에 있으면 한글로, 없으면 대문자로 표시
            media_display = MEDIA_MAP.get(eng_id, eng_id.upper() if eng_id else "뉴스")
            
            first_s = get_first_sentence(item['description'])
            st.markdown(f'''
            <div class="news-item">
                <div class="header-line">
                    <span class="media-tag">{media_display}</span>
                    <a href="{item["link"]}" target="_blank" class="title-link">{raw_title}</a>
                </div>
                <div class="first-sentence">{first_s}</div>
            </div>
            ''', unsafe_allow_html=True)

    with col2:
        st.caption("🔹 구글 뉴스")
        entries = get_google_news(kw)
        for entry in entries:
            raw_t = clean_text(entry.title)
            title_part, media_part = raw_t.rsplit(" - ", 1) if " - " in raw_t else (raw_t, "구글")
            first_s = get_first_sentence(entry.summary if 'summary' in entry else "")
            display_s = first_s if len(first_s) > 10 and title_part[:10] not in first_s else ""
            
            st.markdown(f'''
            <div class="news-item">
                <div class="header-line">
                    <span class="media-tag">{media_part}</span>
                    <a href="{entry.link}" target="_blank" class="title-link">{title_part}</a>
                </div>
                <div class="first-sentence">{display_s}</div>
            </div>
            ''', unsafe_allow_html=True)
    st.divider()

# 5. 사이드바
st.sidebar.info("사용자: 현대그룹 커뮤니케이션실")
if st.sidebar.button("지금 새로고침"): st.rerun()
st.sidebar.caption("네이버/구글 실시간 뉴스 모니터링 v2.3")
