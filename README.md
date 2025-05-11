# Tennis_Rankings_Explorer

The SportRadar Event Explorer project aims to develop a comprehensive solution for managing, visualizing, and analyzing sports competition data extracted from the Sportradar API.

Approach:
  1.Data Extraction
   ●	Parse and extract data from Sportradar JSON responses.(using API)
   ●	Transform nested JSON structures into a flat relational schema for analysis.
  
  2.Data Storage: 
   ●	Create a SQL database with well-designed schema (e.g., defining appropriate data types and primary keys).   The data to be collected is provided below.

  3.Data Collection:
    1)COLLECT THE COMPETITION DATA FROM THE API ENDPOINTS:
     	1. Categories Table
      2. Competitions Table
    2)COLLECT THE COMPLEXES DATA FROM THE API ENDPOINTS:
       1. Complexes Table
       2. Venues Table
    3)COLLECT THE DOUBLES COMPETITOR RANKINGS DATA FROM THE API ENDPOINTS:
       1. Competitor_Rankings Table
       2. Competitors Table

  4.Data Analysis:
  5.Interactive dashboards:
        Using Streamlit Application

Skills:
      1.	Languages: Python
      2.	Database: MySQL/PostgreSQL
      3.	Application: Streamlit
      4.	API Integration: Sportradar API
