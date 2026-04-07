from nlp.intent_classifier import IntentClassifier
from nlp.entity_extractor import EntityExtractor
from preprocessing.clean import clean_text

clf = IntentClassifier("./data/intents.json")
extractor = EntityExtractor()
clf.train()

while True:
    text = input("> You: ")
    cleaned = clean_text(text)
    intent, confidence = clf.predict(text)
    print(f"Intent {confidence:.2f}: {intent}")
    entities = extractor.extract(cleaned)
    print(f"entities: {entities}")