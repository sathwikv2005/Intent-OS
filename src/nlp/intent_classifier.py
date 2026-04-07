import json
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from preprocessing.clean import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UNKNOWN_FILE = os.path.join(BASE_DIR, "..", "data", "unknown_queries.json")
THRESHOLD = 0.5

class IntentClassifier:
    def __init__(self, intents_path):
        self.intents_path = intents_path
        self.vectorizer = CountVectorizer(ngram_range=(1, 2))
        self.model = LogisticRegression()
        try:
            if os.path.exists(UNKNOWN_FILE):
                with open(UNKNOWN_FILE, "r") as f:
                    self.unknown_queries = json.load(f)
            else:
                self.unknown_queries = []
        except json.JSONDecodeError:
            self.unknown_queries = []
            
            with open(UNKNOWN_FILE, "w") as f:
                json.dump([], f)

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

    def _log_unknown(self, query, confidence, prediction):
        """
        Saves unknown queries
        """
        if not any(q["query"] == query for q in self.unknown_queries):
            self.unknown_queries.append({
                "query": query,
                "confidence": float(confidence),
                "prediction": prediction
            })

            with open(UNKNOWN_FILE, "w") as f:
                json.dump(self.unknown_queries, f, indent=2)

    def predict(self, text):
        cleaned = clean_text(text)
        if len(cleaned.split()) < 2:
            return "Unknown", 0
        X = self.vectorizer.transform([cleaned])

        probs = self.model.predict_proba(X)[0]
        confidence = max(probs)
        prediction = self.model.classes_[probs.argmax()]

        if confidence < THRESHOLD:
            self._log_unknown(cleaned, confidence, prediction)
            return "Sorry, I didn't understand that.", confidence

        return prediction, confidence