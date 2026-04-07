import re

def clean_text(text: str) -> str:
    """
     Converts to lowercase, normalises it, cleans text of punctuation, special chars, extra spaces.
    """

    text = text.lower()
    
    text = text.replace("'s", "")               # normalise 's 

    text = re.sub(r'\s+', ' ', text).strip()    # remove extra white spaces

    text = re.sub(r'[^a-z0-9\s]', '', text)     # remove any char not a alphabet, number or whitespace.

    return text