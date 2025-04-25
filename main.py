# main.py
from dotenv import load_dotenv
import os
from tools.web_search import WebSearchTool
from tools.web_scraper import WebScraper
from tools.content_analyzer import ContentAnalyzer
from tools.news_aggregator import NewsAggregator

# Load environment variables from .env file
load_dotenv()

def test_web_search():
    search_tool = WebSearchTool(use_mock=False)  # Explicitly disable mock mode
    query = input("Enter a search query: ")
    results = search_tool.search(query, num_results=5)
    
    print(f"\nSearch results for: {query}")
    print("-" * 50)
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.title}")
        print(f"   URL: {result.url}")
        print(f"   Snippet: {result.snippet}")
        print(f"   Date: {result.date}")
        print("-" * 50)
    
    return results, query

def test_web_scraper(url):
    scraper = WebScraper(use_mock=False)  # Explicitly disable mock mode
    print(f"\nScraping content from: {url}")
    print("-" * 50)
    
    content = scraper.scrape_url(url)
    
    if content:
        print(f"Title: {content.title}")
        print(f"URL: {content.url}")
        print("\nMain Content (excerpt):")
        print(content.main_content[:200] + "..." if len(content.main_content) > 200 else content.main_content)
        
        print("\nMetadata:")
        for key, value in content.metadata.items():
            print(f"   {key}: {value}")
        
        if content.tables:
            print("\nTables:")
            for i, table in enumerate(content.tables):
                print(f"   Table {i+1}:")
                print(f"      Headers: {table['headers']}")
                print(f"      First row: {table['rows'][0] if table['rows'] else []}")
        
        if content.lists:
            print("\nLists:")
            for i, list_item in enumerate(content.lists):
                print(f"   List {i+1} ({list_item['type']}):")
                items = list_item['items'][:3] + (["..."] if len(list_item['items']) > 3 else [])
                print(f"      Items: {items}")
        
        if content.links:
            print("\nLinks:")
            for i, link in enumerate(content.links[:3]):
                print(f"   Link {i+1}: {link['text']} -> {link['url']}")
            if len(content.links) > 3:
                print(f"   ... and {len(content.links) - 3} more links")
    
    return content

def test_content_analyzer(content, query):
    analyzer = ContentAnalyzer(use_mock=False)  # Explicitly disable mock mode
    print("\nAnalyzing content relevance and extracting information...")
    print("-" * 50)
    
    relevance_score = analyzer.analyze_relevance(content, query)
    print(f"Relevance Score: {relevance_score:.2f}")
    
    key_info = analyzer.extract_key_information(content, query)
    print("\nKey Information:")
    print("   Key Points:")
    for i, point in enumerate(key_info["key_points"]):
        print(f"      {i+1}. {point}")
    
    print("\n   Relevant Terms:")
    print(f"      {', '.join(key_info['relevant_terms'])}")
    
    reliability = analyzer.assess_reliability(content, content.url)
    print("\nReliability Assessment:")
    print(f"   Score: {reliability['reliability_score']}")
    print(f"   Domain Reputation: {reliability['domain_reputation']}")
    print("   Factors:")
    for factor in reliability["factors"]:
        print(f"      - {factor}")
    
    summary = analyzer.summarize_content(content)
    print("\nContent Summary:")
    print(f"   {summary}")
    
    categories = analyzer.categorize_content(content)
    print("\nContent Categories:")
    print(f"   {', '.join(categories)}")
    
    return {
        "relevance": relevance_score,
        "key_information": key_info,
        "reliability": reliability,
        "summary": summary,
        "categories": categories
    }

def test_news_aggregation(query):
    aggregator = NewsAggregator(use_mock=False)  # Explicitly disable mock mode
    print("\nFetching news related to the query...")
    print("-" * 50)
    
    news_articles = aggregator.fetch_news(query, num_articles=3)
    if news_articles:
        print("Top News Articles:")
        for i, article in enumerate(news_articles, 1):
            print(f"{i}. {article.title}")
            print(f"   Source: {article.source}")
            print(f"   URL: {article.url}")
            print(f"   Published: {article.published_date}")
            print("-" * 50)

if __name__ == "__main__":
    # Test web search
    search_results, query = test_web_search()
    
    # Ask user to select a result to scrape and analyze
    if search_results:
        while True:
            try:
                selection = input("\nEnter the number of a result to scrape and analyze (or 'q' to quit): ")
                if selection.lower() == 'q':
                    break
                
                index = int(selection) - 1
                if 0 <= index < len(search_results):
                    selected_url = search_results[index].url
                    scraped_content = test_web_scraper(selected_url)
                    
                    if scraped_content:
                        analysis = test_content_analyzer(scraped_content, query)
                        test_news_aggregation(query)  # Add news aggregation
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number or 'q'.")
            except Exception as e:
                print(f"An error occurred: {e}")