# Agentic-Powered Disease Surveillance and Outbreak Forecasting in Kenya

## 1. Project Overview

**Project Name:** Agentic-Powered Disease Surveillance and Outbreak Forecasting for Kenya

**Description:**  
This project aims to build a real-time, AI-powered disease surveillance and outbreak forecasting solution tailored to Kenya's healthcare landscape. Using Microsoft Fabric for unified data ingestion and transformation and Azure AI for predictive analytics, the system identifies early warning signs of disease outbreaks from health facilities, mobile reports, and environmental data.

**Problem Statement:**  
Kenya faces recurrent health challenges such as malaria, cholera, and pneumonia, often due to fragmented reporting systems and lack of early detection. The solution aims to unify disease-related data, predict outbreaks, and generate actionable insights to support timely interventions.

**Solution Summary:**  
- Ingests raw datasets via medallion architecture using Fabric’s Dataflow Gen2  
- Stores and refines data in the Lakehouse  
- Transforms and enriches data in the Eventhouse for AI-powered retrieval  
- Trains ML models for outbreak forecasting  
- Uses Azure OpenAI for natural language interactions  
- Web UI for interactive querying  
- Power BI for visual analytics

---

## 2. Objectives

- Align with Hackathon goals by deploying a real-world AI solution using Microsoft Fabric  
- Demonstrate advanced use of: Lakehouse, Eventhouse, Dataflow Gen2, ML, and reporting  
- Integrate Azure AI services including OpenAI  
- Create an intuitive natural language chatbot for non-technical users  
- Deliver predictive and real-time insights for Kenyan health decision-makers

---

## 3. Architecture Diagram

*(Add your architecture diagram image here)*

---

## 4. Dataset Documentation

### Mobile Health Reports
- **Source:** Synthetic data  
- **Rows:** 10,000  
- **Key Columns:** County, Disease_Suspected, Symptoms, Severity, Coordinates  
- **Issues:** Missing values, inconsistent formatting  

### Health Facility Reports API
- **Source:** Simulated Health Facility Reports API  
- **Rows:** 10,000  
- **Key Columns:** Facility_ID, County, Disease, Reported_Cases, Reported_Deaths, Date_Reported  
- **Issues:** Incomplete fields, inconsistencies  

---

## 5. Solution Components

### a) Data Ingestion
- Used Microsoft Fabric Pipelines to ingest:
  - CSV files (mobile health reports)
  - API data (facility reports)
- Scheduled refreshes to ensure real-time updates  
- Loaded into Lakehouse and created structured tables  

### b) Data Cleaning & Transformation
- Handled missing values (mean imputation, predictive techniques)  
- Removed outliers using statistical thresholds  
- Joined datasets on County, Year, Month  
- Engineered features (e.g., symptom severity, time variables)  

### c) AI/ML Modeling
- Integrated Azure ML for training and management  
- Models Used:
  - Random Forest Regressor – predict disease cases
  - ARIMA – forecast outbreak trends  
- Evaluated with RMSE and Accuracy  
- Saved predictions to Lakehouse Gold Layer (`Disease_Surveillance_Predictions`)  

### d) Visualization & Reporting
- Built Power BI dashboards using Lakehouse Gold Layer  
- Included:
  - Time-series disease trends  
  - Geographic heatmaps  
  - Resource planning views  
- Real-time filters by County, Date, Disease, Severity  

### e) Alerting & Decision Support
- Used threshold-based alerts via Power Automate  
- Notified users via Microsoft Teams & Email  
- Integrated alerts into dashboards for escalation  

---

## 6. Results

- Accurate outbreak hotspot predictions  
- Enhanced regional health visibility  
- Improved county-level resource planning  
- *(Add screenshots or model outputs here)*  

---

## 7. User Guide

### Prerequisites
- Microsoft Fabric workspace (admin access)  
- Power BI Pro or Premium per User  
- Azure OpenAI resource & access keys  
- Required CSV datasets

### Step-by-Step

**Step 1: Fabric Environment Setup**  
- Login to Microsoft Fabric  
- Create new workspace (e.g., `Disease Surveillance`)  
- Enable Lakehouse preview  

**Step 2: Upload Datasets to Lakehouse**  
- Create new Lakehouse (e.g., `DiseaseSurveillanceLakehouse`)  
- Upload CSVs to `Tables` section  

**Step 3: Transform Data**  
- Create Notebook  
- Load tables using PySpark/Pandas  
- Clean & transform (missing values, normalize, join)  
- Save new structured tables  

**Step 4: AI Model Training (Optional)**  
- Use ML interface in Fabric or Azure ML Studio  
- Train Random Forest/ARIMA  
- Save results to Lakehouse Gold Layer  

**Step 5: Chatbot with Azure OpenAI**  
- Deploy GPT model on Azure OpenAI  
- Use Flask or Node.js backend to query Lakehouse  
- Store credentials securely  

**Step 6: Power BI Dashboards**  
- Create Power BI Report  
- Connect to Lakehouse tables  
- Build visualizations  
- Publish to workspace  

---

## 8. Challenges Faced

- Data inconsistencies and gaps  
- Limited real-world labels for training  
- Designing near real-time data pipelines in Fabric  

---

## 9. Team

- **Malvin Owuor** – Data & AI Engineer  
- **Sammy Chesire** – Data & ML Engineer  
- **Edgar Ochieng** – Data & AI Engineer  

---

## 10. Future Work

- Integrate live APIs (e.g., DHIS2)  
- Add mobility/social media signals  
- Deploy as a full government portal app  

---

## 11. License

MIT License

