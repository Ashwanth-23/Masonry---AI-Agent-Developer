# utils/helpers.py

import re
from typing import Dict, List, Any

class QueryAnalyzer:
    """Helper class for analyzing user queries."""
    
    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Analyze a query to determine intent and search strategy.
        
        Args:
            query: User query
            
        Returns:
            Dictionary with query analysis
        """
        query_lower = query.lower()
        
        # Determine intent
        is_news_related = any(term in query_lower for term in ["latest", "recent", "news", "update"])
        is_factual = any(term in query_lower for term in ["price", "data", "statistic", "fact"])
        is_exploratory = len(query.split()) > 5 or any(term in query_lower for term in ["about", "overview"])
        
        # Generate search terms
        search_query = query
        if is_factual:
            search_query = re.sub(r'\b(in|at|of)\b', '', query_lower).strip()
        
        return {
            "original_query": query,
            "search_query": search_query,
            "is_news_related": is_news_related,
            "is_factual": is_factual,
            "is_exploratory": is_exploratory
        }

def generate_report(query: str, analyses: List[Dict], news_articles: List[Any], contradictions: List[Dict]) -> Dict[str, Any]:
    """
    Generate a structured research report.
    
    Args:
        query: Original query
        analyses: List of content analyses
        news_articles: List of news articles
        contradictions: List of identified contradictions
        
    Returns:
        Structured report
    """
    report = {
        "query": query,
        "summary": "",
        "key_findings": [],
        "news": [article.to_dict() for article in news_articles],
        "contradictions": contradictions,
        "sources": []
    }
    
    # Sort analyses by relevance
    sorted_analyses = sorted(analyses, key=lambda x: x["analysis"]["relevance"], reverse=True)
    
    # Generate key findings
    for analysis in sorted_analyses[:3]:  # Top 3 sources
        report["key_findings"].extend(analysis["analysis"]["key_information"]["key_points"])
        report["sources"].append({
            "title": analysis["title"],
            "url": analysis["url"],
            "relevance": analysis["analysis"]["relevance"],
            "reliability": analysis["analysis"]["reliability"]["reliability_score"]
        })
    
    # Generate summary
    summaries = [analysis["analysis"]["summary"] for analysis in sorted_analyses[:2]]
    report["summary"] = " ".join(summaries)[:500] + "..." if len(" ".join(summaries)) > 500 else " ".join(summaries)
    
    return report