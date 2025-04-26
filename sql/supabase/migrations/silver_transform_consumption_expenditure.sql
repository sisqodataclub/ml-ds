-- First: create the FUNCTION to add primary key constraint

-- First: create the sequence for the id column



CREATE OR REPLACE FUNCTION silver.add_id_column()
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    -- Step to add primary key constraint (no need to add id column anymore)
    ALTER TABLE silver.consumption_expenditure
    ADD PRIMARY KEY (id);
END;
$$;


CREATE OR REPLACE FUNCTION silver.lowercase_column_names(tablename TEXT)
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    col RECORD;
BEGIN
    FOR col IN
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'silver'
          AND table_name = tablename
    LOOP
        IF col.column_name <> lower(col.column_name) THEN
            EXECUTE format(
                'ALTER TABLE silver.%I RENAME COLUMN %I TO %I;',
                tablename,
                col.column_name,         -- old column name (with spaces)
                lower(replace(col.column_name, ' ', '_'))  -- new column name lowercase + replace spaces with _
            );
        END IF;
    END LOOP;
END;
$$;


-- Then: create the PROCEDURE that uses it
CREATE OR REPLACE PROCEDURE silver.transform_consumption_expenditure()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Step 0: Drop table if exists
    DROP TABLE IF EXISTS silver.consumption_expenditure;
    -- Step 0.1: Drop the sequence if exists
    DROP SEQUENCE IF EXISTS silver.consumption_expenditure_id_seq;

    -- Step 0.2: Create the sequence for the id column
    CREATE SEQUENCE silver.consumption_expenditure_id_seq
        START WITH 1
        INCREMENT BY 1
        NO MINVALUE
        NO MAXVALUE
        CACHE 1;

    -- Step 1: Create the table with the id column as the first column
    CREATE TABLE silver.consumption_expenditure AS
    SELECT
        -- Add 'id' column explicitly as the first column in the SELECT statement
        nextval('silver.consumption_expenditure_id_seq') AS id,
        "Country Name",
        "Country Code",
        "Indicator Name",
        "Indicator Code",
        kv.key::INT AS year,
        NULLIF(kv.value, '')::NUMERIC AS value,
        NOW()::TIMESTAMP AS inserted_at
    FROM bronze.consumption_expenditure AS b
    CROSS JOIN LATERAL (
        SELECT *
        FROM jsonb_each_text(
            to_jsonb(b)
            - 'Country Name'
            - 'Country Code'
            - 'Indicator Name'
            - 'Indicator Code'
            - '2024'
            - 'Unnamed: 69'
        )
        WHERE jsonb_each_text.key ~ '^\d{4}$'
    ) AS kv;


    -- Lowercase all columns
    PERFORM silver.lowercase_column_names('consumption_expenditure');

    -- Step 2: Call the function to add primary key constraint
    PERFORM silver.add_id_column();

END;
$$;
