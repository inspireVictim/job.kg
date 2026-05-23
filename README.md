# Корпоративный портал с системой авторизации

Дипломный проект: веб-приложение для внутренних коммуникаций предприятия с разграничением прав доступа на основе ролей.

## Технологический стек

- **Бэкенд:** Python 3.10+ / FastAPI / SQLAlchemy 2.0
- **БД:** SQLite, файл `backend/portal.db`
- **Авторизация:** JSON Web Token + bcrypt
- **Фронтенд:** HTML5 / CSS3 / Vanilla JavaScript

## Структура проекта

```text
job.kg/
├── backend/                     # FastAPI-приложение
│   ├── app/
│   │   ├── api/                 # Маршруты: auth, users, news, documents
│   │   ├── core/                # config, security, database
│   │   ├── models/              # SQLAlchemy-модели
│   │   ├── schemas/             # Pydantic-схемы
│   │   ├── init_db.py           # Создание таблиц и тестовых данных
│   │   └── main.py              # Точка входа FastAPI
│   ├── uploads/                 # Загруженные документы
│   ├── portal.db                # SQLite-файл
│   └── requirements.txt
├── frontend/
│   ├── css/styles.css
│   ├── js/api.js, layout.js
│   └── pages/                   # login, index, employees, documents, profile
├── generate_pz.py
└── ПЗ_Корпоративный_Портал.docx
```

## Запуск

### 1. Создание виртуального окружения

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
```

### 2. Запуск сервера

```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

При первом запуске автоматически создается база данных и наполняется тестовыми данными.

### 3. Открытие портала

- **Главная страница / вход:** http://127.0.0.1:8000/
- **Документация API (Swagger):** http://127.0.0.1:8000/docs
- **Альтернативная документация (ReDoc):** http://127.0.0.1:8000/redoc

### Демонстрационные учетные записи

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

Скрипт автоматически установит `python-docx`, если она еще не установлена, и создаст файл `ПЗ_Корпоративный_Портал.docx` в корне проекта.

## Администрирование БД

База `backend/portal.db` открывается универсальным клиентом **DBeaver**:
*Database -> New Connection -> SQLite -> Path: backend/portal.db*.
