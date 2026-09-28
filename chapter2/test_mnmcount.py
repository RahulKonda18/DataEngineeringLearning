import pytest
from pyspark.sql import SparkSession
from chapter2.mnmcount import aggregate_mnm_counts


@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder.appName("TestMnMCount")
        .master("local[1]")
        .getOrCreate()
    )
    yield session
    session.stop()


def test_aggregate_mnm_counts_all(spark):
    data = [
        ("CA", "Red", 10),
        ("CA", "Red", 20),
        ("NV", "Blue", 15),
        ("CA", "Blue", 5),
    ]
    df = spark.createDataFrame(data, ["State", "Color", "Count"])

    result_df = aggregate_mnm_counts(df)
    results = result_df.collect()

    assert len(results) == 3
    # First item should be CA Red with total 30 (since 30 > 15 > 5)
    assert results[0]["State"] == "CA"
    assert results[0]["Color"] == "Red"
    assert results[0]["sum(Count)"] == 30

    assert results[1]["State"] == "NV"
    assert results[1]["Color"] == "Blue"
    assert results[1]["sum(Count)"] == 15

    assert results[2]["State"] == "CA"
    assert results[2]["Color"] == "Blue"
    assert results[2]["sum(Count)"] == 5


def test_aggregate_mnm_counts_filter_state(spark):
    data = [
        ("CA", "Red", 10),
        ("CA", "Red", 20),
        ("NV", "Blue", 15),
        ("CA", "Blue", 5),
    ]
    df = spark.createDataFrame(data, ["State", "Color", "Count"])

    result_df = aggregate_mnm_counts(df, state="CA")
    results = result_df.collect()

    assert len(results) == 2
    for row in results:
        assert row["State"] == "CA"

    assert results[0]["Color"] == "Red"
    assert results[0]["sum(Count)"] == 30
    assert results[1]["Color"] == "Blue"
    assert results[1]["sum(Count)"] == 5
