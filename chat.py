import sys
import anthropic
import os

# Проверка наличия аргумента (сообщения)
if len(sys.argv) < 2:
    print("❌ Напиши сообщение для Claude. Пример: python chat.py 'Привет, как дела?'")
    sys.exit(1)

# Сообщение от пользователя
user_input = sys.argv[1]

# Инициализация клиента (ключ должен быть установлен через переменную окружения)
client = anthropic.Anthropic()

# Отправка сообщения
response = client.messages.create(
    model="claude-3-opus-20240229",  # Можно заменить на haiku или sonnet
    max_tokens=1000,
    temperature=0.7,
    messages=[
        {"role": "user", "content": user_input}
    ]
)

# Вывод ответа
print("\n🤖 Ответ Claude:\n")
print(response.content[0].text)
