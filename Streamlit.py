import streamlit as st
import psycopg2 
import pandas as pd
import numpy as np


import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os


import json
import toml


import sys
import os


#PostgreSQL Connectinon:
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# Load environment
try:
    with open("C:/Users/dhars/Downloads/Dhass/codeing/GUVI/2. MainBoot/4.Project_Code/Project1/Tennis_Data_SportRadar/config.json", "r") as f:
        config = json.load(f)

    env = config["environment"] # 'local' or 'cloud'
except FileNotFoundError:
    raise FileNotFoundError("⚠️ 'config.json' not found. Please check the path.")
except json.JSONDecodeError:
    raise ValueError("⚠️ 'config.json' is not a valid JSON file.")
except KeyError:
    raise KeyError("⚠️ 'environment' key not found in config.json.")

# Load secrets from your custom toml file
local_secrets = toml.load("C:/Users/dhars/Downloads/Dhass/codeing/GUVI/2. MainBoot/4.Project_Code/Project1/Tennis_Data_SportRadar/.pwd/pwd.toml")


# Append the directory where db_utils.py is located
sys.path.append(os.path.abspath('C:/Users/dhars/Downloads/Dhass/codeing/GUVI/2. MainBoot/4.Project_Code/Project1/Tennis_Data_SportRadar'))

from db_utils import connect_to_postgres, connect_to_sportradar

#DataBase Connection Details
try:  
    # Connect to default DB and create target DB if needed
    my_db_connection = connect_to_postgres(env, local_secrets) #connect to existing database first
    
    # Set autocommit so CREATE DATABASE works
    my_db_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Create cursor and check for database existence
    mycursor = my_db_connection.cursor()
    mycursor.execute("SELECT * FROM pg_database WHERE datname='sportradar'")
    exists = mycursor.fetchone()
    
    if not exists:
        mycursor.execute("CREATE DATABASE sportradar")   #create target DB
        print("Database 'sportradar' created")
    else:
        print("Database 'sportradar' already exists")
        
    mycursor.close()
    my_db_connection.close()
    
    # Reconnect to the newly ensured 'sportradar' database
    my_db_connection = connect_to_sportradar(env, local_secrets)
    
    my_db_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    #I need to connect the db and the python:
    mycursor = my_db_connection.cursor()
    
    print("Connected to 'sportradar' database.")
except Exception as e:
    st.error(f"Error connecting to the database: {e}")
    st.stop()


#TITLE
st.title("Tennis Rankings Explorer")


#---------------------------------Filters--------------------------------
#COMPETITOR NAMES FILTER
mycursor.execute("Select competitor_name from competitors_table")
result = mycursor.fetchall()

competitors_names = []
for i in result:
    competitors_names.append(i[0])
selected_competitor = st.sidebar.multiselect("Select a Competitor",competitors_names)




#COMPETITION GENDER FILTER
mycursor.execute("Select distinct(competition_gender) from competition_table")
result = mycursor.fetchall()

competiton_gender = []
for i in result:
    competiton_gender.append(i[0])

selected_gender = st.sidebar.selectbox("Gender",["Select Gender"] + competiton_gender)

#COUNTRY FILTER
mycursor.execute("Select distinct(competitor_country) from competitors_table order by competitor_country asc")
result = mycursor.fetchall()

competiton_country = []
for i in result:
    competiton_country.append(i[0])

selected_country = st.sidebar.multiselect("Select a Country",competiton_country)



#COMPETITIOR RANK FILTER
mycursor.execute("Select distinct(competitor_rank) from competitor_rankings_table order by competitor_rank asc")
result = mycursor.fetchall()

competitor_rank = []
for i in result:
    competitor_rank.append(i[0])

selected_competitor_rank = st.sidebar.select_slider('Competitor Rank', options=[""] +competitor_rank)



#COMPETITIOR RANK POINTS FILTER
mycursor.execute("Select distinct(competitor_rank_points) from competitor_rankings_table order by competitor_rank_points asc")
result = mycursor.fetchall()

competitor_rank_points = []
for i in result:
    competitor_rank_points.append(i[0])

selected_competitor_rank_points = st.sidebar.select_slider('Competitor Rank Points', options=[""] +competitor_rank_points)


#COMPETITIONS PLAYED
mycursor.execute("Select distinct(competitor_rank_competitions_played) from competitor_rankings_table order by competitor_rank_competitions_played asc")
result = mycursor.fetchall()

competitions_played = []
for i in result:
    competitions_played.append(i[0])

selected_competitions_played = st.sidebar.select_slider('No.Of.Competitions.Played',options=[""] + competitions_played)
#---------------------------------Filters--------------------------------

#MAIN TABS
tab1,tab2,tab3,tab4,tab5= st.tabs(['Summary Statistics','Competitor Details Viewer','Country-Wise Analysis','Leader Board','Run NoteBook Files'])


with tab5:
    try:
        # List of notebook files to run
        notebooks = [
                "tennis_db_loader/1_Category_Details.ipynb",
                "tennis_db_loader/2_Competition_Details.ipynb",
                "tennis_db_loader/3_Complexes_Details.ipynb",
                "tennis_db_loader/4_Venues_Details.ipynb",
                "tennis_db_loader/5_Competitors_Details.ipynb",
                "tennis_db_loader/6_Competitor_Rankings.ipynb",
                "SQL_Queries/sql_queries.ipynb"]
        
        def run_notebook(notebook_path):
            try:
                with open(notebook_path, 'r', encoding='utf-8') as f:
                  nb = nbformat.read(f, as_version=4)
                  ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
                  ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path) or './'}})
                  st.success(f"Successfully executed {notebook_path}")
            except Exception as e:
                st.error(f"Failed to execute {notebook_path}: {e}")
                
        
        
        if st.button("Run All Notebooks"):
            for nb_file in notebooks:
                run_notebook(nb_file)
            st.title("All ipynb files executed successfully")
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")


with tab1:
    try:
        #Total no.of competitors:
        mycursor.execute("SELECT COUNT(*) FROM competitors_table;")
        result = mycursor.fetchone()
        st.header("Total Competitors")
        st.markdown(f"{result[0]}")
        

        #No.of countires represented:
        mycursor.execute("Select count(distinct(competitor_country)) from competitors_table;")
        result = mycursor.fetchone()
        st.header("Countries Represented")
        st.markdown(f"{result[0]}")

        #Highest points scored by a competitor.
        mycursor.execute("""SELECT comp.competitor_name,comp_rank.competitor_rank_points FROM 
                         competitors_table comp Inner Join competitor_rankings_table comp_rank 
                         ON comp.competitor_id = comp_rank.competitor_id where  
                         comp_rank.competitor_rank_points = 
                         (SELECT MAX(competitor_rank_points) FROM competitor_rankings_table)""")
        result = mycursor.fetchall()
        # result = (competitor_name, points)
        if result:
             df = pd.DataFrame(result, columns=["Competitor Name", "Rank Points"])
             st.subheader("Highest Points scored by a Competitor")
             st.table(df)
        else:
             st.warning("No data found for highest rank points.")

        #Highest competitions played by a competitor.
        mycursor.execute("""SELECT comp.competitor_name,comp_rank.competitor_rank_competitions_played FROM 
                         competitors_table comp Inner Join competitor_rankings_table comp_rank 
                         ON comp.competitor_id = comp_rank.competitor_id where  
                         comp_rank.competitor_rank_competitions_played = 
                         (SELECT MAX(competitor_rank_competitions_played) FROM competitor_rankings_table)""")
        result = mycursor.fetchall()
        # result = (competitor_name, rank)
        if result:
             df = pd.DataFrame(result, columns=["Competitor Name", "Competitions Played"])
             st.subheader("Highest Competitions played by a Competitor")
             st.table(df)
        else:
             st.warning("No data found for Competitions played.")


        #Highest rank scored by a competitor.
        mycursor.execute("""SELECT comp.competitor_name,comp_rank.competitor_rank FROM 
                         competitors_table comp Inner Join competitor_rankings_table comp_rank 
                         ON comp.competitor_id = comp_rank.competitor_id where  
                         comp_rank.competitor_rank = (SELECT MAX(competitor_rank) FROM competitor_rankings_table)""")
        result = mycursor.fetchall()
        # result = (competitor_name, rank)
        if result:
             df = pd.DataFrame(result, columns=["Competitor Name", "Rank"])
             st.subheader("Highest Ranks scored by a Competitor")
             
             st.bar_chart(df.set_index("Competitor Name"))
            #  st.table(df)
        else:
             st.warning("No data found for highest rank.")


        #Top 3 Countries with the Highest Number of Competitions Played
        mycursor.execute("""SELECT comp.competitor_country,max(comp_rank.competitor_rank_competitions_played) as max_comp_played FROM 
                         competitors_table comp Inner Join competitor_rankings_table comp_rank 
                         ON comp.competitor_id = comp_rank.competitor_id 
						 group by competitor_country order by max_comp_played desc limit 3""")
        result = mycursor.fetchall()
        
        
        if result:
             df = pd.DataFrame(result, columns=["Country", "Maximum Competitions Played"])
             st.subheader("Top 3 Countries with the Highest Number of Competitions Played")
             
             st.line_chart(df.set_index("Country"))
            #  st.table(df)
        else:
             st.warning("No data found.")

    except Exception as e:
        st.error(f"Failed to fetch data: {e}")


with tab2:
    #Choose Competitor Name, Based on Competitor Name all the details will be fetched
    try:
        if selected_competitor:
            placeholders = ','.join(['%s'] * len(selected_competitor))

            query = f"""SELECT comp.competitor_name,comp.competitor_country,
            comp_rank.competitor_rank_points,comp_rank.competitor_rank,comp_rank.competitor_rank_movement,
            comp_rank.competitor_rank_competitions_played
            FROM competitors_table comp JOIN competitor_rankings_table comp_rank
            ON comp.competitor_id = comp_rank.competitor_id where comp.competitor_name in ({placeholders})"""

            # Prepare parameters for %s
            params = tuple(selected_competitor) 

            mycursor.execute(query, params)
            result = mycursor.fetchall()

            if result:
                st.subheader("Filtered Competitor Information:")
                df = pd.DataFrame(result, columns=["Competitor Name","Country", "Rank Points", "Rank", "Rank Movement", "Competitions Played"])
                st.table(df)
            else:
                st.warning("No Competitor Details found.")
        else:
            st.info("Select a Competitor.")
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")

    #Choose Competitor Rank, Based on Competitor Rank all the details will be fetched
    try:
        if selected_competitor_rank and selected_competitor_rank != "":           
            query = f"""SELECT comp.competitor_name,comp.competitor_country,
            comp_rank.competitor_rank_points,comp_rank.competitor_rank,comp_rank.competitor_rank_movement,
            comp_rank.competitor_rank_competitions_played
            FROM competitors_table comp JOIN competitor_rankings_table comp_rank
            ON comp.competitor_id = comp_rank.competitor_id where comp_rank.competitor_rank = %s"""

            # Prepare parameters for %s
            params = (selected_competitor_rank,) 

            mycursor.execute(query, params)
            result = mycursor.fetchall()

            if result:
                st.subheader("Filtered Competitor Rank Information:")
                df = pd.DataFrame(result, columns=["Competitor Name","Country", "Rank Points", "Rank", "Rank Movement", "Competitions Played"])
                st.table(df)
            else:
                st.warning("No Competitor Rank Details found.")
        else:
            st.info("Choose a Competitor Rank")
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")

    #Choose Competitor Rank Points, Based on Competitor Rank Points all the details will be fetched
    try:
        if selected_competitor_rank_points and selected_competitor_rank_points != "":           
            query = f"""SELECT comp.competitor_name,comp.competitor_country,
            comp_rank.competitor_rank_points,comp_rank.competitor_rank,comp_rank.competitor_rank_movement,
            comp_rank.competitor_rank_competitions_played
            FROM competitors_table comp JOIN competitor_rankings_table comp_rank
            ON comp.competitor_id = comp_rank.competitor_id where comp_rank.competitor_rank_points = %s"""

            # Prepare parameters for %s
            params = (selected_competitor_rank_points,) 

            mycursor.execute(query, params)
            result = mycursor.fetchall()

            if result:
                st.subheader("Filtered Competitor Rank Points Information:")
                df = pd.DataFrame(result, columns=["Competitor Name","Country", "Rank Points", "Rank", "Rank Movement", "Competitions Played"])
                st.table(df)
            else:
                st.warning("No Competitor Rank Points Details found.")
        else:
            st.info("Choose a Competitor Rank Points")
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")


    #Choose No.Of.Competions.Played, Based on No.Of.Competions.Played all the details will be fetched
    try:
        if selected_competitions_played and selected_competitions_played != "":           
            query = f"""SELECT comp.competitor_name,comp.competitor_country,
            comp_rank.competitor_rank_points,comp_rank.competitor_rank,comp_rank.competitor_rank_movement,
            comp_rank.competitor_rank_competitions_played
            FROM competitors_table comp JOIN competitor_rankings_table comp_rank
            ON comp.competitor_id = comp_rank.competitor_id where comp_rank.competitor_rank_competitions_played = %s"""

            # Prepare parameters for %s
            params = (selected_competitions_played,) 

            mycursor.execute(query, params)
            result = mycursor.fetchall()

            if result:
                st.subheader("Filtered - No Of Competions Played:")
                df = pd.DataFrame(result, columns=["Competitor Name","Country", "Rank Points", "Rank", "Rank Movement", "Competitions Played"])
                st.table(df)
            else:
                st.warning("No Competions Played Details found.")
        else:
            st.info("Choose a No. Of Competions Played")
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")       


    #Choose Gender, Based on Gender all the details will be fetched
    try:
        if selected_gender and selected_gender != "Select Gender":     
            query = f"""SELECT comp.competition_gender,comp.competition_type, COUNT(comp.competition_id) AS No_Of_Competitions 
            FROM competition_table comp where comp.competition_gender = %s
            GROUP BY comp.competition_gender,comp.competition_type order by competition_gender asc """

            # Prepare parameters for %s
            params = (selected_gender,) 

            mycursor.execute(query, params)
            result = mycursor.fetchall()

            if result:
                st.subheader("Filtered - No. of Competitions by Gender and Type:")
                df = pd.DataFrame(result, columns=["Gender","Type", "No. Of. Competitions Played"])
                st.table(df)
            else:
                st.warning("No Details found.")
        else:
            st.info("Select a gender")
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")   

   

with tab3:
    #Choose Country, Based on Country all the details will be fetched
    try:
        if selected_country:
            placeholders = ','.join(['%s'] * len(selected_country))

            query = f"""SELECT comp.competitor_country as Countries, count(comp_rank.competitor_rank_id) as No_of_competitors, 
            avg(comp_rank.competitor_rank_points) as Avg_Rank_Points FROM competitors_table comp
            inner JOIN competitor_rankings_table comp_rank ON comp.competitor_id = comp_rank.competitor_id 
            where comp.competitor_country in ({placeholders})  group by competitor_country """

            params = tuple(selected_country) 

            mycursor.execute(query, params)
            result = mycursor.fetchall()

            if result:
                st.header("Filtered Country Information")
                df = pd.DataFrame(result, columns=["Country", "No. Of. Competitors", "Avg. Rank Points"])
                st.table(df)
            else:
                st.warning("No Country Details Found.")
        else:
            st.info("Select a Country.")
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")


with tab4:
    try:
        # if selected_competitor:
        #     placeholders = ','.join(['%s'] * len(selected_competitor))

        #     query = f"""Select comp.competitor_name,comp_rank.competitor_rank 
        #     from competitors_table comp inner join competitor_rankings_table comp_rank 
        #     on comp_rank.competitor_id = comp.competitor_id where competitor_rank <=5 AND comp.competitor_name IN ({placeholders}) 
        #     order by competitor_rank asc"""

        #     # Prepare parameters for %s
        #     params = tuple(selected_competitor) 

        #     mycursor.execute(query, params)
        # else:
            query = """SELECT comp.competitor_name, comp_rank.competitor_rank 
                       FROM competitors_table comp 
                       INNER JOIN competitor_rankings_table comp_rank 
                       ON comp_rank.competitor_id = comp.competitor_id 
                       WHERE comp_rank.competitor_rank <= 5 
                       ORDER BY comp_rank.competitor_rank ASC"""
            mycursor.execute(query)
            result = mycursor.fetchall()

            if result:
                st.subheader("Top Ranking Competitors:")
                df = pd.DataFrame(result, columns=["Competitor Name","Rank"])
                st.table(df)
            else:
                st.warning("No Competitor Details found.")
        # else:
        #     st.info("Select a Competitor.")
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")