# Marketplace API Test (curl)

## 1) Зарегистрировать пользователя

```bash
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Aizada User",
    "email": "user@demo.com",
    "age": 25,
    "password": "UserPass123!"
  }'
```

## 2) Зарегистрировать партнера

```bash
curl -X POST "http://localhost:8000/partners/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nomad Travel",
    "description": "Mountain and city tours",
    "website": "https://nomad.example",
    "address": "Bishkek, Chui 77",
    "rating": 4.9,
    "contact_email": "partner@demo.com",
    "phone_number": "+996555111222",
    "password": "PartnerPass123!"
  }'
```

## 3) Создать категорию тура

```bash
curl -X POST "http://localhost:8000/categories/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Adventure",
    "description": "Rafting, hiking, jeep tours"
  }'
```

## 4) Партнер публикует тур (продажа)

```bash
curl -X POST "http://localhost:8000/marketplace/tours" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_id": 1,
    "category_id": 1,
    "title": "Ala-Kol Weekend",
    "description": "2 days trekking with guide",
    "price": 12000,
    "destination": "Karakol",
    "start_date": "2026-05-10T08:00:00",
    "end_date": "2026-05-12T20:00:00",
    "slots_available": 12
  }'
```

## 5) Партнер добавляет акцию на тур

```bash
curl -X POST "http://localhost:8000/marketplace/promotions" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_id": 1,
    "tour_id": 1,
    "discount_percent": 20,
    "expires_at": "2026-06-01T00:00:00"
  }'
```

## 6) Витрина маркетплейса

```bash
curl "http://localhost:8000/marketplace/tours"
```

Фильтры:

```bash
curl "http://localhost:8000/marketplace/tours?category_id=1"
curl "http://localhost:8000/marketplace/tours?destination=Karakol"
```

## 7) Пользователь покупает тур

```bash
curl -X POST "http://localhost:8000/marketplace/purchase" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "tour_id": 1,
    "seats": 2
  }'
```

Это создаёт запись в `payments` и уменьшает `slots_available` у тура.

## 8) История покупок пользователя

```bash
curl "http://localhost:8000/users/1/payments"
```
