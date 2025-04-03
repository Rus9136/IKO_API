#!/bin/bash

echo "Останавливаем контейнеры..."
docker-compose down

echo "Удаляем старые образы..."
docker-compose rm -f

echo "Пересобираем образы..."
docker-compose build --no-cache

echo "Запускаем приложение..."
docker-compose up -d

echo "Вывод логов..."
docker-compose logs -f app