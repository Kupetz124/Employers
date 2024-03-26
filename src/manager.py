import psycopg2  # type: ignore


class DBManager:
    """Класс для работы с информацией в базе данных."""

    def __init__(self, baza_name: str, params: dict) -> None:
        self.baza_name = baza_name
        self.params = params

    def get_companies_and_vacancies_count(self) -> None:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """

        try:
            # подключаемся к базе данных.
            conn = psycopg2.connect(dbname=self.baza_name, **self.params)

            # считываем данные из таблицы "employers".
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select name, count_vacancies from employers
                    """
                )
                data = cur.fetchall()
                for item in data:
                    print(*item)

            conn.close()

        except psycopg2.Error as e:

            print(e)

    def get_all_vacancies(self) -> None:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        """

        try:
            # подключаемся к базе данных.
            conn = psycopg2.connect(dbname=self.baza_name, **self.params)

            # считываем данные.
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select name, job_title, salary_from, city, url_vacancy
                    from employers
                    JOIN vacancies USING (employer_id)
                    """
                )
                data = cur.fetchall()
                for item in data:
                    print(*item)

            conn.close()

        except psycopg2.Error as e:
            print(e)

    def get_avg_salary(self) -> None:
        """
        Получает среднюю зарплату по вакансиям.
        """

        try:
            # подключаемся к базе данных.
            conn = psycopg2.connect(dbname=self.baza_name, **self.params)

            # считываем данные.
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT AVG(salary_from)
                    FROM vacancies
                    """
                )
                data = cur.fetchone()

                print(f"\nСредняя зарплата по всем вакансиям: {round(*data)} ₽")

            conn.close()

        except psycopg2.Error as e:
            print(e)

    def get_vacancies_with_higher_salary(self) -> None:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """

        try:
            # подключаемся к базе данных.
            conn = psycopg2.connect(dbname=self.baza_name, **self.params)

            # считываем данные.
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT date_create, salary_from, job_title, city, url_vacancy
                    FROM vacancies
                    where salary_from > (SELECT AVG(salary_from) FROM vacancies)
                    """
                )

                data = cur.fetchall()
                for item in data:
                    print(*item)

            conn.close()

        except psycopg2.Error as e:
            print(e)

    def get_vacancies_with_keyword(self, search: str) -> None:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """

        try:
            # подключаемся к базе данных.
            conn = psycopg2.connect(dbname=self.baza_name, **self.params)

            # считываем данные.
            with conn.cursor() as cur:
                cur.execute(f" SELECT * FROM vacancies" f" WHERE job_title LIKE '%{search}%'")

                data = cur.fetchall()

                if data:
                    for item in data:
                        print(*item)
                else:
                    print("Информации по вашему запросу не нашлось!\n" "Попробуйте изменить поиск!")

        except psycopg2.Error as e:
            print(e)

    def delete_database(self) -> None:
        """
        Удаляет базу данных.

        """

        try:
            # подключение к базе данных по умолчанию
            conn = psycopg2.connect(dbname="postgres", **self.params)
            conn.autocommit = True
            cur = conn.cursor()

            # считываем данные.
            with conn.cursor() as cur:
                cur.execute(f"DROP DATABASE {self.baza_name}")
                print(f"База данных {self.baza_name} удалена!")

        except psycopg2.Error as e:
            print(e)
