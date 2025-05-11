# 🏆 Tennis Rankings Explorer

The **Tennis Rankings Explorer** project is a comprehensive data engineering and visualization solution built using the **Sportradar API**. It focuses on extracting, storing, analyzing, and presenting data from professional tennis competitions.

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
* **Database:** PostgreSQL / MySQL
* **Framework:** Streamlit
* **API Integration:** Sportradar API

---

## ✨ Demo & Usage

*(Add your Streamlit Cloud URL or usage instructions here)*

---

## 📚 License

*(Add license details if applicable)*

---

## ✉️ Contact

For questions or suggestions, feel free to reach out via [GitHub Issues](https://github.com/your-repo/issues).
