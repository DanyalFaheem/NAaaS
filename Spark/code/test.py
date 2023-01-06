from pyspark import SparkConf, SparkContext

# Configure the connection to the Spark cluster
conf = SparkConf().setAppName("My App2").setMaster("spark://spark-master:7077")

# Create a SparkContext object
sc = SparkContext(conf=conf)

# Create a list of numbers
numbers = [1, 2, 3, 4, 5]

# Convert the list to a Spark RDD
numbers_rdd = sc.parallelize(numbers)

# Calculate the sum of the numbers in the RDD
sums = numbers_rdd.sum()
print("Pokemon")
# Print the sum
print(sums)

# Stop the SparkContext
sc.stop()
