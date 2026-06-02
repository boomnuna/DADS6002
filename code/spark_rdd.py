import sys
from pyspark.sql import SparkSession

def main():
    # Create a Spark session
    spark = SparkSession.builder \
        .appName("Assignment2_AverageIncome_RDD") \
        .master("local[*]") \
        .getOrCreate()

    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    # input file path (default to /workspace/input.txt directly from the local root folder)
    # Alternatively, you can point it to HDFS if needed: hdfs://namenode:9000/user/root/...
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "file:///workspace/input.txt"

    print("=" * 50)
    print("Part 1: Using Spark RDD")
    print("=" * 50)

    # 1. Read data using RDD
    lines = sc.textFile(input_file)

    # Split each line by comma and map to (district_id, (personal_income, 1))
    # line format is: person_id, district_id, personal_income
    rdd = lines.map(lambda line: line.split(",")) \
               .map(lambda parts: (int(parts[1]), (float(parts[2]), 1)))

    # Reduce by key (district_id) to calculate the sum of incomes and the count of people
    # x and y represent the tuples (sum_income, count)
    sum_count_rdd = rdd.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))

    # Map to calculate the average
    # value is (sum, count), so average is value[0] / value[1]
    avg_rdd = sum_count_rdd.mapValues(lambda value: value[0] / value[1])

    # Sort and collect the results
    result_rdd = avg_rdd.sortByKey().collect()

    for district, avg_income in result_rdd:
        print(f"District {district}: Average Income = {avg_income:.2f}")

    spark.stop()

if __name__ == "__main__":
    main()
