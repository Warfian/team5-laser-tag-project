# import psycopg2
# from psycopg2 import sql

#main.py is our entry table
import main

# Define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    #'password': 'student',
    #'host': 'localhost',
    #'port': '5432'
}

def add(id, name):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        # Execute a query
        cursor.execute("SELECT version();")

        # Fetch and display the result
        version = cursor.fetchone()
        print(f"Connected to - {version}")


        # Insert sample data
        cursor.execute('''
            INSERT INTO players (id, codename)
            VALUES (%s, %s)
        ''', (id, name))

        # Commit the changes
        conn.commit()

        # Fetch and display data from the table
        cursor.execute("SELECT * FROM players;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def disconnect():
    # Connect to PostgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM players")
    conn.commit()

    cursor.execute("SELECT * FROM players;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    if cursor:
        cursor.close()
    if conn:
        conn.close()