# Import the necessary libraries.
# Since we are using Python, import the SparkSession and related functions
# from the PySpark module.
import os
import sys

from pyspark.sql import SparkSession


def validate_file_path(path: str) -> str:
    """
    Validates and resolves the provided file path.
    Ensures the path exists, is a regular file, and resolves absolute path.
    """
    if not path:
        raise ValueError("File path cannot be empty.")

    abs_path = os.path.abspath(path)

    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Specified file does not exist: {path}")

    if not os.path.isfile(abs_path):
        raise ValueError(f"Specified path is not a file: {path}")

    return abs_path


if __name__ == "__main__":
   if len(sys.argv) != 2:
       print("Usage: mnmcount <file>", file=sys.stderr)
       sys.exit(-1)

   # Validate input file path before initializing Spark Session
   raw_file_path = sys.argv[1]
   try:
       mnm_file = validate_file_path(raw_file_path)
   except (ValueError, FileNotFoundError) as e:
       print(f"Error: {e}", file=sys.stderr)
       sys.exit(1)

   # Build a SparkSession using the SparkSession APIs.
   # If one does not exist, then create an instance. There
   # can only be one SparkSession per JVM.
   spark = (SparkSession
     .builder
     .appName("PythonMnMCount")
     .getOrCreate())
   # Read the file into a Spark DataFrame using the CSV
   # format by inferring the schema and specifying that the
   # file contains a header, which provides column names for comma-
   # separated fields.
   mnm_df = (spark.read.format("csv") 
     .option("header", "true") 
     .option("inferSchema", "true") 
     .load(mnm_file))

   # We use the DataFrame high-level APIs. Note
   # that we don't use RDDs at all. Because some of Spark's 
   # functions return the same object, we can chain function calls.
   # 1. Select from the DataFrame the fields "State", "Color", and "Count"
   # 2. Since we want to group each state and its M&M color count,
   #    we use groupBy()
   # 3. Aggregate counts of all colors and groupBy() State and Color
   # 4  orderBy() in descending order
   count_mnm_df = (mnm_df
     .select("State", "Color", "Count")
     .groupBy("State", "Color")
     .sum("Count")
     .orderBy("sum(Count)", ascending=False))
   # Show the resulting aggregations for all the states and colors;
   # a total count of each color per state.
   # Note show() is an action, which will trigger the above
   # query to be executed.
   count_mnm_df.show(n=60, truncate=False)
   print("Total Rows = %d" % (count_mnm_df.count()))
   # While the above code aggregated and counted for all 
   # the states, what if we just want to see the data for 
   # a single state, e.g., CA? 
   # 1. Select from all rows in the DataFrame
   # 2. Filter only CA state
   # 3. groupBy() State and Color as we did above
   # 4. Aggregate the counts for each color
   # 5. orderBy() in descending order  
   # Find the aggregate count for California by filtering
   ca_count_mnm_df = (mnm_df
     .select("State", "Color", "Count")
     .where(mnm_df.State == "CA")
     .groupBy("State", "Color")
     .sum("Count")
     .orderBy("sum(Count)", ascending=False))
   # Show the resulting aggregation for California.
   # As above, show() is an action that will trigger the execution of the
   # entire computation. 
   ca_count_mnm_df.show(n=10, truncate=False)
   # Stop the SparkSession
   spark.stop()