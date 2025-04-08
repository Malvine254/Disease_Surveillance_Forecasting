#!/usr/bin/env python
# coding: utf-8

# ## Disease Surveillance ML Notebook
# 
# New notebook

# In[6]:


# ---------------------------------------------
# STEP 1: Load your datasets from Lakehouse
# ---------------------------------------------
df_facility = spark.read.table("LakehouseGold.health_facility_reports_cleaned")
df_mobile = spark.read.table("LakehouseGold.mobile_health_reports_new")

# ---------------------------------------------
# STEP 2: Create Year & Month columns for joins
# ---------------------------------------------
from pyspark.sql.functions import year, month

df_facility = df_facility.withColumn("Year", year("Date_Reported")) \
                         .withColumn("Month", month("Date_Reported"))

df_mobile = df_mobile.withColumn("Year", year("Date")) \
                     .withColumn("Month", month("Date"))

# ---------------------------------------------
# STEP 3: Join datasets on County + Year + Month
# ---------------------------------------------
df_joined = df_facility.join(
    df_mobile,
    on=["County", "Year", "Month"],
    how="inner"
)

# ---------------------------------------------
# STEP 4: Select relevant features
# ---------------------------------------------
df_features = df_joined.select(
    "County", "Disease", "Reported_Cases", "Reported_Deaths",
    "Symptoms", "Severity", "Latitude", "Longitude", "Year", "Month"
)

# ---------------------------------------------
# STEP 5: Convert categories to numeric using StringIndexer
# ---------------------------------------------
from pyspark.ml.feature import StringIndexer

indexers = [
    StringIndexer(inputCol="County", outputCol="CountyIndex"),
    StringIndexer(inputCol="Disease", outputCol="DiseaseIndex"),
    StringIndexer(inputCol="Symptoms", outputCol="SymptomsIndex"),
    StringIndexer(inputCol="Severity", outputCol="SeverityIndex")
]

for indexer in indexers:
    df_features = indexer.fit(df_features).transform(df_features)

# ---------------------------------------------
# STEP 6: Assemble features
# ---------------------------------------------
from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=[
        "CountyIndex", "DiseaseIndex", "SymptomsIndex", "SeverityIndex",
        "Latitude", "Longitude", "Month"
    ],
    outputCol="features"
)

df_model = assembler.transform(df_features).select(
    "County", "Disease", "Year", "Month", "Reported_Cases", "features"
)

# ---------------------------------------------
# STEP 7: Train-Test Split
# ---------------------------------------------
train_data, test_data = df_model.randomSplit([0.8, 0.2], seed=42)

# ---------------------------------------------
# STEP 8: Train Random Forest Regressor
# ---------------------------------------------
from pyspark.ml.regression import RandomForestRegressor

rf = RandomForestRegressor(featuresCol="features", labelCol="Reported_Cases", numTrees=50)
model = rf.fit(train_data)

# ---------------------------------------------
# STEP 9: Predict on Test Set
# ---------------------------------------------
predictions = model.transform(test_data)

# ---------------------------------------------
# STEP 10: Evaluate Model
# ---------------------------------------------
from pyspark.ml.evaluation import RegressionEvaluator

evaluator = RegressionEvaluator(labelCol="Reported_Cases", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print(f"✅ RMSE: {rmse}")

# ---------------------------------------------
# STEP 11: Format and Save Final Results
# ---------------------------------------------
# Rename and select relevant columns
df_output = predictions.select(
    "County", "Disease", "Year", "Month", "Reported_Cases", predictions["prediction"].alias("Predicted_Cases")
)

# Save to Gold Lakehouse
df_output.write.mode("overwrite").format("delta").saveAsTable("LakehouseGold.Disease_Surveillance_Predictions")
print("✅ Final prediction table saved: Disease_Surveillance_Predictions")


# In[7]:


df = spark.sql("SELECT * FROM LakehouseGold.disease_surveillance_predictions LIMIT 1000")
display(df)

