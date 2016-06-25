
from pyspark import SparkContext
from py4j.java_gateway import java_import

sc = SparkContext(appName="Py4jTesting")
java_import(sc._jvm, "org.test.py4j.AdditionApplication")
func = sc._jvm.AdditionApplication()
print func.addition(3, 4)



# from py4j.java_gateway import JavaGateway
# gateway = JavaGateway()
# random = gateway.jvm.java.util.Random() 
# number1 = random.nextInt(10)         
# number2 = random.nextInt(10)
# print(number1,number2)
# addition_app = gateway.entry_point    
# print addition_app.addition(number1,number2)

"""
spark-submit --jars addition.jar test.py
"""


"""
from py4j.java_gateway import JavaGateway

gateway = JavaGateway()
ep = gateway.entry_point.getLP()
"""