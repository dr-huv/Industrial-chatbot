"""
Sentiment analysis for user queries
"""

import re
from textblob import TextBlob


class SentimentAnalyzer:
    def __init__(self):
        # Sentiment lexicons for industrial context
        self.positive_terms = [
            "working", "works", "fixed", "resolved", "solved", "good", "great",
            "excellent", "efficient", "effective", "reliable", "stable",
            "improved", "upgrade", "help", "thanks", "appreciate", "easy",
            "successful", "perfect", "optimal", "optimized"
        ]

        self.negative_terms = [
            "not", "broken", "error", "issue", "problem", "fault", "fail",
            "failed", "failure", "defect", "malfunction", "doesn't work",
            "isn't working", "bad", "poor", "terrible", "inefficient",
            "unstable", "unreliable", "difficulty", "complicated", "complex",
            "frustrated", "frustrating", "annoying", "disappointed"
        ]

        self.urgent_terms = [
            "urgent", "immediately", "emergency", "critical", "severe",
            "serious", "dangerous", "hazard", "risk", "asap", "quickly",
            "right away", "now", "life-threatening", "catastrophic"
        ]

    def analyze_sentiment(self, text):
        """
        Analyze sentiment of text
        Returns: 
            dict with sentiment scores and detected mood
        """
        # Use TextBlob for basic sentiment analysis
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Count positive and negative terms
        text_lower = text.lower()
        positive_count = sum(1 for term in self.positive_terms if re.search(
            r'\b' + re.escape(term) + r'\b', text_lower))
        negative_count = sum(1 for term in self.negative_terms if re.search(
            r'\b' + re.escape(term) + r'\b', text_lower))
        urgent_count = sum(1 for term in self.urgent_terms if re.search(
            r'\b' + re.escape(term) + r'\b', text_lower))

        # Adjust polarity based on domain-specific terms
        domain_polarity = (positive_count - negative_count) / \
            max(1, positive_count + negative_count)
        weighted_polarity = 0.7 * domain_polarity + 0.3 * polarity

        # Determine mood category
        if urgent_count > 0:
            mood = "urgent"
        elif weighted_polarity >= 0.2:
            mood = "positive"
        elif weighted_polarity <= -0.2:
            mood = "negative"
        else:
            mood = "neutral"

        return {
            'polarity': weighted_polarity,
            'subjectivity': subjectivity,
            'positive_terms': positive_count,
            'negative_terms': negative_count,
            'urgent_terms': urgent_count,
            'mood': mood
        }


# Create a singleton instance
sentiment_analyzer = SentimentAnalyzer()


def analyze_query_sentiment(query):
    """Analyze sentiment of a user query"""
    return sentiment_analyzer.analyze_sentiment(query)
