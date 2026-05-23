# Корпоративный портал с системой авторизации

Дипломный проект. Веб-приложение для внутренних коммуникаций предприятия
с разграничением прав доступа на основе ролевой модели.

## Технологический стек

- **Бэкенд:** Python 3.9+ / FastAPI / SQLAlchemy 2.0
- **БД:** SQLite (файл `backend/portal.db`)
- **Авторизация:** JSON Web Token + bcrypt
- **Фронтенд:** HTML5 / CSS3 / Vanilla JavaScript (Fetch API)

## Структура проекта

```
job.kg/
├── backend/                     # FastAPI приложение
│   ├── app/
│   │   ├── api/                 # Маршруты: auth, users, news, documents
│   │   ├── core/                # config, security, database
│   │   ├── models/              # SQLAlchemy-модели
│   │   ├── schemas/             # Pydantic-схемы
│   │   ├── init_db.py           # Создание таблиц и тестовых данных
│   │   └── main.py              # Точка входа FastAPI
│   ├── uploads/                 # Загруженные документы
│   ├── portal.db                # SQLite-файл (создаётся автоматически)
│   └── requirements.txt
├── frontend/
│   ├── css/styles.css           # Корпоративная стилистика
│   ├── js/api.js, layout.js     # HTTP-клиент и общий каркас
│   └── pages/                   # login.html, index.html, employees.html,
│                                # documents.html, profile.html
├── generate_pz.py               # Скрипт генерации ПЗ.docx по ГОСТ
└── ПЗ_Корпоративный_Портал.docx # Пояснительная записка
```

## Запуск

### 1. Установка зависимостей

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Запуск сервера

```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

При первом запуске автоматически создаётся БД и наполняется тестовыми данными.

### 3. Открытие портала

- **Главная страница / вход:** http://127.0.0.1:8000/
- **Документация API (Swagger):** http://127.0.0.1:8000/docs
- **Альтернативная док-я (ReDoc):** http://127.0.0.1:8000/redoc

### Демонстрационные учётные записи

| Логин    | Пароль     | Роль          |
|----------|------------|---------------|
| `admin`  | `admin123` | Администратор |
| `hr`     | `hr123456` | HR-менеджер   |
| `ivanov` | `user1234` | Сотрудник     |
| `petrov` | `user1234` | Сотрудник     |

## Генерация ПЗ.docx

```bash
python generate_pz.py
```

Скрипт автоматически установит `python-docx`, если она ещё не установлена, и
создаст файл `ПЗ_Корпоративный_Портал.docx` в корне проекта, оформленный по
ГОСТ КР: Times New Roman 14, межстрочный интервал 1.5, абзацный отступ 1.25 см.

## Администрирование БД

База `backend/portal.db` открывается универсальным клиентом **DBeaver**:
*Database → New Connection → SQLite → Path: backend/portal.db*.
