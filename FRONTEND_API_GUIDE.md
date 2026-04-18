# NomadAI Frontend API Guide

Документ для frontend-разработчиков: какие есть эндпоинты, какие поля отправлять, что приходит в ответ и как обрабатывать ошибки.

## Base URL

- Локально: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

---

## Общие правила

- Все тела запросов: `Content-Type: application/json`
- Сейчас API без JWT (id пользователя/партнера передается в теле запроса там, где нужно).
- Даты в ISO-формате: `YYYY-MM-DDTHH:mm:ss`
- Ошибка API обычно приходит как:

```json
{
  "detail": "Текст ошибки"
}
```

---

## 1) Auth: Users

### `POST /users/register`

Регистрация пользователя.

**Request**

```json
{
  "full_name": "Aizada User",
  "email": "user@demo.com",
  "age": 25,
  "password": "UserPass123!"
}
```

**Response 200**

```json
{
  "id": 1,
  "full_name": "Aizada User",
  "email": "user@demo.com",
  "age": 25,
  "is_active": true
}
```

### `POST /users/login`

Логин пользователя.

**Request**

```json
{
  "email": "user@demo.com",
  "password": "UserPass123!"
}
```

**Response 200** — объект пользователя (аналогично register).

---

## 2) Auth: Partners

### `POST /partners/`

Регистрация партнера.

**Request**

```json
{
  "name": "Nomad Travel",
  "description": "Mountain and city tours",
  "website": "https://nomad.example",
  "address": "Bishkek, Chui 77",
  "rating": 4.9,
  "contact_email": "partner@demo.com",
  "phone_number": "+996555111222",
  "password": "PartnerPass123!"
}
```

**Response 200**

```json
{
  "id": 1,
  "name": "Nomad Travel",
  "description": "Mountain and city tours",
  "website": "https://nomad.example",
  "address": "Bishkek, Chui 77",
  "rating": 4.9,
  "contact_email": "partner@demo.com",
  "phone_number": "+996555111222",
  "is_active": true
}
```

### `POST /partners/login`

Логин партнера.

**Request**

```json
{
  "contact_email": "partner@demo.com",
  "password": "PartnerPass123!"
}
```

**Response 200** — объект партнера (аналогично register).

---

## 3) Marketplace: категории и туры

### `POST /categories/`

Создать категорию.

**Request**

```json
{
  "name": "Adventure",
  "description": "Rafting, hiking, jeep tours"
}
```

**Response 200**

```json
{
  "id": 1,
  "name": "Adventure",
  "description": "Rafting, hiking, jeep tours"
}
```

### `POST /marketplace/tours`

Партнер публикует тур (продажа).

**Request**

```json
{
  "partner_id": 1,
  "category_id": 1,
  "title": "Ala-Kol Weekend",
  "description": "2 days trekking with guide",
  "price": 12000,
  "destination": "Karakol",
  "start_date": "2026-05-10T08:00:00",
  "end_date": "2026-05-12T20:00:00",
  "slots_available": 12
}
```

**Response 200**

```json
{
  "id": 1,
  "title": "Ala-Kol Weekend",
  "description": "2 days trekking with guide",
  "price": 12000,
  "destination": "Karakol",
  "start_date": "2026-05-10T08:00:00",
  "end_date": "2026-05-12T20:00:00",
  "slots_available": 12,
  "partner_id": 1
}
```

### `POST /marketplace/promotions`

Партнер ставит акцию на свой тур.

**Request**

```json
{
  "partner_id": 1,
  "tour_id": 1,
  "discount_percent": 20,
  "expires_at": "2026-06-01T00:00:00"
}
```

**Response 200**

```json
{
  "id": 1,
  "tour_id": 1,
  "discount_percent": 20,
  "promo_price": 9600,
  "is_active": true,
  "expires_at": "2026-06-01T00:00:00"
}
```

### `GET /marketplace/tours`

Витрина маркетплейса (список туров для клиентов).

Опциональные query:
- `category_id`
- `destination`

Пример: `/marketplace/tours?category_id=1`

**Response 200**

```json
[
  {
    "id": 1,
    "title": "Ala-Kol Weekend",
    "description": "2 days trekking with guide",
    "destination": "Karakol",
    "price": 12000,
    "category": "Adventure",
    "partner_name": "Nomad Travel",
    "slots_available": 10,
    "promo_price": 9600,
    "discount_percent": 20
  }
]
```

---

## 4) Покупка тура (клиент)

### `POST /marketplace/purchase`

Покупка тура пользователем.

**Request**

```json
{
  "user_id": 1,
  "tour_id": 1,
  "seats": 2
}
```

**Response 200**

```json
{
  "id": 1,
  "user_id": 1,
  "tour_id": 1,
  "seats": 2,
  "amount": 19200,
  "status": "paid",
  "created_at": "2026-04-18T15:33:00"
}
```

### `GET /users/{user_id}/payments`

История покупок пользователя.

**Response 200**

```json
[
  {
    "id": 1,
    "user_id": 1,
    "tour_id": 1,
    "seats": 2,
    "amount": 19200,
    "status": "paid",
    "created_at": "2026-04-18T15:33:00"
  }
]
```

---

## 5) AI-консультации

### `POST /ai/consult`

Чат пользователя с ИИ-консультантом.

**Request**

```json
{
  "user_id": 1,
  "messages": [
    {
      "role": "user",
      "content": "Я хочу недорогой тур на 3 дня в горы, что посоветуешь?"
    }
  ],
  "temperature": 0.3
}
```

`role` может быть: `system`, `user`, `assistant`.

**Response 200**

```json
{
  "model": "openai/gpt-4o-mini",
  "answer": "Рекомендую рассмотреть ...",
  "provider": "openrouter"
}
```

---

## Ошибки и статусы

- `400` — невалидные бизнес-данные (например, мест не хватает, неверные даты).
- `401` — неверный логин/пароль.
- `403` — партнер пытается редактировать не свой тур.
- `404` — сущность не найдена (user/tour/partner/category).
- `409` — email уже занят.
- `422` — ошибка валидации тела запроса (не хватает поля, неверный формат email/даты).
- `500/502` — внешняя ошибка AI/OpenRouter или серверная ошибка.

---

## Пример API helper для фронта (JS/TS)

```ts
const API_URL = "http://localhost:8000";

export async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
    ...options,
  });

  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const body = await res.json();
      detail = body?.detail || detail;
    } catch {}
    throw new Error(detail);
  }

  return res.json() as Promise<T>;
}
```

---

## Что важно учесть на UI

- После покупки перезапрашивать `/marketplace/tours`, чтобы обновить `slots_available`.
- Показывать акционную цену, если есть `promo_price`, и перечеркнутую базовую `price`.
- На форме тура валидировать даты: `start_date < end_date`.
- Ошибки API показывать пользователю через `detail`.
- Для production следующий шаг — JWT/refresh-token и отказ от передачи `user_id/partner_id` в теле.
