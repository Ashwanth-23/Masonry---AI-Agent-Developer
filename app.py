from flask import Flask, request, render_template
import logging
from tools.web_search import WebSearchTool
from tools.web_scraper import WebScraper
from tools.content_analyzer import ContentAnalyzer
from tools.news_aggregator import NewsAggregator

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        search_tool = WebSearchTool(use_mock=False)
        results = search_tool.search(query, num_results=5)
        return render_template("index.html", results=results, query=query)
    return render_template("index.html", results=None, query="")

@app.route("/scrape")
def scrape():
    url = request.args.get("url")
    query = request.args.get("query")
    scraper = WebScraper(use_mock=False)
    analyzer = ContentAnalyzer(use_mock=False)
    aggregator = NewsAggregator(use_mock=False)

    content = scraper.scrape_url(url)
    if content:
        try:
            # Normalize content to ensure it's a dictionary with string attributes
            if hasattr(content, 'main_content') and callable(getattr(content, 'main_content')):
                normalized_content = {"main_content": content.main_content(), "title": getattr(content, 'title', '')(), "url": url}
            else:
                normalized_content = {
                    "main_content": getattr(content, 'main_content', '') if hasattr(content, 'main_content') else str(content),
                    "title": getattr(content, 'title', '') if hasattr(content, 'title') else '',
                    "url": url
                }

            relevance = analyzer.analyze_relevance(normalized_content, query)
            key_info = analyzer.extract_key_information(normalized_content, query)
            # Ensure key_info is a dict with lists
            key_info = {
                "key_points": key_info.get("key_points", []),
                "relevant_terms": key_info.get("relevant_terms", []),
                "mentions": key_info.get("mentions", {}),
                "topic_relevance": key_info.get("topic_relevance", 0.0)
            }
            reliability = analyzer.assess_reliability(normalized_content, url)
            # Ensure reliability is a dict with values
            reliability = {
                "reliability_score": reliability.get("reliability_score", 0.0),
                "factors": reliability.get("factors", []),
                "domain_reputation": reliability.get("domain_reputation", "Unknown")
            }
            summary = analyzer.summarize_content(normalized_content)
            categories = analyzer.categorize_content(normalized_content)
            news = aggregator.fetch_news(query, num_articles=3)

            # Log data for debugging
            logger.debug(f"Normalized Content: {normalized_content}")
            logger.debug(f"Key Info: {key_info}")
            logger.debug(f"Reliability: {reliability}")
            logger.debug(f"Summary: {summary}")
            logger.debug(f"Categories: {categories}")
            logger.debug(f"News: {news}")

            template_data = {
                "content": normalized_content,
                "relevance": relevance,
                "key_info": key_info,
                "reliability": reliability,
                "summary": summary,
                "categories": categories,
                "news": news
            }

            return render_template("result.html", **template_data)
        except Exception as e:
            logger.error(f"Error in scrape route: {str(e)}", exc_info=True)
            return f"Error processing content: {str(e)}"
    return "Failed to scrape content."

if __name__ == "__main__":
    app.run(debug=True)