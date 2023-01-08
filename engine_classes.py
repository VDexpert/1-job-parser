from abc import ABC, abstractmethod
import requests as rq
from connector import Connector

class Engine(ABC):
    all_engines = {}

    def __init__(self, quantity, key_word):
        self.__quantity = quantity
        self.__count = 0
        self.__key_word = key_word
        self.__filename = f"JSON-{self.__class__.__name__}-dump-{self.key_word}.json"
        self.all_engines[self.__filename] = self


    @abstractmethod
    def get_request(self):
        raise NotImplementedError("Метод get_request должен быть переопределен в дочернем классе")

    @staticmethod
    def get_connector(filename):
        """ Возвращает экземпляр класса Connector """
        return Connector(filename)

    @property
    def quantity(self):
        return self.__quantity

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value

    def __radd__(self, other):
        return self.__count + other

    @property
    def filename_json(self):
        return self.__filename

    @property
    def key_word(self):
        return self.__key_word

    @key_word.setter
    def key_word(self, value):
        self.__key_word = value


class HH(Engine):
    __url = "https://api.hh.ru/vacancies"
    __per_page = 100

    @property
    def per_page(self):
        return self.__per_page

    def get_request(self, page):
        self.__params = {"text": self.key_word, "page": page, "per_page": self.__per_page}
        response = rq.get(self.__url, self.__params)
        if response.status_code != 200:
            raise Exception(f"Ошибка запроса объекта класса {self.__class__.__name__}: {response.status_code}")

        origin_data = response.json()["items"]
        res_data = []

        for vac in origin_data:
            id_vac = vac["id"]
            name = vac["name"]
            href = vac["alternate_url"]
            company = vac["employer"]["name"]

            req_vac = rq.get(self.__url + "/" + id_vac)
            experience = req_vac.json()["experience"]["name"].lower()

            description = req_vac.json()["description"]
            salary = "По договорённости"
            rate_salary = 1
            if vac["salary"]:
                cur_code = vac["salary"]["currency"]

                if cur_code != "RUR":
                    rate = rq.get("https://api.hh.ru/dictionaries")
                    if rate.status_code != 200:
                        raise Exception(f"Ошибка запроса значений валют в объекте класса {self.__class__.__name__}: {response.status_code}")
                    for cur in rate.json()["currency"]:
                        if cur["code"] == cur_code:
                            rate_salary = cur["rate"]

            if vac["salary"]:
                if vac["salary"]["from"] and vac["salary"]["to"]:
                    salary = str(round(vac["salary"]["from"] / rate_salary)) + \
                             "\u2014" + str(round(vac["salary"]["to"] / rate_salary))
                elif vac["salary"]["from"] and not vac["salary"]["to"]:
                    salary = "от" + str(round(vac["salary"]["from"] / rate_salary))
                elif not vac["salary"]["from"] and vac["salary"]["to"]:
                    salary = "до" + str(round(vac["salary"]["to"] / rate_salary))

            res_data.append(
                {"name": name, "href": href, "experience": experience, "company": company, "salary": salary,
                 "description": description})
            self.count += 1
            if self.count == self.quantity:
                break

        self.get_connector(self.filename_json)
        Connector.all_connectors[self.filename_json].insert(res_data)


class SuperJob(Engine):
    __url = f"https://api.superjob.ru/2.0/vacancies/"
    __per_page = 100

    @property
    def per_page(self):
        return self.__per_page

    def get_request(self, page):
        self.__params = {"keyword": self.key_word, "page": page, "count": self.__per_page, "order_field": "payment", "order_direction": "desc"}
        self.__secret_key = {"X-Api-App-Id": "v3.r.137228722.e8991bb405e73fc133aa1aa5927d54b3d5e55fc3.e6686c61c5b8bdf5acab068a86154863b5a2d1f1"}

        response = rq.get(self.__url, params=self.__params, headers=self.__secret_key)

        if response.status_code != 200:
            raise Exception(f"Ошибка запроса объекта класса {self.__class__.__name__}: {response.status_code}")

        container_exper = {
            3: "от 3 до 6 лет",
            2: "от 1 года до 3 лет",
            0: "не указано",
            1: "нет опыта",
            4: "более 6 лет"
        }
        res_data = []
        origin_data = response.json()["objects"]

        for vac in origin_data:
            name = vac["profession"]
            href = vac["link"]
            company = vac["firm_name"]
            experience = vac["experience"]["id"]
            if vac["work"]:
                description = vac["work"]
            elif vac["vacancyRichText"]:
                description = vac["vacancyRichText"]
            try:
                if vac["payment"]:
                    salary = str(vac["payment"])
            except KeyError:
                if vac["payment_from"] and vac["payment_to"]:
                    salary = str(vac["payment_from"]) + "\u2014" + str(vac["payment_to"])
                elif vac["payment_from"]:
                    salary = "от " + str(vac["payment_from"])
                elif vac["payment_to"]:
                    salary = "до " + str(vac["payment_to"])

            res_data.append(
                {"name": name, "href": href, "company": company, "experience": container_exper[experience],
                 "salary": salary, "description": description})

            self.count += 1
            if self.count == self.quantity:
                break

        self.get_connector(self.filename_json)
        Connector.all_connectors[self.filename_json].insert(res_data)

if __name__ == "__main__":
    hh1 = HH(100, "python")
    hh1.get_request(1)

    sj1 = SuperJob(100, "python")
    sj1.get_request(5)
