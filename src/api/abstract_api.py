from abc import ABC, abstractmethod
from typing import Dict, List


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API платформ с вакансиями."""

    @abstractmethod
    def _connect_to_api(self) -> None:
        """Подключение к API. Должен быть реализован в дочерних классах."""
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str, per_page: int = 100) -> List[Dict]:
        """
        Получение вакансий с платформы по ключевому слову.

        :param search_query: Ключевое слово для поиска вакансий
        :param per_page: Количество вакансий на странице
        :return: Список словарей с вакансиями
        """
        pass
