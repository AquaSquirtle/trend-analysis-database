import os
import time
import psycopg2
import importlib.util
from faker import Faker
from dotenv import load_dotenv
load_dotenv()
DB = {
    'host':     os.getenv("POSTGRES_HOST", "postgres"),
    'port':     os.getenv("POSTGRES_PORT", 5432),
    'dbname':   os.getenv('POSTGRES_DB', "mypostgres"),
    'user':     os.getenv('POSTGRES_USER', "postgres"),
    'password': os.getenv('POSTGRES_PASSWORD', "postgres"),
}
COUNT     = int(os.getenv('SEED_COUNT', 10))
ENV       = os.getenv('APP_ENV', 'prod')
VERSION   = os.getenv('VERSION', 999)

if ENV.lower() != 'dev':
    exit(0)
repeats = 0
VERSION = int(VERSION) if VERSION and VERSION != "latest" else 999
while repeats < 10:
    try:
        conn = psycopg2.connect(**DB)
        cur  = conn.cursor()
        cur.execute("""
                    SELECT COUNT(*)
                    FROM public.flyway_schema_history
                    WHERE success = TRUE
                    """)
        applied = cur.fetchone()[0]
        conn.close()
        repeats += 1
        if applied == int(VERSION):
            break
    except psycopg2.OperationalError:
        pass
    time.sleep(1)
conn = psycopg2.connect(**DB)
cur  = conn.cursor()
fake = Faker()
base    = os.path.dirname(__file__)
for i in range(1, VERSION + 1):
    name = f"seed{i}.py"
    path = os.path.join(base, name)
    if not os.path.exists(path):
        print(f"Seed file {name} not found, skipping")
        continue
        
    try:
        spec = importlib.util.spec_from_file_location(f"seed_v{i}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, 'seed'):
            mod.seed(cur, fake, int(COUNT))
            conn.commit()
            print(f"Successfully seeded version {i}")
        else:
            print(f"Seed file {name} has no seed() function, skipping")
    except Exception as e:
        print(f"Error seeding version {i}: {str(e)}")
cur.close()
conn.close()