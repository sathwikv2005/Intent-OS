from nlp.intent_classifier import IntentClassifier

clf = IntentClassifier("./data/intents.json")
clf.train()

while True:
    text = input("You: ")
    intent, confidence = clf.predict(text)

    if confidence < 0.3:
        print("I didn't understand that.")
    else:
        print("Intent:", intent)