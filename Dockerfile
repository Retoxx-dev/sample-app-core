FROM python:3.9-slim

COPY requirements.txt .

RUN pip install --user --no-cache-dir --upgrade -r requirements.txt

COPY app/ ./app/

WORKDIR /app

EXPOSE 80

CMD ["sh","-c","alembic upgrade head && uvicorn app:app --host 0.0.0.0 --port 80"]
