from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("test-pc").getOrCreate()

data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
df = spark.createDataFrame(data, ["name", "value"])
df.show()

spark.stop()