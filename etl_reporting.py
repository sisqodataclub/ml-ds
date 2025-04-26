import psycopg2

def create_top10_consumption_view(db_params):
    query = """
    CREATE OR REPLACE VIEW gold.top10_consumption_2023 AS
    WITH cleaned AS (
        SELECT
            country_name,
            value
        FROM silver.consumption_expenditure
        WHERE year = 2023
        AND country_name NOT IN (
            'World', 'IDA & IBRD total', 'IBRD only', 'IDA only',
            'High income', 'Low income', 'Middle income', 'Upper middle income',
            'Lower middle income', 'Low & middle income', 'OECD members',
            'Post-demographic dividend', 'Pre-demographic dividend',
            'Early-demographic dividend', 'Late-demographic dividend',
            'Least developed countries: UN classification',
            'Fragile and conflict affected situations', 'Heavily indebted poor countries (HIPC)',
            'Sub-Saharan Africa', 'East Asia & Pacific', 'Europe & Central Asia',
            'Latin America & Caribbean', 'Middle East & North Africa', 'South Asia', 'North America',
            'East Asia & Pacific (excluding high income)', 'Euro area', 'South Asia (IDA & IBRD)',
            'European Union', 'East Asia & Pacific (IDA & IBRD countries)',
            'Latin America & the Caribbean (IDA & IBRD countries)',
            'Sub-Saharan Africa (IDA & IBRD countries)', 'Sub-Saharan Africa (excluding high income)',
            'Europe & Central Asia (excluding high income)',
            'Middle East & North Africa (IDA & IBRD countries)',
            'Latin America & Caribbean (excluding high income)', 'Arab World',
            'Middle East & North Africa (excluding high income)',
            'Central Europe and the Baltics', 'Africa Eastern and Southern'
        )
        AND value IS NOT NULL
        AND value::text NOT ILIKE 'NaN'
    )
    SELECT
        country_name,
        value
    FROM cleaned
    ORDER BY value DESC
    LIMIT 10;

    """

    check_query = """
    SELECT table_name
    FROM information_schema.views
    WHERE table_schema = 'gold' AND table_name = 'top10_consumption_2023';
    """

    conn = psycopg2.connect(**db_params)

    try:
        cursor = conn.cursor()
        cursor.execute(check_query)
        view_exists = cursor.fetchone()
        if not view_exists:
            cursor.execute(query)
            conn.commit()
            print("✅ View created successfully.")
        else:
            print("ℹ️ View already exists. Skipping creation.")
    finally:
        conn.close()
        print("🔌 Connection closed.")


db_params = {
        "host": "127.0.0.1",
        "database": "my_database",
        "user": "postgres",
        "password": "password"
    }
create_top10_consumption_view(db_params)
