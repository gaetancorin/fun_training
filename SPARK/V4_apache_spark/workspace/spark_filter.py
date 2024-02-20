from pyspark.sql import SparkSession

# Création de la session Spark
spark = SparkSession.builder.appName("test-pc-3").getOrCreate()

# Données
data = [("Alice", 25), ("Bob", 17), ("Charlie", 30), ("Diana", 22)]
df = spark.createDataFrame(data, ["name", "age"])

# Affichage du DataFrame original
print("DataFrame original :")
df.show()

# Filtrer les personnes de plus de 20 ans
df_filtered = df.filter(df.age > 20)

# Trier par âge décroissant
df_sorted = df_filtered.orderBy(df.age.desc())

print("Filtré et trié :")
df_sorted.show()

# Arrêt de la session Spark
spark.stop()