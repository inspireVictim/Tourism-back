# AI Consultation (OpenRouter) - curl tests

## 1) Подготовка `.env`

Скопируй `.env.example` в `.env` и заполни `OPENROUTER_API_KEY`.

## 2) Запуск сервера

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 3) Базовый запрос на консультацию

```bash
curl -X POST "http://localhost:8000/ai/consult" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "messages": [
      {
        "role": "user",
        "content": "Я хочу недорогой тур на 3 дня в горы, что посоветуешь?"
      }
    ]
  }'
```

## 4) Запрос с явным выбором модели

```bash
curl -X POST "http://localhost:8000/ai/consult" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-4o-mini",
    "temperature": 0.2,
    "messages": [
      {"role": "system", "content": "Отвечай кратко и по делу."},
      {"role": "user", "content": "Сравни Каракол и Сон-Куль для семейного тура."}
    ]
  }'
```
