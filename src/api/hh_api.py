import json
from typing import Any, Dict, List, Union

import requests

from src.api.abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API HeadHunter."""

    _BASE_URL: str = "https://api.hh.ru/vacancies"

    def __init__(self) -> None:
        """Автоматически проверяет подключение при инициализации."""
        self._connect_to_api()

    def _connect_to_api(self) -> None:
        """Приватный метод для проверки подключения к API."""
        try:
            params: Dict[str, Union[str, int]] = {"text": "test", "per_page": 1}
            response = requests.get(self._BASE_URL, params=params, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка подключения к API: {e}")

    def get_vacancies(
        self, search_query: str, per_page: int = 100
    ) -> List[Dict[str, Any]]:
        """Основной метод для получения вакансий."""
        params: Dict[str, Union[str, int, bool]] = {
            "text": str(search_query),
            "per_page": int(per_page),
            "area": 113,  # Россия
            "only_with_salary": True,
        }
        try:
            response = requests.get(
                self._BASE_URL, params=params, timeout=10  # type: ignore[arg-type]
            )
            response.raise_for_status()
            return response.json().get("items", [])
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []
