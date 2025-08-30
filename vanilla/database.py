import psycopg

def get_db_connection():
    try:
        conn = psycopg.connect(
            host="localhost",
            dbname="healthlinkr_db",
            user="postgres",
            password="postgres",
            port=5433
        )
        return conn
    except Exception as e:
        print(f"Error: Could not connect to the database. {e}")
        return None