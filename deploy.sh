# На сервере: nano ~/nihuybot/deploy.sh
#!/bin/bash
cd ~/nihuybot

echo "🔄 Остановка старых контейнеров..."
docker compose down

echo "🗑️ Удаление старого образа бота..."
docker rmi nihuybot-bot:latest 2>/dev/null || true

echo "🏗️ Сборка нового образа..."
docker compose build --no-cache bot

echo " Запуск..."
docker compose up -d

echo "✅ Готово! Логи:"
docker compose logs -f bot