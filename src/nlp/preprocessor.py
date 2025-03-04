import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)


class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess(self, text):
        """
        Preprocess text:
        1. Convert to lowercase
        2. Tokenize
        3. Remove stopwords and punctuation
        4. Lemmatize
        """
        # Lowercase and tokenize
        tokens = word_tokenize(text.lower())

        # Remove stopwords and punctuation
        tokens = [t for t in tokens if t.isalnum() and t not in self.stop_words]

        # Lemmatize
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens]

        return tokens


# Create a singleton instance
preprocessor = TextPreprocessor()


def preprocess_query(query):
    """Preprocess a user query"""
    return preprocessor.preprocess(query)
