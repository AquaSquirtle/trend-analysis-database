import os
import psycopg2
from psycopg2 import sql

DB_HOST = os.getenv('POSTGRES_HOST', "localhost")
DB_PORT = os.getenv('POSTGRES_PORT', 5432)
DB_NAME = os.getenv('POSTGRES_DB', "postgres")
DB_USER = os.getenv('POSTGRES_USER', "postgres")
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', "postgres")
analyst_names = os.getenv('ANALYST_NAMES', '').split(',')

def create_analytic_role_and_users():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'analytic') THEN
                    CREATE ROLE analytic;
                END IF;
            END $$;
        """)
        cur.execute("""
            GRANT USAGE ON SCHEMA public TO analytic;
            GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytic;
        """)
        for name in analyst_names:
            name = name.strip()
            if not name:
                continue
                
            cur.execute(sql.SQL("""
                DO $$ 
                BEGIN 
                    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = {}) THEN
                        CREATE USER {} WITH PASSWORD {};
                    END IF;
                END $$;
            """).format(
                sql.Literal(name),
                sql.Identifier(name),
                sql.Literal(f'{name}_123')
            ))

            cur.execute(sql.SQL("GRANT analytic TO {};").format(sql.Identifier(name)))

        print(f"Successfully created analytic role and {len(analyst_names)} users")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    if not analyst_names or analyst_names == ['']:
        print("Error: ANALYST_NAMES environment variable is empty or not set")
    else:
        create_analytic_role_and_users()