from pyspark.sql import *
from pyspark import *
# Initialize SparkContext
sc = SparkContext(appName="MyApp")
# spark = SparkSession.builder.appName("MyApp").getOrCreate()

# Create an RDD of elements to be processed
data = sc.parallelize([1, 2, 3, 4, 5])

# Define the function to be applied to each element
def process(x):
  # Do some processing here
  return x * 2

# Apply the function to each element in the RDD
result = data.map(process)

# Collect the results and print them
print(result.collect())
# Output: [2, 4, 6, 8, 10]