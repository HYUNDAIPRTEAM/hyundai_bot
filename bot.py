import requests
import os
import feedparser
from urllib.parse import quote

# 1. 네이버 뉴스 가져오기 (10개)
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

# 2. 구글 뉴스 가져오기 (10개)
def get_google_news(query):
    try:
        encoded_query = quote(query)
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(url)
        return feed.entries[:10] 
    except:
        return []

# 3. 텔레그램 전송
def send_telegram(kw, naver_items, google_items):
    if not naver_items and not google_items: return
    
    message = f"📢 [{kw}] 통합 뉴스 브리핑\n\n"
    
    if naver_items:
        message += "🔹 네이버 주요 뉴스\n"
        for item in naver_items:
            title = item['title'].replace('<b>','').replace('</b>','').replace('&quot;', '"').replace('&amp;', '&')
            message += f"• {title}\n🔗 {item['link']}\n\n"
            
    if google_items:
        message += "🔹 구글 주요 뉴스\n"
        for item in google_items:
            message += f"• {item.title}\n🔗 {item.link}\n\n"
    
    # 메시지가 너무 길면 텔레그램에서 잘릴 수 있으니 4000자까지만 자름
    if len(message) > 4000:
        message = message[:4000] + "\n...(이하 생략)"

    url = f"https://api.telegram.org/bot{os.environ.get('TELEGRAM_TOKEN')}/sendMessage"
    requests.get(url, params={"chat_id": os.environ.get("CHAT_ID"), "text": message})

if __name__ == "__main__":
    # 팀장님이 요청하신 정교한 키워드
    keywords = ["현정은 회장", "현대엘리베이터", "현대무벡스"]
    for kw in keywords:
        n_news = get_naver_news(kw)
        g_news = get_google_news(kw)
        send_telegram(kw, n_news, g_news)
