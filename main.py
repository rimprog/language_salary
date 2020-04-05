import os
from statistics import mean

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        expected_salary = mean([salary_from, salary_to])
    elif salary_from and not salary_to:
        expected_salary = salary_from * 1.2
    elif not salary_from and salary_to:
        expected_salary = salary_to * 0.8
    else:
        return None

    return int(expected_salary)


def predict_rub_salary_for_hh(vacancy):
    vacancy_salary = vacancy['salary']

    if vacancy_salary['currency'] != 'RUR':
        return None

    expected_salary =  predict_salary(vacancy_salary['from'], vacancy_salary['to'])

    return expected_salary


def predict_rub_salary_for_sj(vacancy):
    if vacancy['currency'] != 'rub':
        return None

    expected_salary = predict_salary(vacancy['payment_from'], vacancy['payment_to'])

    return expected_salary


def calculate_average_salary_by_programming_language_for_hh(programming_language):
    average_salaries_by_pages = []
    vacancies_processed_by_pages = []

    page = 0
    pages_number = 1
    while page < pages_number:
        url = 'https://api.hh.ru/vacancies'
        payload = {
          'text': 'Программист {}'.format(programming_language),
          'only_with_salary': 'true',
          'page': page,
          'per_page': 100
        }

        page_response = requests.get(url, params=payload)
        page_response.raise_for_status()

        vacancies = page_response.json()

        vacancies_salaries = []
        for vacancy in vacancies['items']:
            vacancies_salaries.append(predict_rub_salary_for_hh(vacancy))
        vacancies_salaries = [vacancy_salary for vacancy_salary in vacancies_salaries if vacancy_salary]
        mean_vacancies_salaries = mean(vacancies_salaries)
        average_salaries_by_pages.append(mean_vacancies_salaries)

        vacancies_found = vacancies['found']

        vacancies_processed_by_pages.append(len(vacancies_salaries))

        pages_number = vacancies["pages"]
        page += 1

    average_salary = mean(average_salaries_by_pages)
    vacancies_processed = sum(vacancies_processed_by_pages)

    average_salary_by_programming_language = {
      'vacancies_found': vacancies_found,
      'vacancies_processed': vacancies_processed,
      'average_salary': average_salary
    }

    return average_salary_by_programming_language


def calculate_average_salary_by_programming_language_for_sj(programming_language, superjob_token):
    average_salaries_by_pages = []
    vacancies_processed_by_pages = []

    page = 0
    pages_number = 1
    while page < pages_number:
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
            'X-Api-App-Id': superjob_token
        }
        payload = {
            'keyword': 'Программист {}'.format(programming_language),
            'catalogues': 48,
            'count': 100,
            'page': page,
        }

        page_response = requests.get(url, headers=headers, params=payload)
        page_response.raise_for_status()

        vacancies = page_response.json()


        if vacancies['total'] > 0:
            vacancies_found = vacancies['total']
        else:
            return None

        vacancies_salaries = []
        for vacancy in vacancies['objects']:
            vacancies_salaries.append(predict_rub_salary_for_sj(vacancy))
        vacancies_salaries = [vacancy_salary for vacancy_salary in vacancies_salaries if vacancy_salary]

        mean_vacancies_salaries = mean(vacancies_salaries)

        average_salaries_by_pages.append(mean_vacancies_salaries)

        vacancies_processed_by_pages.append(len(vacancies_salaries))

        pages_number = vacancies_found / 100
        page += 1

    average_salary = mean(average_salaries_by_pages)
    vacancies_processed = sum(vacancies_processed_by_pages)

    average_salary_by_programming_language = {
      'vacancies_found': vacancies_found,
      'vacancies_processed': vacancies_processed,
      'average_salary': average_salary
    }

    return average_salary_by_programming_language


def create_console_statistics_table(average_salary_by_programming_languages, title):
    table_data = [['Языки программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]

    for programming_language in average_salary_by_programming_languages:
        try:
            table_data.append([
                programming_language,
                average_salary_by_programming_languages[programming_language]['vacancies_found'],
                average_salary_by_programming_languages[programming_language]['vacancies_processed'],
                average_salary_by_programming_languages[programming_language]['average_salary']
            ])
        except TypeError:
            table_data.append([
                programming_language,
                None,
                None,
                None
            ])

    table = AsciiTable(table_data, title)

    return table.table


def main():
    load_dotenv()
    superjob_token = os.getenv('SUPERJOB_TOKEN')

    popular_programming_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C', 'Scala', 'Swift', 'TypeScript']

    average_salary_by_programming_languages_for_hh = {}
    average_salary_by_programming_languages_for_sj = {}
    for programming_language in popular_programming_languages:
        average_salary_by_programming_languages_for_hh[programming_language] = calculate_average_salary_by_programming_language_for_hh(programming_language)
        average_salary_by_programming_languages_for_sj[programming_language] = calculate_average_salary_by_programming_language_for_sj(programming_language, superjob_token)

    title = 'HeadHunter'
    console_statistics_table_hh = create_console_statistics_table(average_salary_by_programming_languages_for_hh, title)
    print(console_statistics_table_hh)

    title = 'Superjob'
    console_statistics_table_sj = create_console_statistics_table(average_salary_by_programming_languages_for_sj, title)
    print(console_statistics_table_sj)


if __name__=='__main__':
    main()
