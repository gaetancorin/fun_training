from pyspark.sql import SparkSession
import socket

spark = SparkSession.builder.appName("WorkerMemory").master("spark://spark-master:7077").getOrCreate()
sc = spark.sparkContext

def get_mem_info(_):
    mem_total, mem_free = 0, 0
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    mem_total = int(line.split()[1])  # kB
                elif line.startswith("MemFree:"):
                    mem_free = int(line.split()[1])
    except:
        pass
    hostname = socket.gethostname()
    return (hostname, mem_total, mem_free)

# RDD avec partitions
rdd = sc.parallelize(range(100), 100)

# Collecte les infos
workers_mem_raw = rdd.map(get_mem_info).collect()

# Réduire pour garder une seule ligne par hostname
workers_mem = {}
for hostname, total, free in workers_mem_raw:
    if hostname not in workers_mem:
        workers_mem[hostname] = (total, free)
    else:
        # optionnel : garder la valeur la plus faible de free
        workers_mem[hostname] = (total, min(workers_mem[hostname][1], free))

# Affichage propre
print(f"{'Hostname':<15} {'Total(MB)':>12} {'Free(MB)':>10}")
for hostname, (total, free) in workers_mem.items():
    print(f"{hostname:<15} {total//1024:>12} {free//1024:>10}")

spark.stop()
