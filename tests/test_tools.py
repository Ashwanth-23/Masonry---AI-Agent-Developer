# tests/test_tools.py

import unittest
from agent.research_agent import WebResearchAgent

class TestWebResearchAgent(unittest.TestCase):
    def setUp(self):
        self.agent = WebResearchAgent(use_mock=True, max_results=3)
    
    def test_research_factual_query(self):
        query = "latest price of lemon tree in BSC and NSC"
        report = self.agent.research(query)
        self.assertIn("query", report)
        self.assertIn("key_findings", report)
        self.assertGreater(len(report["sources"]), 0)
        self.assertTrue(report["summary"])
    
    def test_research_news_query(self):
        query = "recent news about lemon tree stock"
        report = self.agent.research(query, time_range="week")
        self.assertGreater(len(report["news"]), 0)
    
    def test_empty_results(self):
        # Simulate empty results by modifying WebSearchTool (not implemented here)
        query = "nonexistent topic 12345"
        report = self.agent.research(query)
        self.assertIn("error", report)
    
    def test_refine_search(self):
        query = "lemon tree price"
        additional_terms = ["BSC", "2025"]
        report = self.agent.refine_search(query, additional_terms)
        self.assertIn("key_findings", report)

if __name__ == "__main__":
    unittest.main()