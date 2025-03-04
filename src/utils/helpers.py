"""
Helper utilities for the chatbot
"""

import re
import datetime
import json
import random


def format_timestamp(timestamp=None):
    """Format a timestamp for display"""
    if timestamp is None:
        timestamp = datetime.datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def clean_html(text):
    """Remove HTML tags from text"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def truncate_text(text, max_length=100):
    """Truncate text to maximum length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def get_random_greeting():
    """Get a random greeting message"""
    greetings = [
        "Hello! How can I assist with your industrial equipment today?",
        "Welcome! What equipment or process can I help you with?",
        "Hi there! I'm here to solve your industrial support needs.",
        "Greetings! How may I assist you with your equipment today?",
        "Hello! I'm your industrial support assistant. What can I help you with?"
    ]
    return random.choice(greetings)


def format_json_response(data):
    """Format JSON data for display"""
    return json.dumps(data, indent=2)


def extract_keywords(text, max_keywords=5):
    """Extract main keywords from text using simple frequency analysis"""
    from collections import Counter
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    # Tokenize and lowercase
    tokens = word_tokenize(text.lower())

    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalpha(
    ) and token not in stop_words and len(token) > 2]

    # Count frequencies
    word_counts = Counter(tokens)

    # Get most common words
    return [word for word, count in word_counts.most_common(max_keywords)]


def calculate_response_similarity(response1, response2):
    """Calculate similarity between two responses"""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    # Create vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform
    tfidf_matrix = vectorizer.fit_transform([response1, response2])

    # Calculate cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return similarity
