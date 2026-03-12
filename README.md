# Система межведомственного обмена сообщениями

## Описание проекта

Данный проект реализует сервис обмена транзакциями между информационными системами.  
Сервис принимает, хранит и обрабатывает сообщения, связанные с банковскими гарантиями.

Основная задача системы:

- передача сообщений между системами
- контроль целостности данных через `Hash`
- имитация цифровой подписи (`Sign`)
- хранение транзакций
- формирование ответных сообщений

Система поддерживает обмен следующими типами сообщений:

| Тип сообщения | Описание |
|---------------|----------|
| **201** | Выдача банковской гарантии |
| **202** | Подтверждение получения гарантии |
| **215** | Уведомление о результате обработки |

Все сообщения передаются в формате **Base64(JSON)**.

---

# Используемые технологии

В проекте используются следующие технологии:

- **Python 3.11+**
- **FastAPI**
- **Pydantic**
- **SQLite**
- **Uvicorn**

---

# Инструкция по установке и запуску

## 1. Клонирование проекта

```
git clone https://github.com/smile-rus1/interdepartmental_exchange_systems.git
cd project
```

## 2. Создание виртуального окружения
```
python -m venv venv
```

### Активация
#### Windows
```
venv\Scripts\activate
```

#### Linux / macOS
```
source venv/bin/activate
```

## 3. Установка зависимостей
```
pip install -r requirements.txt
```
## 3.1 Создание файла .env
```
touch .env
```
#### Пример файла .env
```
HOST=YOUR_HOST
PORT=YOUR_PORT
```

## 4. Запуск
### Можно через терминал 
```
uvicorn src.main:app --reload
```

### Можно запустить просто файл
```
python main.py
```

### После запуска сервер будет доступен по адресу:
```
http://localhost:8000
```
### Документация будет доступна по адресу:
```
http://localhost:8000/docs
```

# Примеры curl-запросов

#### Endpoint: /api/health
```
curl -X GET http://localhost:8000/api/health
```

##### Ответ
```
"OK"
```

#### Endpoint: /debug/search
#### Этот endpint нужен для теста: /api/messages/outgoing
```
curl -X GET http://localhost:8000/debug/search
```

##### Ответ
```
"eyJTdGFydERhdGUiOiAiMjAyNC0wMS0wMVQwMDowMDowMFoiLCAiRW5kRGF0ZSI6ICIyMDI1LTAxLTAxVDAwOjAwOjAwWiIsICJMaW1pdCI6IDEwLCAiT2Zmc2V0IjogMH0="
```

#### Endpoint: /api/messages/outgoing
```
curl -X 'POST' \
  'http://localhost:8000/api/messages/outgoing' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "Data": "eyJTdGFydERhdGUiOiAiMjAyNC0wMS0wMVQwMDowMDowMFoiLCAiRW5kRGF0ZSI6ICIyMDI1LTAxLTAxVDAwOjAwOjAwWiIsICJMaW1pdCI6IDEwLCAiT2Zmc2V0IjogMH0=",
  "Sign": "",
  "SignerCert": "test"
}
```

##### Ответ
```
{
  "Data": "eyJUcmFuc2FjdGlvbnMiOiBbXSwgIkNvdW50IjogMH0=",
  "Sign": "",
  "SignerCert": "U1lTVEVNX0I="
}
```

#### Endpoint: /api/messages/incoming

```
curl -X 'POST' \
  'http://localhost:8000/api/messages/incoming' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "Data": "BASE64_DATA",
  "Sign": "",
  "SignerCert": "U1lTVEVNX0E="
}'
```

##### Ответ
```
"string"
```


```
project
│
├── src
│   │
│   ├── main.py                # точка входа FastAPI
│   │
│   ├── models                 # модели данных (Pydantic)
│   │   ├── message.py
│   │   └── transaction.py
│   │
│   ├── services               # бизнес-логика
│   │   └── crypto.py
│   │
│   ├── storage                # слой хранения данных
│   │   └── sqlite_storage.py
│       └── memory_storage.py
│   │
│   ├── utils                  # вспомогательные функции
│   │   ├── base64_utils.py
│   │   └── hash_utils.py
│   │
│   └── api                    # API маршруты
│       └── messages.py
│
├── test                       # тестовые скрипты
│
├── README.md
├── .env.example               # пример файла с переменными окружения
└── requirements.txt           # зависимости
```