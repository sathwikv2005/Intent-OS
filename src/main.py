from preprocessing.clean import clean_text
from preprocessing.tokenize import tokenize

text = ">-< test te/xt to test t\he clean functi%on. &* "
cleansed = clean_text(text)

print("original => "+text)
print("cleaned => "+cleansed)
print(f"Tokenized => {tokenize(cleansed)}")