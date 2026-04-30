import requests
import os
import feedparser
from urllib.parse import quote

# [추가] Streamlit 앱 깨우기 함수 (앱이 잠들지 않도록 툭 치고 오는 기능)
def wake_up_streamlit(url):
    try:
        requests.get(url, timeout=10)
        print(f"✅ Streamlit 앱 깨우기 성공: {url}")
    except Exception as e:
        print(f"❌ 앱 접속 실패: {e}")

# 1. 네이버 뉴스 가져오기
def get_naver_news(query):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=10&sort=date"
    headers = {
        "X-Naver-Client-Id": os.environ.get("NAVER_ID"),
        "X-Naver-Client-Secret": os.environ.get("NAVER_SECRET")
    }
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except:
        return []

# 2. 구글 뉴스 가져오기
def get_google_news(query):
    try:
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
        d = feedparser.parse(url)
        return d.entries[:5]
    except:
        return []

# 3. 텔레그램 메시지 보내기
def send_telegram(message):
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': False
    }
    try:
        requests.post(url, data=payload)
    except:
        pass

if __name__ == "__main__":
    # 뉴스 배달 전, 팀장님의 Streamlit 앱부터 깨웁니다.
    target_app_url = "https://hyundaibot-y3wa9pmbgyqkjivxitbmmt.streamlit.app/"
    wake_up_streamlit(target_app_url)
    
    # 뉴스 키워드 설정 (현대엘리베이터, 현대무벡스 등)
    keywords = ["현대엘리베이터", "현대무벡스", "현대그룹"]
    
    for kw in keywords:
        naver_news = get_naver_news(kw)
        google_news = get_google_news(kw)
        
        # 메시지 구성 및 발송 (생략된 기존 로직 그대로 작동)
        # ... (이하 생략)
        print(f"{kw} 브리핑 완료")
