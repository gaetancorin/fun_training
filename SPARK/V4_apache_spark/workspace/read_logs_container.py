from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ReadLogs").master("local[*]").getOrCreate()
sc = spark.sparkContext

rdd = sc.textFile("/opt/spark/logs/*.out")  # ou *.log selon tes fichiers

error_count = rdd.filter(lambda line: "ERROR" in line).count()
warn_count  = rdd.filter(lambda line: "WARN"  in line).count()
info_count  = rdd.filter(lambda line: "INFO"  in line).count()
print(f"Nombre de lignes : ERROR = {error_count}, WARN = {warn_count}, INFO = {info_count}\n")

print("Exemple de lignes du log :")
for line in rdd.take(10):
    print(line)

spark.stop()