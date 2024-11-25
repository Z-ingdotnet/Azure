#Inferring a schema
%%pyspark. #magic
df = spark.read.load('Files/data/products.csv',
    format='csv',
    header=True
)
display(df.limit(10))


'''Scala implementation 
#%%spark
#val df = spark.read.format("csv").option("header", "true").load("Files/data/products.csv")
#display(df.limit(10))
'''


#Specifying an explicit schema
from pyspark.sql.types import *
from pyspark.sql.functions import *

productSchema = StructType([
    StructField("ProductID", IntegerType()),
    StructField("ProductName", StringType()),
    StructField("Category", StringType()),
    StructField("ListPrice", FloatType())
    ])

df = spark.read.load('Files/data/product-data.csv',
    format='csv',
    schema=productSchema,
    header=False)
display(df.limit(10))


#chain methods
bikes_df = df.select("ProductName", "Category", "ListPrice").where((df["Category"]=="Mountain Bikes") | (df["Category"]=="Road Bikes"))
display(bikes_df)