# FIUBER-Metrics

[![codecov](https://codecov.io/gh/TallerDeProgramacion2-2022-2c-Grupo7/FIUBER-Metrics/branch/main/graph/badge.svg?token=KJPOL2HW69)](https://codecov.io/gh/TallerDeProgramacion2-2022-2c-Grupo7/FIUBER-Metrics)


## Local installation & usage

1. Copy the Firebase credentials JSON (`firebase_credentials.json`) into the `src` directory of the repository.

2. Install the requirements.
```
pip install -r requirements.txt
```

3. Create database volume (execute only once).
```bash
docker volume create fiuber-metrics-db-volume
```

4. Start the PostgreSQL instance.
```bash
docker run -it --rm \
    -e POSTGRES_PASSWORD=admin \
    -p 5432:5432 \
    -v fiuber-metrics-db-volume:/var/lib/postgresql/data \
    postgres
```

5. In another terminal, start the server:
```bash
cd src
uvicorn main:app --reload
```

The API will be available on `http://localhost:8000/`.

## Local tests execution
Execute the following script to build and run the tests using `Docker Compose`.
```bash
./run_tests.sh
```

## Repository & okteto deployment setup

The following GitHub Actions Secrets are required:
1. `DOCKERHUB_USERNAME`
2. `DOCKERHUB_TOKEN`
3. `KUBE_CONFIG_DATA` (generated with `cat kubeconfig.yaml | base64 -w 0`)
4. `DATABASE_HOST`
5. `DATABASE_PASSWORD`
6. `FIREBASE_CREDENTIALS` (generated with `cat firebase-credentials.json | base64 -w 0`)
