from abc import ABC, abstractmethod
import requests as rq
from connector import Connector
from bs4 import BeautifulSoup


class Engine(ABC):
    all_engines = {}

    def __init__(self, quantity, key_word):
        self.__quantity = quantity
        self.__count = 0
        self.__key_word = key_word
        self.__filename = f"JSON-{self.__class__.__name__}-dump-keyword-{self.key_word}-{quantity}"
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
    def filename(self):
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
        r = rq.get(self.__url, self.__params)
        if r.status_code != 200:
            raise Exception(f"Ошибка запроса объекта класса {self.__class__.__name__}: {r.status_code}")

        orig_data = r.json()["items"]
        res_data = []

        for i in orig_data:
            name = i["name"]
            href = i["alternate_url"]
            company = i["employer"]["name"]
            description = i["snippet"]["responsibility"]
            salary = "По договорённости"
            rate_salary = 1
            if i["salary"]:
                cur_code = i["salary"]["currency"]

                if cur_code != "RUR":
                    rate = rq.get("https://api.hh.ru/dictionaries")
                    if rate.status_code != 200:
                        raise Exception(f"Ошибка запроса значений валют в объекте класса {self.__class__.__name__}: {r.status_code}")
                    for cur in rate.json()["currency"]:
                        if cur["code"] == cur_code:
                            rate_salary = cur["rate"]

            if i["salary"]:
                if i["salary"]["from"] and i["salary"]["to"]:
                    salary = str(round(i["salary"]["from"] / rate_salary)) + "\u2014" + str(round(i["salary"]["to"] / rate_salary))
                elif i["salary"]["from"] and not i["salary"]["to"]:
                    salary = "от" + str(round(i["salary"]["from"] / rate_salary))
                elif not i["salary"]["from"] and i["salary"]["to"]:
                    salary = "до" + str(round(i["salary"]["to"] / rate_salary))

            res_data.append(
                {
                    "name": name,
                    "href": href,
                    "company": company,
                    "salary": salary,
                    "description": description
                }
            )
            self.count += 1
            if self.count == self.quantity:
                break

        self.get_connector(self.filename)
        Connector.all_connectors[self.filename].insert(res_data)


class SuperJob(Engine):
    __url = f"https://russia.superjob.ru/vacancy/search/?keywords="
    __per_page = 37

    @property
    def per_page(self):
        return self.__per_page

    def get_request(self, page):
        url = f"{self.__url}{self.key_word}&page={page}"
        r = rq.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.find_all("div", class_="f-test-search-result-item")
            prev_vac = []

            for item in items:
                try:
                    salary = " ".join(item.find("span", "_2eYAG _1B2ot _3EXZS _3pAka _3GChV").get_text().split("\xa0"))
                    if salary != "По договорённости":
                        salary = salary[0:-2]
                        salary = salary.replace(" ", "")

                    prev_vac.append(
                        {
                            "name": item.find("span", class_="_2s70W").find("a", class_="_1IHWd").get_text(),
                            "href": "https://russia.superjob.ru" + item.find("a", class_="_1IHWd").get("href"),
                            "company": item.find("span", class_="_3nMqD").find("a", class_="_1IHWd").get_text(),
                            "salary": salary,
                            "description": item.find("span", class_="_1G5lt _3EXZS _3pAka _3GChV _2GgYH").get_text()
                        }
                    )
                    self.count += 1
                    if self.count == self.quantity:
                        break

                except AttributeError:
                    continue

            self.get_connector(self.filename)
            Connector.all_connectors[self.filename].insert(prev_vac)
        else:
            raise Exception(f"Ошибка запроса объекта класса {self.__class__.__name__}: {r.status_code}")


if __name__ == "__main__":
    hh1 = HH(100)
    hh1.get_request(1)

    sj1 = SuperJob(30)
    sj1.get_request(1)
