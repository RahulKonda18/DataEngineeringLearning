import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """
    Session-scoped PySpark SparkSession fixture for testing.
    Creates a local Spark session with UI disabled and quiet log level.
    """
    session = (SparkSession.builder
               .master("local[2]")
               .appName("PySpark-UnitTest")
               .config("spark.ui.enabled", "false")
               .config("spark.sql.shuffle.partitions", "2")
               .getOrCreate())
    session.sparkContext.setLogLevel("ERROR")
    yield session
    session.stop()
