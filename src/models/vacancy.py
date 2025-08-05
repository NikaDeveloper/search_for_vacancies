from typing import Any, Dict, List, Optional


class Vacancy:
    """Класс для представления вакансии."""

    __slots__ = [
        "_title",
        "_url",
        "_salary_from",
        "_salary_to",
        "_currency",
        "_description",
        "_requirements",
    ]

    def __init__(
        self,
        title: str,
        url: str,
        salary_from: Optional[int] = None,
        salary_to: Optional[int] = None,
        currency: Optional[str] = None,
        description: Optional[str] = None,
        requirements: Optional[str] = None,
    ):
        self._title = title
        self._url = url
        self._salary_from = salary_from
        self._salary_to = salary_to
        self._currency = (
            currency.lower() if currency else None
        )  # Приводим к нижнему регистру
        self._description = description
        self._requirements = requirements
        self._validate_data()

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary_from(self) -> Optional[int]:
        return self._salary_from

    @property
    def salary_to(self) -> Optional[int]:
        return self._salary_to

    @property
    def currency(self) -> Optional[str]:
        return self._currency

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def requirements(self) -> Optional[str]:
        return self._requirements

    def _validate_data(self) -> None:
        """Приватный метод для валидации данных."""
        if not isinstance(self._title, str) or not self._title:
            raise ValueError("Название вакансии должно быть непустой строкой")

        if not isinstance(self._url, str) or not self._url.startswith(
            ("http://", "https://")
        ):
            raise ValueError(
                "URL вакансии должен быть валидной ссылкой (начинаться с http:// или https://)"
            )

        self._salary_from = self._validate_salary(self._salary_from)
        self._salary_to = self._validate_salary(self._salary_to)

        if (
            self._salary_to
            and self._salary_from
            and self._salary_to < self._salary_from
        ):
            self._salary_from, self._salary_to = self._salary_to, self._salary_from

    @staticmethod
    def _validate_salary(salary: Any) -> int:
        """Валидация зарплаты."""
        if salary is None:
            return 0
        try:
            return int(salary)
        except (ValueError, TypeError):
            return 0

    def __lt__(self, other: "Vacancy") -> bool:
        """Сравнение вакансий по зарплате (для сортировки)."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return (self._salary_from or 0) < (other._salary_from or 0)

    def __eq__(self, other: object) -> bool:
        """Проверка на равенство вакансий."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return (
            self._title == other._title
            and self._url == other._url
            and self._salary_from == other._salary_from
            and self._salary_to == other._salary_to
            and self._currency == other._currency
        )

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict]) -> List["Vacancy"]:
        """
        Преобразование списка словарей с вакансиями в список объектов Vacancy.
        """
        vacancies = []
        for vacancy_data in vacancies_data:
            try:
                salary_data = vacancy_data.get("salary")
                if salary_data:
                    salary_from = salary_data.get("from")
                    salary_to = salary_data.get("to")
                    currency = salary_data.get("currency")
                else:
                    salary_from = salary_to = currency = None

                # Преобразуем RUR в RUB для единообразия
                if currency and currency.upper() == "RUR":
                    currency = "RUB"

                vacancy = cls(
                    title=vacancy_data.get("name", ""),
                    url=vacancy_data.get("alternate_url", ""),
                    salary_from=salary_from,
                    salary_to=salary_to,
                    currency=currency,
                    description=vacancy_data.get("description"),
                    requirements=vacancy_data.get("snippet", {}).get("requirement"),
                )
                vacancies.append(vacancy)
            except (ValueError, KeyError) as e:
                print(f"Ошибка при создании вакансии: {e}")
        return vacancies

    def __str__(self) -> str:
        """Строковое представление вакансии."""
        salary_info = "не указана"
        if self._salary_from or self._salary_to:
            salary_parts = []
            if self._salary_from:
                salary_parts.append(f"от {self._salary_from}")
            if self._salary_to:
                salary_parts.append(f"до {self._salary_to}")
            salary_info = " ".join(salary_parts)
            if self._currency and self._currency.lower() in ["rur", "rub"]:
                salary_info += " RUR"
            elif self._currency:
                salary_info += f" {self._currency}"

        return (
            f"Вакансия: {self._title}\n"
            f"Ссылка: {self._url}\n"
            f"Зарплата: {salary_info}\n"
            f"Требования: {self._requirements or 'не указаны'}\n"
            f"Описание: {self._description or 'не указано'}\n"
        )
