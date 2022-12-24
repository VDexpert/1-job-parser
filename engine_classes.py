from abc import ABC, abstractmethod
import requests as rq
from connector import Connector
from bs4 import BeautifulSoup
import json


class Engine(ABC):
    __key_word = "python"

    @abstractmethod
    def get_request(self):
        raise NotImplementedError("Метод get_request должен быть переопределен в дочернем классе")

    @staticmethod
    def get_connector(filename):
        """ Возвращает экземпляр класса Connector """
        return Connector(filename)

    @property
    def key_word(self):
        return self.__key_word

    @key_word.setter
    def key_word(self, value):
        self.__key_word = value


class HH(Engine):
    __url = "https://api.hh.ru/vacancies"
    __per_page = 5
    __count_geting = 0

    def get_request(self, page):
        self.__params = {"text": self.key_word, "page": page, "per_page": self.__per_page}
        r = rq.get(self.__url, self.__params)
        if r.status_code == 200:
            filename = f"HH-dump-keyword-{self.key_word}"
            self.get_connector(filename)
            Connector.all_connectors[filename].insert(r.json())
        else:
            raise Exception(f"Ошибка запроса объекта класса {self.__class__.__name__}: {r.status_code}")

class SuperJob(Engine):
    __url = f"https://russia.superjob.ru/vacancy/search/?keywords="

    def get_request(self, page):
        r = rq.get(f"{self.__url}{self.key_word}&page={page}")
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.find_all("div", class_="f-test-search-result-item")
            prev_vac = []
            count_err = 0

            for item in items:
                try:
                    prev_vac.append(
                        {
                            "name": item.find("span", class_="_2s70W").find("a", class_="_1IHWd").get_text(strip=True),
                            "href": "https://russia.superjob.ru" + item.find("a", class_="_1IHWd").get("href"),
                            "company": item.find("span", class_="_3nMqD").find("a", class_="_1IHWd").get_text(strip=True),
                            "salary": " ".join(item.find("span", "_2eYAG _1B2ot _3EXZS _3pAka _3GChV").get_text(strip=True).split("\xa0")),
                            "description": item.find("span", class_="_1G5lt _3EXZS _3pAka _3GChV _2GgYH").get_text(strip=True)
                        }
                    )
                except AttributeError:
                    count_err += 1
                    continue

            dump = [{"items": prev_vac}]
            with open("temp_file.json", "w") as temp_f:
                json.dump(dump, temp_f, indent=2, separators=(',', ':'))

            with open("temp_file.json", "r", errors='ignore') as temp_r_f:
                out_data = json.load(temp_r_f, strict=False)
                filename = f"SJ-dump-keyword-{self.key_word}"
                self.get_connector(filename)
                Connector.all_connectors[filename].insert(dict(*out_data))
        else:
            raise Exception(f"Ошибка запроса объекта класса {self.__class__.__name__}: {r.status_code}")


if __name__ == "__main__":
    hh1 = HH()
    hh1.get_request(1)

    sj1 = SuperJob()
    sj1.get_request(1)
