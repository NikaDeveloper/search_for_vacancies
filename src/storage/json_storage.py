import json
from pathlib import Path
from typing import Dict, List, Optional

from src.models.vacancy import Vacancy
from src.storage.abstract_storage import AbstractStorage


class JSONStorage(AbstractStorage):
    """Класс для работы с JSON-файлом как хранилищем вакансий."""

    def __init__(self, file_name: str = "vacancies.json"):
        """
        Инициализация хранилища.

        :param file_name: Имя файла для хранения данных
        """
        self._file_name = file_name
        self._data_dir = Path("data")
        self._file_path = self._data_dir / self._file_name

        # Создаем папку data, если ее нет
        if not self._data_dir.exists():
            self._data_dir.mkdir()

        # Создаем файл, если его нет
        if not self._file_path.exists():
            with open(self._file_path, "w", encoding="utf-8") as file:
                json.dump([], file)

    def _read_vacancies(self) -> List[Dict]:
        """Чтение вакансий из файла."""
        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_vacancies(self, vacancies: List[Dict]) -> None:
        """Запись вакансий в файл."""
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в файл с проверкой дубликатов."""
        vacancies = self._read_vacancies()

        vacancy_dict = {
            "title": vacancy.title,
            "url": vacancy.url,
            "salary_from": vacancy.salary_from,
            "salary_to": vacancy.salary_to,
            "currency": vacancy.currency,
            "description": vacancy.description,
            "requirements": vacancy.requirements,
        }

        # Проверяем дубликаты по URL (так как он уникален для каждой вакансии)
        if not any(v["url"] == vacancy_dict["url"] for v in vacancies):
            vacancies.append(vacancy_dict)
            self._write_vacancies(vacancies)

    def get_vacancies(self, criteria: Optional[dict] = None) -> List[Vacancy]:
        """
        Получение вакансий по критериям.

        :param criteria: Словарь с критериями поиска
        :return: Список объектов Vacancy
        """
        vacancies_data = self._read_vacancies()
        vacancies = []

        for vacancy_data in vacancies_data:
            try:
                vacancy = Vacancy(
                    title=str(vacancy_data.get("title", "")),
                    url=str(vacancy_data.get("url", "")),
                    salary_from=vacancy_data.get("salary_from"),
                    salary_to=vacancy_data.get("salary_to"),
                    currency=vacancy_data.get("currency"),
                    description=vacancy_data.get("description"),
                    requirements=vacancy_data.get("requirements"),
                )

                if not criteria or self._vacancy_matches_criteria(vacancy, criteria):
                    vacancies.append(vacancy)
            except ValueError as e:
                print(f"Ошибка при создании вакансии: {e}")

        return vacancies

    def _vacancy_matches_criteria(self, vacancy: Vacancy, criteria: dict) -> bool:
        """Проверяет, соответствует ли вакансия критериям."""
        for key, value in criteria.items():
            if key == "keyword":
                if not (
                    value.lower() in (vacancy.description or "").lower()
                    or value.lower() in (vacancy.requirements or "").lower()
                    or value.lower() in vacancy.title.lower()
                ):
                    return False
            elif key == "salary_from":
                if not vacancy.salary_from or vacancy.salary_from < value:
                    return False
            elif key == "salary_to":
                if not vacancy.salary_to or vacancy.salary_to > value:
                    return False
        return True

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из файла."""
        vacancies = self._read_vacancies()

        vacancy_dict = {
            "title": vacancy.title,
            "url": vacancy.url,
            "salary_from": vacancy.salary_from,
            "salary_to": vacancy.salary_to,
            "currency": vacancy.currency,
            "description": vacancy.description,
            "requirements": vacancy.requirements,
        }

        if vacancy_dict in vacancies:
            vacancies.remove(vacancy_dict)
            self._write_vacancies(vacancies)
