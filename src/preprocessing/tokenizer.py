# src/preprocessing/tokenizer.py
from typing import List
import re

class Tokenizer:
    """
    Simple regex-based tokenizer for cleaned text.
    Fully avoids NLTK 'punkt' dependency to prevent LookupError.
    """

    def __init__(self, lowercase: bool = True):
        self.lowercase = lowercase

    def sentence_tokenize(self, text: str) -> List[str]:
        """
        Split text into sentences using regex only.
        """
        if not text:
            return []
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if self.lowercase:
            sentences = [s.lower() for s in sentences]
        return [s.strip() for s in sentences if s.strip()]

    def word_tokenize(self, text: str) -> List[str]:
        """
        Split text into words using regex.
        """
        if not text:
            return []
        # Split on whitespace and punctuation
        tokens = re.findall(r'\b\w+\b', text)
        if self.lowercase:
            tokens = [t.lower() for t in tokens]
        return tokens

    def tokenize_corpus_sentences(self, texts: List[str]) -> List[List[str]]:
        return [self.sentence_tokenize(t) for t in texts]

    def tokenize_corpus_words(self, texts: List[str]) -> List[List[str]]:
        return [self.word_tokenize(t) for t in texts]
