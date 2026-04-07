import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from preprocessing.clean import clean_text

class IntentClassifier:
    def __init__(self, intents_path):
        self.intents_path = intents_path
        self.vectorizer = CountVectorizer(ngram_range=(1, 2))
        self.model = LogisticRegression()

    def load_data(self):
        with open(self.intents_path, 'r') as f:
            data = json.load(f)

        texts = []
        labels = []

        for intent in data["intents"]:
            tag = intent["tag"]
            for pattern in intent["patterns"]:
                cleaned = clean_text(pattern)
                texts.append(cleaned)
                labels.append(tag)

        return texts, labels
    

    def train(self):
        """
        Train a intent classifier model on given intents data.
        """
        texts, labels = self.load_data()

        X = self.vectorizer.fit_transform(texts)
        y = labels

        self.model.fit(X, y)

    def predict(self, text):
        cleaned = clean_text(text)
        if len(cleaned.split()) < 2:
            return "Unknown", 0
        X = self.vectorizer.transform([cleaned])

        probs = self.model.predict_proba(X)[0]
        max_prob = max(probs)
        prediction = self.model.classes_[probs.argmax()]

        return prediction, max_prob