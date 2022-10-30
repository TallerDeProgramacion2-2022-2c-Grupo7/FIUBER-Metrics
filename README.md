# FIUBER-Metrics

## Local installation & usage

1. Copy the Firebase credentials JSON (`firebase_credentials.json`) into the `src` directory of the repository.
2. Start the PostgreSQL instance: `docker run -e POSTGRES_PASSWORD=admin -it --rm -p 5432:5432 postgres`.
3. Start the server: `uvicorn main:app --reload`.

The API will be available on `http://localhost:8000/`.
