"""
Тестовый скрипт для проверки маршрутов Flask приложения без запуска сервера.
"""

from app import create_app

# Создаем тестовое приложение
app = create_app()

# Выводим все зарегистрированные маршруты
print("===== ЗАРЕГИСТРИРОВАННЫЕ МАРШРУТЫ =====")
for rule in sorted(app.url_map.iter_rules(), key=lambda x: str(x)):
    print(f"{rule.rule} -> {rule.endpoint}")

# Проверка наличия конкретного маршрута
bulk_create_route = [r for r in app.url_map.iter_rules() if '/api/v1/documents/bulk-create' in str(r)]
if bulk_create_route:
    print("\n===== МАРШРУТ BULK-CREATE НАЙДЕН =====")
    for route in bulk_create_route:
        print(f"{route.rule} -> {route.endpoint}")
else:
    print("\n===== МАРШРУТ BULK-CREATE НЕ НАЙДЕН =====")
    
# Проверка правильности очередности объявления маршрутов
print("\n===== ПРОВЕРКА ОЧЕРЕДНОСТИ МАРШРУТОВ =====")
document_routes = [r for r in app.url_map.iter_rules() if '/api/v1/documents' in str(r)]
for i, route in enumerate(document_routes):
    print(f"{i+1}. {route.rule} -> {route.endpoint}")