FROM python
RUN pip install fastapi uvicorn firebase-admin
RUN pip install psycopg2-binary sqlalchemy
WORKDIR /app
COPY . .
WORKDIR /app/src
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
