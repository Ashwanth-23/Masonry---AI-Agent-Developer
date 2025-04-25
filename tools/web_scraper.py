# tools/web_scraper.py

import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict

class ScrapedContent:
    """Class to hold scraped content from a webpage."""
    def __init__(self, title: str, url: str, main_content: str, metadata: Dict, tables: List[Dict], lists: List[Dict], links: List[Dict]):
        self.title = title
        self.url = url
        self.main_content = main_content
        self.metadata = metadata
        self.tables = tables
        self.lists = lists
        self.links = links

class WebScraper:
    """Tool for scraping content from web pages."""
    
    def __init__(self, use_mock: bool = True):
        """
        Initialize the WebScraper.
        
        Args:
            use_mock: Whether to use mock data for testing
        """
        self.use_mock = use_mock
    
    def _mock_scrape(self, url: str) -> ScrapedContent:
        """Generate mock scraped content for testing."""
        return ScrapedContent(
            title=f"Page about {url.split('/')[-1]}",
            url=url,
            main_content="This is the main content of the page at {}. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.".format(url),
            metadata={
                "author": "Alex Johnson",
                "publication_date": "2024-01-07",
                "description": f"This is a page about {url}."
            },
            tables=[{
                "headers": ["Column 1", "Column 2", "Column 3"],
                "rows": [["Value 1-1", "Value 1-2", "Value 1-3"]]
            }],
            lists=[{
                "type": "ul",
                "items": ["Item 1", "Item 2", "Item 3", "..."]
            }],
            links=[{
                "text": f"Related Link {i+1}",
                "url": f"{url}-related{i+1}.com"
            } for i in range(3)]
        )
    
    def _respect_robots_txt(self, url: str) -> bool:
        """Check robots.txt for permission to scrape (simplified)."""
        # Placeholder implementation; in production, use a robots.txt parser
        return True
    
    def scrape_url(self, url: str) -> Optional[ScrapedContent]:
        """
        Scrape content from a given URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            ScrapedContent object or None if scraping fails
        """
        if self.use_mock:
            return self._mock_scrape(url)
        
        if not self._respect_robots_txt(url):
            print(f"Scraping not allowed by robots.txt for {url}")
            return None
        
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract the title
            title = soup.find("title").text if soup.find("title") else "No title"
            
            # Initialize main content
            main_content = ""
            
            # Try multiple common selectors for article content
            content_selectors = [
                {"tag": "div", "attrs": {"class": ["article-body", "content-body", "story-body"]}},
                {"tag": "section", "attrs": {"class": ["article", "content", "main-content"]}},
                {"tag": "div", "attrs": {"class": "field--body"}},
                {"tag": "div", "attrs": {"id": "mw-content-text"}},
                {"tag": "article", "attrs": {}},  # Generic <article> tag
                {"tag": "div", "attrs": {"class": ["entry-content", "post-content"]}},
            ]

            content_div = None
            for selector in content_selectors:
                content_div = soup.find(selector["tag"], **selector.get("attrs", {}))
                if content_div:
                    break

            if content_div:
                # Extract paragraphs
                paragraphs = content_div.find_all("p")
                for p in paragraphs:
                    if p.text.strip():
                        main_content += p.text.strip() + "\n"
                
                # Try to extract rankings from a table, list, or div with ranked items
                ranking_list = content_div.find(["table", "ul", "ol", "div"])
                if ranking_list:
                    if ranking_list.name == "table":
                        main_content += "\nRanking Table:\n"
                        headers = [th.text.strip() for th in ranking_list.find_all("th")]
                        if headers:
                            main_content += f"Headers: {headers}\n"
                        for i, row in enumerate(ranking_list.find_all("tr")[1:6], 1):  # Top 5 rows
                            cols = row.find_all(["td", "th"])
                            if cols:
                                row_text = [col.text.strip() for col in cols]
                                main_content += f"Rank {i}: {', '.join(row_text)}\n"
                    elif ranking_list.name in ["ul", "ol"]:
                        main_content += "\nList of Rankings:\n"
                        for li in ranking_list.find_all("li")[:5]:
                            main_content += f"- {li.text.strip()}\n"
                    else:  # div, try to find ranked items (e.g., <div> with class 'rank-item')
                        rank_items = ranking_list.find_all("div", class_=["rank-item", "list-item"])[:5]
                        if rank_items:
                            main_content += "\nRanked Items:\n"
                            for i, item in enumerate(rank_items, 1):
                                main_content += f"Rank {i}: {item.text.strip()}\n"
            else:
                # Fallback: try to find a significant text block with keywords related to the query
                main_content_elements = soup.find_all(["p", "div", "article"], recursive=True)
                for element in main_content_elements:
                    text = element.text.strip()
                    if text and len(text) > 100 and any(keyword.lower() in text.lower() for keyword in ["university", "college", "ranking", "top"]):
                        main_content += text + "\n"
                        break
                else:
                    # Last resort: first significant block
                    for element in main_content_elements:
                        text = element.text.strip()
                        if text and len(text) > 100:
                            main_content += text + "\n"
                            break
            
            # Extract metadata (improved to capture more fields)
            metadata = {}
            for tag in soup.find_all("meta"):
                if tag.get("name") and tag.get("content"):
                    metadata[tag.get("name")] = tag.get("content")
                elif tag.get("property") and tag.get("content"):
                    metadata[tag.get("property")] = tag.get("content")
            
            # Extract tables (capture all rows for the first relevant table)
            tables = []
            for table in soup.find_all("table")[:1]:  # Limit to first table (main ranking table)
                headers = [th.text.strip() for th in table.find_all("th")]
                rows = []
                for row in table.find_all("tr")[1:6]:  # Extract top 5 rows (skip header row)
                    cols = row.find_all("td")
                    if cols:  # Ensure row has data
                        rows.append([col.text.strip() for col in cols])
                if headers and rows:  # Only include if table has headers and data
                    tables.append({"headers": headers, "rows": rows})
            
            # Extract lists (excluding navigation)
            lists = []
            for ul in soup.find_all(["ul", "ol"])[:3]:
                items = [li.text.strip() for li in ul.find_all("li")]
                # Exclude navigation lists and ensure relevance
                if items and "Main page" not in items and "Contents" not in items and "Jobs" not in items and "Employers" not in items:
                    lists.append({"type": ul.name, "items": items[:10]})
            
            # Extract links (limited to the first 5 relevant links)
            links = []
            for a in soup.find_all("a", href=True):
                link_text = a.text.strip()
                link_url = a.get("href")
                # Exclude navigation and irrelevant links
                if link_text and link_url and not link_url.startswith("#") and "signup" not in link_url and "login" not in link_url:
                    links.append({"text": link_text, "url": link_url})
                    if len(links) >= 5:
                        break
            
            return ScrapedContent(
                title=title,
                url=url,
                main_content=main_content,
                metadata=metadata,
                tables=tables,
                lists=lists,
                links=links
            )
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

if __name__ == "__main__":
    pass