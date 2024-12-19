# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "2201502c-735a-4855-8bfd-8e448f913c90",
# META       "default_lakehouse_name": "dev_lakehouse",
# META       "default_lakehouse_workspace_id": "4aca0508-e966-40a7-a2a2-84861b281c83",
# META       "known_lakehouses": [
# META         {
# META           "id": "2201502c-735a-4855-8bfd-8e448f913c90"
# META         }
# META       ]
# META     },
# META     "environment": {
# META       "environmentId": "86b2682d-aaff-4b81-bbc7-8f76340b229b",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# CELL ********************

#parameter section
# _git_message
row_num = _parameter_row_num
concurrency = _setting_concurrency
storage_account = _secret_storage_account

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************


# MARKDOWN ********************

# #### Read Account key secret from Key Vault and Mount the ADLS Container

# CELL ********************

# Replace with your Key Vault name and secret name
key_vault_name = "ydeu2aml6491325893"
secret_name = "storage-ak-secret"
kv_uri = f"https://{key_vault_name}.vault.azure.net"

# Retrieve the ADLS account key
accountKey = mssparkutils.credentials.getSecret(kv_uri, secret_name)
print(accountKey)

# mounting the olmoloce-test container as mount point olga-test
notebookutils.fs.mount(  
    "abfss://olmoloce-test@fabcodestore.dfs.core.windows.net",  
    "/olga-test",  
    {"accountKey":accountKey}
)




# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#File read
with open(notebookutils.fs.getMountPath('/olga-test') + "/root/fabric-test.txt", "r") as f:
    print(f.read())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#load the NYC Taxi dataset 
nyc_df = spark.read.parquet("abfss://4aca0508-e966-40a7-a2a2-84861b281c83@onelake.dfs.fabric.microsoft.com/2201502c-735a-4855-8bfd-8e448f913c90/Files/NYC-Taxi-Green/")

#display top 100
display(nyc_df.limit(row_num))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Count distinct vendorID
distinct_vendor_count = nyc_df.select("vendorID").distinct().count()

print(f"Distinct vendorID count: {distinct_vendor_count}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Count values for each vendorID
vendor_counts = nyc_df.groupBy("vendorID").count()
vendor_counts.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

nyc_df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run Notebook 2XX

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
