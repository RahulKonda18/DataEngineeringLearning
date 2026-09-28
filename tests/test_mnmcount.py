import os
from chapter2.mnmcount import count_mnm, count_mnm_for_state
from pyspark.sql.types import IntegerType, StringType, StructField, StructType


def test_count_mnm_aggregation_and_sorting(spark):
    """
    Test count_mnm aggregates counts by State and Color and sorts by sum(Count) descending.
    """
    data = [
        ("CA", "Red", 10),
        ("CA", "Red", 20),
        ("CA", "Blue", 5),
        ("WA", "Red", 50),
        ("WA", "Blue", 15),
    ]
    schema = StructType([
        StructField("State", StringType(), True),
        StructField("Color", StringType(), True),
        StructField("Count", IntegerType(), True),
    ])

    df = spark.createDataFrame(data, schema)
    result_df = count_mnm(df)
    results = result_df.collect()

    assert len(results) == 4
    # WA Red has sum(Count) = 50 (highest)
    assert results[0]["State"] == "WA"
    assert results[0]["Color"] == "Red"
    assert results[0]["sum(Count)"] == 50

    # CA Red has sum(Count) = 30 (second highest)
    assert results[1]["State"] == "CA"
    assert results[1]["Color"] == "Red"
    assert results[1]["sum(Count)"] == 30

    # WA Blue has sum(Count) = 15
    assert results[2]["State"] == "WA"
    assert results[2]["Color"] == "Blue"
    assert results[2]["sum(Count)"] == 15

    # CA Blue has sum(Count) = 5
    assert results[3]["State"] == "CA"
    assert results[3]["Color"] == "Blue"
    assert results[3]["sum(Count)"] == 5


def test_count_mnm_for_state_filtering(spark):
    """
    Test count_mnm_for_state filters rows for the specified state and aggregates counts.
    """
    data = [
        ("CA", "Red", 10),
        ("CA", "Red", 20),
        ("CA", "Blue", 5),
        ("WA", "Red", 50),
    ]
    schema = StructType([
        StructField("State", StringType(), True),
        StructField("Color", StringType(), True),
        StructField("Count", IntegerType(), True),
    ])

    df = spark.createDataFrame(data, schema)
    ca_results = count_mnm_for_state(df, "CA").collect()

    assert len(ca_results) == 2
    assert all(row["State"] == "CA" for row in ca_results)
    assert ca_results[0]["Color"] == "Red"
    assert ca_results[0]["sum(Count)"] == 30
    assert ca_results[1]["Color"] == "Blue"
    assert ca_results[1]["sum(Count)"] == 5


def test_count_mnm_empty_dataframe(spark):
    """
    Test behavior with an empty DataFrame.
    """
    schema = StructType([
        StructField("State", StringType(), True),
        StructField("Color", StringType(), True),
        StructField("Count", IntegerType(), True),
    ])

    empty_df = spark.createDataFrame([], schema)
    result_df = count_mnm(empty_df)
    results = result_df.collect()

    assert len(results) == 0


def test_mnmcount_integration_with_csv(spark):
    """
    Integration test using the actual mnm_dataset.csv dataset.
    """
    csv_path = "chapter2/mnm_dataset.csv"
    assert os.path.exists(csv_path)

    mnm_df = (spark.read.format("csv")
              .option("header", "true")
              .option("inferSchema", "true")
              .load(csv_path))

    count_df = count_mnm(mnm_df)
    total_rows = count_df.count()

    # 10 States x 6 Colors = 60 grouped rows
    assert total_rows == 60

    ca_count_df = count_mnm_for_state(mnm_df, "CA")
    ca_rows = ca_count_df.collect()

    assert len(ca_rows) == 6
    assert all(row["State"] == "CA" for row in ca_rows)
