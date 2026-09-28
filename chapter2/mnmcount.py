# Import the necessary libraries.
# Since we are using Python, import the SparkSession and related functions
# from the PySpark module.
import sys

from pyspark.sql import DataFrame, SparkSession


def aggregate_mnm_counts(df: DataFrame, state: str = None) -> DataFrame:
    """Aggregates M&M counts by State and Color, sorted descending by sum(Count).

    Optionally filters by state if specified.
    """
    selected_df = df.select("State", "Color", "Count")
    if state is not None:
        selected_df = selected_df.where(selected_df.State == state)

    return (
        selected_df.groupBy("State", "Color")
        .sum("Count")
        .orderBy("sum(Count)", ascending=False)
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: mnmcount <file>", file=sys.stderr)
        sys.exit(-1)

    # Build a SparkSession using the SparkSession APIs.
    # If one does not exist, then create an instance. There
    # can only be one SparkSession per JVM.
    spark = (
        SparkSession.builder.appName("PythonMnMCount").getOrCreate()
    )
    # Get the M&M data set filename from the command-line arguments
    mnm_file = sys.argv[1]
    # Read the file into a Spark DataFrame using the CSV
    # format by inferring the schema and specifying that the
    # file contains a header, which provides column names for comma-
    # separated fields.
    mnm_df = (
        spark.read.format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .load(mnm_file)
    )

    # We use the DataFrame high-level APIs via helper function aggregate_mnm_counts.
    count_mnm_df = aggregate_mnm_counts(mnm_df)
    # Show the resulting aggregations for all the states and colors;
    # a total count of each color per state.
    # Note show() is an action, which will trigger the above
    # query to be executed.
    count_mnm_df.show(n=60, truncate=False)
    print("Total Rows = %d" % (count_mnm_df.count()))

    # Find the aggregate count for California by filtering
    ca_count_mnm_df = aggregate_mnm_counts(mnm_df, state="CA")
    # Show the resulting aggregation for California.
    ca_count_mnm_df.show(n=10, truncate=False)

    # Stop the SparkSession
    spark.stop()
