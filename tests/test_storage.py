import json

from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage


def test_add_vacancy(storage):
    """Тест добавления вакансии."""
    vacancy = Vacancy(title="Python Developer", url="https://hh.ru/vacancy/123")

    storage.add_vacancy(vacancy)
    vacancies = storage.get_vacancies()

    assert len(vacancies) == 1
    assert vacancies[0].title == "Python Developer"


def test_add_duplicate_vacancy(storage):
    """Тест добавления дублирующейся вакансии."""
    vacancy = Vacancy(title="Python Developer", url="https://hh.ru/vacancy/123")

    storage.add_vacancy(vacancy)
    storage.add_vacancy(vacancy)  # Дубликат
    vacancies = storage.get_vacancies()

    assert len(vacancies) == 1


def test_delete_vacancy(storage):
    """Тест удаления вакансии."""
    vacancy = Vacancy(title="Python Developer", url="https://hh.ru/vacancy/123")

    storage.add_vacancy(vacancy)
    storage.delete_vacancy(vacancy)
    vacancies = storage.get_vacancies()

    assert len(vacancies) == 0


def test_get_vacancies_with_criteria(storage):
    """Тест фильтрации вакансий по критериям."""
    vacancy1 = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/1",
        salary_from=100000,
        description="Python разработчик",
    )
    vacancy2 = Vacancy(
        title="Java Developer",
        url="https://hh.ru/vacancy/2",
        salary_from=150000,
        description="Java разработчик",
    )

    storage.add_vacancy(vacancy1)
    storage.add_vacancy(vacancy2)

    # Фильтр по ключевому слову
    python_vacancies = storage.get_vacancies({"keyword": "Python"})
    assert len(python_vacancies) == 1
    assert python_vacancies[0].title == "Python Developer"

    # Фильтр по зарплате
    high_salary_vacancies = storage.get_vacancies({"salary_from": 120000})
    assert len(high_salary_vacancies) == 1
    assert high_salary_vacancies[0].title == "Java Developer"


def test_file_creation(tmp_path):
    """Тест создания файла при инициализации."""
    test_file = tmp_path / "new_vacancies.json"
    assert not test_file.exists()

    JSONStorage(file_name=str(test_file))
    assert test_file.exists()

    with open(test_file, "r") as f:
        content = json.load(f)
        assert content == []
