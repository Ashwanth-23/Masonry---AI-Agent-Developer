# tools/web_search.py

import requests
import os
import json
from typing import List, Dict, Optional, Union
import random

class SearchResult:
    """Class to represent a single search result."""
    
    def __init__(self, title: str, url: str, snippet: str, date: Optional[str] = None):
        self.title = title
        self.url = url
        self.snippet = snippet
        self.date = date
    
    def __repr__(self):
        return f"SearchResult(title='{self.title[:30]}...', url='{self.url}')"
    
    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "date": self.date
        }

class WebSearchTool:
    """
    Tool for performing web searches.
    This implementation supports both real API calls and mock responses for testing.
    """
    
    def __init__(self, api_key: Optional[str] = None, use_mock: bool = False):
        self.api_key = api_key or os.environ.get("SERPAPI_KEY")
        self.use_mock = use_mock or not self.api_key
        self.base_url = "https://serpapi.com/search"
        
        if not self.use_mock and not self.api_key:
            print("Warning: No SerpAPI key provided. Using mock search results instead.")
            self.use_mock = True
    
    def search(self, query: str, num_results: int = 10, time_range: Optional[str] = None, 
               language: str = "en") -> List[SearchResult]:
        """
        Perform a web search using the provided query.
        
        Args:
            query: The search query string
            num_results: Number of results to return
            time_range: Time range for results (e.g., "day", "week", "month")
            language: Language code for results
            
        Returns:
            List of SearchResult objects
        """
        if self.use_mock:
            return self._mock_search(query, num_results)
        
        # Real API implementation
        params = {
            "q": query,
            "api_key": self.api_key,
            "num": num_results,
            "hl": language
        }
        
        if time_range:
            if time_range == "day":
                params["tbs"] = "qdr:d"
            elif time_range == "week":
                params["tbs"] = "qdr:w"
            elif time_range == "month":
                params["tbs"] = "qdr:m"
            elif time_range == "year":
                params["tbs"] = "qdr:y"
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("organic_results", []):
                result = SearchResult(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    snippet=item.get("snippet", ""),
                    date=item.get("date", None)
                )
                results.append(result)
            
            return results
        
        except requests.RequestException as e:
            print(f"Search request failed: {e}")
            return []
    
    def _mock_search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """Generate mock search results for testing."""
        search_domain = query.lower().split()
        if len(search_domain) > 2:
            search_domain = search_domain[:2]
        domain = "".join(search_domain)
        
        results = []
        for i in range(min(num_results, 10)):
            title = f"Result {i+1} for {query}"
            url = f"https://example-{domain}.com/page{i+1}"
            snippet = f"This is a mock snippet for the search query '{query}'. It contains some sample text that might be relevant to the search terms."
            date = f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            
            results.append(SearchResult(title, url, snippet, date))
        
        return results
    
    def refine_search(self, original_query: str, additional_terms: List[str]) -> List[SearchResult]:
        """
        Refine an existing search with additional terms.
        
        Args:
            original_query: The original search query
            additional_terms: List of terms to add to the query
            
        Returns:
            List of SearchResult objects from the refined search
        """
        refined_query = original_query + " " + " ".join(additional_terms)
        return self.search(refined_query)