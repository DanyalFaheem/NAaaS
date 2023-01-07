# Import the necessary modules
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Create a SparkSession
spark = SparkSession.builder \
   .appName("My App") \
   .config("spark.some.config.option", "some-value") \
   .getOrCreate()

# # Create a simple Python list
# data = [("Alice", 1), ("Bob", 2), ("Charlie", 3), ("David", 4), ("Edward", 5)]

# # Convert the list to a Spark DataFrame
# df = spark.createDataFrame(data, ["name", "age"])

# # Print the DataFrame
# df.show()

# # Select the "name" column and show the first 10 rows
# df.select("name").show(10)

# # Filter the DataFrame to only include people who are 25 or older
# df.filter(df["age"] >= 25).show()

# # Calculate the average age
# df.agg(avg(df["age"])).show()
# sc = SparkContext(conf=conf)

rdd = spark.sparkContext.parallelize(range(1, 100))


print("THE SUM IS HERE: ", rdd.sum())
# Stop the SparkSession
spark.stop()
