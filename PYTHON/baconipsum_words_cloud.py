import requests
from collections import Counter
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(counter)
plt.figure(figsize=(12,6))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title("Nuage de mots Bacon Ipsum")
plt.show()

# Histogramme "viande vs remplissage"
meat_keywords = ["bacon", "pork", "beef", "ham", "sausage", "jerky", "salami", "prosciutto", "pancetta", "porchetta", "strip", "loin", "rib"]
meat_count = sum(counter[word] for word in meat_keywords if word in counter)
filler_count = sum(counter.values()) - meat_count

plt.figure(figsize=(6,6))
plt.bar(["Viande", "Remplissage"], [meat_count, filler_count], color=['red', 'grey'])
plt.title("Occurrences : Viande vs Remplissage")
plt.ylabel("Nombre d'occurrences")
plt.show()
