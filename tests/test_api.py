from unittest.mock import Mock, patch

import pytest
import requests

from src.api.hh_api import HeadHunterAPI


@patch("src.api.hh_api.requests.get")
def test_get_vacancies_success(mock_get):
    """Тест успешного получения вакансий."""
    # Мокаем ответ для _connect_to_api
    mock_connect_response = Mock()
    mock_connect_response.raise_for_status.return_value = None
    mock_connect_response.json.return_value = {"items": []}

    # Мокаем ответ для get_vacancies
    mock_vacancies_response = Mock()
    mock_vacancies_response.json.return_value = {
        "items": [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "description": "Описание",
                "snippet": {"requirement": "Требования"},
            }
        ],
        "found": 1,
    }
    mock_vacancies_response.raise_for_status.return_value = None

    # Настраиваем mock_get возвращать разные ответы для разных вызовов
    mock_get.side_effect = [mock_connect_response, mock_vacancies_response]

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("Python")

    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Python Developer"
    assert mock_get.call_count == 2


@patch("src.api.hh_api.requests.get")
def test_get_vacancies_failure(mock_get):
    """Тест обработки ошибки при запросе."""
    # Мокаем ответы для обоих вызовов requests.get
    mock_response_success = Mock()
    mock_response_success.raise_for_status.return_value = None
    mock_response_success.json.return_value = {"items": []}

    # Для второго вызова делаем так, чтобы raise_for_status вызывал исключение
    mock_response_error = Mock()
    mock_response_error.raise_for_status.side_effect = requests.RequestException(
        "API Error"
    )

    mock_get.side_effect = [mock_response_success, mock_response_error]

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("Python")

    assert vacancies == []
    assert mock_get.call_count == 2


@patch("src.api.hh_api.requests.get")
def test_connect_to_api_success(mock_get):
    """Тест успешного подключения к API."""
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"items": []}

    mock_get.side_effect = [mock_response, mock_response]

    hh_api = HeadHunterAPI()
    # Теперь просто проверяем, что метод выполняется без исключений
    hh_api._connect_to_api()  # Возвращает None, но мы проверяем вызовы

    assert mock_get.call_count == 2
    mock_get.assert_called_with(
        hh_api._BASE_URL, params={"text": "test", "per_page": 1}, timeout=5
    )


@patch("src.api.hh_api.requests.get")
def test_connect_to_api_failure(mock_get):
    """Тест неудачного подключения к API."""
    mock_get.side_effect = requests.RequestException("Connection error")

    hh_api = HeadHunterAPI()
    # Проверяем, что исключение обрабатывается внутри метода
    hh_api._connect_to_api()
