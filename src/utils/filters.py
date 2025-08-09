from typing import List

from src.models.vacancy import Vacancy


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """
    Фильтрация вакансий по ключевым словам.

    :param vacancies: Список вакансий
    :param filter_words: Список ключевых слов
    :return: Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        text_to_search = f"{vacancy.title} {vacancy.description or ''} {vacancy.requirements or ''}".lower()

        if all(word.lower() in text_to_search for word in filter_words):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(
    vacancies: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    """
    Фильтрация вакансий по диапазону зарплат.
    Теперь учитывает как минимальную, так и максимальную зарплату.
    """
    if not salary_range or "-" not in salary_range:
        return vacancies

    try:
        min_salary, max_salary = map(int, salary_range.split("-"))
    except ValueError:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        # Вакансии без зарплаты пропускаем
        if not vacancy.salary_from and not vacancy.salary_to:
            continue

        # Если валюта не указана или не RUR/RUB - пропускаем
        if vacancy.currency and vacancy.currency.lower() not in ["rur", "rub"]:
            continue

        # Проверяем, попадает ли зарплата в диапазон
        salary_from = vacancy.salary_from or 0
        salary_to = vacancy.salary_to or float("inf")

        if (salary_from >= min_salary or salary_to >= min_salary) and (
            salary_from <= max_salary or salary_to <= max_salary
        ):
            filtered.append(vacancy)

    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка вакансий по зарплате (от большей к меньшей)."""
    return sorted(
        vacancies, key=lambda x: (x.salary_from or 0, x.salary_to or 0), reverse=True
    )


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Получение топ N вакансий.

    :param vacancies: Список вакансий
    :param top_n: Количество вакансий для вывода
    :return: Список топ N вакансий
    """
    return vacancies[:top_n] if top_n > 0 else vacancies


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Вывод вакансий в консоль."""
    if not vacancies:
        print("Вакансии не найдены.")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"Вакансия #{i}")
        print(vacancy)
        print("-" * 50)
