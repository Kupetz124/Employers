import requests  # type: ignore


class Parser:
    """
    Класс для получения вакансий работодателей.
    """

    def __init__(self, search: str) -> None:
        self.search = search
        self.employers = self.get_employers_id
        self.vacancies = self.get_vacancies

    def __str__(self) -> str:
        count = 0
        for item in self.employers:
            count += int(item["open_vacancies"])

        return f"\nНайдено {len(self.employers)} работодателей."

    @property
    def get_employers_id(self) -> list[dict]:
        """Получает id работодателей из списка с ресурса HH по ключевым словам."""

        list_id = []

        # выполняем поиск работодателя по ключевому слову

        params_dict = {
            "text": self.search,  # ключевое слово
            "per_page": 100,  # количество работодателей на странице
            "only_with_vacancies": True,  # Выводить работодателей только с открытыми вакансиями
            "area": 113,  # поиск только по России
        }

        print("Идёт поиск информации по работодателю...")

        res = requests.get("https://api.hh.ru/employers", params=params_dict).json()

        # добавляем в список id и название найденных работодателей.
        for line in res["items"]:
            new_dict = dict()

            new_dict["id"] = line["id"]  # id работодателя
            new_dict["name"] = line["name"]  # название работодателя
            new_dict["open_vacancies"] = line["open_vacancies"]  # число открытых вакансий
            new_dict["url"] = line["alternate_url"]  # ссылка на страницу работодателя

            list_id.append(new_dict)

        return list_id

    @property
    def get_vacancies(self) -> list[dict]:
        """
        Получаем список вакансий работодателей с указанной зарплатой больше нуля.
        :return:
        """
        print("Идёт поиск вакансий...")
        list_vacancies = []
        for item in self.employers:

            params = {
                "employer_id": item["id"],
                "per_page": 100,  # Кол-во вакансий на 1 странице
                "area": 113,
                "only_with_salary": True,
            }
            req = requests.get("https://api.hh.ru/vacancies", params).json()

            for line in req["items"]:
                new_dict = dict()
                if line["salary"]["from"]:
                    new_dict["vacancy_id"] = line["id"]
                    new_dict["job_title"] = line["name"]
                    new_dict["employer_id"] = line["employer"]["id"]
                    new_dict["salary_from"] = line["salary"]["from"]
                    new_dict["url"] = line["alternate_url"]
                    new_dict["city"] = line["area"]["name"]
                    new_dict["employer_name"] = line["employer"]["name"]
                    new_dict["date_create"] = line["created_at"][:10]

                    list_vacancies.append(new_dict)

        return list_vacancies
