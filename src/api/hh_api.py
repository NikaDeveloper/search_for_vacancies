import requests
from typing import List, Dict
from src.api.abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API HeadHunter."""

    _BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self._connect_to_api()

    def _connect_to_api(self) -> None:
        """Подключение к API HeadHunter с проверкой доступности."""
        try:
            response = requests.get(self._BASE_URL, params={"text": "test", "per_page": 1})
            response.raise_for_status()
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API HeadHunter: {e}")

    def get_vacancies(self, search_query: str, per_page: int = 100) -> List[Dict]:
        """
        Получение вакансий с HeadHunter по ключевому слову.

        :param search_query: Ключевое слово для поиска
        :param per_page: Количество вакансий
        :return: Список вакансий
        """
        params = {
            "text": search_query,
            "per_page": per_page,
            "area": 113,  # Россия
            "only_with_salary": True,  # Только вакансии с указанной зарплатой
            "search_field": "name"  # Ищем в названии вакансии
        }

        try:
            response = requests.get(self._BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            # Добавляем логирование для отладки
            print(f"Найдено вакансий: {data.get('found', 0)}")
            print(f"Запрошено вакансий: {per_page}")

            return data.get("items", [])
        except requests.RequestException as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []
