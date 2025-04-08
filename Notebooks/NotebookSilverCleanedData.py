#!/usr/bin/env python
# coding: utf-8

# ## NotebookSilverCleanedData
# 
# New notebook

# In[2]:


mobile_health = spark.read.format("delta").load("abfss://ac53fe58-7aee-48aa-9fe9-110fe6af150f@onelake.dfs.fabric.microsoft.com/5ea71609-9ec1-4a32-8b12-bb4076ec4824/Tables/mobile_health_reports")
display(mobile_health)


# In[3]:


df = spark.sql("SELECT * FROM LakehouseSilver.mobile_health_silver LIMIT 1000")
display(df)


# In[4]:


# Step 2: Convert back to Spark DataFrame
spark_mobile_health_clean = spark.createDataFrame(pandas_mobile_health_clean)

# Step 3: Save cleaned data into Silver layer
spark_mobile_health_clean.write.mode("overwrite").format("delta").save("Tables/mobile_health_silver")


# In[5]:


from pyspark.sql import functions as F
from pyspark.sql import types as T
import random

# ✅ List of random realistic symptoms
symptoms_list = [
    "Fever", "Cough", "Fatigue", "Headache", "Nausea", "Shortness of breath",
    "Diarrhea", "Sore throat", "Loss of smell", "Muscle pain", "Vomiting", "Chills"
]

# ✅ UDF to randomly assign a symptom
random_symptom_udf = F.udf(lambda: random.choice(symptoms_list), T.StringType())

def clean_data(df):
    # ✅ Overwrite 'Symptoms' column with random values
    df = df.withColumn("Symptoms", random_symptom_udf())

    return df

# Run the cleaning function
df_clean = clean_data(df)

# Display the cleaned DataFrame
display(df_clean)


# 

# In[6]:


# ✅ Save to the default Lakehouse tables as 'mobile_health_silver'
df_clean.write.mode("overwrite").saveAsTable("mobile_health_silver")

print("✅ Table 'mobile_health_silver' saved to default Lakehouse.")


# In[9]:


df = spark.sql("SELECT * FROM LakehouseSilver.mobile_health_silver LIMIT 1000")
display(df)

