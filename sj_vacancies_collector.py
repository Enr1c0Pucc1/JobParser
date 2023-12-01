import requests
from help_functions import predict_rub_salary_sj, count_processed_vacancies


def get_vacancies_from_sj(area, lang, catalogues, per_page, page, api_key):
    headers = {"X-Api-App-Id": api_key}
    params = {'town': area,
              'keyword': lang,
              'catalogues': catalogues,
              'count': per_page,
              'page': page}
    response = requests.get('https://api.superjob.ru/2.0/vacancies',
                            headers=headers,
                            params=params)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies['total'], vacancies['objects'], vacancies['more']


def get_average_salary_sj(programming_languages, api_key):
    salaries_by_lang = {}
    area = 4  # Moscow ID (in SJ)
    catalogue = 48
    per_page = 100
    for programming_language in programming_languages:
        pages_left = True
        page = 0
        vacancies_found = 0
        vacancies_processed = 0
        salaries = 0
        while pages_left:
            vacancies_found, vacancies, pages_left = get_vacancies_from_sj(
                area,
                programming_language,
                catalogue,
                per_page,
                page,
                api_key)
            page += 1
            for vacancy in vacancies:
                salary = predict_rub_salary_sj(vacancy)
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
