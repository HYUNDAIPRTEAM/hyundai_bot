import streamlit as st
import requests
import base64
import os
from datetime import datetime
import re

# 1. 폰트 로드 및 CSS 생성 함수 (f-string 중복 중괄호 오류 제거)
def get_style():
    font_b_path = "NeoHyundai_B.woff2"
    font_r_path = "NeoHyundai_R.woff2"
    
    font_face_css = ""
    
    # Bold 폰트 파일 체크 및 로드
    if os.path.exists(font_b_path):
        with open(font_b_path, "rb") as f:
            b64_b = base64.b64encode(f.read()).decode()
        font_face_css += f"""
        @font-face {{
            font-family: 'NeoHyundaiBold';
            src: url(data:font/woff2;base64,{b64_b}) format('woff2');
        }}"""
    
    # Regular 폰트 파일 체크 및 로드
    if os.path.exists(font_r_path):
        with open(font_r_path, "rb") as f:
            b64_r = base64.b64encode(f.read()).decode()
        font_face_css += f"""
        @font-face {{
            font-family: 'NeoHyundaiReg';
            src: url(data:font/woff2;base64,{b64_r}) format('woff2');
        }}"""
    
    # 최종 스타일 시트 (image_0e8d79.png의 코드 노출 방지)
    return f"""
    <style>
    {font_face_css}
    
    html, body, [class*="css"], .stMarkdown, p {{
        font-family: 'NeoHyundaiReg', sans-serif !important;
    }}
    .stTitle, h1, h2, h3, .m-tag, b, strong {{
        font-family: 'NeoHyundaiBold', sans-serif !important;
        color: #002c5f !important;
    }}
    .news-card {{
        padding: 12px;
        border-bottom: 1px solid #eee;
        display: flex;
        align-items: center;
        gap: 15px;
        min-height: 55px;
    }}
    .m-tag {{
        min-width: 95px;
        text-align: center;
        font-size: 0.75rem;
        background: #f1f6fa;
        padding: 5px 8px;
        border-radius: 4px;
        border: 1px solid #dce6f0;
        color: #002c5f;
        font-weight: bold;
    }}
    .n-link {{
        font-size: 1rem;
        font-weight: 500;
        color: #333;
        text-decoration: none;
        line-height: 1.4;
    }}
    .n-link:hover {{ color: #002c5f; text-decoration: underline; }}
    </style>
    """

# 2. 메인 설정 및 스타일 주입
st.set_page_config(page_title="현대 실시간 뉴스", page_icon="🗞️", layout="wide")
st.markdown(get_style(), unsafe_allow_html=True)

# 3. 매체명 매핑 (TypeError 발생 구문 수정)
MEDIA_MAP = {
    'busan.com': '부산일보', 'etoday': '이투데이', 'biz.chosun': '조선비즈',
    'bizwn': '비즈니스포스트', 'businesspost': '비즈니스포스트', 'hankookilbo': '한국일보',
    'hankyung': '한국경제', 'mk.co.kr': '매일경제', 'yna.co.kr': '연합뉴스',
    'sedaily': '서울경제', 'edaily': '이데일리', 'mt.co.kr': '머니투데이',
    'heraldcorp': '헤럴드경제', 'news1.kr': '뉴스1', 'newsis': '뉴시스',
    'pinpointnews': '핀포인트뉴스', 'topdaily': '톱데일리', 'insight': '인사이트',
    'labortoday': '매일노동뉴스', 'ccdaily': '충청일보', 'ccdn': '충청매일'
}

def get_kor_media(link):
    link = link.lower()
    for domain, kor_name in MEDIA_MAP.items():
        if domain in link: return kor_name
    match = re.search(r'https?://(?:www\.)?([^/.]+)', link)
    if match:
        name = match.group(1).upper()
        return name.replace("NEWS", "뉴스") if "NEWS" in name else name
    return "뉴스"

def clean_text(text):
    return re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6});', '', text).strip()

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

# 4. 화면 UI 출력
st.title("📢 현대 실시간 미디어 모니터링")
st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

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
