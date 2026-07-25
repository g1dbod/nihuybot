#!/bin/bash
cd ~/nihuybot

# Проверка что контейнер запущен
if ! docker compose ps | grep -q "Up"; then
    echo "⚠️ Бот не работает! Перезапускаем..."
    docker compose restart bot
    # Отправка уведомления (можно добавить Telegram webhook)
fi