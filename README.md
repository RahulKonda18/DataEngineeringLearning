# DataEngineeringLearning

Welcome to the **DataEngineeringLearning** repository! This project serves as a structured repository for learning Apache Spark, PySpark, and data engineering concepts through hands-on examples, notes, and standalone applications.

---

## 📂 Repository Structure

```
.
├── README.md
├── chapter1/
│   ├── chapter1.md        # Notes on PySpark shell, transformations, actions, lazy evaluation
│   └── sample.txt         # Sample text file used for PySpark shell exercises
└── chapter2/
    ├── chapter2.md        # Notes on Apache Spark architecture, DataFrames, and spark-submit
    ├── gen_mnm_dataset.py # Script to generate synthetic M&M dataset
    ├── mnm_dataset.csv    # Dataset with columns: State, Color, Count
    └── mnmcount.py        # PySpark application for aggregations and filtering on M&M dataset
```

---

## 📖 Chapter Summary

### [Chapter 1: Getting Started with PySpark Shell](./chapter1/chapter1.md)
Focuses on interactive exploration using the `pyspark` shell:
* **Spark Context & Session**: Overview of predefined variables (`spark` for `SparkSession` and `sc` for `SparkContext`).
* **Transformations vs Actions**: Understanding how transformations create new DataFrames lazily while actions trigger actual computation/execution.
* **Lazy Evaluation**: How Spark builds a logical execution plan and optimizes execution when actions like `collect()` or `save()` are invoked.

### [Chapter 2: Standalone PySpark Applications & DataFrame APIs](./chapter2/chapter2.md)
Focuses on building standalone PySpark applications and submitting them using `spark-submit`:
* **Spark Architecture**: Concepts including `SparkSession`, Driver Program, Cluster Manager, and Executors.
* **Structured APIs**: Advantages of High-Level DataFrame APIs over low-level RDDs (Catalyst Optimizer, Tungsten execution engine).
* **M&M Candy Count Application (`mnmcount.py`)**: Practical application performing CSV ingestion, schema inference, aggregations (`groupBy`, `sum`), sorting (`orderBy`), and filtering.

---

## 🚀 Getting Started

### Prerequisites
* Java 8 or 11
* Apache Spark (with PySpark installed)
* Python 3.x

### Running the Chapter 2 M&M Count Application

To submit and execute the PySpark M&M candy count application:

```bash
spark-submit chapter2/mnmcount.py chapter2/mnm_dataset.csv
```

---

## 📝 License
This repository is maintained for personal learning and educational purposes.
