import sys

from teachbase_api import HttpClient


def create_user(client: HttpClient):
    params = {
        "users": [
            {
                "email": "test@teachbase.ru",
                "name": "John",
                "description": "Corrupti natus quia recusandae.",
                "last_name": "Doe",
                "phone": 792177788666,
                "role_id": 1,
                "auth_type": 0,
                "external_id": "u-007",
                "labels": {"1": "2", "3": "4"},
                "password": "qwerty",
                "lang": "ru",
            }
        ],
        "options": {
            "activate": True,
            "verify_emails": True,
            "skip_notify_new_users": True,
            "skip_notify_active_users": True,
        },
        "external_labels": True,
    }
    return client.create_user(params)


def get_courses(client: HttpClient):
    return client.get_courses()


def get_course_sessions(client: HttpClient, course_id: int):
    return client.get_course_sessions(course_id)


def register_user_to_session(client: HttpClient, session_id: int, params: dict):
    return client.register_user_to_course(session_id, params)


def main(access_token: str):
    client = HttpClient(access_token=access_token)
    print("Создание пользователя")
    user = create_user(client)[0]
    print("Пользователь создан:")
    print(user)
    print()

    print("Получение списка курсов")
    courses = get_courses(client)
    print("Курсы:")
    for course in courses:
        print(course)
    print()

    print("Получение списка сессий курса")
    all_sessions = []
    for course in courses:
        sessions = get_course_sessions(client, course["id"])
        print(f"Сессии курса id={course['id']}:")
        print(sessions)
        print()
        all_sessions.extend(sessions)

    session_for_register = all_sessions[0]
    print(f"Записываем пользователя на сессию id={session_for_register['id']}")
    register_user_to_session(
        client,
        session_for_register["id"],
        {"user_id": user["id"], "email": user["email"], "phone": user["phone"]},
    )
    print("Пользователь записан")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Необходимо передать access_token первым аргументом")
        sys.exit(1)
    token = sys.argv[1]
    main(token)
