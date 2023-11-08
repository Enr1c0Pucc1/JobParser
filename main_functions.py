from terminaltables import DoubleTable


def predict_rub_salary_hh(vacancy):
    if not vacancy:
        return None
    salary_from = vacancy.get('from')
    salary_to = vacancy.get('to')
    if not salary_from and not salary_to:
        return None
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_to:
        return salary_to * 0.8
    elif salary_from:
        return salary_from * 1.2


def predict_rub_salary_sj(vacancy):
    if not vacancy:
        return None
    salary_from = vacancy.get('payment_from')
    salary_to = vacancy.get('payment_to')
    if not salary_from and not salary_to:
        return None
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_to:
        return salary_to * 0.8
    elif salary_from:
        return salary_from * 1.2


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
