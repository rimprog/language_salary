from statistics import mean
import requests


def predict_rub_salary_on_hh(vacancy):
    vacancy_salary = vacancy['salary']

    if vacancy_salary['currency'] != 'RUR':
        return None
    elif vacancy_salary['from'] and vacancy_salary['to']:
        expected_salary = mean([vacancy_salary['from'], vacancy_salary['to']])
    elif vacancy_salary['from'] and not vacancy_salary['to']:
        expected_salary = vacancy_salary['from'] * 1.2
    elif not vacancy_salary['from'] and vacancy_salary['to']:
        expected_salary = vacancy_salary['to'] * 0.8

    return int(expected_salary)


def calculate_average_salary_by_programming_language_on_hh(programming_language):
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
            vacancies_salaries.append(predict_rub_salary_on_hh(vacancy))
        vacancies_salaries = [vacancy_salary for vacancy_salary in vacancies_salaries if vacancy_salary]
        mean_vacancies_salaries = mean(vacancies_salaries)
        average_salaries_by_pages.append(mean_vacancies_salaries)

        vacancies_found = vacancies['found']

        vacancies_processed_by_pages.append(len(vacancies_salaries))

        pages_number = vacancies["pages"]
        page += 1

    print(average_salaries_by_pages)
    average_salary = mean(average_salaries_by_pages)
    vacancies_processed = sum(vacancies_processed_by_pages)

    average_salary_by_programming_language = {
      'vacancies_found': vacancies_found,
      'vacancies_processed': vacancies_processed,
      'average_salary': average_salary
    }

    return average_salary_by_programming_language


def main():
    # url = 'https://api.hh.ru/vacancies'
    # payload = {
    #   'specialization': 1.221,
    #   'area': 1,
    #   'period': 30
    # }
    # response = requests.get(url, params=payload)
    # response.raise_for_status()
    # vacancies = response.json()

    popular_programming_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C', 'Scala', 'Swift', 'TypeScript']

    average_salary_by_programming_languages = {}
    for programming_language in popular_programming_languages:
        average_salary_by_programming_languages[programming_language] = calculate_average_salary_by_programming_language_on_hh(programming_language)
    print(average_salary_by_programming_languages)

    # payload = {
    #   'text': 'Программист Python',
    #   'only_with_salary': 'true'
    # }
    # response = requests.get(url, params=payload)
    # response.raise_for_status()
    # python_vacancies = response.json()
    #
    # for vacancy in python_vacancies['items']:
    #     print(predict_rub_salary_on_hh(vacancy))
    #
    #
    #
    #
    # ' https://api.hh.ru/vacancies?specialization=1.221&text=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82%20Python&clusters=True&per_page=0'

if __name__=='__main__':
    main()
