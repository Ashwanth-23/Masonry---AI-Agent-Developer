# tools/news_aggregator.py
import os
from dotenv import load_dotenv
import requests
from typing import List, Optional

class NewsArticle:
    def __init__(self, title: str, source: str, url: str, published_date: str):
        self.title = title
        self.source = source
        self.url = url
        self.published_date = published_date

class NewsAggregator:
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        load_dotenv()
        self.api_key = os.environ.get("NEWSAPI_KEY")

    def _mock_fetch_news(self, query: str, num_articles: int) -> List[NewsArticle]:
        return [NewsArticle(f"Mock Article {i}", "Mock Source", f"http://mock{i}.com", "2025-04-24") for i in range(num_articles)]

    def fetch_news(self, query: str, num_articles: int) -> Optional[List[NewsArticle]]:
        if self.use_mock or not self.api_key:
            return self._mock_fetch_news(query, num_articles)
        
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={self.api_key}&language=en&pageSize={num_articles}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            return [NewsArticle(
                article.get("title", "No title"),
                article.get("source", {}).get("name", "Unknown"),
                article.get("url", ""),
                article.get("publishedAt", "No date")
            ) for article in articles[:num_articles]]
        except Exception as e:
            print(f"Error fetching news: {e}")
            return None