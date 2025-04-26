import psycopg2
import logging
from logging import StreamHandler, FileHandler
from datetime import datetime

def import_sql_to_postgres(db_params, sql_file_path, log_file="import_sql.log"):
    """
    Connects to PostgreSQL, checks if a stored procedure exists, imports it if missing,
    then calls the stored procedure.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            FileHandler(log_file, encoding="utf-8"),
            StreamHandler()
        ],
        encoding="utf-8"
    )

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        print("Connection successful!")
        logging.info("Connection successful!")

        # Step 1: Check if the stored procedure exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM pg_proc
                JOIN pg_namespace ns ON ns.oid = pg_proc.pronamespace
                WHERE proname = 'transform_consumption_expenditure'
                  AND ns.nspname = 'silver'
            );
        """)
        exists = cursor.fetchone()[0]

        if exists:
            print("Stored procedure already exists.")
            logging.info("Stored procedure already exists.")
        else:
            # Step 2: If it doesn't exist, import the SQL file
            print("Stored procedure not found. Importing SQL file...")
            logging.info("Stored procedure not found. Importing SQL file...")

            with open(sql_file_path, "r", encoding="utf-8") as file:
                sql_script = file.read()
                cursor.execute(sql_script)

            connection.commit()

            print(f"SQL file '{sql_file_path}' imported successfully!")
            logging.info(f"SQL file '{sql_file_path}' imported successfully!")

        # Step 3: Call the stored procedure
        print("Calling stored procedure silver.transform_consumption_expenditure()...")
        logging.info("Calling stored procedure silver.transform_consumption_expenditure()...")

        cursor.execute("CALL silver.transform_consumption_expenditure();")
        connection.commit()

        print("Stored procedure executed successfully!")
        logging.info("Stored procedure executed successfully!")

        return True

    except Exception as e:
        error_msg = f"Error: {e}"
        sanitized_error_msg = error_msg.encode("ascii", "ignore").decode()
        print(sanitized_error_msg)
        logging.error(sanitized_error_msg)
        if connection:
            connection.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Connection closed.")
            logging.info("Connection closed.")







if __name__ == "__main__":
    db_params = {
        "host": "127.0.0.1",
        "database": "my_database",
        "user": "postgres",
        "password": "password"
    }

    sql_file_path = r"C:\Users\fd92u\ml-ds\sql\supabase\migrations\silver_transform_consumption_expenditure.sql"

    import_sql_to_postgres(db_params, sql_file_path)
    

