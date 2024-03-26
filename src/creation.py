from typing import Any

import psycopg2  # type: ignore


class DBase:
    """
    Класс для создания БД и таблиц и заполнения их данными.
    """

    def __init__(self, baza_name: str, data: Any, params: dict) -> None:
        self.baza_name = baza_name
        self.data = data
        self.params = params
        self.create_database()
        self.save_data_to_database()

    def create_database(self) -> None:
        """Создание базы данных и таблиц для сохранения данных о работодателях и их вакансиях."""

        try:
            # подключение к базе данных по умолчанию
            conn = psycopg2.connect(dbname="postgres", **self.params)
            conn.autocommit = True
            cur = conn.cursor()

            # если база данных не создана, создаём её.
            cur.execute(f" CREATE DATABASE {self.baza_name}")

            print(f"\nБаза данных {self.baza_name} создана.")

            cur.close()
            conn.close()

        except psycopg2.Error:
            pass

        try:
            # подключаемся к нужной базе данных.
            conn = psycopg2.connect(dbname=self.baza_name, **self.params)

            # создаём таблицу "employers"
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE  employers (
                        employer_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        count_vacancies INTEGER,
                        url_employer TEXT
                        )
                """
                )

            # создаём таблицу "vacancies"
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE vacancies (
                        vacancy_id INTEGER PRIMARY KEY,
                        job_title TEXT,
                        salary_from INTEGER,
                        city TEXT,
                        employer_id INTEGER REFERENCES employers(employer_id),
                        date_create DATE,
                        url_vacancy TEXT
                    )
                """
                )

            conn.commit()

            conn.close()

            print("Таблицы для данных созданы.")

        except psycopg2.Error:
            pass

    def save_data_to_database(self) -> None:
        """Сохранение информации о работодателях и их вакансиях в базу данных."""

        try:
            conn = psycopg2.connect(dbname=self.baza_name, **self.params)

            with conn.cursor() as cur:
                # заполняем таблицу "employers"
                for item in self.data.employers:
                    cur.execute(
                        """
                        INSERT INTO employers (
                        employer_id,
                        name,
                        count_vacancies,
                        url_employer)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (item["id"], item["name"], item["open_vacancies"], item["url"]),
                    )

                # заполняем таблицу "vacancies"
                for line in self.data.vacancies:
                    cur.execute(
                        """
                        INSERT INTO vacancies (
                        vacancy_id,
                        job_title,
                        salary_from,
                        city,
                        employer_id,
                        date_create,
                        url_vacancy
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            line["vacancy_id"],
                            line["job_title"],
                            line["salary_from"],
                            line["city"],
                            line["employer_id"],
                            line["date_create"],
                            line["url"],
                        ),
                    )

            conn.commit()
            if self.data.employers and self.data.vacancies:
                print("\nДанные успешно записаны в таблицы!\n")

            conn.close()

        except psycopg2.Error as e:
            print(e)
