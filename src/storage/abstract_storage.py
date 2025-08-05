from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.vacancy import Vacancy


class AbstractStorage(ABC):
    """Абстрактный класс для работы с хранилищем вакансий."""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в хранилище."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[dict] = None) -> List[Vacancy]:
        """Получение вакансий по критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из хранилища."""
        pass
