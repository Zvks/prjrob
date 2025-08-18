FROM python:3.13-alpine
WORKDIR /app
# Копируем и устанавливаем зависимости
COPY requirements.txt readme.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY rmqsetup.py .
# Настройка проверки здоровья
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
CMD ["python", "rmqsetup.py"]