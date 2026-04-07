from nlp.intent_classifier import IntentClassifier

clf = IntentClassifier("./data/intents.json")
clf.train()

while True:
    text = input("You: ")
    intent, confidence = clf.predict(text)
    print(f"Intent {confidence:.2f}: {intent}")