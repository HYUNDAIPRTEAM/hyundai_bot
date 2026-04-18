import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import streamlit as st
import requests
import google.generativeai as genai
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 설정 (기존 키 유지) ---
NAVER_ID = "AN1H3gnsFZ5PDcFsULeS"
NAVER_SECRET = "zOSGFX7_G6"
GEMINI_API_KEY = "AQ.Ab8RN6JNm7dzH02Na_Fcilb3EJ79GE1aV1EultnZet6pwOdIxQ"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 페이지 설정 ---
st.set_page_config(page_title="현대그룹 핵심 모니터링", layout="wide")

# 30분 단위 자동 새로고침
count = st_autorefresh(interval=1800 * 1000, key="newscheck")
now_time = datetime.now().strftime('%H시 %M분 %S초')

st.title("🚀 현대그룹 실시간 뉴스 대시보드")
st.success(f"✅ **최근 업데이트 시각: {now_time}** (총 {count + 1}회 실행됨)")

# 사이드바 설정 (불필요한 '부고' 키워드 제거)
st.sidebar.header("모니터링 설정")
default_keywords = "현정은, 정지이, 현대엘리베이터, 현대무벡스, 현대아산"
keywords = st.sidebar.text_input("검색 키워드", default_keywords)
kw_list = [k.strip() for k in keywords.split(",")]

def get_formatted_date_and_check(raw_date):
    try:
        parse_date = datetime.strptime(raw_date, '%a, %d %b %Y %H:%M:%S +0900')
        now = datetime.now()
        is_recent = (now - parse_date) <= timedelta(hours=12)
        return parse_date.strftime('%Y-%m-%d %H:%M'), is_recent
    except:
        return raw_date, False

def analyze_ai(title):
    prompt = f"뉴스 제목: {title}\n현대그룹(현정은 회장 계열) 관점에서 '부정' 혹은 '정상' 중 하나만 출력."
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "분석불가"

# --- 메인 로직 ---
start_time_limit = (datetime.now() - timedelta(hours=12)).strftime('%m/%d %H:%M')
st.info(f"⏱️ **{start_time_limit} 이후 올라온 소식입니다.**")

obituary_list = []
normal_news_dict = {}

for kw in kw_list:
    if not kw: continue
    
    url = f"https://openapi.naver.com/v1/search/news.json?query={kw}&display=20&sort=date"
    headers = {"X-Naver-Client-Id": NAVER_ID, "X-Naver-Client-Secret": NAVER_SECRET}
    res = requests.get(url, headers=headers)
    
    if res.status_code == 200:
        items = res.json().get('items', [])
        for item in items:
            formatted_time, is_recent = get_formatted_date_and_check(item['pubDate'])
            if is_recent:
                title = item['title'].replace('<b>','').replace('</b>','').replace('&quot;','"')
                link = item['link']
                
                # 핵심 키워드 결과 중 '부고/별세' 단어가 있을 때만 상단 노출
                if "부고" in title or "별세" in title:
                    obituary_list.append({"title": title, "link": link, "time": formatted_time, "kw": kw})
                else:
                    if kw not in normal_news_dict:
                        normal_news_dict[kw] = []
                    normal_news_dict[kw].append({"title": title, "link": link, "time": formatted_time})

# 1. 우리 그룹 관련 부고 섹션 (있을 때만 표시)
if obituary_list:
    st.error("🕯️ **그룹 관련 부고/별세 소식 (감지됨)**")
    for obit in obituary_list:
        col1,