from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ReadLogs").master("local[*]").getOrCreate()
sc = spark.sparkContext

# Lire les fichiers logs directement depuis le container master
rdd = sc.textFile("/opt/spark/logs/*.out")  # ou *.log selon tes fichiers

# Exemple : compter les occurrences du mot "ERROR"
info_count = rdd.filter(lambda line: "INFO" in line).count()
print(f"Nombre de lignes avec INFO : {info_count}")

for line in rdd.take(10):
    print(line)

spark.stop()