# src/preprocessing/text_cleaner.py

import re
import string
from typing import List

class TextCleaner:
    """
    Production-ready text cleaner for DocuShield.
    Removes boilerplate, normalizes text, and prepares it
    for tokenization, embeddings, or rule-based NLP analysis.
    """

    def __init__(self, remove_numbers: bool = True, lower_case: bool = True):
        self.remove_numbers = remove_numbers
        self.lower_case = lower_case

        # Precompiled regex patterns for performance
        self.url_pattern = re.compile(r"http[s]?://\S+")
        self.email_pattern = re.compile(r"\S+@\S+")
        self.non_printable_pattern = re.compile(r"[\x00-\x1f\x7f-\x9f]")
        self.extra_whitespace_pattern = re.compile(r"\s+")

    def clean_text(self, text: str) -> str:
        """
        Clean a single text string from raw document extraction.
        """
        if not text:
            return ""

        # Remove URLs and email addresses
        text = self.url_pattern.sub(" ", text)
        text = self.email_pattern.sub(" ", text)

        # Remove non-printable/control characters
        text = self.non_printable_pattern.sub(" ", text)

        # Remove numbers if configured
        if self.remove_numbers:
            text = re.sub(r"\d+", " ", text)

        # Lowercase if configured
        if self.lower_case:
            text = text.lower()

        # Remove punctuation
        text = text.translate(str.maketrans("", "", string.punctuation))

        # Normalize whitespace
        text = self.extra_whitespace_pattern.sub(" ", text).strip()

        return text

    def clean_corpus(self, texts: List[str]) -> List[str]:
        """
        Clean a list of text strings in batch.
        """
        return [self.clean_text(t) for t in texts]
