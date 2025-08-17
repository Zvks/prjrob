FROM python:3.13-alpine
WORKDIR /app
# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY rmqsetup.py .
CMD ["python", "rmqsetup.py"]