# fast_api

<!-- without auto reloading -->
# uvicorn main:app

<!-- to run the main file with auto reloading -->
# uvicorn main:app --reload

<!-- intial only one to done in a project "alembic init" and alembic is file name to create the  migrations -->
# alembic init alembic

<!-- after this init change the line alembic.ini file lines  -->
# sqlalchemy.url = postgresql+psycopg2://postgres.uicdyanzztdwumhxqzhl:cbemlad01jElgxxm@aws-0-ap-south-1.pooler.supabase.com:6543/postgres

<!-- and inside the env.py file as -->
 # Import Base from database.py(which is connecting the database file)
# target_metadata = Base.metadata

<!-- to make migration the words with in the "" are user text -->
# alembic revision --autogenerate -m "migrated new fields"

<!-- to migrate the migrations -->
# alembic upgrade head

