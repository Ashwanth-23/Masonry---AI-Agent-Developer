from flask import Flask, request, render_template
from tools.web_search import WebSearchTool
from tools.web_scraper import WebScraper
from tools.content_analyzer import ContentAnalyzer
from tools.news_aggregator import NewsAggregator

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
        relevance = analyzer.analyze_relevance(content, query)
        key_info = analyzer.extract_key_information(content, query)
        reliability = analyzer.assess_reliability(content, url)
        summary = analyzer.summarize_content(content)
        categories = analyzer.categorize_content(content)
        news = aggregator.fetch_news(query, num_articles=3)

        return render_template(
            "result.html",
            content=content,
            relevance=relevance,
            key_info=key_info,
            reliability=reliability,
            summary=summary,
            categories=categories,
            news=news
        )
    return "Failed to scrape content."

if __name__ == "__main__":
    app.run(debug=True)