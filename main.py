# from hh_vacancies_collector import average_salary_hh
from sj_vacancies_collector import average_salary_sj
from help_functions import draw_table
from dotenv import load_dotenv
import os


if __name__ == '__main__':
    programming_languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'Go']
    load_dotenv()
    superjob_key = os.environ["SJ_API_KEY"]
    # hh_statistic = average_salary_hh(programming_languages)
    # draw_table(hh_statistic, "HeadHunter Moscow")
    sj_statistic = average_salary_sj(programming_languages, superjob_key)
    print(draw_table(sj_statistic, "SuperJob Moscow"))
