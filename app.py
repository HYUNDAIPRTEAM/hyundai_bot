import streamlit as st
import requests
import base64
import os
from datetime import datetime
import re

# 1. 폰트 로드 및 CSS 생성 (오류 방지를 위해 로직 분리)
def get_font_style():
    font_b_path = "NeoHyundai_B.woff2"
    font_r_path = "NeoHyundai_R.woff2"
    
    style_content = ""
    
    # Bold 폰트 처리
    if os.path.exists(font_b_path):
        with open(font_b_path, "rb") as f:
            b64_b = base64.b64encode(f.read()).decode()
        style_content += f"""
        @font-face {{
            font-family: 'NeoHyundaiBold';
            src: url(data:font/woff2;base64,{b64_b}) format('woff2');
        }}
        """
    
    # Regular 폰트 처리
    if os.path.exists(font_r_path):
        with open(font_r_path, "rb") as f:
            b64_r = base64.b64encode(f.read()).decode()
        style_content += f"""
        @font-face {{
            font-family: 'NeoHyundaiReg';
            src: url(data:font/woff2;base64,{b64_r}) format('woff2');
        }}
        """
    
    # 전체 스타일 적용 (이미지처럼 텍스트가 튀어나오지 않게 정리)
    final_style = f"""
    <style>
    {style_content}
    
    /* 폰트 적용 */
    html, body, [class*="css"], .stMarkdown, p {{
        font-family: 'NeoHyundaiReg', sans-serif !important;
    }}
    .stTitle, h1, h2, h3, .m-tag, b, strong {{
        font-family: 'NeoHyundaiBold', sans-serif !important;
        color: #002c5f !important;
    }}
    
    /* 레이아웃 깨짐 방지 */
    .news-card {{
        padding: 12px;
        border-bottom: 1px solid #eee;
        display: flex;
        align-items: center;
        gap: 15px;
        min-height: 50px;
    }}
    .m-tag {{
        min-width: 90px;
        text-align: center;
        font-size: 0.72rem;
        background: #f1f6fa;
        padding: 4px 8px;
        border-radius: 4px;
        border: 1px solid #dce6f0;
    }}
    .n-link {{
        font-size: 1.05rem;
        font-weight: 500;
        color: #333;
        text-decoration: none;
        line-height: 1.4;
    }}
    </style>
    """
    return final_style

# 2. 메인 설정
st.set_page_config(page_title="현대 실시간 뉴스", page_icon="🗞️", layout="wide")

# 스타일 주입
st.markdown(get_font_style(), unsafe_allow_html=True)

# 3. 데이터 로직 (네이버 뉴스 매체명 매핑)
MEDIA_MAP = {{
    'busan.com': '부산일보', 'etoday': '이투데이', 'biz.chosun': '조선비즈',
    'bizwn': '비즈니스포스트', 'businesspost': '비즈니스포스트', 'hankookilbo': '한국일보',
    'hankyung': '한국경제', 'mk.co.kr': '매일경제', 'yna.co.kr': '연합뉴스',
    'sedaily': '서울경제', 'edaily': '이데일리', 'mt.co.kr': '머니투데이',
    'heraldcorp': '헤럴드경제', 'news1.kr': '뉴스1', 'newsis': '뉴시스',
    'pinpointnews': '핀포인트뉴스', 'topdaily': '톱데일리', 'insight': '인사이트'
}}

def get_kor_media(link):
    link = link.lower()
    for domain, kor_name in MEDIA_MAP.items():
        if domain in link: return kor_name
    match = re.search(r'https?://(?:www\.)?([^/.]+)', link)
    return match.group(1).upper() if match else "뉴스"

def clean_text(text):
    return re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6});', '', text).strip()

def get_naver_news(query):
    # 팀장님, secrets 설정 확인 부탁드립니다.
    url = f"https://openapi.naver.com/v1/search/news.json?query={{query}}&display=10&sort=date"
    headers = {{
        "X-Naver-Client-Id": st.secrets.get("NAVER_ID", ""),
        "X-Naver-Client-Secret": st.secrets.get("NAVER_SECRET", "")
    }}
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except: return []

# 4. 화면 구성
st.title("📢 현대 실시간 미디어 모니터링")
st.caption(f"최종 업데이트: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")

keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

for kw in keywords:
    with st.expander(f"🔍 {{kw}} 실시간 뉴스", expanded=True):
        items = get_naver_news(kw)
        if items:
            col1, col2 = st.columns(2)
            for i, item in enumerate(items):
                target_col = col1 if i < len(items)//2 else col2
                media_name = get_kor_media(item['originallink'])
                with target_col:
                    st.markdown(f'''
                    <div class="news-card">
                        <div class="m-tag">{{media_name}}</div>
                        <a href="{{item['link']}}" target="_blank" class="n-link">{{clean_text(item['title'])}}</a>
                    </div>
                    ''', unsafe_allow_html=True)
