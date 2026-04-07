STOPWORDS = {
    "my", "the", "is", "are", "for", "a", "an", "to", "of"
}

def tokenize(text: str) -> list:
    """
    Converts cleaned text into tokens (words)
   """
    tokens = text.split()
    tokens = [word for word in tokens if word not in STOPWORDS]
    return tokens