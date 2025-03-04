import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src.utils.config import get_config


class EnhancedRetriever:
    def __init__(self, knowledge_base=None):
        config = get_config()
        # Load the sentence transformer model
        model_name = config['nlp'].get(
            'sentence_transformer', 'all-MiniLM-L6-v2')
        self.model = SentenceTransformer(model_name)

        # Store knowledge base
        self.knowledge_base = knowledge_base
        self.encoded_chunks = None
        self.chunk_metadata = []

        # If knowledge base is provided, encode it immediately
        if knowledge_base:
            self.prepare_knowledge_base()

    def prepare_knowledge_base(self):
        """Process and encode the knowledge base for efficient retrieval"""
        chunks = []
        self.chunk_metadata = []

        # Process FAQs
        if 'faqs' in self.knowledge_base:
            for faq in self.knowledge_base['faqs']:
                # Create a chunk from the question and answer
                chunk_text = f"Question: {faq['question']} Answer: {faq['answer']}"
                chunks.append(chunk_text)
                self.chunk_metadata.append({
                    'type': 'faq',
                    'id': faq['id'],
                    'data': faq,
                    'source': f"FAQ #{faq['id']}"
                })

        # Process complaints
        if 'complaints' in self.knowledge_base:
            for complaint in self.knowledge_base['complaints']:
                # Create a chunk from the description and solution
                chunk_text = f"Problem: {complaint['description']} Solution: {complaint['solution']}"
                chunks.append(chunk_text)
                self.chunk_metadata.append({
                    'type': 'complaint',
                    'id': complaint['id'],
                    'data': complaint,
                    'source': f"Complaint #{complaint['id']}"
                })

        # Process products for additional context
        if 'products' in self.knowledge_base:
            for product in self.knowledge_base['products']:
                # Create a chunk from the product information
                chunk_text = f"Product: {product['name']} Description: {product['description']} Category: {product['category']}"
                chunks.append(chunk_text)
                self.chunk_metadata.append({
                    'type': 'product',
                    'id': product['id'],
                    'data': product,
                    'source': f"Product #{product['id']}"
                })

        # Encode all chunks
        if chunks:
            self.encoded_chunks = self.model.encode(chunks)

    def retrieve(self, query, top_k=5):
        """Retrieve the most relevant chunks for a query"""
        if self.encoded_chunks is None or len(self.encoded_chunks) == 0:
            return []

        # Encode the query
        query_embedding = self.model.encode(query)

        # Calculate similarities
        similarities = cosine_similarity(
            [query_embedding], self.encoded_chunks)[0]

        # Get indices of top-k most similar chunks
        top_indices = np.argsort(similarities)[::-1][:top_k]

        # Return the chunks and their metadata
        results = []
        for idx in top_indices:
            results.append({
                'text': self.get_chunk_text(idx),
                'metadata': self.chunk_metadata[idx],
                'similarity': float(similarities[idx])
            })

        return results

    def get_chunk_text(self, idx):
        """Reconstruct the chunk text based on its metadata"""
        metadata = self.chunk_metadata[idx]
        if metadata['type'] == 'faq':
            return f"Question: {metadata['data']['question']} Answer: {metadata['data']['answer']}"
        elif metadata['type'] == 'complaint':
            return f"Problem: {metadata['data']['description']} Solution: {metadata['data']['solution']}"
        elif metadata['type'] == 'product':
            return f"Product: {metadata['data']['name']} Description: {metadata['data']['description']}"
        return ""
