# Example of integration of the FastAPI Users library with Dishka

## Start up project
1. Create .env in /example_dishka_fastapiusers/
````
# Example!


# DB settings
DB_HOST=postgres
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=123

DATABASE_URI=postgresql+asyncpg://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# Fastapi users
SECRET_JWT=FDSJFSKJ!3@!sfhu4823482hfjsdfjksd!FDGfdsf432!83128*&*13fdsg
SECRET_MANAGER=fdgkgi!i45$@tiGFGBXdsagfdg3$@
````
2. Build docker in /example_dishka_fastapiusers/
``docker compose up --build``
3. Check docs in ``loclahost:8000/docs``

Dishka docs: https://dishka.readthedocs.io/en/stable/
\
FastAPI Users docs: https://fastapi-users.github.io/fastapi-users/10.1/configuration/full-example/