import requests
from dotenv import load_dotenv
import os
from main_functions import predict_rub_salary_sj, draw_table


def predict_rub_salary_for_superjob(vacancy):
    if vacancy['currency'] != 'rub':
        return None
    return predict_rub_salary_sj(vacancy)


def get_vacancies_from_sj(lang, page):
    load_dotenv()
    superjob_key = os.environ["SJ_API_KEY"]
    headers = {"X-Api-App-Id": superjob_key}
    params = {'town': 4,
              'keyword': lang,
              'catalogues': 48,
              'count': 100,
              'page': page}
    response = requests.get('https://api.superjob.ru/2.0/vacancies',
                            headers=headers,
                            params=params)
    response.raise_for_status()
    objects = response.json()
    return objects['objects'], objects['total']


def get_average_salary_sj(programming_languages):
    salaries_by_lang = {}
    vacancies_number_limit = 500
    for i, plang in enumerate(programming_languages, start=0):
        pages = 1
        page = 0
        vacancies_found = 0
        vacancies_processed = 0
        salaries = 0
        while page < pages:
            vacancies, total = get_vacancies_from_sj(programming_languages[i],
                                                     page)
            if total > vacancies_number_limit:
                pages = vacancies_number_limit // 500
            elif total == 0:
                break
            elif total < 100:
                pages = 1
            else:
                pages = total // 100
            page += 1
            for m, vacancy in enumerate(vacancies, start=1):
                salary = predict_rub_salary_for_superjob(vacancy)
                vacancies_found += 1
                if salary:
                    vacancies_processed += 1
                    salaries += salary
            salaries_by_lang[plang] = {
                'vacancies_found': vacancies_found,
                'vacancies_processed': vacancies_processed,
                'average_salary': (salaries//vacancies_processed)
                }
    return salaries_by_lang


def draw_superjob_statistic(languages):
    sj_statistic = get_average_salary_sj(languages)
    return draw_table(sj_statistic, "SuperJob Moscow")
