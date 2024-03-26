from src.config import config
from src.creation import DBase
from src.manager import DBManager
from src.parser import Parser
from src.utils import greet_user

PARAMS = config("database.ini")
DB_NAME = "hh"


def main() -> None:
    print(greet_user())
    while True:
        print(
            """
    Выбери действие:
        
    1 - поиск компании по ключевому слову.
    2 - просмотреть уже сохранённые вакансии.
    0 - выход из программы.
    """
        )
        choice = input()
        if choice == "0":
            print("Программа завершена, до свидания!")
            break

        elif choice == "1":
            employer = input("\nВведите название работодателя.\n")
            print(employer)
            all_data = Parser(employer)
            print(all_data)
            DBase(DB_NAME, all_data, PARAMS)

        elif choice == "2":
            data = DBManager(DB_NAME, PARAMS)
            while True:
                print(
                    """
    Выбери действие:

    1 - Выбрать список всех компаний и количества их вакансий.
    2 - Посмотреть список всех вакансий.
    3 - Получить среднюю зарплату по всем вакансиям.
    4 - Посмотреть вакансии с зарплатой выше средней по базе данных.
    5 - Выполнить поиск по вакансиям по ключевому слову.
    
    DEL - Удалить базу данных.
     
    0 - Выход в предыдущее меню.
      """
                )
                choice = input()

                if choice == "0":
                    break

                elif choice == "1":
                    data.get_companies_and_vacancies_count()

                elif choice == "2":
                    data.get_all_vacancies()

                elif choice == "3":
                    data.get_avg_salary()

                elif choice == "4":
                    data.get_vacancies_with_higher_salary()

                elif choice == "5":
                    search = input("\nВведите слово для поиска:\n")
                    data.get_vacancies_with_keyword(search)

                elif choice == "DEL":
                    data.delete_database()

                else:
                    print("Такой команды нет!")

        else:
            print("Такой команды нет!")


if __name__ == "__main__":
    main()
