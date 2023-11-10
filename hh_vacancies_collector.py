import requests
from help_functions import predict_rub_salary_hh


def get_pages_for_lang(lang, area, per_page, period):
    params = {
        'text': lang,
        'area': area,
        'per_page': per_page,
        'period': period
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    return response.json()['pages']


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
    return response.json()['items'], response.json()['found']


def average_salary_hh(programming_languages):
    vacancies_per_page = 50
    period = 30  # days
    salaries_by_lang = {}
    for plang in programming_languages:
        pages_number = get_pages_for_lang(plang, 1, vacancies_per_page, period)
        vacancies_prcssd = 0
        vacancies_with_salaries = 0
        for page in range(pages_number):
            vacancies, vacancies_found = get_vacancies_from_hh(
                plang, 1, page, vacancies_per_page, period)
            for vacancy in vacancies:
                salary = predict_rub_salary_hh(vacancy['salary'])
                if salary:
                    vacancies_prcssd += 1
                    vacancies_with_salaries += salary
                if vacancies_prcssd != 0:
                    average_salary = vacancies_with_salaries//vacancies_prcssd
                else:
                    average_salary = 'N/A'
            salaries_by_lang[plang] = {
                    'vacancies_found': vacancies_found,
                    'vacancies_processed': vacancies_prcssd,
                    'average_salary': average_salary
                    }
    return salaries_by_lang
