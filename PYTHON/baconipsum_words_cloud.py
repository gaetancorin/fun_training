import requests
from collections import Counter
import re

N = 5

url = f"https://baconipsum.com/api/?type=meat-and-filler&paras={N}"
response = requests.get(url)
paragraphs = response.json()

print(f"{len(paragraphs)} paragraphes récupérés :\n")
for i, para in enumerate(paragraphs, 1):
    print(f"Paragraphe {i} : {para}\n")

text = " ".join(paragraphs).lower()
words = re.findall(r'\b\w+\b', text)
counter = Counter(words)
most_common = counter.most_common(20)

print("Top 20 mots les plus fréquents :")
for word, count in most_common:
    print(f"{word} : {count}")
