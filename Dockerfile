FROM python:3.7-buster

LABEL maintainer="Çalgan Aygün <calgan.aygun@mysa.tc>"

WORKDIR /app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]