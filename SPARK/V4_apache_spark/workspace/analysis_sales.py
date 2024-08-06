from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, max, min, col

spark = SparkSession.builder.appName("SalesAnalysis").getOrCreate()

# fictif data
data = [
    ("Alice", "Electronics", 1200),
    ("Bob", "Electronics", 1500),
    ("Alice", "Clothing", 300),
    ("Bob", "Clothing", 400),
    ("Charlie", "Electronics", 700),
    ("Charlie", "Clothing", 350),
]

columns = ["customer", "category", "amount"]

df = spark.createDataFrame(data, columns)
total_sales = df.agg(sum("amount").alias("total_sales")).collect()[0]["total_sales"]
average_sales = df.agg(avg("amount").alias("average_sales")).collect()[0]["average_sales"]

print(f"Total sales: {total_sales}")
print(f"Average sale amount: {average_sales:.2f}\n")


print("Sales by category:")
df.groupBy("category").agg(
    sum("amount").alias("total"),
    avg("amount").alias("average"),
    max("amount").alias("max_sale"),
    min("amount").alias("min_sale")
).show()

print("Sales by customer:")
df.groupBy("customer").agg(
    sum("amount").alias("total"),
    avg("amount").alias("average"),
    max("amount").alias("max_sale")
).show()

spark.stop()