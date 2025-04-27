import psycopg2
import pandas as pd
from gspread_dataframe import set_with_dataframe


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



# For regular expressions
import re
# For handling string
import string
# To interact with Google Sheets.
import gspread
#  For authenticating with Google APIs.
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials

scope= ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

credentials=ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\fd92u\Downloads\service_account.json', scope)
client=gspread.authorize(credentials)

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
# Write DataFrame to Google Sheets
set_with_dataframe(worksheet3, missing_consumption_view_df)
# Write DataFrame to Google Sheets
set_with_dataframe(worksheet4, total_consumption_view_df)
set_with_dataframe(worksheet5, top10_consumption_2023_df)