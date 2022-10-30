# FIUBER-Metrics

## Local installation & usage

1. Copy the Firebase credentials JSON (`firebase_credentials.json`) into the `src` directory of the repository.
2. Start the PostgreSQL instance: `docker run --name admin -e POSTGRES_PASSWORD=admin -it --rm -p 5432:5432 postgres`
3. Start the server: `DATABASE_URL="postgresql://postgres:admin@localhost:5432/postgres" uvicorn main:app --reload`.

The API will be available on `http://localhost:8000/`.
