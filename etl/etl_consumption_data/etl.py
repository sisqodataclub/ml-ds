import os
import subprocess
import pandas as pd
from datetime import datetime

def run_supabase_migration(folder: str, migration_name: str):
    """
    Runs a Supabase migration command inside a specified folder and returns the generated filename.
    """
    print(f"📌 Running Supabase migration in {folder}...")

    command = f'cd {folder} && supabase migration new {migration_name}'
    subprocess.run(command, shell=True, check=True)

    # Get the latest created migration file
    migration_folder = os.path.join(folder, "supabase", "migrations")
    files = sorted(os.listdir(migration_folder), reverse=True)

    for file in files:
        if migration_name in file and file.endswith(".sql"):
            migration_file = os.path.join(migration_folder, file)
            print(f"✅ Migration file created: {migration_file}")
            return migration_file

    print("❌ Error: Migration file not found!")
    return None

def write_sql_to_existing_file(csv_file, table_name, migration_file):
    """
    Writes a SQL CREATE TABLE statement from a CSV file to an existing migration file.
    """
    print(f"📌 Checking CSV file -> {csv_file}")

    if not os.path.exists(csv_file):
        print(f"❌ Error: CSV file '{csv_file}' does not exist!")
        return None

    try:
        df = pd.read_csv(csv_file, skiprows=4)
        print(f"✅ CSV loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return None

    if df.empty:
        print("❌ Error: CSV file is empty!")
        return None

    sql_types = {
        "int64": "INTEGER",
        "float64": "FLOAT",
        "object": "TEXT",
        "datetime64": "TIMESTAMP"
    }

    sql_statement_schema = """
    -- Create Bronze, Silver, and Gold schemas
    CREATE SCHEMA IF NOT EXISTS bronze;
    CREATE SCHEMA IF NOT EXISTS silver;
    CREATE SCHEMA IF NOT EXISTS gold;
    """
    sql_statements = ["-- SQL Migration Script\n"]
    
    sql_create_table = f"CREATE TABLE IF NOT EXISTS bronze.{table_name} (\n    id SERIAL PRIMARY KEY,\n"

    for col in df.columns:
        col_type = sql_types.get(str(df[col].dtype), "TEXT")  # Default to TEXT if unknown
        sql_create_table += f'    "{col}" {col_type},\n'

    sql_create_table = sql_create_table.rstrip(",\n") + "\n);\n"
    sql_statements.append(sql_statement_schema)
    sql_statements.append(sql_create_table)
   

    sql_content = "\n".join(sql_statements)

    print("📌 Writing SQL to:", migration_file)

    try:
        with open(migration_file, "w", encoding="utf-8") as f:
            f.write(sql_content)
            f.flush()
        print(f"✅ SQL migration file written successfully: {migration_file}")
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return None

    return migration_file

# 🏗 **Full Workflow Execution**
folder = "sql"
migration_name = "global"
csv_file = r"C:\Users\fd92u\Downloads\API_NE.CON.PRVT.PP.CD_DS2_en_csv_v2_29916\Households and NPISHs Final consumption expenditure, PPP (constant 2021 international $).csv"
table_name = "consumption_expenditure"

# Step 1: Create Supabase migration
migration_file = run_supabase_migration(folder, migration_name)

# Step 2: Write SQL only if migration file was created
if migration_file:
    write_sql_to_existing_file(csv_file, table_name, migration_file)