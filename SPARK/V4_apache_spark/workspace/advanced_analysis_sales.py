from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, max, month, round
from pyspark.sql.types import StringType, IntegerType, DateType
from datetime import datetime, timedelta
import random

spark = SparkSession.builder.appName("AdvancedSalesAnalysisRandom").getOrCreate()

# generate 1000 lines
customers = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace"]
products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Printer", "Tablet", "Headphones"]

def random_date(start, end):
    """Retourne une date aléatoire entre start et end"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

data = []
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

for _ in range(1000):
    date = random_date(start_date, end_date).strftime("%Y-%m-%d")
    customer = random.choice(customers)
    product = random.choice(products)
    amount = random.randint(20, 2000)  # montant aléatoire
    data.append((date, customer, product, amount))

columns = ["date", "customer", "product", "amount"]

df = spark.createDataFrame(data, columns)
df = df.withColumn("date", col("date").cast(DateType()))

# do stats
total_sales = df.agg(sum("amount").alias("total_sales")).collect()[0]["total_sales"]
average_sales = df.agg(avg("amount").alias("avg_sales")).collect()[0]["avg_sales"]
print(f"Total sales: {total_sales}, Average sale: {average_sales:.2f}\n")

# analysis:
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
