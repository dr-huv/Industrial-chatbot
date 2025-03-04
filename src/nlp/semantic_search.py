from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SemanticSearch:
    def __init__(self):
        # Load a pre-trained sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def encode(self, texts):
        """Encode texts into embeddings"""
        return self.model.encode(texts)

    def search(self, query_embedding, corpus_embeddings, top_k=3):
        """Search for the most similar texts"""
        # Calculate cosine similarity
        similarities = cosine_similarity(
            [query_embedding], corpus_embeddings)[0]

        # Get indices of top-k most similar items
        top_indices = np.argsort(similarities)[::-1][:top_k]

        return [(idx, similarities[idx]) for idx in top_indices]


# Create a singleton instance
semantic_search = SemanticSearch()


def find_best_match(query, knowledge_base, top_k=3):
    """Find the best matching entries from the knowledge base"""
    # Prepare knowledge base items
    items = []
    item_texts = []

    # Prepare FAQs
    for idx, faq in enumerate(knowledge_base["faqs"]):
        items.append({"type": "faq", "id": faq["id"], "data": faq})
        item_texts.append(faq["question"])

    # Prepare Complaints
    for idx, complaint in enumerate(knowledge_base["complaints"]):
        items.append(
            {"type": "complaint", "id": complaint["id"], "data": complaint})
        item_texts.append(complaint["description"])

    # Encode query
    query_text = " ".join(query) if isinstance(query, list) else query
    query_embedding = semantic_search.model.encode(query_text)

    # Encode all items
    corpus_embeddings = semantic_search.model.encode(item_texts)

    # Search for most similar items
    results = semantic_search.search(query_embedding, corpus_embeddings, top_k)

    # Format results
    matches = []
    for idx, score in results:
        item = items[idx]
        matches.append({
            "type": item["type"],
            "id": item["id"],
            "data": item["data"],
            "similarity": float(score)
        })

    return matches
