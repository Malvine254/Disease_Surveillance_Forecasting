# Agentic-Powered Disease Surveillance and Outbreak Forecasting in Kenya

![mela_logo](https://github.com/user-attachments/assets/6479dd4a-666f-4f9b-8d1f-8abb6afa4fb6)

## 1. Project Overview
## Project Name: Agentic-Powered Disease Surveillance and Outbreak Forecasting for Kenya

**Description**: This project aims to build a real-time, AI-powered disease surveillance and outbreak forecasting solution tailored to Kenya's healthcare landscape. Using Microsoft Fabric for unified data ingestion and transformation and Azure AI for predictive analytics, the system identifies early warning signs of disease outbreaks from health facilities, mobile reports, and environmental data.

**Problem Statement**: Kenya faces recurrent health challenges such as malaria, cholera, and pneumonia, often due to fragmented reporting systems and lack of early detection. The solution aims to unify disease-related data, predict outbreaks, and generate actionable insights to support timely interventions.

**Solution Summary:** Our solution ingests raw datasets through a medallion architecture using Fabric’s Dataflow Gen2, storing and refining data in the Lakehouse. Cleaned and transformed data is enriched in the Eventhouse for AI-powered retrieval. Built-in ML models in Fabric forecast outbreak trends, and Azure OpenAI provides natural language processing for interactive chatbot capabilities. A web-based UI allows users to ask questions in plain English and receive insights. Power BI dashboards complete the reporting and visualization layer.


## 3. Objectives

- Align closely with the Hackathon goal by designing and deploying a real-world AI application using Microsoft Fabric
- Demonstrate advanced usage of Fabric technologies: Lakehouse, Eventhouse, Dataflow Gen2, built-in ML, and reporting
- Integrate Azure AI services, including OpenAI for conversational AI
- Build an intuitive natural language chatbot interface for non-technical users
- Provide predictive and real-time insights to support disease surveillance and decision-making in Kenya


## 5. Architecture Diagram

![dtf (1)](https://github.com/user-attachments/assets/83cc36ce-f0f3-4aa8-b424-b036befb78bc)

# Project Video 

[![Watch the video](https://img.youtube.com/vi/-Drs5XrSfTI/maxresdefault.jpg)](https://youtu.be/-Drs5XrSfTI)



## 6. Dataset Documentation
# Mobile Health Reports
- Source: Synthetic data
- Rows: 10,000
- Key Columns: County, Disease\_Suspected, Symptoms, Severity, Coordinates
- Issues: Missing values, inconsistent formatting

# Health Facility Reports API
- Source: Simulated Health Facility Reports API
- Rows: 10,000
- Key Columns: Facility\_ID, County, Disease, Reported\_Cases, Reported\_Deaths, Date\_Reported 
- Issues: Incomplete fields, inconsistencies

## 7. Solution Components

**a) Data Ingestion**
- Utilized Microsoft Fabric Pipelines to ingest data from: 
- CSV files containing mobile health reports.
- APIs provide structured health facility reports.
- Loaded the data into a Lakehouse with scheduled refreshes to ensure near real-time updates.
- Created Lakehouse tables for both sources to streamline transformations and modeling.
![image](https://github.com/user-attachments/assets/c4acc8e5-565f-4cff-a26c-b48c1a1b1633)


**b) Data Cleaning & Transformation**
- Applied data transformation logic within Microsoft Fabric notebooks: 
- Missing values were filled using mean imputation or predictive techniques based on historical patterns.
- Outliers were identified and filtered out using statistical thresholds.
- Datasets were joined on County, Year, and Month to create a unified data model.
- Features were engineered (e.g., symptom severity indexing, time variables).

![image](https://github.com/user-attachments/assets/6b1b67ae-b522-4a4d-a27c-61ce3f3906a7)


**c) AI/ML Modeling**
- Integrated with Azure Machine Learning for scalable training and model management.
- Trained models included: 
- Random Forest Regressor – to predict disease case numbers using categorical and geospatial data.
- Used RMSE and Accuracy as evaluation metrics to ensure model quality and reliability.
- Final predictions were saved to the Lakehouse Gold Layer as Disease\_Surveillance\_Predictions.

![AI Model image](https://github.com/user-attachments/assets/0d828b17-e796-4d7a-9d1f-99c6e51e3184)

![ML Model image](https://github.com/user-attachments/assets/de0912dc-e942-4ab7-b644-46be3f9973cc)



**d) Visualization & Reporting**
- Built interactive Power BI dashboards connected directly to the Lakehouse Gold layer.
- Dashboards include: 
  - Total Reported Cases.
  - Map of reported cases by county.
  - Total Predicted Cases
  - Agentic Insights.
 
![image](https://github.com/user-attachments/assets/0888632f-6bee-45a1-8040-7d2135537ab1)


**e) Custom Agentic AI**

Our solution includes a custom Agentic AI designed to provide intelligent, conversational interactions with end users. Built with advanced reasoning capabilities, the agent can interpret natural language queries, retrieve relevant data, and assist with decision-making. 
It connects seamlessly to our data ecosystem, enabling dynamic responses based on real-time insights and curated knowledge sources.

![Screenshot 2025-04-08 123759](https://github.com/user-attachments/assets/5cb87b21-8dca-46ff-856f-c15082f99bb6)


![Screenshot 2025-04-08 124321](https://github.com/user-attachments/assets/d5b4120f-674f-4a74-bebc-394623049ced)



**7. User Guide**
Step-by-Step Guide to Replicating the Microsoft Fabric Solution
Prerequisites:
Access to Microsoft Fabric workspace with admin rights
Power BI license (Pro or Premium per user)
Azure OpenAI resource and access keys
Required CSV datasets (as provided in the data folder)

## Step-by-Step Guide to Replicating the Microsoft Fabric Solution

###  Step 1: Set Up Your Microsoft Fabric Environment
- Go to [Microsoft Fabric](https://app.fabric.microsoft.com) and log in.
- Create a new Workspace and name it appropriately (e.g., `Disease Surveillance`).
- Enable the Lakehouse preview feature if not already enabled.

###  Step 2: Create a Lakehouse and Upload Datasets
- In your workspace, click **New > Lakehouse** and name it `DiseaseSurveillanceLakehouse`.
- Open the Lakehouse and click **Upload > Files**, then upload each dataset CSV.
- Ensure the files are saved in the **Tables** section to auto-generate structured tables.

###  Step 3: Data Transformation with Notebooks
- In your Lakehouse, click **New notebook**.
- Load each table using PySpark or Pandas commands:

### Step 4: Train and Register AI Model (Optional)
- If performing modeling in Fabric, use the ML model notebook interface.
- Alternatively, train and register your Azure ML model separately.
- Use Azure ML Studio or Python SDK to train outbreak forecasting models and expose them as endpoints.

### Step 5: Connect Azure OpenAI and Build Chatbot
- Set up your Azure OpenAI resource and deploy a GPT model.
- Use Power BI or a web interface with a backend (Flask, Node.js, etc.) to create a chatbot that queries Fabric tables.
- Securely store your OpenAI keys and Fabric workspace endpoints

### Step 6: Create Dashboards in Power BI
1.	From your Fabric workspace, click New > Power BI Report.
   - Connect to Lakehouse tables using Direct Lake or Power BI Dataset.
   - Build visualizations:
      o	Disease trends
      o	Regional case distribution
      o	High-risk population charts
   - Save and publish dashboards to your workspace.


## 8. Challenges Faced

- Creating Vector Embedding in the EventHouse
- Training accurate models with limited real-world labels
- Synthetic data which was inconsistent

**9. Team**

- Malvine Owuor
- Sammy Chesire
- Edgar Ochieng

**10. Future Work**

- Integrate live health API feeds (e.g., DHIS2)
- Incorporate mobility and social media signals
- Deploy as a fully managed app for government health portals

## 10. License

# MIT License (c) 2025

Permission is granted free of charge to use, copy, modify, merge, publish, distribute, sublicense, and/or sell this software and its documentation, under the following conditions:

- The original copyright and permission notice must be included.
- The software is provided **"as is"**, without any warranty—express or implied.
- The authors are not liable for any damages arising from its use.


