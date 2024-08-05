from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, col, count
import requests
import matplotlib.pyplot as plt

N = 5
url = f"https://baconipsum.com/api/?type=meat-and-filler&paras={N}"
response = requests.get(url)
paragraphs = response.json()

print(f"{len(paragraphs)} paragraphes récupérés :\n")
for i, para in enumerate(paragraphs, 1):
    print(f"Paragraphe {i} : {para}\n")

spark = SparkSession.builder.appName("BaconIpsumWordCount").getOrCreate()

df = spark.createDataFrame([(p,) for p in paragraphs], ["paragraph"])
words_df = df.select(explode(split(lower(col("paragraph")), r'\W+')).alias("word"))
word_counts = words_df.groupBy("word").agg(count("word").alias("count")).orderBy(col("count").desc())

top_20 = word_counts.limit(20).toPandas()
print("Top 20 mots les plus fréquents :")
print(top_20)


meat_keywords = ["bacon", "pork", "beef", "ham", "sausage", "jerky", "salami",
                 "prosciutto", "pancetta", "porchetta", "strip", "loin", "rib"]

meat_count = words_df.filter(col("word").isin(meat_keywords)).count()
filler_count = words_df.count() - meat_count

plt.figure(figsize=(6,6))
plt.bar(["Viande", "Remplissage"], [meat_count, filler_count], color=['red', 'grey'])
plt.title("Occurrences : Viande vs Remplissage")
plt.ylabel("Nombre d'occurrences")
plt.show()

spark.stop()
