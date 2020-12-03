from typing import Union
import requests


class User:
    def __init__(self, email: str, user_id: int, auth_token: str, is_active: bool = True, is_superuser: bool = False):
        self._email = email
        self._user_id = user_id
        self._auth_token = auth_token
        self._is_active = is_active
        self._is_superuser = is_superuser
        self._is_anonymous = False

    @property
    def is_authenticated(self):
        return self._auth_token is not None

    @is_authenticated.setter
    def is_authenticated(self, token):
        self._auth_token = token

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    @property
    def is_anonymous(self):
        return self._is_anonymous

    @is_anonymous.setter
    def is_anonymous(self, value):
        self._is_anonymous = value

    @property
    def is_superuser(self):
        return self._is_superuser

    @is_superuser.setter
    def is_superuser(self, value):
        self._is_superuser = value

    def get_id(self):
        return self._email


class RestApiInterface:
    BASE_URL = "http://localhost/api/v1"
    BASE_USERS_URL = BASE_URL + '/users'
    BASE_ITEMS_URL = BASE_URL + '/items'
    BASE_CATEGORIES_URL = BASE_URL + '/categories/'
    BASE_PAYMENTS_URL = BASE_URL + '/payments/'

    def __init__(self):
        self.auth_token = None

    def login(self, username: str, password: str):
        login_data = {"username": username, "password": password}
        try:
            r = requests.post(f"{self.BASE_URL}/login/access-token", data=login_data)
        except requests.exceptions.ConnectionError as e:
            raise ApiConnectionError(e)

        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ApiLoginError(e)

        tokens = r.json()

        if r.ok:
            a_token = tokens['access_token']
            self.auth_token = {"Authorization": f"Bearer {a_token}"}
        else:
            detail = tokens.get('detail')
            raise ApiLoginError(f"{detail}")

        return self.auth_token

    def get_user(self, id: Union[int, str]) -> User:
        url = self.BASE_USERS_URL
        r = requests.get(f"{url}/{id}", headers=self.auth_token)
        if r.status_code == 200:
            api_user = r.json()
            return User(api_user['email'], api_user['id'], self.auth_token,
                        api_user['is_active'], api_user['is_superuser'])
        else:
            raise ApiException(f"Could not find user with id={id}")

    def whoami(self) -> User:
        url = self.BASE_USERS_URL + "/me"
        r = requests.get(url, headers=self.auth_token)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ApiException(e)

        api_user = r.json()
        return User(api_user['email'], api_user['id'], self.auth_token,
                    api_user['is_active'], api_user['is_superuser'])

    def add_user(self, user_name: str, email: str, password: str) -> User:
        data = {"user": user_name, "email": email, "password": password}
        r = requests.put(self.BASE_USERS_URL, headers=self.auth_token, json=data)
        if r.ok:
            api_user = r.json()
            return User(api_user['email'], api_user['id'], self.auth_token,
                        api_user['is_active'], api_user['is_superuser'])
        else:
            raise ApiException(f"Could not add user, {r.content}")

    def get_items(self, **data):
        r = requests.get(self.BASE_ITEMS_URL, headers=self.auth_token, params=data)
        if r.ok:
            items = r.json()
            return items
        else:
            raise ApiException(f"Could not retrieve items, {r.content}")

    def get_categories(self):
        r = requests.get(self.BASE_CATEGORIES_URL, headers=self.auth_token)
        if r.ok:
            categories = r.json()
            return categories
        else:
            raise ApiException(f"Could not retrieve categories, {r.content}")

    def get_payments(self):
        r = requests.get(self.BASE_PAYMENTS_URL, headers=self.auth_token)
        if r.ok:
            payments = r.json()
            return payments
        else:
            raise ApiException(f"Could not retrieve payment types, {r.content}")

    def create_item(self, data: dict):
        r = requests.post(self.BASE_ITEMS_URL, headers=self.auth_token, json=data)
        if r.ok:
            item = r.json()
            return item
        else:
            raise ApiException(f"Could not create item={data} -> {r.content}")


class ApiException(Exception):
    pass


class ApiConnectionError(Exception):
    pass


class ApiLoginError(Exception):
    pass


iface = RestApiInterface()
