#!/usr/bin/env python
# coding: utf-8

# ## Azure AI Notebook
# 
# New notebook

# In[1]:


import requests
import json
 
# 🔐 Fill in your Azure OpenAI credentials
api_key = "91ebc42e-ccbc-4edf-a1ac-2e3918d94288"  # Replace with your key
endpoint = "https://mango-bush-0a9e12903.5.azurestaticapps.net/api/v1"  # No trailing slash!
deployment_name = "gpt-4"  #Open AI Deployment name
 
# Full URL with API version
url = f"{endpoint}openai/deployments/{deployment_name}/chat/completions?api-version=2023-07-01-preview"


# In[7]:


headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}
 
data = {
    "messages": [
        {"role": "system", "content": "You are a helpful health data assistant responsible for assisting County Health Teams, Hospitals and government officials get information on Disease Surveillance and Outbreak Forecasting"},
        {"role": "user", "content": "Which County had the highest number of predicted cases?"}
    ],
    "temperature": 0.8,
    "max_tokens": 350
}
 
response = requests.post(url, headers=headers, data=json.dumps(data))


# In[3]:


if response.status_code == 200:
    result = response.json()
    print("✅ Response:")
    print(result["choices"][0]["message"]["content"])
else:
    print("❌ Error:")
    print("Status Code:", response.status_code)
    print(response.text)


# In[1]:


df = spark.sql("SELECT * FROM disease_surveillance_predictions").toPandas()
df.head()


# In[3]:


def summarize_row(row):
    prompt = f"This County {row['County']}has the the highest Predicted cases {row['Predicted_Cases']}  of Disease {row['Disease']} in {row['Year']}. Give a comprehensive insight."
 
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
 
    data = {
    "messages": [
        {"role": "system", "content": "You are a helpful health data assistant responsible for assisting County Health Teams, Hospitals and government officials get information on Disease Surveillance and Outbreak Forecasting"},
        {"role": "user", "content": "Which County had the highest number of predicted cases?"}
    ],
    "temperature": 0.8,
    "max_tokens": 350
}

    response = requests.post(url, headers=headers, data=json.dumps(data))
 
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"


# In[4]:


df["Insight"] = df.apply(summarize_row, axis=1)
df.head()


# In[5]:


spark_df = spark.createDataFrame(df)
spark_df.write.mode("overwrite").format("delta").saveAsTable("ML_Predicted__Insights")


# In[6]:


df = spark.sql("SELECT * FROM LakehouseGold.ml_predicted__insights LIMIT 1000")
display(df)

