FROM python:3.10-slim

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "viewer.py"]
