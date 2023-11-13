"""
Schedule ETL scripts with Jobs for smooth data handling.
"""

import psycopg2
import os
import numpy as np
import psycopg2.extras as extras
import pandas as pd

# This form uses environment variables. To make it work properly, add your keys to your workspace's environment variables in the sidebar.

# DB Creds 1:
user_1 = os.environ.get("DB_USER")
password_1 = os.environ.get("DB_PASSWORD")
host_1 = os.environ.get("DB_HOST_1")
database_name_1 = "raw_db"
port_1 = os.environ.get("DB_PORT_1")

# DB Creds 2:
user_2 = os.environ.get("DB_USER")
password_2 = os.environ.get("DB_PASSWORD")
host_2 = os.environ.get("DB_HOST_2")
database_name_2 = "processed_db"
port_2 = os.environ.get("DB_PORT_2")


def postgresql_to_dataframe(conn, select_query, column_names):
    """
    Transform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1

    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()

    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df


def execute_values(conn, df, table):

    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (author, columns)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()


def pandas_preprocessed(df):
    df = df.drop_duplicates()

    df = df.dropna()

    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])

    return df


query_authors = """
SELECT * from authors
"""

query_events = """
SELECT * from events
"""

query_workspaces = """
SELECT * from workspaces
"""

# Connect server
conn1 = psycopg2.connect(
    database=database_name_1, user=user_1, password=password_1, host=host_1, port=port_1
)

conn2 = psycopg2.connect(
    database=database_name_2, user=user_2, password=password_2, host=host_2, port=port_2
)

columns_name_authors = ["id", "created_at",
                        "updated_at", "deleted_at", "name", "email", "phone"]
columns_name_events = ["id", "created_at", "type", "author_id"]
columns_name_workspaces = ["id", "created_at",
                           "updated_at", "deleted_at", "author_id", "name"]

data = [{"tables_name": "authors", "select_query": query_authors, "columns_name": columns_name_authors},
        {"tables_name": "events", "select_query": query_events,
            "columns_name": columns_name_events},
        {"tables_name": "workspaces", "select_query": query_workspaces, "columns_name": columns_name_workspaces}]

for d in data:
    df = postgresql_to_dataframe(conn1, d.get(
        'select_query'), d.get('columns_names'))

    pandas_preprocessed(df)

    execute_values(conn2, df, d.get('tables_name'))