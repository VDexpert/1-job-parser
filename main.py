from engine_classes import*
from jobs_classes import*
import csv
from del_temp_file import*

def starter():
    key_word = input("Введите ключевое слово, по которому будем искать вакансии [python]: ")
    key_word = key_word.lower()
    if key_word == "":
        key_word = "python"

    quantity_vac = input("Введите количество вакансий, которое надо найти на каждом сервисе [1000]: ")
    if quantity_vac == "":
        quantity_vac = 1000

    hh = HH(quantity_vac, key_word)
    sj = SuperJob(quantity_vac, key_word)
    range_hh = quantity_vac // hh.per_page + 2
    range_sj = quantity_vac // sj.per_page + 2

    print("\n", "*"*10, "Извлечение данных с сайта hh.ru", "*"*10, "\n")
    for i in range(1, range_hh):
        hh.get_request(i)

    data_hh = Connector.all_connectors[hh.filename].connect()
    count_hh = 0
    print("\n", "*" * 10, "Форматирование данных с сайта hh.ru", "*" * 10, "\n")
    for i in data_hh:
        count_hh += 1
        HHVacancy(i["name"], i["href"], i["company"], i["salary"], i["description"],
                  hh.filename)
        if count_hh == quantity_vac:
            break

    outfile_hh = f"HH-vacancies-{hh.key_word}.csv"
    print("\n", "*" * 10, f"Загрузка данных в файл {outfile_hh}", "*" * 10, "\n")
    with open(outfile_hh, "w") as f:
        for i in Vacancy.hh_vacancies:
            file_writer = csv.writer(f)
            file_writer.writerow([str(i)])
    print("\n", "*" * 10, f"Данные загружены в файл {outfile_hh}", "*" * 10, "\n")

    print("\n", "*" * 10, "Извлечение данных с сайта superjob.ru", "*" * 10, "\n")
    for i in range(1, range_sj):
        sj.get_request(i)

    data_sj = Connector.all_connectors[sj.filename].connect()
    count_sj = 0
    print("\n", "*" * 10, "Форматирование данных с сайта superjob.ru", "*" * 10, "\n")
    for i in  data_sj:
        count_sj += 1
        SJVacancy(i["name"], i["href"], i["company"], i["salary"], i["description"],
                  sj.filename)
        if count_sj == quantity_vac:
            break

    outfile_sj = f"SJ-vacancies-{sj.key_word}.csv"
    print("\n", "*" * 10, f"Загрузка данных в файл {outfile_sj}", "*" * 10, "\n")
    with open(outfile_sj, "w") as f:
        for i in Vacancy.sj_vacancies:
            file_writer = csv.writer(f)
            file_writer.writerow([str(i)])
    print("\n", "*" * 10, f"Данные загружены в файл {outfile_sj}", "*" * 10, "\n")

    print(f"Вы можете произвести с выгруженными данными сортировку \n"
          f"всех вакансий по уровню зарплаты (для этого введите 1) или выгрузить \n"
          f"ТОП-количество самых высокооплачиваемых вакансий (для этого введите 2) \n"
          f"Для выхода из программы наберите stop \n")

    additionals = input("Сортировка (1) или ТОП-вакансий (2)? Введите 1 или 2 [1]: ")
    orders = {"1": "desc", "2": "asc"}

    if additionals == "":
        additionals = "1"
    else:
        additionals = additionals.replace(" ", "")

    if additionals.lower().replace(" ", "") == "stop":
        return f"Программа завершена"

    if additionals == "1":
        order = input("По убыванию (1) или по возрастанию (2) сортировать вакансии? Ваш ответ [1]: ")
        if order == "":
            order = orders["1"]
        else:
            order = orders[order.replace(" ", "")]

        outfile_hh_sort = f"HH-sort-in-{order}-vacancies.csv"
        with open(outfile_hh_sort, "w") as f:
            for i in sorting(Vacancy.hh_vacancies, order):
                file_writer = csv.writer(f)
                file_writer.writerow([str(i)])
        print("\n", "*" * 10, f"Отсортированные вакансии в файле HH-sort-in-{order}-vacancies.csv", "*" * 10, "\n")

        outfile_sj_sort = f"SJ-sort-in-{order}-vacancies.csv"
        with open(outfile_sj_sort, "w") as f:
            for i in sorting(Vacancy.sj_vacancies, order):
                file_writer = csv.writer(f)
                file_writer.writerow([str(i)])
        print("\n", "*" * 10, f"Отсортированные вакансии в файле SJ-sort-in-{order}-vacancies.csv", "*" * 10, "\n")

    elif additionals == "2":
        top_count = input("Введите количество ТОП-вакансий, которые нужно вывести [30]: ")
        if top_count == "":
            top_count = 30
        else:
            top_count = int(top_count.replace(" ", ""))

        outfile_hh_top = f"HH-TOP-{top_count}-vacancies.csv"
        with open(outfile_hh_top, "w") as f:
            for i in get_top(Vacancy.hh_vacancies, top_count, orders["1"]):
                file_writer = csv.writer(f)
                file_writer.writerow([str(i)])
        print("\n", "*" * 10, f"ТОП-{top_count} вакансий загружены в файл {outfile_hh_top}", "*" * 10, "\n")

        outfile_sj_top = f"SJ-TOP-{top_count}-vacancies.csv"
        with open(outfile_sj_top, "w") as f:
            for i in get_top(Vacancy.sj_vacancies, top_count, orders["1"]):
                file_writer = csv.writer(f)
                file_writer.writerow([str(i)])
        print("\n", "*" * 10, f"ТОП-{top_count} вакансий загружены в файл {outfile_sj_top}", "*" * 10, "\n")

    del_temp_json(hh.filename)
    del_temp_json(sj.filename)

    return True


if __name__ == "__main__":
    starter()