import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from src.utils.config import get_config


class FewShotLearner:
    def __init__(self, examples_file=None):
        config = get_config()
        model_name = config['nlp'].get(
            'sentence_transformer', 'all-MiniLM-L6-v2')
        self.model = SentenceTransformer(model_name)

        # Load examples if file is provided
        self.examples = []
        self.embeddings = None

        if examples_file and os.path.exists(examples_file):
            self.load_examples(examples_file)
        else:
            # Generate default examples from knowledge base
            self.generate_default_examples()

    def load_examples(self, file_path):
        """Load examples from a JSON file"""
        try:
            with open(file_path, 'r') as f:
                self.examples = json.load(f)

            # Encode examples
            self._encode_examples()
        except Exception as e:
            print(f"Error loading examples: {str(e)}")

    def generate_default_examples(self):
        """Generate default examples from the knowledge base"""
        # This would typically get examples from your database
        # For now, we'll use a few hardcoded examples
        self.examples = [
            {
                "query": "How do I reset my SmartBulb Pro?",
                "response": "To reset your SmartBulb Pro, turn it off and on 5 times in rapid succession. The bulb will flash to indicate a successful reset. Then, open the SmartHaven app and follow the instructions to reconnect it to your network.",
                "category": "reset",
                "product": "SmartBulb Pro"
            },
            {
                "query": "My SmartSense temperature readings are wrong",
                "response": "If your SmartSense is showing incorrect temperature readings, try these steps:\n1. Make sure it's placed away from direct heat sources like vents, sunlight, or appliances.\n2. In the SmartHaven app, go to Devices > SmartSense > Settings > Calibration to run the calibration wizard.\n3. Ensure your firmware is up to date by checking for updates in the app.",
                "category": "accuracy",
                "product": "SmartSense"
            },
            {
                "query": "Can I control SmartHaven devices when I'm not home?",
                "response": "Yes, you can control all your SmartHaven devices remotely from anywhere with an internet connection. As long as your SmartHaven Hub is connected to the internet, you can use the SmartHaven mobile app to monitor and control all connected devices. This works over both Wi-Fi and cellular connections.",
                "category": "remote access",
                "product": "Hub"
            }
        ]

        # Encode examples
        self._encode_examples()

    def _encode_examples(self):
        """Encode all examples for similarity matching"""
        if not self.examples:
            return

        texts = [ex["query"] for ex in self.examples]
        self.embeddings = self.model.encode(texts)

    def get_similar_examples(self, query, num_examples=2):
        """Get examples similar to the given query"""
        if not self.examples or self.embeddings is None:
            return []

        # Encode the query
        query_embedding = self.model.encode(query)

        # Calculate similarities
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]

        # Get indices of top examples
        top_indices = np.argsort(similarities)[::-1][:num_examples]

        # Return the top examples
        return [self.examples[i] for i in top_indices]

    def create_few_shot_prompt(self, query, examples=None):
        """Create a prompt with few-shot examples"""
        if examples is None:
            examples = self.get_similar_examples(query)

        if not examples:
            return f"Answer this industrial support question: {query}"

        prompt = "Answer these industrial support questions in a helpful, detailed manner:\n\n"

        # Add examples
        for example in examples:
            prompt += f"Question: {example['query']}\n"
            prompt += f"Answer: {example['response']}\n\n"

        # Add the actual query
        prompt += f"Question: {query}\n"
        prompt += "Answer:"

        return prompt
