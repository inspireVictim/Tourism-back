# Auth API Test Guide (curl)

## 1) Запуск сервера

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Swagger: `http://localhost:8000/docs`

---

## 2) Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Ivan Ivanov",
    "email": "ivan@example.com",
    "age": 28,
    "password": "StrongPass123!"
  }'
```

## 3) Вход пользователя

```bash
curl -X POST "http://localhost:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ivan@example.com",
    "password": "StrongPass123!"
  }'
```

---

## 4) Регистрация партнера

```bash
curl -X POST "http://localhost:8000/partners/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Best Travel",
    "description": "Family and business tours",
    "website": "https://besttravel.example",
    "address": "Bishkek, Chui Ave 123",
    "rating": 4.8,
    "contact_email": "partner@example.com",
    "phone_number": "+996700123456",
    "password": "PartnerPass123!"
  }'
```

## 5) Вход партнера

```bash
curl -X POST "http://localhost:8000/partners/login" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_email": "partner@example.com",
    "password": "PartnerPass123!"
  }'
```

---

## 6) Проверка, что пароль хэшируется

SQLite база хранится в файле `sqlite3.db`.

```bash
python -c "import sqlite3; c=sqlite3.connect('sqlite3.db'); print(c.execute(\"select email, password_hash from users\").fetchall()); print(c.execute(\"select contact_email, password_hash from partners\").fetchall()); c.close()"
```

В `password_hash` должно быть значение вида:

`120000$<salt_base64>$<hash_base64>`

Пароль в открытом виде в БД не хранится.
