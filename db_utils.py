import psycopg2
import streamlit as st


# --- Function to connect to the default 'postgres' database ---
def connect_to_postgres(env, local_secrets):
    if env == "local":
        return psycopg2.connect(
            host=local_secrets["host"],
            user=local_secrets["user"],
            password=local_secrets["password"],
            database="postgres"
        )
    elif env == "cloud":
        return psycopg2.connect(
            host=st.secrets["host"],
            user=st.secrets["user"],
            password=st.secrets["password"],
            database="postgres",
            port=st.secrets["port"]
        )
    else:
        raise ValueError(f"Unknown environment: {env}")

# --- Function to connect to the actual 'sportradar' database ---
def connect_to_sportradar(env, local_secrets):
    if env == "local":
        return psycopg2.connect(
            host=local_secrets["host"],
            user=local_secrets["user"],
            password=local_secrets["password"],
            database=local_secrets["database"]
        )
    elif env == "cloud":
        return psycopg2.connect(
            host=st.secrets["host"],
            user=st.secrets["user"],
            password=st.secrets["password"],
            database=st.secrets["database"],
            port=st.secrets["port"]
        )
    else:
        raise ValueError(f"Unknown environment: {env}")
