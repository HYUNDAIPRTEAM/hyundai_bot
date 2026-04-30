import requests
import os
import feedparser
from urllib.parse import quote

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
    except: return []

# 2. 구글 뉴스 가져오기
def get_google_news(query):
    try:
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
        return feedparser.parse(url).entries[:10]
    except: return []

# 3. 텔레그램으로 전송
def send_telegram(kw, n_news, g_news):
    if not n_news and not g_news: return
    
    msg = f"📢 [{kw}] 뉴스 브리핑\n\n"
    if n_news:
        msg += "🔹 네이버 뉴스\n"
        for i in n_news:
            t = i['title'].replace('<b>','').replace('</b>','').replace('&quot;', '"')
            msg += f"• {t}\n🔗 {i['link']}\n\n"
    if g_news:
        msg += "🔹 구글 뉴스\n"
        for i in g_news:
            msg += f"• {i.title}\n🔗 {i.link}\n\n"

    # 메시지가 너무 길면 잘라서 전송 (텔레그램 제한)
    url = f"https://api.telegram.org/bot{os.environ.get('TELEGRAM_TOKEN')}/sendMessage"
    requests.get(url, params={"chat_id": os.environ.get("CHAT_ID"), "text": msg[:4000]})

if __name__ == "__main__":
    # 팀장님 맞춤 키워드 리스트
    keywords = ["현정은 회장", "현대엘리베이터", "현대무벡스"] 
    for kw in keywords:
        send_telegram(kw, get_naver_news(kw), get_google_news(kw))
