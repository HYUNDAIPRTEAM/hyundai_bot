import streamlit as st
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime
import re
import base64
import os

# 1. 시스템 설정
st.set_page_config(page_title="HYUNDAI NEWS MONITORING", page_icon="🗞️", layout="wide")

# 🔹 폰트 로드 함수
def load_font(font_file):
    if os.path.exists(font_file):
        with open(font_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 🔹 폰트 데이터 로딩
font_bold = "NeoHyundai_B.woff2"
font_reg = "NeoHyundai_R.woff2"
data_b = load_font(font_bold)
data_r = load_font(font_reg)

# 🔹 CSS 적용
if data_b and data_r:
    st.markdown(f"""
    <style>
    @font-face {{ font-family: 'NeoHyundaiBold'; src: url(data:font/woff2;base64,{data_b}) format('woff2'); }}
    @font-face {{ font-family: 'NeoHyundaiReg'; src: url(data:font/woff2;base64,{data_r}) format('woff2'); }}
    * {{ font-family: 'NeoHyundaiReg', sans-serif !important; }}
    .custom-title {{ font-family: 'NeoHyundaiBold', sans-serif !important; font-size: 2.2rem; color: #002c5f; margin-bottom: 10px; }}
    .news-item {{ padding: 10px 0; border-bottom: 1px solid #f2f2f2; display: flex; align-items: center; gap: 15px; }}
    .media-tag {{ font-family: 'NeoHyundaiBold', sans-serif !important; font-size: 0.75rem; color: #002c5f; background-color: #f0f4f8; padding: 4px 12px; border-radius: 4px; min-width: 100px; text-align: center; border: 1px solid #dce6f0; }}
    .blog-tag {{ font-family: 'NeoHyundaiBold', sans-serif !important; font-size: 0.75rem; color: #2db400; background-color: #f0fff0; padding: 4px 12px; border-radius: 4px; min-width: 100px; text-align: center; border: 1px solid #2db400; }}
    .title-link {{ font-size: 1.05rem; color: #333; text-decoration: none; line-height: 1.4; }}
    .title-link:hover {{ color: #002c5f; text-decoration: underline; }}
    </style>
    """, unsafe_allow_html=True)

# 2. 유틸리티 함수
def clean_text(text):
    return re.sub(r'<.*?>|&[a-z0-9]+;', '', text).strip()

def get_kor_media_name(link):
    KOR_MEDIA_DICT = {'bizwn': '비즈니스포스트', 'hankookilbo': '한국일보', 'hankyung': '한국경제', 'mk.co.kr': '매일경제', 'yna.co.kr': '연합뉴스', 'chosun': '조선일보', 'donga': '동아일보', 'joins
