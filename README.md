# FIUBER-Metrics

## Local installation & usage

1. Copy the Firebase credentials JSON (`firebase_credentials.json`) into the `src` directory of the repository.
2. Start the PostgreSQL instance.
```bash
docker volume create fiuber-metrics-db-volume # Ejecutar por única vez
docker run -e POSTGRES_PASSWORD=admin -it --rm -p 5432:5432 -v fiuber-metrics-db-volume:/var/lib/postgresql/data postgres
```
3. Start the server:
```bash
uvicorn main:app --reload
```

The API will be available on `http://localhost:8000/`.

## How to run tests locally
1. Start the PostgreSQL instance.
```bash
docker run -e POSTGRES_PASSWORD=admin -it --rm -p 5432:5432 postgres
```
2. Run tests.
```bash
cd src
pytest test.py
```

## Repository setup & okteto deployment

The following GitHub Actions Secrets are required:
1. `DOCKERHUB_USERNAME`
2. `DOCKERHUB_TOKEN`
3. `KUBE_CONFIG_DATA` (generated with `cat kubeconfig.yaml | base64 -w 0`)
4. `DATABASE_HOST`
5. `DATABASE_PASSWORD`
6. `FIREBASE_CREDENTIALS` (generated with `cat firebase-credentials.json | base64 -w 0`)
