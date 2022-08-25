import pytest

from teachbase_api.exceptions import TeachbaseApiException


def test_get_courses(client):
    courses = client.get_courses()
    assert len(courses) > 0


def test_get_course(client, existent_course_id):
    course = client.get_course(existent_course_id)
    assert course["id"] == existent_course_id

    with pytest.raises(TeachbaseApiException):
        client.get_course(1)  # not existent course


def test_create_user(client):
    params = {
        "users": [
            {
                "email": "test@teachbase.ru",
                "name": "John",
                "description": "Corrupti natus quia recusandae.",
                "last_name": "Doe",
                "phone": None,
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
    users = client.create_user(params)
    assert len(users) == 1
    assert "id" in users[0]


def test_get_course_sessions(client, existent_course_id):
    sessions = client.get_course_sessions(existent_course_id)
    assert sessions is not None
