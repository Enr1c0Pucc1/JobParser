import requests
from main_functions import predict_rub_salary_hh, draw_table


def get_pages_for_lang(lang, area):
    params = {
        'text': lang,
        'area': area,
        'per_page': 50,
        'period': 30
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    return response.json()['pages']


def get_vacancies_from_hh(lang, area, page):
    params = {
        'text': lang,
        'area': area,
        'page': page,
        'per_page': 50,
        'period': 30
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    return response.json()['items'], response.json()['found']


def get_average_salary(programming_languages):
    salaries_by_lang = {}
    for i, plang in enumerate(programming_languages, start=0):
        pages_number = get_pages_for_lang(programming_languages[i], 1)
        vacancies_processed = 0
        salaries = 0
        for page in range(pages_number):
            vacancies, vacancies_found = get_vacancies_from_hh(
                programming_languages[i], 1, page)
            for m, vacancy in enumerate(vacancies, start=1):
                salary = predict_rub_salary_hh(vacancy['salary'])
                if salary:
                    vacancies_processed += 1
                    salaries += salary
            salaries_by_lang[plang] = {
                    'vacancies_found': vacancies_found,
                    'vacancies_processed': vacancies_processed,
                    'average_salary': (salaries//vacancies_processed)
                    }
    return salaries_by_lang


def draw_hh_statistic(languages):
    hh_statistic = get_average_salary(languages)
    return draw_table(hh_statistic, "HeadHunter Moscow")
