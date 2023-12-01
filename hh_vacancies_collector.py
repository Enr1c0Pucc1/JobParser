import requests
from help_functions import predict_rub_salary_hh
from help_functions import count_processed_vacancies, get_pages_for_hh


def get_vacancies_from_hh(lang, area, per_page, period):
    pages_number = get_pages_for_hh(lang,
                                    area,
                                    per_page,
                                    period)
    all_vacancies = []
    for page in range(pages_number):
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
        all_vacancies.extend(vacancies['items'])
    return all_vacancies, vacancies['found']


def get_average_salary_hh(programming_languages):
    vacancies_per_page = 50
    period = 30  # days
    area = 1  # Moscow id
    salaries_by_lang = {}
    for programming_language in programming_languages:
        vacancies_processed = 0
        salaries = 0
        all_vacancies, vacancies_found = get_vacancies_from_hh(
            programming_language, area, vacancies_per_page, period)
        for vacancy in all_vacancies:
            salary = predict_rub_salary_hh(vacancy['salary'])
            if salary:
                vacancies_processed += 1
                salaries += salary
        average_salary = count_processed_vacancies(vacancies_processed,
                                                   salaries)
        salaries_by_lang[programming_language] = {
            'vacancies_processed': vacancies_processed,
            'vacancies_found': vacancies_found,
            'average_salary': average_salary
        }
    return salaries_by_lang
