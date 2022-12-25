from connector import Connector

class Vacancy:
    __slots__ = ("name", "href", "company", "salary", "description",
                 "salary_for_comparison", "__filename", "count", "step_iter", "stop", "value")
    hh_vacancies = []
    sj_vacancies = []

    def __init__(self, name, href, company, salary, description, filename):
        self.name = name
        self.href = href
        self.company = company
        self.salary_for_comparison = self.convert_for_comparison(salary)
        self.salary = salary
        if "от" in salary[0:2] or "до" in salary[0:2]:
            self.salary = salary[0:2] + " " + salary[2:]
        self.description = description
        self.__filename = filename
        if self.__class__.__name__ == "HH":
            self.hh_vacancies.append(self)
            self.count = len(self.hh_vacancies)
        elif self.__class__.__name__ == "SuperJob":
            self.sj_vacancies.append(self)
            self.count = len(self.sj_vacancies)
        self.step_iter = 1


    def __gt__(self, other):
        return self.salary_for_comparison > other.salary_for_comparison

    def __lt__(self, other):
        return self.salary_for_comparison < other.salary_for_comparison

    def __str__(self):
        if self.salary == "По договорённости":
            return f'{self.__class__.__name__}(№ {self.count} из {self.get_count_of_vacancy(self.filename)}): {self.company}, ' \
                   f'зарплата: {self.salary}, ссылка: {self.href}'
        else:
            return f'{self.__class__.__name__}(№ {self.count} из {self.get_count_of_vacancy(self.filename)}): {self.company}, ' \
                   f'зарплата: {self.salary} руб/мес, ссылка: {self.href}'

    @staticmethod
    def convert_for_comparison(salary):
        if "\u2014" in salary:
            indx_sep = salary.index("\u2014")
            salary = salary[indx_sep + 1:]
            return int(salary)
        if salary == "По договорённости":
            salary = 0
            return salary
        elif "от" in salary[0:2] or "до" in salary[0:2]:
            salary = salary[2:]
            return int(salary)
        else:
            return int(salary)

    @property
    def filename(self):
        return self.__filename

class CountMixin:

    def get_count_of_vacancy(self, filename):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        data = Connector.all_connectors[filename].connect()
        count = 0
        for item in data:
            for i in item["items"]:
                count += 1
            return count


class HH(Vacancy, CountMixin):
    """ HeadHunter Vacancy """
    pass



class SuperJob(Vacancy, CountMixin):
    """ SuperJob Vacancy """
    pass


def sorting(vacancies, reversed=False):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    if reversed:
        vacancies.sort(reverse=True)
    else:
        vacancies.sort()
    return vacancies


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    vacancies = sorting(vacancies, reversed=True)
    result = []
    count = 0
    for i in vacancies:
        count += 1
        result.append(i)
        if count == top_count:
            break
    return result

if __name__ == "__main__":
    connector_sj = Connector("SuperJob-dump-keyword-python")
    data = connector_sj.connect()
    for item in data:
        for i in item["items"]:
            SuperJob(i["name"], i["href"], i["company"], i["salary"], i["description"],
                      "SuperJob-dump-keyword-python")

    sorting(Vacancy.sj_vacancies)
    for i in Vacancy.sj_vacancies:
        print(i)
    count = 0
    for i in get_top(Vacancy.sj_vacancies, 25):
        count += 1
        print(count, i)



