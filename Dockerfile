FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Метка с датой сборки для отслеживания
LABEL build-date=$(date +%Y%m%d%H%M%S)

CMD ["python", "-m", "app.bot"]