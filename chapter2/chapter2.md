# CHAPTER 2: Downloading Apache Spark and Getting Started

## Overview
In this chapter, we transition from the interactive PySpark shell to building and running standalone Apache Spark applications using the high-level DataFrame APIs and submitting them via `spark-submit`.

---

## Key Spark Architecture Concepts

* **SparkSession**: 
  * The unified entry point for Spark functionality introduced in Spark 2.0.
  * In standalone scripts, created using `SparkSession.builder.appName(...).getOrCreate()`.
  * Encapsulates previous contexts (`SQLContext`, `HiveContext`, `SparkContext`). Only one `SparkSession` exists per JVM.
* **Driver Program**: 
  * Orchestrates the execution, converts user code into Spark jobs, stages, and tasks, and coordinates with the Cluster Manager.
* **Cluster Manager**: 
  * Allocates physical resources across nodes (e.g., Standalone, YARN, Mesos, Kubernetes).
* **Executors**: 
  * Worker processes running on cluster worker nodes responsible for executing tasks and storing cached data.

---

## High-Level DataFrame API vs RDDs

* Modern Spark applications prioritize **DataFrames and Datasets** (Structured APIs) over low-level RDDs.
* DataFrames provide schema enforcement, type safety, and internal optimization via the **Catalyst Optimizer** and **Tungsten execution engine**.
* Computations can be expressed declaratively with chained method calls (`select`, `groupBy`, `orderBy`).

---

## Hands-on: M&M Candy Count Application (`mnmcount.py`)

This application demonstrates loading structured CSV data, performing multi-dimensional aggregations, and filtering using DataFrame APIs.

### 1. Ingesting CSV Data
```python
mnm_df = (spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(mnm_file))
```
* `header=true`: Uses the first row as column names (`State`, `Color`, `Count`).
* `inferSchema=true`: Automatically detects data types (e.g., strings, integers).

### 2. Aggregations (Group By & Count)
```python
count_mnm_df = (mnm_df
    .select("State", "Color", "Count")
    .groupBy("State", "Color")
    .sum("Count")
    .orderBy("sum(Count)", ascending=False))
```
* Groups data by state and color, computes the sum of candy counts, and sorts in descending order.

### 3. Filtering
```python
ca_count_mnm_df = (mnm_df
    .select("State", "Color", "Count")
    .where(mnm_df.State == "CA")
    .groupBy("State", "Color")
    .sum("Count")
    .orderBy("sum(Count)", ascending=False))
```
* Filters specifically for records where `State == "CA"` before grouping and aggregating.

### 4. Triggering Actions & Cleanup
* **`count_mnm_df.show(n=60, truncate=False)`**: Action triggering execution and rendering results to stdout.
* **`count_mnm_df.count()`**: Action returning total aggregated row count.
* **`spark.stop()`**: Terminates the active `SparkSession` and releases driver resources.

---

## Running the Application

Execute the Python script using `spark-submit`:

```bash
spark-submit chapter2/mnmcount.py chapter2/mnm_dataset.csv
```
