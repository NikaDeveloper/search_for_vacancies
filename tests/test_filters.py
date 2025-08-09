from src.utils.filters import (
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
)


def test_filter_vacancies(sample_vacancies):
    """Тест фильтрации по ключевым словам."""
    # Фильтр по одному слову
    filtered = filter_vacancies(sample_vacancies, ["Python"])
    assert len(filtered) == 1
    assert filtered[0].title == "Python Developer"

    # Фильтр по нескольким словам
    filtered = filter_vacancies(sample_vacancies, ["опыт", "Django"])
    assert len(filtered) == 1
    assert filtered[0].title == "Python Developer"

    # Без фильтра
    filtered = filter_vacancies(sample_vacancies, [])
    assert len(filtered) == len(sample_vacancies)


def test_get_vacancies_by_salary(sample_vacancies):
    """Тест фильтрации по зарплате."""
    # Фильтр по диапазону
    filtered = get_vacancies_by_salary(sample_vacancies, "100000-150000")
    assert len(filtered) == 2  # Python и Java разработчики

    # Проверка валюты (USD не должен попасть в результаты)
    for vacancy in filtered:
        assert vacancy.currency in ["rur", "rub"]

    # Без фильтра
    filtered = get_vacancies_by_salary(sample_vacancies, "")
    assert len(filtered) == len(sample_vacancies)


def test_sort_vacancies(sample_vacancies):
    """Тест сортировки вакансий."""
    sorted_list = sort_vacancies(sample_vacancies)

    # Проверяем порядок сортировки (по убыванию зарплаты)
    assert sorted_list[0].title == "Java Developer"
    assert sorted_list[1].title == "Python Developer"
    assert sorted_list[2].title == "JavaScript Developer"
    assert sorted_list[3].title == "DevOps Engineer"


def test_get_top_vacancies(sample_vacancies):
    """Тест получения топ N вакансий."""
    # Сначала сортируем вакансии по зарплате
    sorted_vacancies = sorted(
        sample_vacancies,
        key=lambda x: (x.salary_from or 0, x.salary_to or 0),
        reverse=True,
    )

    # Получаем топ 2
    top = get_top_vacancies(sorted_vacancies, 2)
    assert len(top) == 2
    assert top[0].title == "Java Developer"  # Зарплата 120000
    assert top[1].title == "Python Developer"  # Зарплата 100000

    # Получаем больше, чем есть
    top = get_top_vacancies(sorted_vacancies, 10)
    assert len(top) == len(sorted_vacancies)
