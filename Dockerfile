# Use an official Python runtime as a parent image
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8001"]