import requests
import os

# 깃허브 설정(Secrets)에서 정보 가져오기
NAVER_ID = os.environ.get("NAVER_ID")
NAVER_SECRET = os.environ.get("NAVER_SECRET")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def get_news(query):
    # 각 키워드당 최신 뉴스 3개씩 가져오기
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=3&sort=date"
    headers = {
        "X-Naver-Client-Id": NAVER_ID, 
        "X-Naver-Client-Secret": NAVER_SECRET
    }
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('items', [])
    except:
        return []

def send_telegram(kw, items):
    if not items:
        return
    
    # 여러 기사를 하나의 메시지로 깔끔하게 묶기
    message = f"📢 [{kw}] 실시간 뉴스 브리핑\n\n"
    for item in items:
        # 제목에서 HTML 태그 제거
        title = item['title'].replace('<b>','').replace('</b>','').replace('&quot;', '"').replace('&amp;', '&')
        message += f"• {title}\n🔗 {item['link']}\n\n"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    # 메시지 전송 (미리보기 포함)
    requests.get(url, params={"chat_id": CHAT_ID, "text": message})

# 팀장님이 관심 있으신 키워드 목록
keywords = ["현정은", "현대엘리베이터", "현대무벡스"]

# 실행!
if __name__ == "__main__":
    for kw in keywords:
        news_items = get_news(kw)
        send_telegram(kw, news_items)
