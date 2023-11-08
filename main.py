from hh_vacancies_collector import draw_hh_statistic
from sj_vacancies_collector import draw_superjob_statistic


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
    print(draw_hh_statistic(programming_languages))
    print(draw_superjob_statistic(programming_languages))
