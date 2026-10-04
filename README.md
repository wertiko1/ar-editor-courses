# AR Course Editor

Веб-редактор курсов для AR-очков Epson. Позволяет создавать пошаговые инструкции с текстом, изображениями, видео и QR-верификацией.

## Возможности

- Визуальный редактор шагов с эмулятором экрана Epson (1920x1080)
- Шаблоны верстки: StandardAR, CenterFocus, MediaOnly, Custom
- Drag & drop элементов на превью
- Undo/Redo, автосохранение в localStorage
- Экспорт/импорт course.json
- Режим презентации

## Запуск

```bash
docker compose up --build
```

Редактор будет доступен на `http://localhost:8000`.

## Разработка

```bash
pip install poetry
poetry install
uvicorn backend.app.main:app --reload
```

## API

| Метод    | Путь                   | Описание          |
|----------|------------------------|--------------------|
| `GET`    | `/`                    | Редактор (HTML)    |
| `GET`    | `/api/courses`         | Список курсов      |
| `POST`   | `/api/courses`         | Создать курс       |
| `GET`    | `/api/courses/{id}`    | Получить курс      |
| `PUT`    | `/api/courses/{id}`    | Обновить курс      |
| `DELETE` | `/api/courses/{id}`    | Удалить курс       |

## Стек

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Vanilla JS (single HTML)
- **Deploy**: Docker, GitHub Actions → self-hosted runner
