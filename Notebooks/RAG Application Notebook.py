ing#!/usr/bin/env python
# coding: utf-8

# ## RAG Application Notebook
# 
# New notebook

# In[ ]:


# Welcome to your new notebook
# Type here in the cell editor to add code!


# In[ ]:


# Example of query for reading data from Kusto. Replace T with your <tablename>.
kustoQuery = "['SurveillanceEmbeddings'] | take 10"
# The query URI for reading the data e.g. https://<>.kusto.data.microsoft.com.
kustoUri = "kustoUri"
# The database with data to be read.
database = "RAG_EventHouse"
# The access credentials.
accessToken = mssparkutils.credentials.getToken(kustoUri)
kustoDf  = spark.read\
    .format("com.microsoft.kusto.spark.synapse.datasource")\
    .option("accessToken", accessToken)\
    .option("kustoCluster", kustoUri)\
    .option("kustoDatabase", database)\
    .option("kustoQuery", kustoQuery).load()

# Example that uses the result data frame.
kustoDf.show()


# In[2]:


# The command is not a standard IPython magic command. It is designed for use within Fabric notebooks only.
# %pip install openai==1.12.0 azure-kusto-data langchain tenacity langchain-openai pypdf


# In[3]:


from openai import AzureOpenAI
from IPython.display import display, HTML
import os
import textwrap
import json 
from notebookutils import mssparkutils
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table

from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from tenacity import retry, wait_random_exponential, stop_after_attempt

OPENAI_GPT4_DEPLOYMENT_NAME="gpt-4"
OPENAI_DEPLOYMENT_ENDPOINT="OPENAI_DEPLOYMENT_ENDPOINT" 
OPENAI_API_KEY="OPENAI_API_KEY"
OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME = "armelyembed"

KUSTO_URI = "KUSTO_URI"
KUSTO_DATABASE = "KUSTO_DATABASE"
KUSTO_TABLE = "KUSTO_TABLE"
accessToken = mssparkutils.credentials.getToken(KUSTO_URI)
     


# In[14]:


pip install openai


# In[16]:


import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Set the base URL and your API key
openai.api_base = OPENAI_DEPLOYMENT_ENDPOINT  # Azure endpoint
openai.api_key = OPENAI_API_KEY  # API key for Azure OpenAI
openai.api_version = "2023-09-01-preview"

# Retry logic to handle throttling
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def generate_embeddings(text): 
    # replace newlines, which can negatively affect performance
    txt = text.replace("\n", " ")
    # Request embedding generation
    response = openai.Embedding.create(input=[txt], model=OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME)
    return response['data'][0]['embedding']


# In[17]:


import pandas as pd

# Create an empty DataFrame to store document chunks
df = pd.DataFrame(columns=['document_name', 'content', 'embedding'])

# Create a list to store new rows
new_rows = []

# Process each document and add to DataFrame
for document in documents:
    # Split document into pages
    pages = splitter.split_text(document)
    # Add each page to the list of rows
    for page in pages:
        new_rows.append({'document_name': 'disease_surveillance_predictions', 'content': page, 'embedding': ""})

# Convert the list of new rows to a DataFrame
new_df = pd.DataFrame(new_rows)

# Concatenate the new DataFrame with the existing one
df = pd.concat([df, new_df], ignore_index=True)

# Display the first few rows of the DataFrame
df.head()


# In[9]:


import pandas as pd

# Create an empty DataFrame to store document chunks
df = pd.DataFrame(columns=['document_name', 'content', 'embedding'])

# Create a list to store new rows
new_rows = []

# Process each document and add to list of new rows
for document in documents:
    # Split document into pages
    pages = splitter.split_text(document)
    # Add each page to the list of rows
    for page in pages:
        new_rows.append({'document_name': 'disease_surveillance_predictions', 'content': page, 'embedding': ""})

# Convert the list of new rows into a DataFrame
new_df = pd.DataFrame(new_rows)

# Concatenate the new DataFrame with the existing one
df = pd.concat([df, new_df], ignore_index=True)

# Display the first few rows of the DataFrame
df.head()



# In[19]:


df["embedding"] = df.content.apply(lambda x: generate_embeddings(x))
print(df.head(2))
     


# In[ ]:


#write the data to MS Fabric Eventhouse
df_sp = spark.createDataFrame(df)

df_sp.write.\
format("com.microsoft.kusto.spark.synapse.datasource").\
option("kustoCluster",KUSTO_URI).\
option("kustoDatabase",KUSTO_DATABASE).\
option("kustoTable", KUSTO_TABLE).\
option("accessToken", accessToken ).\
mode("Append").save()
     


# In[ ]:


def call_openAI(text):
    response = client.chat.completions.create(
        model=OPENAI_GPT4_DEPLOYMENT_NAME,
        messages = text,
        temperature=0
    )

    return response.choices[0].message.content


# In[ ]:


def get_answer_from_eventhouse(question, nr_of_answers=1):
        searchedEmbedding = generate_embeddings(question)
        kusto_query = KUSTO_TABLE + " | extend similarity = series_cosine_similarity(dynamic("+str(searchedEmbedding)+"), embedding) | top " + str(nr_of_answers) + " by similarity desc "
        kustoDf  = spark.read\
        .format("com.microsoft.kusto.spark.synapse.datasource")\
        .option("kustoCluster",KUSTO_URI)\
        .option("kustoDatabase",KUSTO_DATABASE)\
        .option("accessToken", accessToken)\
        .option("kustoQuery", kusto_query).load()

        return kustoDf


# In[ ]:


nr_of_answers = 2
question = "Which County had the highest number of Predicted Cases?"
answers_df = get_answer_from_eventhouse(question, nr_of_answers)

answer = ""
for row in answers_df.rdd.toLocalIterator():
    answer = answer + " " + row['content']

prompt = 'Question: {}'.format(question) + '\n' + 'Information: {}'.format(answer)
# prepare prompt
messages = [{"role": "system", "content": "You are a HELPFUL assistant answering users questions. Answer the question using the provided information and do not add anything else."},
            {"role": "user", "content": prompt}]

result = call_openAI(messages)
display(result)

