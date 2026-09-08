# CHAPTER 1
## In this chapter I have created a sample Spark application using pyspark shell.

* pyspark shell provides sparkSession using the variable -> spark
* pyspark shell provides sparkContext using the variable -> sc 
* there are two types of operations that can be performed in spark. transformations and actions.
* Transformations: These operations transform the data by creating a new DataFrame without modifying the original dataFrame
* Actions: These operations interact with the storage directly like saving the data, collecting the data partitions, they perform the shuffle
* Spark evaluates transformations lazily, It builds a logical plan and only when a action like save() or collect() is performed, it optimizes the plan the executes the transformations in a efficient way.