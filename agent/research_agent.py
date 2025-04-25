# agent/research_agent.py

from tools.web_search import WebSearchTool
from tools.web_scraper import WebScraper
from tools.content_analyzer import ContentAnalyzer
from tools.news_aggregator import NewsAggregator
from utils.helpers import QueryAnalyzer, generate_report
import logging
from typing import List, Dict, Any

class WebResearchAgent:
    """Web Research Agent for automated research and report generation."""
    
    def __init__(self, use_mock: bool = True, max_results: int = 5):
        """
        Initialize the agent with tools.
        
        Args:
            use_mock: Whether to use mock data for testing
            max_results: Maximum number of search results to process
        """
        self.web_search = WebSearchTool(use_mock=use_mock)
        self.scraper = WebScraper(use_mock=use_mock)
        self.analyzer = ContentAnalyzer(use_mock=use_mock)
        self.news_aggregator = NewsAggregator(use_mock=use_mock)
        self.query_analyzer = QueryAnalyzer()
        self.max_results = max_results
        self.logger = logging.getLogger(__name__)
    
    def research(self, query: str, time_range: str = None) -> Dict[str, Any]:
        """
        Perform research based on a user query and generate a report.
        
        Args:
            query: User research query
            time_range: Optional time range for news (e.g., "day", "week")
            
        Returns:
            Research report as a dictionary
        """
        try:
            # Step 1: Analyze query
            query_info = self.query_analyzer.analyze(query)
            self.logger.info(f"Query analysis: {query_info}")
            
            # Step 2: Perform web search
            search_results = self.web_search.search(
                query_info["search_query"],
                num_results=self.max_results,
                time_range=time_range
            )
            if not search_results:
                self.logger.warning("No search results found.")
                return {"error": "No results found for the query."}
            
            # Step 3: Scrape and analyze content
            scraped_contents = []
            analyses = []
            for result in search_results[:self.max_results]:
                content = self.scraper.scrape_url(result.url)
                if content:
                    analysis = self.analyzer.test_content_analyzer(content, query)
                    scraped_contents.append(content)
                    analyses.append({
                        "url": result.url,
                        "title": result.title,
                        "analysis": analysis
                    })
            
            # Step 4: Fetch news for time-sensitive queries
            news_articles = []
            if query_info["is_news_related"]:
                news_articles = self.news_aggregator.fetch_news(
                    query_info["search_query"],
                    time_range or "week",
                    max_results=3
                )
            
            # Step 5: Check for contradictions
            contradictions = self.analyzer.find_contradictions(scraped_contents)
            
            # Step 6: Synthesize report
            report = generate_report(
                query=query,
                analyses=analyses,
                news_articles=news_articles,
                contradictions=contradictions
            )
            
            self.logger.info("Research completed successfully.")
            return report
            
        except Exception as e:
            self.logger.error(f"Research failed: {e}")
            return {"error": str(e)}
    
    def refine_search(self, query: str, additional_terms: List[str]) -> Dict[str, Any]:
        """
        Refine the search with additional terms.
        
        Args:
            query: Original query
            additional_terms: Terms to refine the search
            
        Returns:
            Refined research report
        """
        refined_query = query + " " + " ".join(additional_terms)
        return self.research(refined_query)