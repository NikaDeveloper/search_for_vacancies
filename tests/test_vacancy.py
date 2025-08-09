import pytest

from src.models.vacancy import Vacancy


def test_vacancy_creation():
    """Тест создания вакансии с корректными данными."""
    vacancy = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
        description="Разработка на Python",
        requirements="Опыт работы 3+ года",
    )

    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.currency == "rur"
    assert vacancy.description == "Разработка на Python"
    assert vacancy.requirements == "Опыт работы 3+ года"


def test_vacancy_without_salary():
    """Тест создания вакансии без зарплаты."""
    vacancy = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        description="Разработка на Python",
    )

    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0
    assert vacancy.currency is None


def test_vacancy_validation():
    """Тест валидации данных вакансии."""
    with pytest.raises(ValueError):
        Vacancy(title="", url="https://hh.ru/vacancy/123")

    with pytest.raises(ValueError):
        Vacancy(title="Python", url="invalid_url")


def test_vacancy_comparison():
    """Тест сравнения вакансий по зарплате."""
    vacancy1 = Vacancy(title="A", url="https://hh.ru/vacancy/1", salary_from=100000)
    vacancy2 = Vacancy(
        title="A",  # То же название
        url="https://hh.ru/vacancy/1",  # Тот же URL
        salary_from=150000,
    )
    vacancy3 = Vacancy(title="A", url="https://hh.ru/vacancy/1", salary_from=100000)

    assert vacancy1 < vacancy2
    assert not vacancy2 < vacancy1
    assert vacancy1 == vacancy3


def test_cast_to_object_list():
    """Тест преобразования данных API в список объектов Vacancy."""
    api_data = [
        {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/123",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "description": "Описание",
            "snippet": {"requirement": "Требования"},
        }
    ]

    vacancies = Vacancy.cast_to_object_list(api_data)
    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Developer"


def test_str_representation():
    """Тест строкового представления вакансии."""
    vacancy = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
    )

    assert "Python Developer" in str(vacancy)
    assert "100000" in str(vacancy)
    assert "RUR" in str(vacancy)
