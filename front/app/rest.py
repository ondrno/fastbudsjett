from typing import Optional, Union
import requests


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
        tokens = r.json()

        if r.ok:
            a_token = tokens['access_token']
            self.auth_token = {"Authorization": f"Bearer {a_token}"}
        else:
            detail = tokens.get('detail')
            raise ApiLoginError(f"{detail}")

        return self.auth_token

    def get_user(self, id: Union[int, str]) -> dict:
        url = self.BASE_USERS_URL
        r = requests.get(f"{url}/{id}", headers=self.auth_token)
        if r.status_code == 200:
            api_user = r.json()
            return api_user
        else:
            raise ApiException(f"Could not find user with id={id}")

    def whoami(self) -> dict:
        url = self.BASE_USERS_URL + "/me"
        r = requests.get(url, headers=self.auth_token)
        if r.status_code == 200:
            api_user = r.json()
            return api_user
        else:
            raise ApiException(f"I do not know who I am.")

    def add_user(self, user_name: str, email: str, password: str):
        data = {"user": user_name, "email": email, "password": password}
        r = requests.put(self.BASE_USERS_URL, headers=self.auth_token, json=data)
        if r.ok:
            api_user = r.json()
            return api_user
        else:
            raise ApiException(f"Could not add user, {r.content}")

    def get_items(self):
        data = [{
            "description": "Coop: butter, milk, yoghurt",
            "amount": 10.25,
            "date": "2020-11-28",
            "category_id": 2,
            "payment_id": 2,
            "id": 1,
            "owner_id": 0
        },
        {
            "description": "Amazon: Samsung TV 53inch",
            "amount": 499.99,
            "date": "2020-11-29",
            "category_id": 1,
            "payment_id": 1,
            "id": 2,
            "owner_id": 0
        },
        {
            "description": "Amazon: Apple iPhone 12",
            "amount": 1100.00,
            "date": "2020-11-30",
            "category_id": 1,
            "payment_id": 1,
            "id": 3,
            "owner_id": 0
        },
        {
            "description": "Porsche Stuttgart: Cayenne Turbo S E-Hybrid III, Cayenne Turbo Design 21inch Platinum wheels, white metallic, 462hp, hybrid engine",
            "amount": 99543.00,
            "date": "2020-12-01",
            "category_id": 3,
            "payment_id": 3,
            "id": 3,
            "owner_id": 0
        }
        ]
        return data
        r = requests.get(self.BASE_ITEMS_URL, headers=self.auth_token)
        if r.ok:
            items = r.json()
            return items
        else:
            raise ApiException(f"Could not retrieve items, {r.content}")

    def get_categories(self):
        data = [{'id': 1, 'name': 'household'}, {'id': 2, 'name': 'food'}, {'id': 3, 'name': 'car'}]
        return data
        r = requests.get(self.BASE_CATEGORIES_URL, headers=self.auth_token)
        if r.ok:
            categories = r.json()
            return categories
        else:
            raise ApiException(f"Could not retrieve categories, {r.content}")

    def get_payments(self):
        data = [{'id': 1, 'name': 'cash'}, {'id': 2, 'name': 'debit'}, {'id': 3, 'name': 'transfer'}]
        return data
        r = requests.get(self.BASE_PAYMENTS_URL, headers=self.auth_token)
        if r.ok:
            payments = r.json()
            return payments
        else:
            raise ApiException(f"Could not retrieve payment types, {r.content}")


class ApiException(Exception):
    pass


class ApiConnectionError(Exception):
    pass


class ApiLoginError(Exception):
    pass


iface = RestApiInterface()
