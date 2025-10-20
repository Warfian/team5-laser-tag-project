import psycopg2
from psycopg2 import sql

#main.py is our entry table
import main

# Define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    'password': 'student',
    'host': 'localhost',
    'port': '5432'
}


try:
    conn = psycopg2.connect(**connection_params)
    # Connect to PostgreSQL
    cursor = conn.cursor()

    # Execute a query
    cursor.execute("SELECT version();")

    # Fetch and display the result
    version = cursor.fetchone()
    print(f"Connected to - {version}")
except Exception as error:
    print(f"Error connecting to PostgreSQL database: {error}")

def add(id, name):
    # Insert data
    cursor.execute('''
        INSERT INTO players (id, codename)
        VALUES (%s, %s)
    ''', (id, name))

    # Commit the changes
    conn.commit()

    # Fetch and display data from the table
    print(f"Successfully addded to database! Currently in table:")
    cursor.execute("SELECT * FROM players;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def retrieve_table():
    cursor.execute("SELECT * FROM players;")
    return cursor.fetchall()

def disconnect():
    cursor.close()
    conn.close()
