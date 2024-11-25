#Connect to data sources and ingest data


#to Azure blob storage, read data and list df
# Azure Blob Storage access info
blob_account_name = "azureopendatastorage"
blob_container_name = "nyctlc"
blob_relative_path = "yellow"

# blob_sas_token = "add your SAS token here" 
# Construct the path for connection
wasbs_path = f'wasbs://{blob_container_name}@{blob_account_name}.blob.core.windows.net/{blob_relative_path}'

# WASBS path for connection including SAS token
# wasbs_path = f'wasbs://{blob_container_name}@{blob_account_name}.blob.core.windows.net/{blob_relative_path}?{blob_sas_token}'

# Read parquet data from Azure Blob Storage path
blob_df = spark.read.parquet(wasbs_path)

# Display the Azure Blob DataFrame
display(blob_df)



'''
alternate authentication
 Service Principal
'''

# Azure SQL Database connection info
server_name = "us_standards3.database.windows.net"
port_number = 1433  # Default port number for SQL Server
database_name = "test_db"
table_name = "test" # Database table

client_id = "IversonZHOU"  # Service principal client ID
client_secret = "YOUR_CLIENT_SECRET"  # Service principal client secret

# Build the Azure SQL Database JDBC URL with Service Principal 
jdbc_url = f"jdbc:sqlserver://{server_name}:{port_number};database={database_name};encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;Authentication=ActiveDirectoryServicePrincipal"

# Properties for the JDBC connection 
properties = {
    "user": client_id,
    "password": client_secret
            }

# Read table from Azure SQL Database using Entra ID Service Principal
sql_df = spark.read.jdbc(url=jdbc_url, table=table_name, properties=properties)

# Display the Azure SQL dataframe
display (sql_df)




# Write data into a lakehouse file
# Dataframe to Parquet file format (optimized columnar storage structure, and efficient compression capabilities)
parquet_output_path = "Files/your_folder/your_file_name"

df.write.mode("overwrite").parquet(parquet_output_path)

print(f"DataFrame has been written to Parquet file: {parquet_output_path}")




'''
Write to a Delta table
Delta tables are a key feature of Fabric lakehouses as supoport ACID transactions

'''
# Write dataframe to Delta table
delta_table_name = "test_table"
df.write.format("delta").mode("overwrite").saveAsTable(delta_table_name)

# Confirm load as Delta table
print(f"DataFrame has been written to Delta table: {delta_table_name}")



'''
V-Order enables faster and more efficient reads by various compute engines, such as Power BI, SQL, and Spark. V-order applies special sorting, distribution, encoding, and compression on parquet files at write-time.
Optimize write improves the performance and reliability by increasing files sizes, and so reducing the number of files written. It's useful for scenarios where the Delta tables have suboptimal or nonstandard file sizes, or where the extra write latency is tolerable.
'''