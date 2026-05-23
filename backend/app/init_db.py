"""Создание таблиц и наполнение БД демонстрационными данными."""

from datetime import datetime, timedelta

from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.user import User
from app.models.news import News
from app.models.document import Document  # noqa: F401  — обеспечивает регистрацию модели


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            admin = User(
                username="admin",
                email="admin@portal.kg",
                password_hash=hash_password("admin123"),
                full_name="Администратор Системы",
                department="Администрация",
                position="Системный администратор",
                phone="+996 (555) 100-001",
                role="admin",
            )
            hr = User(
                username="hr",
                email="hr@portal.kg",
                password_hash=hash_password("hr123456"),
                full_name="Айгуль Жумабекова",
                department="Отдел кадров",
                position="HR-менеджер",
                phone="+996 (555) 100-002",
                role="hr",
            )
            employees = [
                User(
                    username="ivanov",
                    email="ivanov@portal.kg",
                    password_hash=hash_password("user1234"),
                    full_name="Иван Иванов",
                    department="Разработка",
                    position="Старший разработчик",
                    phone="+996 (555) 100-101",
                    role="employee",
                ),
                User(
                    username="petrov",
                    email="petrov@portal.kg",
                    password_hash=hash_password("user1234"),
                    full_name="Пётр Петров",
                    department="Разработка",
                    position="Frontend-разработчик",
                    phone="+996 (555) 100-102",
                    role="employee",
                ),
                User(
                    username="sidorova",
                    email="sidorova@portal.kg",
                    password_hash=hash_password("user1234"),
                    full_name="Анна Сидорова",
                    department="Бухгалтерия",
                    position="Главный бухгалтер",
                    phone="+996 (555) 100-103",
                    role="employee",
                ),
                User(
                    username="kasymov",
                    email="kasymov@portal.kg",
                    password_hash=hash_password("user1234"),
                    full_name="Бакыт Касымов",
                    department="Отдел продаж",
                    position="Менеджер по продажам",
                    phone="+996 (555) 100-104",
                    role="employee",
                ),
                User(
                    username="orozova",
                    email="orozova@portal.kg",
                    password_hash=hash_password("user1234"),
                    full_name="Назгуль Орозова",
                    department="Маркетинг",
                    position="Маркетолог-аналитик",
                    phone="+996 (555) 100-105",
                    role="employee",
                ),
            ]
            db.add_all([admin, hr, *employees])
            db.commit()
            db.refresh(admin)
            db.refresh(hr)

            news_items = [
                News(
                    title="Запуск корпоративного портала",
                    content=(
                        "Уважаемые коллеги! Сегодня в промышленную эксплуатацию вводится новый "
                        "корпоративный портал. Платформа объединяет ленту корпоративных новостей, "
                        "телефонный справочник сотрудников и единую базу регламентов компании. "
                        "Для входа используйте логин и пароль, выданные HR-службой."
                    ),
                    author_id=admin.id,
                    created_at=datetime.utcnow() - timedelta(days=3),
                ),
                News(
                    title="Обновление политики информационной безопасности",
                    content=(
                        "С 1 числа текущего месяца вступает в силу обновлённая политика "
                        "информационной безопасности. Просим всех сотрудников ознакомиться с "
                        "документом в разделе «Документы» и подтвердить его прочтение у "
                        "непосредственного руководителя."
                    ),
                    author_id=hr.id,
                    created_at=datetime.utcnow() - timedelta(days=1),
                ),
                News(
                    title="График корпоративных мероприятий на квартал",
                    content=(
                        "HR-служба подготовила сводный график обучающих семинаров, тимбилдингов "
                        "и внутренних встреч на ближайший квартал. Бланк регистрации участников "
                        "доступен в базе документов портала."
                    ),
                    author_id=hr.id,
                    created_at=datetime.utcnow(),
                ),
            ]
            db.add_all(news_items)
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("База данных инициализирована.")
