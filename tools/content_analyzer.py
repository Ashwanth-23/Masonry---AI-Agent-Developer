# tools/content_analyzer.py

from typing import Dict, List, Any, Optional, Tuple
import re
import random
from collections import Counter
import json

class ContentAnalyzer:
    """Tool for analyzing and extracting relevant information from scraped content."""
    
    def __init__(self, ai_model=None, use_mock: bool = False):
        """
        Initialize the ContentAnalyzer.
        
        Args:
            ai_model: Optional AI model for advanced analysis (e.g., OpenAI, Claude)
            use_mock: Whether to use mock responses for testing
        """
        self.ai_model = ai_model
        self.use_mock = use_mock or not ai_model
        
        if not self.use_mock and not ai_model:
            print("Warning: No AI model provided. Using mock analysis instead.")
            self.use_mock = True
    
    def analyze_relevance(self, content: Dict[str, Any], query: str) -> float:
        """
        Analyze how relevant the content is to the query.
        
        Args:
            content: Scraped content (can be dict or ScrapedContent object)
            query: Original search query
            
        Returns:
            Relevance score between 0.0 and 1.0
        """
        if self.use_mock:
            return self._mock_relevance_score(content, query)
        
        # Implement real AI-based relevance scoring here
        # This would typically involve sending the content and query to an AI model
        # and getting back a relevance assessment
        pass
    
    def extract_key_information(self, content: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Extract key information from content relevant to the query.
        
        Args:
            content: Scraped content (can be dict or ScrapedContent object)
            query: Original search query
            
        Returns:
            Dictionary of extracted information
        """
        if self.use_mock:
            return self._mock_extract_information(content, query)
        
        # Implement real AI-based information extraction here
        pass
    
    def assess_reliability(self, content: Dict[str, Any], source_url: str) -> Dict[str, Any]:
        """
        Assess the reliability of the content and its source.
        
        Args:
            content: Scraped content (can be dict or ScrapedContent object)
            source_url: URL of the content source
            
        Returns:
            Dictionary with reliability score and factors
        """
        if self.use_mock:
            return self._mock_reliability_assessment(content, source_url)
        
        # Implement real AI-based reliability assessment here
        pass
    
    def find_contradictions(self, contents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identify contradictions across multiple content sources.
        
        Args:
            contents: List of scraped content from different sources
            
        Returns:
            List of identified contradictions
        """
        if self.use_mock:
            return self._mock_find_contradictions(contents)
        
        # Implement real contradiction detection here
        pass
    
    def summarize_content(self, content: Dict[str, Any], max_length: int = 200) -> str:
        """
        Generate a concise summary of the content.
        
        Args:
            content: Scraped content to summarize
            max_length: Maximum length of summary in characters
            
        Returns:
            Summary string
        """
        if self.use_mock:
            return self._mock_summarize(content, max_length)
        
        # Implement real AI-based summarization here
        pass
    
    def categorize_content(self, content: Dict[str, Any]) -> List[str]:
        """
        Categorize the content into topics or themes.
        
        Args:
            content: Scraped content to categorize
            
        Returns:
            List of categories/topics
        """
        if self.use_mock:
            return self._mock_categorize(content)
        
        # Implement real AI-based categorization here
        pass
    
    def _get_content_text(self, content) -> str:
        """Extract the main text from content object or dict."""
        if hasattr(content, 'main_content'):
            return content.main_content
        
        if isinstance(content, dict):
            return content.get('main_content', '')
        
        return str(content)
    
    def _get_content_title(self, content) -> str:
        """Extract the title from content object or dict."""
        if hasattr(content, 'title'):
            return content.title
        
        if isinstance(content, dict):
            return content.get('title', '')
        
        return ''
    
    def _mock_relevance_score(self, content: Any, query: str) -> float:
        """Generate a mock relevance score based on simple text matching."""
        content_text = self._get_content_text(content)
        content_title = self._get_content_title(content)
        
        # Count query terms in content
        query_terms = query.lower().split()
        content_lower = content_text.lower() + " " + content_title.lower()
        
        # Count occurrences of query terms
        term_counts = 0
        for term in query_terms:
            term_counts += content_lower.count(term)
        
        # Calculate a score based on term frequency
        score = min(1.0, 0.5 + (term_counts / (len(query_terms) * 2)))
        
        # Add some randomness for testing
        score = min(1.0, max(0.0, score + random.uniform(-0.1, 0.1)))
        
        return score
    
    def _mock_extract_information(self, content: Any, query: str) -> Dict[str, Any]:
        """Generate mock extracted information based on content and query."""
        content_text = self._get_content_text(content)
        content_title = self._get_content_title(content)
        
        # Extract sentences that might contain relevant information
        sentences = re.split(r'[.!?]+', content_text)
        query_terms = query.lower().split()
        
        # Find sentences containing query terms
        relevant_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and any(term in sentence.lower() for term in query_terms):
                relevant_sentences.append(sentence)
        
        # For mock purposes, create key points
        key_points = []
        if relevant_sentences:
            key_points = relevant_sentences[:3]  # Use top 3 sentences
        else:
            # Generate mock key points
            query_topic = " ".join(query_terms[:2])
            key_points = [
                f"Information about {query_topic} is discussed on this page.",
                f"The page contains relevant details related to {query_topic}.",
                f"Several aspects of {query_topic} are covered in this content."
            ]
        
        # Create a structured response
        extracted_info = {
            "key_points": key_points,
            "relevant_terms": self._extract_relevant_terms(content_text, query),
            "mentions": self._extract_entity_mentions(content_text),
            "topic_relevance": self._mock_relevance_score(content, query)
        }
        
        return extracted_info
    
    def _extract_relevant_terms(self, text: str, query: str) -> List[str]:
        """Extract terms from text that seem relevant to the query."""
        # This is a simplified version - real implementation would use NLP techniques
        words = re.findall(r'\b\w+\b', text.lower())
        query_terms = query.lower().split()
        
        # Count word frequencies
        word_freq = Counter(words)
        
        # Remove common stopwords, short words, and query terms themselves
        stopwords = {'the', 'and', 'is', 'in', 'to', 'of', 'a', 'for', 'with', 'on', 'by', 'that', 'this', 'are', 'or'}
        relevant_terms = [(word, freq) for word, freq in word_freq.most_common(20) 
                         if word not in stopwords and word not in query_terms and len(word) > 3]
        
        # Return just the words without frequencies
        return [word for word, _ in relevant_terms[:10]]
    
    def _extract_entity_mentions(self, text: str) -> Dict[str, List[str]]:
        """Extract potential named entities from text."""
        # This is a very simplified mock version - real implementation would use NER
        
        # Look for patterns that might indicate different entity types
        # People: capitalized words followed by capitalized words
        people = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text)
        
        # Organizations: sequences of capitalized words
        orgs = re.findall(r'\b([A-Z][a-z]+ ){1,3}(Corporation|Inc|Ltd|LLC|Company)\b', text)
        
        # Dates: simple date patterns
        dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b', text)
        
        return {
            "people": list(set(people))[:5],  # Limit to 5 unique names
            "organizations": [" ".join(org) for org in orgs][:5],
            "dates": list(set(dates))[:5]
        }
    
    def _mock_reliability_assessment(self, content: Any, source_url: str) -> Dict[str, Any]:
        """Generate a mock reliability assessment of the content and source."""
        # For mock purposes, generate a random but reasonable reliability score
        # In reality, this would consider factors like domain reputation, content quality, etc.
        
        # Domain-based factors (would be based on real reputation databases)
        domain = source_url.split('//')[1].split('/')[0] if '//' in source_url else source_url.split('/')[0]
        
        # Generate a base score from domain
        base_score = random.uniform(0.6, 0.9)  # Most content is reasonably reliable
        
        # For test domains, adjust randomly
        if 'example' in domain:
            base_score = random.uniform(0.7, 0.95)
        elif any(term in domain for term in ['news', 'gov', 'edu']):
            base_score = random.uniform(0.75, 0.98)
        elif any(term in domain for term in ['blog', 'forum']):
            base_score = random.uniform(0.5, 0.8)
        
        # Generate factors that contributed to the score
        factors = []
        if base_score > 0.8:
            factors.append("Reputable domain")
            factors.append("Well-structured content")
        elif base_score > 0.6:
            factors.append("Moderately reliable source")
            factors.append("Some verifiable information")
        else:
            factors.append("Less established domain")
            factors.append("Limited verifiability")
        
        # Add a random factor
        potential_factors = [
            "Contains citations",
            "No citations found",
            "Recent publication date",
            "Older content",
            "Author credentials provided",
            "No author information",
            "Balanced perspective",
            "Potential bias detected"
        ]
        factors.append(random.choice(potential_factors))
        
        return {
            "reliability_score": round(base_score, 2),
            "factors": factors,
            "domain_reputation": "High" if base_score > 0.8 else "Medium" if base_score > 0.6 else "Low"
        }
    
    def _mock_find_contradictions(self, contents: List[Any]) -> List[Dict[str, Any]]:
        """Generate mock contradictions between multiple content sources."""
        # For mock purposes, sometimes generate contradictions
        if random.random() < 0.7 or len(contents) < 2:  # 70% chance of no contradictions, or not enough content
            return []
        
        # Generate 1-2 mock contradictions
        contradictions = []
        
        # Topics that could have contradictions
        potential_topics = ["date", "number", "statistic", "person involved", "sequence of events", "cause", "effect"]
        
        for _ in range(random.randint(1, 2)):
            topic = random.choice(potential_topics)
            contradiction = {
                "topic": topic,
                "contradiction": f"Sources disagree about {topic}",
                "sources": [
                    {
                        "url": getattr(contents[0], 'url', "unknown source 1") if len(contents) > 0 else "unknown source 1",
                        "claim": f"First claim about {topic}"
                    },
                    {
                        "url": getattr(contents[1], 'url', "unknown source 2") if len(contents) > 1 else "unknown source 2",
                        "claim": f"Contradictory claim about {topic}"
                    }
                ]
            }
            contradictions.append(contradiction)
        
        return contradictions
    
    def _mock_summarize(self, content: Any, max_length: int = 200) -> str:
        """Generate a mock summary of the content."""
        content_text = self._get_content_text(content)
        title = self._get_content_title(content)
        
        # For mock purposes, just take the first few sentences
        sentences = re.split(r'[.!?]+', content_text)
        summary_sentences = []
        current_length = 0
        
        # Start with title if available
        if title:
            summary_sentences.append(title + ".")
            current_length += len(title) + 1
        
        # Add sentences until we reach max_length
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence_length = len(sentence) + 1  # +1 for the period
            if current_length + sentence_length <= max_length:
                summary_sentences.append(sentence + ".")
                current_length += sentence_length
            else:
                break
        
        # If we have no sentences yet (e.g., title was too long), take first sentence and truncate
        if not summary_sentences and sentences:
            first_sent = sentences[0].strip()
            if first_sent:
                summary_sentences.append((first_sent[:max_length-3] + "..."))
        
        return " ".join(summary_sentences)
    
    def _mock_categorize(self, content: Any) -> List[str]:
        """Generate mock categories/topics for the content."""
        content_text = self._get_content_text(content)
        title = self._get_content_title(content)
        
        # Combine title and text for analysis
        full_text = title + " " + content_text
        
        # List of potential categories
        categories = [
            "Technology", "Business", "Finance", "Science", "Health", "Politics", 
            "Education", "Entertainment", "Sports", "Travel", "Food", "Art", 
            "Environment", "History", "Literature", "Social Media", "News"
        ]
        
        # For mock purposes, select 2-3 categories somewhat deterministically based on content
        selected = []
        
        # Simple keyword matching (in real implementation, this would use NLP classification)
        keyword_to_category = {
            "tech": "Technology", "software": "Technology", "app": "Technology", "computer": "Technology",
            "business": "Business", "company": "Business", "market": "Business", "industry": "Business",
            "money": "Finance", "invest": "Finance", "bank": "Finance", "stock": "Finance",
            "research": "Science", "scientist": "Science", "study": "Science", "experiment": "Science",
            "health": "Health", "medical": "Health", "doctor": "Health", "patient": "Health",
            "government": "Politics", "election": "Politics", "policy": "Politics", "president": "Politics",
            "school": "Education", "learn": "Education", "student": "Education", "teacher": "Education",
            "movie": "Entertainment", "music": "Entertainment", "celebrity": "Entertainment", "game": "Entertainment",
            "team": "Sports", "player": "Sports", "match": "Sports", "tournament": "Sports",
            "trip": "Travel", "destination": "Travel", "hotel": "Travel", "vacation": "Travel",
            "recipe": "Food", "restaurant": "Food", "cook": "Food", "ingredient": "Food",
            "painting": "Art", "museum": "Art", "artist": "Art", "gallery": "Art",
            "climate": "Environment", "pollution": "Environment", "sustainable": "Environment", "nature": "Environment",
            "historical": "History", "century": "History", "ancient": "History", "heritage": "History",
            "book": "Literature", "author": "Literature", "novel": "Literature", "poem": "Literature",
            "social": "Social Media", "platform": "Social Media", "online": "Social Media", "profile": "Social Media",
            "report": "News", "headline": "News", "journalist": "News", "media": "News"
        }
        
        # Check for keywords in the text
        text_lower = full_text.lower()
        for keyword, category in keyword_to_category.items():
            if keyword in text_lower and category not in selected:
                selected.append(category)
                if len(selected) >= 3:  # Limit to 3 categories
                    break
        
        # If we found fewer than 2 categories, add some random ones
        while len(selected) < 2:
            category = random.choice(categories)
            if category not in selected:
                selected.append(category)
        
        return selected