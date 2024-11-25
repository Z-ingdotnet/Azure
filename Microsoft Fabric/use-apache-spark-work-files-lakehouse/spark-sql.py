#Spark catalog=metastore for relational data objects(views and tables)

#spark temporary view
df.createOrReplaceTempView("products_view")


#Spark SQL API
bikes_df = spark.sql("SELECT ProductID, ProductName, ListPrice \
                      FROM products \
                      WHERE Category IN ('Mountain Bikes', 'Road Bikes')")
display(bikes_df)


%%sql #magic

SELECT Category, COUNT(ProductID) AS ProductCount
FROM products
GROUP BY Category
ORDER BY Category