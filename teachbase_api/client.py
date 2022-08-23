from functools import wraps
from typing import Optional

import requests

from teachbase_api.enums import CourseSessionStatus
from teachbase_api.exceptions import AuthError, BadRequest, TeachbaseApiException


def api_method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 400:
            raise BadRequest(response.json()["error"])
        if response.status_code == 401:
            raise AuthError()
        raise TeachbaseApiException(response.json()["error"])

    return wrapper


class HttpClient:
    def __init__(
        self,
        client_id: Optional[str] = "",
        client_secret: Optional[str] = "",
        access_token: Optional[str] = "",
        base_domain: Optional[str] = "https://go.teachbase.ru",
        api_url: str = "/endpoint/v1",
    ):
        self.session = requests.Session()
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.base_domain = base_domain
        self.base_url = f"{base_domain}{api_url}"

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value: str):
        self._access_token = value
        if self._access_token:
            self.session.headers.update(
                {"Authorization": "Bearer " + self._access_token}
            )

    def check_token(self):
        if not self.access_token:
            return False
        try:
            self._ping()
        except AuthError:
            return False
        return True

    def auth(self):
        response = self.session.post(
            f"{self.base_domain}/oauth/token",
            json={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
            },
        )
        if response.status_code != 200:
            raise AuthError()
        self.access_token = response.json()["access_token"]

    @api_method
    def _ping(self):
        return self.session.get(f"{self.base_url}/_ping")

    @api_method
    def get_courses(
        self,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        types: Optional[list[int]] = None,
    ):
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if types is not None:
            params["types"] = types
        return self.session.get(f"{self.base_url}/courses", params=params)

    @api_method
    def get_course(self, course_id: int):
        return self.session.get(f"{self.base_url}/courses/{course_id}")

    @api_method
    def create_user(self, params: dict):
        return self.session.post(f"{self.base_url}/users/create", json=params)

    @api_method
    def register_user_to_course(self, session_id: int, params: dict):
        return self.session.post(
            f"{self.base_url}/course_sessions/{session_id}/register", json=params
        )

    @api_method
    def get_course_sessions(
        self,
        course_id: int,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        filter: Optional[CourseSessionStatus] = None,
        participant_ids: Optional[list[int]] = None,
    ):
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if filter is not None:
            params["filter"] = filter
        if participant_ids is not None:
            params["participant_ids"] = participant_ids
        return self.session.get(f"{self.base_url}/courses/{course_id}/course_sessions")
