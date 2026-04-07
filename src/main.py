from core.handle_query import handle_query

while True:
    text = input("> You: ")
    print(handle_query(text))