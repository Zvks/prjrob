FROM python:3.13-alpine
WORKDIR /app
# Копируем и устанавливаем зависимости
COPY requirements.txt readme.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY rmqdbstoredata.py .
CMD ["python", "rmqdbstoredata.py"]