from DAL.classes.repository import Repository
import requests


class ApiRepository(Repository):
    def __init__(self, base_url):
        self.base_url = base_url

    def get_all(self):
        response = requests.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def get_by_id(self, entity_id):
        response = requests.get(f"{self.base_url}/{entity_id}")
        response.raise_for_status()
        return response.json()

    def add(self, data):
        response = requests.post(self.base_url, json=data)
        response.raise_for_status()
        return response.json()

    def update(self, entity_id, data):
        response = requests.patch(f"{self.base_url}/{entity_id}", json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, entity_id):
        response = requests.delete(f"{self.base_url}/{entity_id}")
        response.raise_for_status()
        return response.ok