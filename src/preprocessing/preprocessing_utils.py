# src/preprocessing/preprocessing_utils.py

from typing import List
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from .tokenizer import Tokenizer

# Ensure these are downloaded once in your environment
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

class PreprocessingUtils:
    """
    Utilities for text preprocessing: stopword removal and lemmatization.
    Designed to process cleaned text from TextCleaner.
    """

    def __init__(self, language: str = "english"):
        self.stop_words = set(stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer()
        self.tokenizer = Tokenizer(lowercase=True)

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from a list of tokens.
        """
        return [t for t in tokens if t not in self.stop_words]

    def lemmatize_tokens(self, tokens: List[str]) -> List[str]:
        """
        Lemmatize a list of word tokens.
        """
        return [self.lemmatizer.lemmatize(t) for t in tokens]

    def preprocess_text(self, text: str) -> List[str]:
        """
        Full preprocessing for a single cleaned text:
        1. Tokenize into words
        2. Remove stopwords
        3. Lemmatize
        Returns list of processed tokens.
        """
        if not text:
            return []
        tokens = self.tokenizer.word_tokenize(text)
        tokens = self.remove_stopwords(tokens)
        tokens = self.lemmatize_tokens(tokens)
        return tokens

    def preprocess_corpus(self, texts: List[str]) -> List[List[str]]:
        """
        Preprocess a list of cleaned texts.
        """
        return [self.preprocess_text(t) for t in texts]
