from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, max, month, round


spark = SparkSession.builder.appName("AdvancedSalesAnalysis").getOrCreate()

# fictive data
data = [
    ("2025-01-10", "Alice", "Laptop", 1200),
    ("2025-01-15", "Bob", "Laptop", 1500),
    ("2025-02-01", "Alice", "Mouse", 50),
    ("2025-02-02", "Bob", "Keyboard", 100),
    ("2025-02-10", "Charlie", "Laptop", 700),
    ("2025-03-05", "Alice", "Monitor", 300),
    ("2025-03-10", "Charlie", "Mouse", 60),
    ("2025-03-15", "Bob", "Monitor", 350),
    ("2025-04-01", "Alice", "Laptop", 1300),
    ("2025-04-02", "Bob", "Mouse", 55),
    ("2025-04-05", "Charlie", "Keyboard", 110),
]

columns = ["date", "customer", "product", "amount"]
df = spark.createDataFrame(data, columns)

df = df.withColumn("date", col("date").cast("date"))


total_sales = df.agg(sum("amount").alias("total_sales")).collect()[0]["total_sales"]
average_sales = df.agg(avg("amount").alias("avg_sales")).collect()[0]["avg_sales"]
print(f"Total sales: {total_sales}, Average sale: {average_sales:.2f}\n")

print("Top clients:")
df.groupBy("customer").agg(sum("amount").alias("total_spent"), count("*").alias("nb_orders")) \
  .orderBy(col("total_spent").desc()) \
  .show()

print("Top products:")
df.groupBy("product").agg(sum("amount").alias("total_sales"), count("*").alias("nb_sales")) \
  .orderBy(col("total_sales").desc()) \
  .show()

df = df.withColumn("month", month(col("date")))
print("Monthly sales:")
df.groupBy("month").agg(
    sum("amount").alias("total_sales"),
    round(avg("amount"), 2).alias("avg_sales"),
    count("*").alias("nb_sales")
).orderBy("month").show()

total_global = df.agg(sum("amount").alias("total")).collect()[0]["total"]
df.groupBy("product").agg(
    sum("amount").alias("product_sales")
).withColumn("market_share", round(col("product_sales") / total_global * 100, 2)) \
  .orderBy(col("market_share").desc()) \
  .show()

spark.stop()
