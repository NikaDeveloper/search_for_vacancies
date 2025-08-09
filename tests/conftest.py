from unittest.mock import patch

import pytest

from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage


@pytest.fixture
def sample_vacancy():
    from src.models.vacancy import Vacancy

    return Vacancy(
        title="Test Vacancy",
        url="https://hh.ru/vacancy/123",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
    )


@pytest.fixture
def sample_vacancies():
    """Фикстура с тестовыми вакансиями."""
    return [
        Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/1",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы с Django",
        ),
        Vacancy(
            title="Java Developer",
            url="https://hh.ru/vacancy/2",
            salary_from=120000,
            salary_to=180000,
            currency="RUR",
            description="Разработка на Java",
            requirements="Опыт работы с Spring",
        ),
        Vacancy(
            title="JavaScript Developer",
            url="https://hh.ru/vacancy/3",
            salary_from=90000,
            salary_to=120000,
            currency="USD",
            description="Разработка на JavaScript",
            requirements="Опыт работы с React",
        ),
        Vacancy(
            title="DevOps Engineer",
            url="https://hh.ru/vacancy/4",
            description="Настройка инфраструктуры",
            requirements="Опыт работы с Docker",
        ),
    ]


@pytest.fixture
def storage(tmp_path):
    """Фикстура для создания временного хранилища."""
    test_file = tmp_path / "test_vacancies.json"
    return JSONStorage(file_name=str(test_file))


@pytest.fixture
def mock_hh_api():
    with patch("requests.get") as mock_get:
        yield mock_get
