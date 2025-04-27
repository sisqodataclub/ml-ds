import psycopg2
import logging
from datetime import datetime

def import_sql_to_postgres(
    db_params,
    sql_file_path,
    log_file="import_sql.log"
):
    """
    Connects to a PostgreSQL database and executes SQL commands from a file,
    while logging key actions and returning status.

    Args:
        db_params (dict): Connection parameters.
        sql_file_path (str): Absolute path to the SQL file.
        log_file (str): Path to the log file.

    Returns:
        bool: True if successful, False otherwise.
    """
    # Setup logging
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        msg = "✅ Connection successful!"
        print(msg)
        logging.info(msg)

        with open(sql_file_path, "r") as file:
            sql_script = file.read()
            cursor.execute(sql_script)

        connection.commit()
        msg = f"✅ SQL file '{sql_file_path}' imported successfully!"
        print(msg)
        logging.info(msg)
        return True

    except Exception as e:
        error_msg = f"❌ Error: {e}"
        print(error_msg)
        logging.error(error_msg)
        if connection:
            connection.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            logging.info("🔒 Connection closed.")
            print("🔒 Connection closed.")


# Example usage
if __name__ == "__main__":
    db_params = {
        "host": "127.0.0.1",
        "database": "my_database",
        "user": "postgres",
        "password": "password"
    }

    #sql_file_path = r"C:\Users\fd92u\ml-ds\sql\supabase\migrations\20250425184252_global.sql"
    sql_file_path = r"C:\Users\fd92u\ml-ds\sql\supabase\migrations\silver_transform_consumption_expenditure.sql"

    import_sql_to_postgres(db_params, sql_file_path)
