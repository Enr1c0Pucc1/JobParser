import requests
from help_functions import predict_rub_salary_hh
from help_functions import count_prcssd_vacancies, get_pages_for_hh


def get_vacancies_from_hh(lang, area, page, per_page, period):
    params = {
        'text': lang,
        'area': area,
        'page': page,
        'per_page': per_page,
        'period': period
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies['items'], vacancies['found']


def get_average_salary_hh(programming_languages):
    vacancies_per_page = 50
    period = 30  # days
    area = 1  # Moscow id
    salaries_by_lang = {}
    for programming_language in programming_languages:
        pages_number = get_pages_for_hh(programming_language,
                                        area,
                                        vacancies_per_page,
                                        period)
        vacancies_prcssd = 0
        vacancies_with_salary = 0
        for page in range(pages_number):
            vacancies, vacancies_found = get_vacancies_from_hh(
                programming_language, area, page, vacancies_per_page, period)
            for vacancy in vacancies:
                salary = predict_rub_salary_hh(vacancy['salary'])
                if salary:
                    vacancies_prcssd += 1
                    vacancies_with_salary += salary
                average_salary = count_prcssd_vacancies(vacancies_prcssd,
                                                        vacancies_with_salary)
            salaries_by_lang[programming_language] = {
                    'vacancies_found': vacancies_found,
                    'vacancies_processed': vacancies_prcssd,
                    'average_salary': average_salary
                    }
    return salaries_by_lang
