#!/usr/bin/env python
# coding: utf-8

# ## API Raw Data Ingestion Notebook
# 
# New notebook

# In[ ]:


# install pandas
get_ipython().system('pip install pandas --upgrade google-api-python-client google-auth google-auth-oauthlib')


# In[ ]:


import os
import io
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# ✅ Microsoft Fabric Lakehouse file path
SERVICE_ACCOUNT_FILE = "/lakehouse/default/Files/service_account.json"

# ✅ Google Drive read-only scope
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# ✅ Authenticate with Google
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# ✅ Folder ID in Google Drive
FOLDER_ID = "1lXiB1txJNb0kZM-Vk5TtIgFOasHgKeja"

def list_files_in_folder(service, folder_id):
    """ List all files inside a Google Drive folder """
    query = f"'{folder_id}' in parents and mimeType='text/csv'"
    files = []
    page_token = None
    while True:
        results = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token
        ).execute()
        files.extend(results.get("files", []))
        page_token = results.get("nextPageToken")
        if not page_token:
            break
    return files

def download_file_to_memory(service, file_id):
    """ Download file as BytesIO (in-memory) """
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)
    return fh
def clean_column_names(df):
    """Sanitize column names to be Delta Lake compatible"""
    cleaned_columns = [col.strip().replace(" ", "_").replace("(", "").replace(")", "").replace(",", "")
                       .replace(";", "").replace("{", "").replace("}", "").replace("\n", "")
                       .replace("\t", "").replace("=", "") for col in df.columns]
    df.columns = cleaned_columns
    return df

def create_table_from_csv(file_stream, table_name):
    """Load CSV, clean column names, write to Lakehouse as Spark table"""
    try:
        df_pd = pd.read_csv(file_stream)

        # Clean column names for Delta Lake
        df_pd = clean_column_names(df_pd)

        # Convert to Spark DataFrame
        df_spark = spark.createDataFrame(df_pd)

        # Write to Lakehouse table
        df_spark.write.mode("overwrite").saveAsTable(table_name)
        print(f"✅ Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"❌ Failed to create table: {e}")


def download_and_ingest_files():
    try:
        service = build("drive", "v3", credentials=creds)
        files = list_files_in_folder(service, FOLDER_ID)

        if not files:
            print("📂 No CSV files found in the folder.")
            return

        for file in files:
            print(f"📥 Processing file: {file['name']}")
            file_stream = download_file_to_memory(service, file["id"])
            table_name = file['name'].replace(".csv", "").replace(" ", "_").lower()
            create_table_from_csv(file_stream, table_name)

        print("\n✅ All CSV files ingested into Lakehouse tables.")
    except Exception as e:
        print(f"❌ Error: {e}")

# 🚀 Run the process
download_and_ingest_files()


# In[ ]:


df = spark.read.format("csv").option("header","true").load("Files/mobile_health_reports.csv")
# df now is a Spark DataFrame containing CSV data from "Files/mobile_health_reports.csv".
display(df)


# In[25]:


df.write.mode("overwrite").format("delta").save("Tables/mobile_health_reports")


# In[ ]:


df = spark.read.format("csv").option("header","true").load("Files/mobile_health_reports.csv")
# df now is a Spark DataFrame containing CSV data from "Files/mobile_health_reports.csv".
display(df)

