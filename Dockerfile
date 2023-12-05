FROM python:3.10.12-slim

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "5000"]
