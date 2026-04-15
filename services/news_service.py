import feedparser
import html
from datetime import datetime

class NewsService:
    def __init__(self):
        self.rss_url = "https://news.google.com/rss/search?q=scholarship+announcements+india+education+news"
        self.fallback_news = [
            {
                "id": "1",
                "title": "National Merit Scholarship Application Open",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "summary": "The application window for the 2026 National Merit Scholarship is now open for students."
            },
            {
                "id": "2",
                "title": "New STEM Scholarship for Girls",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "summary": "A new scholarship program has been announced specifically for girls pursuing careers in STEM fields."
            }
        ]

    def get_latest_news(self):
        try:
            feed = feedparser.parse(self.rss_url)
            live_news = []
            
            for entry in feed.entries[:10]: # Get top 10 news items
                title = html.unescape(entry.title)
                # Clean title (remove source)
                clean_title = title.rsplit('-', 1)[0].strip()
                
                # Format date
                date_str = datetime.now().strftime("%Y-%m-%d")
                if hasattr(entry, 'published_parsed'):
                    date_dt = datetime(*entry.published_parsed[:6])
                    date_str = date_dt.strftime("%Y-%m-%d")

                live_news.append({
                    "id": entry.link,
                    "title": clean_title,
                    "date": date_str,
                    "summary": getattr(entry, 'summary', clean_title),
                    "link": entry.link,
                    "source": entry.source.title if hasattr(entry, 'source') else "Education News"
                })
            
            return live_news if live_news else self.fallback_news
            
        except Exception as e:
            print(f"Error fetching live news: {e}")
            return self.fallback_news
