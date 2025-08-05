from unittest.mock import Mock, patch

from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage
from src.utils.filters import filter_vacancies, sort_vacancies


@patch("src.api.hh_api.requests.get")
def test_integration_flow(mock_get, tmp_path):
    """Интеграционный тест всего потока работы."""
    # Мокаем ответ API
    mock_response = Mock()
    mock_response.json.return_value = {
        "items": [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/1",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "description": "Python разработчик",
                "snippet": {"requirement": "Опыт работы с Django"},
            },
            {
                "name": "Java Developer",
                "alternate_url": "https://hh.ru/vacancy/2",
                "salary": {"from": 120000, "to": None, "currency": "RUR"},
                "description": "Java разработчик",
                "snippet": {"requirement": "Опыт работы с Spring"},
            },
        ],
        "found": 2,
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Инициализация компонентов
    hh_api = HeadHunterAPI()
    storage = JSONStorage(file_name=str(tmp_path / "test_vacancies.json"))

    # Получаем вакансии
    vacancies_data = hh_api.get_vacancies("Developer")
    vacancies = Vacancy.cast_to_object_list(vacancies_data)

    # Сохраняем
    for vacancy in vacancies:
        storage.add_vacancy(vacancy)

    # Получаем из хранилища
    saved_vacancies = storage.get_vacancies()
    assert len(saved_vacancies) == 2

    # Фильтруем и сортируем
    filtered = filter_vacancies(saved_vacancies, ["Python"])
    assert len(filtered) == 1

    sorted_vacancies = sort_vacancies(saved_vacancies)
    assert sorted_vacancies[0].title == "Java Developer"
    assert sorted_vacancies[1].title == "Python Developer"
