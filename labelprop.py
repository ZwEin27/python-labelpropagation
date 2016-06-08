from pyspark import SparkFiles
from py4j.java_gateway import java_import
from py4j.java_gateway import JavaGateway
from subprocess import check_output
from decimal import Decimal
from pyspark import SparkContext

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-j','--worker_jar', required=True)


    sc = SparkContext(appName="LabelProp")

    fh = open('data/sample.json', 'rb')
    lines = fh.readlines()
    fh.close()
    lines = ''.join(lines)

    lp_runnable_jar_ = SparkFiles.get('labelprop.jar')
    eps = '%.e' % Decimal(eps)  # change decimal into e format
    argsArray = ['java', '-classpath', lp_runnable_jar_, 'org.ooxo.LProp', '-a', 'GFHF', '-m', str(iter), '-e', eps, lines]
    raw_output = check_output(argsArray)

"""
spark-submit --jars /Users/ZwEin/Project/machine_learning/python-labelpropagation/labelprop.jar --driver-class-path /Users/ZwEin/Project/machine_learning/python-labelpropagation/labelprop.jar spark_entrance.py -j /Users/ZwEin/Project/machine_learning/python-labelpropagation/labelprop.jar

"""



"""
from pyspark import SparkContext
from py4j.java_gateway import java_import

sc = SparkContext(appName="LabelProp")
java_import(sc._jvm, "org.ooxo.*")
lp = sc._jvm.LProp()

# load data
fh = open('data/sample.json', 'rb')
lines = fh.readlines()
fh.close()
lines = ''.join(lines)

print lp.do_lp(lines, 0.0001, 100)
"""

# from py4j.java_gateway import JavaGateway
# gateway = JavaGateway()
# lp = gateway.entry_point

# # load data
# fh = open('data/sample.json', 'rb')
# lines = fh.readlines()
# fh.close()
# lines = ''.join(lines)

# print lp.do_lp(lines, 0.0001, 100)




"""
spark-submit labelprop.py

spark-submit --driver-class-path /Users/ZwEin/Project/machine_learning/python-labelpropagation/labelprop.jar labelprop.py

"""