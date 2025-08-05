from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage
from src.utils.filters import (
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary,
    print_vacancies,
    sort_vacancies,
)


def user_interaction():
    """Функция для взаимодействия с пользователем."""
    print("Поиск вакансий на HeadHunter")
    print("=" * 50)

    # Инициализация API и хранилища
    hh_api = HeadHunterAPI()
    storage = JSONStorage()

    # Получение параметров от пользователя
    search_query = input("Введите поисковый запрос (например: Python): ").strip()
    while not search_query:
        print("Поисковый запрос не может быть пустым!")
        search_query = input("Введите поисковый запрос (например: Python): ").strip()

    # Получение количества вакансий
    while True:
        try:
            top_n = int(
                input("Введите количество вакансий для вывода в топ N: ").strip()
            )
            if top_n <= 0:
                print("Число должно быть положительным!")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите целое число!")

    # Получение ключевых слов
    filter_words = (
        input("Введите ключевые слова для фильтрации вакансий (через пробел): ")
        .strip()
        .split()
    )

    # Получение диапазона зарплат
    salary_range = ""
    while True:
        salary_input = input(
            "Введите диапазон зарплат в RUR (например: 100000-200000 или оставьте пустым): "
        ).strip()
        if not salary_input:
            salary_range = ""
            break
        if "-" not in salary_input:
            print(
                "Пожалуйста, используйте формат: минимальная-максимальная (например: 100000-200000)"
            )
            continue
        try:
            min_s, max_s = map(int, salary_input.split("-"))
            if min_s <= 0 or max_s <= 0:
                print("Зарплата должна быть положительным числом!")
                continue
            if min_s > max_s:
                print("Минимальная зарплата не может быть больше максимальной!")
                continue
            salary_range = salary_input
            break
        except ValueError:
            print(
                "Пожалуйста, введите числа в формате: минимальная-максимальная (например: 100000-200000)"
            )

    # Получение и сохранение вакансий
    print("\nПолучаем вакансии с HeadHunter...")
    vacancies_data = hh_api.get_vacancies(
        search_query, per_page=top_n * 2
    )  # Берем больше вакансий для фильтрации
    vacancies = Vacancy.cast_to_object_list(vacancies_data)

    if not vacancies:
        print("По вашему запросу не найдено ни одной вакансии.")
        return

    # Сохраняем все вакансии (фильтрация будет при выводе)
    for vacancy in vacancies:
        storage.add_vacancy(vacancy)

    # Получение и фильтрация вакансий
    all_vacancies = storage.get_vacancies()
    filtered_vacancies = (
        filter_vacancies(all_vacancies, filter_words) if filter_words else all_vacancies
    )
    ranged_vacancies = (
        get_vacancies_by_salary(filtered_vacancies, salary_range)
        if salary_range
        else filtered_vacancies
    )
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Вывод результатов
    print("\nРезультаты поиска:")
    print(f"Найдено вакансий: {len(top_vacancies)} из {len(all_vacancies)}")
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
