FROM python:3.13-alpine
WORKDIR /app
# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY tradingrobot1.py .
CMD ["python", "tradingrobot1.py"]