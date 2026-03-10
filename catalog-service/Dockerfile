FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY catalog-service/ .

EXPOSE 8004

CMD ["python", "manage.py", "runserver", "0.0.0.0:8004"]
