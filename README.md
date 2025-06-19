# 🎬 extract-api (Render-ready)

## 🚀 Быстрый старт

1. Создай новый репозиторий на GitHub
2. Залей файлы из этой папки
3. Перейди в https://render.com → New → Web Service
4. Подключи GitHub, выбери этот репозиторий
5. В Render:
   - Environment: Docker
   - Port: `8000`
   - Name: `extract-api`

✅ Через минуту будет публичный URL.

## 🧪 Пример запроса

```bash
curl -X POST https://<your-app>.onrender.com/extract \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' \
  --output out.wav
```
