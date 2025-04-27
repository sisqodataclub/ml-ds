

# Automating SQL Migrations with Python

This project demonstrates how to automate SQL migrations using Python. The script is designed to work with a PostgreSQL database and leverages Supabase CLI for managing migrations. It includes functionality to generate SQL migration files and populate them with `CREATE TABLE` statements derived from CSV files.

## Key Features

1. **Automated Migration File Creation**:
    - The script uses the Supabase CLI to create a new migration file in a specified folder.
    - It identifies the latest migration file created and returns its path for further processing.

2. **Dynamic SQL Table Generation**:
    - Reads a CSV file and dynamically generates a `CREATE TABLE` SQL statement based on the CSV's structure.
    - Supports common data types such as `INTEGER`, `FLOAT`, `TEXT`, and `TIMESTAMP`.

3. **Schema Management**:
    - Ensures the existence of `bronze`, `silver`, and `gold` schemas in the database, following a layered data architecture.

## Workflow Overview

1. **Create a Migration File**:
    - The function `run_supabase_migration` creates a new migration file using the Supabase CLI.
    - It ensures the migration file is correctly named and located in the appropriate folder.

2. **Generate SQL from CSV**:
    - The function `write_sql_to_existing_file` reads a CSV file and generates a SQL `CREATE TABLE` statement.
    - It writes the SQL statement into the migration file created in the previous step.

3. **Execute the Workflow**:
    - The script ties everything together by creating a migration file and populating it with SQL based on a given CSV file.

## Example Usage

```python
# Define input parameters
folder = "sql"
migration_name = "global"
csv_file = r"C:\path\to\your\file.csv"
table_name = "consumption_expenditure"

# Step 1: Create Supabase migration
migration_file = run_supabase_migration(folder, migration_name)

# Step 2: Write SQL only if migration file was created
if migration_file:
     write_sql_to_existing_file(csv_file, table_name, migration_file)
```

## Prerequisites

- **Supabase CLI**: Ensure the Supabase CLI is installed and configured.
- **Python Libraries**: Install the required Python libraries using `pip install pandas`.

## Notes

- The script assumes the CSV file has a header row and skips the first four rows when reading the file.
- The generated SQL includes a `SERIAL` primary key column named `id`.

This project simplifies the process of creating and managing database migrations, making it easier to integrate structured data into your PostgreSQL database.


## Importing SQL to PostgreSQL

This section introduces a Python function to import SQL commands from a file into a PostgreSQL database. It includes logging for key actions and error handling to ensure a smooth execution process.

### Function Overview

The `import_sql_to_postgres` function connects to a PostgreSQL database, executes SQL commands from a file, and logs the process. It is designed to handle errors gracefully and ensure the database connection is properly closed.

### Key Features

1. **Database Connection**:
    - Establishes a connection to a PostgreSQL database using `psycopg2`.
    - Logs successful connections and errors.

2. **SQL Execution**:
    - Reads SQL commands from a file and executes them.
    - Commits changes to the database upon successful execution.

3. **Error Handling**:
    - Catches exceptions, logs errors, and rolls back transactions if needed.

4. **Logging**:
    - Logs all actions to a specified log file for traceability.

### Example Function

```python
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
```

### Example Usage

```python
if __name__ == "__main__":
    db_params = {
        "host": "127.0.0.1",
        "database": "my_database",
        "user": "postgres",
        "password": "password"
    }

    sql_file_path = r"C:\Users\fd92u\ml-ds\sql\supabase\migrations\silver_transform_consumption_expenditure.sql"

    import_sql_to_postgres(db_params, sql_file_path)
```

### Notes

- Ensure the `psycopg2` library is installed using `pip install psycopg2`.
- Replace `db_params` and `sql_file_path` with your database credentials and SQL file path.
- The log file (`import_sql.log`) will be created in the current working directory unless a different path is specified.

This function provides a robust way to automate SQL imports into PostgreSQL, making it easier to manage database updates and migrations.




## ETL Process: Inserting CSV Data into PostgreSQL

This section introduces a Python function to perform an ETL (Extract, Transform, Load) process, where data from a CSV file is inserted into a PostgreSQL table. The function handles data extraction, transformation, and insertion while ensuring proper error handling and connection management.

### Function Overview

The `etl_insert_consumption_data` function reads data from a CSV file, processes it, and inserts it into a specified PostgreSQL table. It supports skipping rows in the CSV file and dynamically generates SQL `INSERT` statements based on the data structure.

### Key Features

1. **Data Extraction**:
    - Reads a CSV file using `pandas` and preprocesses the data.
    - Supports skipping a configurable number of rows.

2. **Dynamic SQL Insertion**:
    - Dynamically generates `INSERT` statements based on the CSV's column structure.
    - Inserts data into a specified PostgreSQL table.

3. **Error Handling**:
    - Catches exceptions and rolls back transactions in case of errors.
    - Ensures database connections are properly closed.

4. **Logging**:
    - Prints success and error messages to the console for traceability.

### Example Function

```python
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
```

### Example Usage

```python
csv_file = r"C:\Users\fd92u\Downloads\API_NE.CON.PRVT.PP.CD_DS2_en_csv_v2_29916\Households and NPISHs Final consumption expenditure, PPP (constant 2021 international $).csv"

db_config = {
    "host": "127.0.0.1",
    "database": "my_database",
    "user": "postgres",
    "password": "password"
}

etl_insert_consumption_data(csv_file, db_config)
```

### Notes

- Ensure the `pandas` and `psycopg2` libraries are installed using `pip install pandas psycopg2`.
- Replace `csv_file` and `db_config` with the path to your CSV file and database credentials.
- The function assumes the target table already exists in the database.

This ETL function simplifies the process of loading structured data from CSV files into PostgreSQL, making it easier to manage and analyze data. 




## Enhanced SQL Import with Stored Procedure Execution

This section introduces an enhanced Python function to import SQL commands into a PostgreSQL database, check for the existence of a stored procedure, and execute it if available. The function includes robust logging, error handling, and connection management.

### Function Overview

The `import_sql_to_postgres` function connects to a PostgreSQL database, checks if a stored procedure exists, imports it if missing, and then executes the stored procedure. It ensures traceability through detailed logging and handles errors gracefully.

### Key Features

1. **Stored Procedure Check**:
    - Verifies if a specific stored procedure exists in the database.
    - Logs the result and takes appropriate action.

2. **SQL Import**:
    - Imports SQL commands from a file if the stored procedure is not found.
    - Commits changes to the database upon successful execution.

3. **Stored Procedure Execution**:
    - Calls the stored procedure after ensuring its existence.

4. **Logging**:
    - Logs all actions to both the console and a log file for traceability.

5. **Error Handling**:
    - Catches exceptions, logs errors, and rolls back transactions if needed.

### Example Function

```python
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
```

### Example Usage

```python
if __name__ == "__main__":
    db_params = {
        "host": "127.0.0.1",
        "database": "my_database",
        "user": "postgres",
        "password": "password"
    }

    sql_file_path = r"C:\Users\fd92u\ml-ds\sql\supabase\migrations\silver_transform_consumption_expenditure.sql"

    import_sql_to_postgres(db_params, sql_file_path)
```

### Notes

- Ensure the `psycopg2` library is installed using `pip install psycopg2`.
- Replace `db_params` and `sql_file_path` with your database credentials and SQL file path.
- The log file (`import_sql.log`) will be created in the current working directory unless a different path is specified.

This function provides a comprehensive solution for managing stored procedures and automating SQL imports into PostgreSQL, streamlining database operations.



## Creating and Managing PostgreSQL Views

This section introduces Python functions to create and manage PostgreSQL views for analyzing consumption expenditure data. These views are designed to provide insights into top consumption trends, total consumption, and missing data for the year 2023.

### Functions Overview

1. **`create_top10_consumption_view`**:
    - Creates a view showing the top 10 countries with the highest consumption expenditure in 2023.
    - Filters out aggregate regions and invalid data.

2. **`total_consumption_view`**:
    - Creates a view displaying total consumption expenditure for all valid countries in 2023.
    - Orders the data by expenditure in descending order.

3. **`missing_consumption_view`**:
    - Creates a view listing countries with missing or invalid consumption data for 2023.

4. **`create_top10_consumption_trend_view`**:
    - Creates a view showing the historical trend of consumption expenditure for the top 10 countries in 2023.

### Example Usage

```python
import psycopg2

db_params = {
    "host": "127.0.0.1",
    "database": "my_database",
    "user": "postgres",
    "password": "password"
}

# Create views
create_top10_consumption_view(db_params)
total_consumption_view(db_params)
missing_consumption_view(db_params)
create_top10_consumption_trend_view(db_params)
```

### Notes

- Ensure the `psycopg2` library is installed using `pip install psycopg2`.
- Replace `db_params` with your PostgreSQL connection details.
- The functions check if the views already exist before attempting to create them, ensuring idempotency.
- These views are created in the `gold` schema and rely on data from the `silver.consumption_expenditure` table.

This set of functions provides a robust way to analyze and manage consumption expenditure data in PostgreSQL, enabling better insights and decision-making.




## Exporting PostgreSQL Views to Google Sheets

This section introduces a Python script to export PostgreSQL views into Google Sheets. The script connects to a PostgreSQL database, retrieves data from specified views, and writes the data into separate worksheets in a Google Sheet. This process facilitates sharing and visualization of data.

### Key Features

1. **View Loading**:
    - Checks if the specified PostgreSQL views exist.
    - Loads data from the views into Pandas DataFrames.

2. **Google Sheets Integration**:
    - Authenticates with Google Sheets using a service account.
    - Creates a new Google Sheet and adds worksheets for each view.
    - Writes the DataFrames into the corresponding worksheets.

3. **Error Handling**:
    - Handles missing views gracefully.
    - Ensures proper connection management for both PostgreSQL and Google Sheets.

### Example Script

```python
import psycopg2
import pandas as pd
from gspread_dataframe import set_with_dataframe
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_view_as_df(db_params, schema_name, view_name):
    query = f"SELECT * FROM {schema_name}.{view_name};"

    check_query = """
    SELECT table_name
    FROM information_schema.views
    WHERE table_schema = %s AND table_name = %s;
    """

    conn = psycopg2.connect(**db_params)

    try:
        cursor = conn.cursor()
        # First check if the view exists
        cursor.execute(check_query, (schema_name, view_name))
        view_exists = cursor.fetchone()

        if not view_exists:
            print(f"⚠️ View '{schema_name}.{view_name}' does not exist.")
            return None

        # If exists, load into a DataFrame
        df = pd.read_sql_query(query, conn)
        print(f"✅ View '{schema_name}.{view_name}' loaded successfully.")
        return df

    finally:
        conn.close()
        print("🔌 Connection closed.")

# Database connection parameters
db_params = {
    "host": "127.0.0.1",
    "database": "my_database",
    "user": "postgres",
    "password": "password"
}

# Your list of view names
view_names = [
    "top10_consumption_trend",
    "missing_consumption_view",
    "total_consumption_view",
    "top10_consumption_2023"
]

# Dictionary to store the results
dfs = {}

# Simple for loop
for view_name in view_names:
    df = load_view_as_df(db_params, 'gold', view_name)
    dfs[view_name] = df  # Store each DataFrame into a dictionary
    if df is not None:
        print(f"DataFrame for view '{view_name}' created with {len(df)} rows.")
    else:
        print(f"DataFrame for view '{view_name}' could not be created.")

# Access each DataFrame individually
top10_consumption_trend_df = dfs["top10_consumption_trend"]
missing_consumption_view_df = dfs["missing_consumption_view"]
total_consumption_view_df = dfs["total_consumption_view"]
top10_consumption_2023_df = dfs["top10_consumption_2023"]

# Google Sheets Integration
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\fd92u\Downloads\service_account.json', scope)
client = gspread.authorize(credentials)

# Create a new Google Sheet
spreadsheet = client.create("tableau_consumption")

# Share it with your personal Google account so you can see it in Drive
spreadsheet.share('fd92uk@gmail.com', perm_type='user', role='writer')

print("Created Google Sheet:", spreadsheet.url)

# Open the existing Google Sheet (Use the same name from when you created it)
spreadsheet = client.open("tableau_consumption")

# Create new sheets (worksheets)
worksheet2 = spreadsheet.add_worksheet(title="top10_consumption_trend_df", rows="10000", cols="50")
worksheet3 = spreadsheet.add_worksheet(title="missing_consumption_view_df", rows="10000", cols="50")
worksheet4 = spreadsheet.add_worksheet(title="total_consumption_view_df", rows="10000", cols="50")
worksheet5 = spreadsheet.add_worksheet(title="top10_consumption_2023_df", rows="10000", cols="50")

# Write DataFrame to Google Sheets
set_with_dataframe(worksheet2, top10_consumption_trend_df)
set_with_dataframe(worksheet3, missing_consumption_view_df)
set_with_dataframe(worksheet4, total_consumption_view_df)
set_with_dataframe(worksheet5, top10_consumption_2023_df)
```

### Notes

- Ensure the required libraries are installed using `pip install psycopg2 pandas gspread gspread-dataframe oauth2client`.
- Replace `db_params` and `service_account.json` with your PostgreSQL credentials and Google service account key file.
- The script creates a new Google Sheet named `tableau_consumption` and adds worksheets for each view.
- The Google Sheet is shared with the specified email for easy access.

This script provides a seamless way to export PostgreSQL views into Google Sheets, enabling better collaboration and data visualization.
