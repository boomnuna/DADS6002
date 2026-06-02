import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType
import pyspark.sql.functions as F

def main():
    # Create a Spark session
    spark = SparkSession.builder \
        .appName("Assignment2_AverageIncome_SQL") \
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
    print("Part 2: Using Spark SQL")
    print("=" * 50)

    # Define the schema for the DataFrame
    schema = StructType([
        StructField("person_id", IntegerType(), True),
        StructField("district_id", IntegerType(), True),
        StructField("personal_income", DoubleType(), True)
    ])

    # Read the CSV into a DataFrame using the schema
    df = spark.read.csv(input_file, schema=schema)

    # Group by district_id and calculate the average personal_income
    avg_df = df.groupBy("district_id") \
               .agg(F.avg("personal_income").alias("average_income")) \
               .orderBy("district_id")

    # Show the formatted results
    avg_df.show()

    spark.stop()

if __name__ == "__main__":
    main()
