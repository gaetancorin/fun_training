from pyspark.sql import SparkSession
import socket

# Spark en mode cluster (ou master local pour tests)
spark = SparkSession.builder.appName("GetWorkerHostnames").master("spark://spark-master:7077").getOrCreate()
sc = spark.sparkContext

# Crée un RDD avec suffisamment de partitions pour toucher tous les workers
rdd = sc.parallelize(range(100), 100)  # 100 tâches réparties sur le cluster

# Chaque partition renvoie le hostname du conteneur qui l'exécute
hostnames = rdd.map(lambda _: socket.gethostname()).distinct().collect()

print("Nom des conteneurs Docker des workers :")
for hostname in hostnames:
    print(hostname)

spark.stop()
