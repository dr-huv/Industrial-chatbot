import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RelevanceFilter:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def filter_documents(self, query, documents, threshold=0.3):
        """Filter documents based on relevance to the query"""
        if not documents:
            return []

        # Extract text from documents
        doc_texts = [doc['text'] for doc in documents]

        # Add the query to create the corpus
        corpus = [query] + doc_texts

        # Create TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(corpus)

        # Get the query vector (first row of the matrix)
        query_vector = tfidf_matrix[0]

        # Calculate similarities with other documents
        similarities = cosine_similarity(
            query_vector, tfidf_matrix[1:]).flatten()

        # Filter documents based on threshold
        filtered_docs = []
        for i, doc in enumerate(documents):
            if similarities[i] >= threshold:
                # Add similarity score to the document
                doc['tf_idf_similarity'] = float(similarities[i])
                filtered_docs.append(doc)

        # Sort by similarity score
        filtered_docs.sort(key=lambda x: x['tf_idf_similarity'], reverse=True)

        return filtered_docs

    def diversify_results(self, filtered_docs, diversity_factor=0.7):
        """Ensure diversity in the results by avoiding too similar documents"""
        if len(filtered_docs) <= 1:
            return filtered_docs

        # Extract texts
        texts = [doc['text'] for doc in filtered_docs]

        # Create TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(texts)

        # Calculate pairwise similarities
        pairwise_similarities = cosine_similarity(tfidf_matrix)

        # Select diverse documents
        selected_indices = [0]  # Always include the most relevant document
        for i in range(1, len(filtered_docs)):
            # Check if document is sufficiently different from already selected ones
            max_similarity = max(
                pairwise_similarities[i][j] for j in selected_indices)
            if max_similarity < diversity_factor:
                selected_indices.append(i)

        return [filtered_docs[i] for i in selected_indices]
