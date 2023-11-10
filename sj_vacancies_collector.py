import requests
from help_functions import predict_rub_salary_sj


def get_vacancies_from_sj(lang, page, api_key):
    headers = {"X-Api-App-Id": api_key}
    params = {'town': 4,
              'keyword': lang,
              'catalogues': 48,
              'count': 100,
              'page': page}
    response = requests.get('https://api.superjob.ru/2.0/vacancies',
                            headers=headers,
                            params=params)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies['objects'], vacancies['total']


def average_salary_sj(programming_languages, api_key):
    salaries_by_lang = {}
    vacancies_number_limit = 500
    for plang in programming_languages:
        pages = 1
        page = 0
        vacancies_found = 0
        vacancies_prcssd = 0
        vacancies_with_salaries = 0
        while page < pages:
            vacancies, total = get_vacancies_from_sj(plang,
                                                     page, api_key)
            if total > vacancies_number_limit:
                pages = vacancies_number_limit // 500
            elif total == 0:
                break
            elif total < 100:
                pages = 1
            else:
                pages = total // 100
            page += 1
            for vacancy in vacancies:
                salary = predict_rub_salary_sj(vacancy)
                vacancies_found += 1
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
