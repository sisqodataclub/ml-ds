import pandas as pd
import psycopg2

def etl_insert_consumption_data(
    csv_file_path,
    db_params,
    table_name="bronze.consumption_expenditure",
    skip_rows=4
):
    """
    Extracts data from a CSV file and loads it into a PostgreSQL table.

    Parameters:
        csv_file_path (str): Full path to the CSV file.
        db_params (dict): Dictionary with PostgreSQL connection parameters.
        table_name (str): Target table name (include schema).
        skip_rows (int): Number of rows to skip in the CSV (default is 4).
    """
    try:
        # Extract: Load and preprocess CSV
        df = pd.read_csv(csv_file_path, skiprows=skip_rows)
        data_to_insert = df.to_dict(orient='records')

        # Transform & Load: Insert into PostgreSQL
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        for row in data_to_insert:
            columns = ', '.join([f'"{col}"' for col in row.keys()])
            placeholders = ', '.join(['%s'] * len(row))
            values = list(row.values())

            query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
            cursor.execute(query, values)

        connection.commit()
        print("✅ All data inserted successfully!")

    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


csv_file = r"C:\Users\fd92u\Downloads\API_NE.CON.PRVT.PP.CD_DS2_en_csv_v2_29916\Households and NPISHs Final consumption expenditure, PPP (constant 2021 international $).csv"

db_config = {
    "host": "127.0.0.1",
    "database": "my_database",
    "user": "postgres",
    "password": "password"
}

etl_insert_consumption_data(csv_file, db_config)
# print("✅ Data inserted successfully!")

