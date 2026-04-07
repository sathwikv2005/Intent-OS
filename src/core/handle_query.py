import os
from nlp.intent_classifier import IntentClassifier
from nlp.entity_extractor import EntityExtractor
from preprocessing.clean import clean_text
from core.router import route

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
INTENTS_FILE = os.path.join(PROJECT_ROOT, "data", "intents.json")

clf = IntentClassifier(INTENTS_FILE)
extractor = EntityExtractor()
clf.train()

def handle_query(text):
    text = clean_text(text)
    print(f"Cleaned : {text}")
    
    intent, confidence = clf.predict(text)
    print(f"Intent {confidence:.2f}: {intent}")

    entities = extractor.extract(text)
    print(f"entities: {entities}")

    return route(intent, entities)