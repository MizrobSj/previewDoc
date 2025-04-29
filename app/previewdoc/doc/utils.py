import re
import math
from collections import Counter

def tokenize(text):
    """Токенизация текста: разбивает текст на слова. Убирает знаки препинания и приводит к нижнему регистру."""
    return re.findall(r'\b\w+\b', text.lower())

def term_frequency(text):
    """Вычисляет частоту термина (TF) в тексте."""
    words = tokenize(text)
    total_words = len(words)
    term_count = Counter(words)
    
    # Calculate term frequency (TF)
    tf = {word: count / total_words for word, count in term_count.items()}
    
    return tf

def inverse_document_frequency(documents):
    """Вычисляет обратную частоту документа (IDF) для списка документов."""
    N = len(documents)
    word_doc_count = Counter()

    for doc in documents:
        unique_words = set(tokenize(doc))
        for word in unique_words:
            word_doc_count[word] += 1

    idf = {word: math.log(1 + N / word_doc_count[word]) for word in word_doc_count}
    return idf