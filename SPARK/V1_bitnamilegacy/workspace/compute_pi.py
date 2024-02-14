from pyspark.sql import SparkSession
import random

# Crée la session Spark
spark = SparkSession.builder.appName("ComputePi").getOrCreate()
sc = spark.sparkContext

# Nombre de points à générer
NUM_SAMPLES = 1000000

def inside_circle(_):
    x = random.random()
    y = random.random()
    return 1 if x*x + y*y < 1 else 0

# Distribuer les calculs
count = sc.parallelize(range(NUM_SAMPLES)).map(inside_circle).reduce(lambda a, b: a + b)

pi_estimate = 4 * count / NUM_SAMPLES
print(f"Approximation of Pi is {pi_estimate}")

# Stop la session Spark
spark.stop()