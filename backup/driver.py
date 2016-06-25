from pyspark import SparkContext
from py4j.java_gateway import java_import

sc = SparkContext(appName="Py4jTesting")
java_import(sc._jvm, "Calculate")
func = sc._jvm.Calculate()
print func.sqAdd(5)


"""
spark-submit --driver-class-path /Users/ZwEin/Project/machine_learning/python-labelpropagation/pyspark-test.jar driver.py
"""