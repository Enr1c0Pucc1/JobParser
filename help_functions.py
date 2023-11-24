import requests
from terminaltables import DoubleTable


def calculate_average(salary_from, salary_to):
    if not salary_from and not salary_to:
        return None
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_to:
        return salary_to * 0.8
    elif salary_from:
        return salary_from * 1.2


def predict_rub_salary_hh(vacancy):
    if not vacancy:
        return None
    salary_from = vacancy.get('from')
    salary_to = vacancy.get('to')
    average = calculate_average(salary_from, salary_to)
    return average


def predict_rub_salary_sj(vacancy):
    if not vacancy:
        return None
    elif vacancy['currency'] != 'rub':
        return None
    salary_from = vacancy.get('payment_from')
    salary_to = vacancy.get('payment_to')
    average = calculate_average(salary_from, salary_to)
    return average


def count_prcssd_vacancies(vacancies_prcssd, vacancies_with_salaries):
    if vacancies_prcssd:
        average_salary = vacancies_with_salaries//vacancies_prcssd
    else:
        average_salary = 'N/A'
    return average_salary


def get_pages_for_hh(lang, area, per_page, period):
    params = {
        'text': lang,
        'area': area,
        'per_page': per_page,
        'period': period
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    return response.json()['pages']


def draw_table(vacancies_statistic, title):
    raw_table = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ]
    ]
    for language in vacancies_statistic:
        raw_table.append(
            [
                language,
                vacancies_statistic[language]["vacancies_found"],
                vacancies_statistic[language]["vacancies_processed"],
                vacancies_statistic[language]["average_salary"],
            ]
        )
    table_instance = DoubleTable(raw_table, title)
    return table_instance.table
