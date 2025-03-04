"""
Extract entities from user queries
"""

import re
import nltk
from nltk import ne_chunk, pos_tag
from nltk.tree import Tree
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)


class EntityExtractor:
    def __init__(self, knowledge_base=None):
        self.knowledge_base = knowledge_base

        # Common industrial product terms
        self.product_terms = [
            "machine", "device", "equipment", "system", "tool", "sensor",
            "controller", "motor", "pump", "valve", "compressor", "generator",
            "turbine", "engine", "robot", "conveyor", "boiler", "heater",
            "cooler", "filter", "tank", "vessel", "reactor"
        ]

        # Common issue types
        self.issue_types = [
            "error", "failure", "breakdown", "malfunction", "issue", "problem",
            "fault", "defect", "bug", "glitch", "outage", "shutdown",
            "overheating", "leakage", "noise", "vibration", "corrosion",
            "wear", "damage", "contamination"
        ]

        # If knowledge base is provided, extract product names
        if knowledge_base and 'products' in knowledge_base:
            self.product_names = [p['name'].lower()
                                  for p in knowledge_base['products']]
        else:
            self.product_names = []

    def extract_entities(self, query):
        """Extract entities from a query"""
        entities = {
            'products': [],
            'issues': [],
            'parts': [],
            'locations': []
        }

        # Tokenize and tag parts of speech
        tokens = word_tokenize(query)
        tagged = pos_tag(tokens)

        # Extract named entities using NLTK's ne_chunk
        named_entities = ne_chunk(tagged)

        # Process named entities
        for chunk in named_entities:
            if isinstance(chunk, Tree):
                if chunk.label() == 'PERSON':
                    continue  # Skip person names
                if chunk.label() == 'GPE':  # Geo-political entity (locations)
                    entity_name = ' '.join(c[0] for c in chunk.leaves())
                    entities['locations'].append(entity_name)
                # Add other entity types as needed

        # Extract product names and terms
        for product_name in self.product_names:
            if product_name.lower() in query.lower():
                entities['products'].append(product_name)

        for term in self.product_terms:
            if re.search(r'\b' + term + r'\b', query.lower()):
                entities['parts'].append(term)

        # Extract issue types
        for issue in self.issue_types:
            if re.search(r'\b' + issue + r'\b', query.lower()):
                entities['issues'].append(issue)

        return entities


# Create a singleton instance
entity_extractor = EntityExtractor()


def extract_entities_from_query(query, knowledge_base=None):
    """Extract entities from a user query"""
    global entity_extractor

    # Update knowledge base if provided
    if knowledge_base:
        entity_extractor = EntityExtractor(knowledge_base)

    return entity_extractor.extract_entities(query)
