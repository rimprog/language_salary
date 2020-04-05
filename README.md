# Programming vacancies compare

This script get and counting average salaries by popular programming languages. All data fetches from [Head Hunter API](https://github.com/hhru/api) and [SuperJob API](https://api.superjob.ru/) for last month. Just use console command `python main.py`.

```
In:
python3 main.py

Out:
+HeadHunter--------------+------------------+---------------------+------------------+
| Языки программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+------------------------+------------------+---------------------+------------------+
| JavaScript             | 3406             | 1736                | 106212           |
| Java                   | 1570             | 1411                | 136726           |
| Python                 | 1138             | 1035                | 128735           |
| Ruby                   | 236              | 207                 | 139694           |
| PHP                    | 2189             | 1798                | 96057            |
| C++                    | 253              | 238                 | 100807           |
| C#                     | 1165             | 1055                | 108002           |
| C                      | 684              | 653                 | 97281            |
| Go                     | 271              | 225                 | 146713           |
| Objective-C            | 171              | 155                 | 143282           |
| Scala                  | 97               | 78                  | 165552           |
| Swift                  | 309              | 285                 | 161206           |
| TypeScript             | 503              | 444                 | 134301           |
+------------------------+------------------+---------------------+------------------+
+Superjob----------------+------------------+---------------------+------------------+
| Языки программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+------------------------+------------------+---------------------+------------------+
| JavaScript             | 52               | 43                  | 110412           |
| Java                   | 43               | 21                  | 122333           |
| Python                 | 12               | 9                   | 108777           |
| Ruby                   | None             | None                | None             |
| PHP                    | 51               | 42                  | 80941            |
| C++                    | 76               | 59                  | 89267            |
| C#                     | 78               | 50                  | 106416           |
| C                      | 20               | 15                  | 100733           |
| Go                     | 26               | 15                  | 128000           |
| Objective-C            | 1                | 1                   | 100000           |
| Scala                  | 2                | 2                   | 180000           |
| Swift                  | 1                | 1                   | 100000           |
| TypeScript             | 1                | 1                   | 122500           |
+------------------------+------------------+---------------------+------------------+
```

### How to install

You need create SuperJob API token. 
First, you need get SuperJob sercet key. To do this, follow these steps:
1. Register on [SuperJob](https://api.superjob.ru/register)
2. Get 'Secret Key' on [api info page](https://api.superjob.ru/info/)
If you are unable to do this, read the additional information in the [Getting Started section](https://api.superjob.ru/#gettin).

After get 'Secret Key', create .env file in root project folder and place 'Secret Key' in SUPERJOB_TOKEN variable.

Example .env:
```
SUPERJOB_TOKEN = YOUR_SUPERJOB_SECRET_KEY
```

Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
