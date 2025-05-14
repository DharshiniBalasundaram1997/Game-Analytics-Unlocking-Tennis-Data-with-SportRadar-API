# 🏆 Game Analytics: Unlocking Tennis Data with SportRadar API
The **Tennis Rankings Explorer** project is a comprehensive data engineering and visualization solution built using the **Sportradar API**. It focuses on extracting, storing, analyzing, and presenting data from professional tennis competitions.

---
## Domain:	
* Sports/Data Analytics
---
## 📌 Project Goals
* Parse and transform sports competition data.
* Design and maintain a structured SQL database.
* Provide interactive insights through a Streamlit dashboard.

---

## 🔍 Approach:
### 1️⃣ Data Extraction
* Fetch JSON responses from Sportradar API.
* Parse and flatten nested structures into tabular format.

### 2️⃣ Data Storage
* Design normalized SQL schema.
* Use PostgreSQL or MySQL for persistent data storage.
* Define appropriate data types and primary keys for each table.

### 3️⃣ Data Collection
**From API Endpoints:**
* **Competition Data:**
  * `Categories` Table
  * `Competitions` Table

* **Complexes Data:**
  * `Complexes` Table
  * `Venues` Table

* **Doubles Competitor Rankings:**
  * `Competitor_Rankings` Table
  * `Competitors` Table

### 4️⃣ Data Analysis
* Perform statistical analysis on rankings, competitors, and event metadata.

### 5️⃣ Interactive Dashboards
* Built using **Streamlit** for real-time exploration of tennis rankings and event data.
---

## 🧰 Skills & Technologies
* **Languages:** Python
* **Database:** PostgreSQL / MySQL, 
* **Framework:** Streamlit
* **API Integration:** Sportradar API
* **Cloud Platform:** Render (used for PostgreSQL database deployment and hosting)

---

## ✨ Demo & Usage
        1. Execute Competition_Details.ipynb,Complexes_Details.ipynb,venues_details.ipynb,Competitors_Details.ipynb,Competitor_Rankings.ipynb,sql_queries.ipynb,Streamlit.py
        2. Execute the above files in any IDE(VisualStudioCode) and for database for local use postgresql or for cloud use cloud streamlit
        3. If using cloud, change the environment to cloud in config.json. IF using local database, then change the environment to local
        4. Added the passwords in the secrets.toml folder (for cloudDB) and Added the passwords in the pwd.toml folder (for local DB)
                     project directory like this:
                               ![image](https://github.com/user-attachments/assets/a3823128-8d83-4c5e-9fea-e0bde1b4bcee)

                     Inside secrets.toml/pwd.toml:
                         host = "localhost"
                         user = "youruser"
                         password = "yourpassword"
                         database = "yourdbname"
                         port = "5432"
         5. To Set secrets in Streamlit Cloud UI:
                 Go to Streamlit Cloud.
                 Open your deployed app.
                 Click the “Manage app” button (bottom right).
                 Go to the “Secrets” tab.
                 Add your secrets in the following format:
                                 host = "your-db-host"
                                 user = "your-db-user"
                                 password = "your-db-password"
                                 database = "your-db-name"
                                 port = "5432"
         6. Using Render for PostgreSQL database deployment and hosting. Those connections I have been using in the Streamlit Cloud

---
