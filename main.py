from engine_classes import*
from jobs_classes import*
from del_temp_file import*
from write_to_outfile import write_vac_to_outfile
import time
import math

def starter():
    key_word = input("Введите ключевое слово, по которому будем искать вакансии [python]: ")
    key_word = key_word.lower()
    if key_word == "":
        key_word = "python"

    quantity_vac = input("Введите количество вакансий, которое надо найти на каждом сервисе [100]: ")
    if quantity_vac == "":
        quantity_vac = 100
    else:
        quantity_vac = int(quantity_vac)

    hh = HH(quantity_vac, key_word)
    sj = SuperJob(quantity_vac, key_word)
    range_hh = quantity_vac // hh.per_page + 1
    range_sj = quantity_vac // sj.per_page + 1

    print("\n", "*"*10, "Парсинг данных с сайта hh.ru", "*"*10, "\n")
    start = time.perf_counter()
    for page in range(1, range_hh):
        hh.get_request(page)
    print(f"Время парсинга {(time.perf_counter() - start) // 60} минут {round((time.perf_counter() - start) % 60)} секунд")

    data_hh = Connector.all_connectors[hh.filename].connect()
    count_hh = 0
    print("\n", "*" * 10, "Форматирование данных с сайта hh.ru", "*" * 10, "\n")
    for vac in data_hh:
        count_hh += 1
        HHVacancy(name=vac["name"], href=vac["href"], company=vac["company"], experience=vac["experience"],
                  salary=vac["salary"], description=vac["description"], filename=hh.filename)
        if count_hh == quantity_vac:
            break

    outfile_hh = f"HH-vacancies-{hh.key_word}.csv"
    start = time.perf_counter()
    print("\n", "*" * 10, f"Загрузка данных в файл {outfile_hh}", "*" * 10, "\n")
    write_vac_to_outfile(Vacancy.hh_vacancies, outfile_hh)
    print("\n", "*" * 10, f"Данные загружены в файл {outfile_hh}", "*" * 10, "\n")
    print(f"Время загрузки {(time.perf_counter() - start) // 60} минут {round((time.perf_counter() - start) % 60)} секунд")


    start = time.perf_counter()
    print("\n", "*" * 10, "Парсинг данных с сайта superjob.ru", "*" * 10, "\n")
    for page in range(1, range_sj):
        sj.get_request(page)
    print(f"Время парсинга {(time.perf_counter() - start) // 60} минут {round((time.perf_counter() - start) % 60)} секунд")

    data_sj = Connector.all_connectors[sj.filename].connect()
    count_sj = 0
    print("\n", "*" * 10, "Форматирование данных с сайта superjob.ru", "*" * 10, "\n")
    for vac in  data_sj:
        count_sj += 1
        SJVacancy(name=vac["name"], href=vac["href"], company=vac["company"], experience=vac["experience"],
                  salary=vac["salary"], description=vac["description"], filename=sj.filename)
        if count_sj == quantity_vac:
            break

    start = time.perf_counter()
    outfile_sj = f"SJ-vacancies-{sj.key_word}.csv"
    print("\n", "*" * 10, f"Загрузка данных в файл {outfile_sj}", "*" * 10, "\n")
    write_vac_to_outfile(Vacancy.sj_vacancies, outfile_sj)
    print("\n", "*" * 10, f"Данные загружены в файл {outfile_sj}", "*" * 10, "\n")
    print(f"Время загрузки {(time.perf_counter() - start) // 60} минут {round((time.perf_counter() - start) % 60)} секунд \n")

    print(f"Вы можете произвести с выгруженными данными сортировку всех вакансий по зарплате (для этого введите 1) "
          f"или выгрузить ТОП-количество самых высокооплачиваемых вакансий (для этого введите 2) \n"
          f"или отобрать из файла только вакансии с определенным опытом работы (для этого введите 3) \n"
          f"или удалить из файла только вакансии с определенным опытом работы (для этого введите 4)"
          f"Для выхода из программы наберите stop \n")

    additionals = input("Сортировка (1) / ТОП-вакансий (2) / отбор по опыту (3) / удаление по опыту (4) "
                        "Введите 1, 2, 3 или 4 [1]: ")
    orders = {"1": "desc", "2": "asc"}

    if additionals == "":
        additionals = "1"
    else:
        additionals = additionals.replace(" ", "")

    if additionals.lower() == "stop":
        return f"Программа завершена"

    if additionals == "1":
        order = input("По убыванию (1) или по возрастанию (2) сортировать вакансии? Ваш ответ [1]: ")
        if order == "":
            order = orders["1"]
        else:
            order = orders[order.replace(" ", "")]

        outfile_hh_sort = f"HH-sort-in-{order}-vacancies.csv"
        write_vac_to_outfile(sorting(Vacancy.hh_vacancies, order), outfile_hh_sort)
        print("\n", "*" * 10, f"Отсортированные вакансии в файле HH-sort-in-{order}-vacancies.csv", "*" * 10, "\n")

        outfile_sj_sort = f"SJ-sort-in-{order}-vacancies.csv"
        write_vac_to_outfile(sorting(Vacancy.sj_vacancies, order), outfile_sj_sort)
        print("\n", "*" * 10, f"Отсортированные вакансии в файле SJ-sort-in-{order}-vacancies.csv", "*" * 10, "\n")


    elif additionals == "2":
        top_count = input("Введите количество ТОП-вакансий, которые нужно вывести [30]: ")
        if top_count == "":
            top_count = 30
        else:
            top_count = int(top_count.replace(" ", ""))

        outfile_hh_top = f"HH-TOP-{top_count}-vacancies.csv"
        write_vac_to_outfile(get_top(Vacancy.hh_vacancies, top_count, orders["1"]), outfile_hh_top)
        print("\n", "*" * 10, f"ТОП-{top_count} вакансий загружены в файл {outfile_hh_top}", "*" * 10, "\n")

        outfile_sj_top = f"SJ-TOP-{top_count}-vacancies.csv"
        write_vac_to_outfile(get_top(Vacancy.sj_vacancies, top_count, orders["1"]), outfile_sj_top)
        print("\n", "*" * 10, f"ТОП-{top_count} вакансий загружены в файл {outfile_sj_top}", "*" * 10, "\n")


    elif additionals == "3":

        sel_exper = input(f"ОТБОР ВАКАНСИЙ ПО ОПЫТУ РАБОТЫ \n"
                           f"Значения поля опыта: 1 = 'Нет опыта', 2 = 'от 1 года до 3 лет', 3 = 'от 3 до 6 лет', 4 = 'более 6 лет' \n"
                           f"Введите значение опыта 1, 2, 3 или 4, по которым нужно отфильтровать вакансии [1: 'Нет опыта']: ")

        contain_sel_exper = {"1": "нет опыта", "2": "от 1 года до 3 лет", "3": "от 3 до 6 лет", "4": "более 6 лет"}

        if sel_exper.replace(" ", "") == "":
            sel_exper = "нет опыта"
        else:
            sel_exper = contain_sel_exper[sel_exper.replace(" ", "")]

        contain_id_exper = {"нет опыта": "noExperience", "от 1 года до 3 лет": "between1And3",
                            "от 3 до 6 лет": "between3And6", "более 6 лет": "moreThan6"}
        id_sel_exper = contain_id_exper[sel_exper]

        query_sel = {"experience": sel_exper}

        outfile_hh_select = f"HH-select-vacancies-for-{id_sel_exper}.csv"
        print("\n", "*" * 10, f"Отбор данных в файл {outfile_hh_select}", "*" * 10, "\n")
        write_vac_to_outfile(Connector.all_connectors[hh.filename].select(query_sel), outfile_hh_select)
        print("\n", "*" * 10, f"Селективные данные в файле {outfile_hh_select}", "*" * 10, "\n")

        outfile_sj_select = f"SJ-select-vacancies-for-{id_sel_exper}.csv"
        print("\n", "*" * 10, f"Отбор данных в файл {outfile_sj_select}", "*" * 10, "\n")
        write_vac_to_outfile(Connector.all_connectors[sj.filename].select(query_sel), outfile_sj_select)
        print("\n", "*" * 10, f"Селективные данные в файле {outfile_sj_select}", "*" * 10, "\n")

    elif additionals == "4":

        del_exper = input(f"УДАЛЕНИЕ ВАКАНСИЙ ПО ОПЫТУ РАБОТЫ \n"
            f"Значения поля опыта: 1 = 'Нет опыта', 2 = 'от 1 года до 3 лет', 3 = 'от 3 до 6 лет', 4 = 'более 6 лет' \n"
            f"Введите значение опыта 1, 2, 3 или 4, по которым нужно удалять вакансии [1: 'Нет опыта']: ")

        contain_del_exper = {"1": "Нет опыта", "2": "от 1 года до 3 лет", "3": "от 3 до 6 лет", "4": "более 6 лет"}
        if del_exper.replace(" ", "") == "":
            del_exper = "Нет опыта"
        else:
            del_exper = contain_del_exper[del_exper.replace(" ", "")]

        contain_id_exper = {"Нет опыта": "noExperience", "от 1 года до 3 лет": "between1And3",
                            "от 3 до 6 лет": "between3And6", "более 6 лет": "moreThan6"}
        id_del_exper = contain_id_exper[del_exper]

        query_del = {"experience": del_exper}

        outfile_hh_del = f"HH-delete-vacancies-for-{id_del_exper}.csv"
        print("\n", "*" * 10, f"Удаление ненужных данных и загрузка нужных в файл {outfile_hh_del}", "*" * 10, "\n")
        write_vac_to_outfile(Connector.all_connectors[hh.filename].delete(query_del), outfile_hh_del)
        print("\n", "*" * 10, f"Данные удалены. Нужные данные в файле {outfile_hh_del}", "*" * 10, "\n")

        outfile_sj_del = f"SJ-delete_vacancies-for-{id_del_exper}.csv"
        print("\n", "*" * 10, f"Удаление ненужных данных и загрузка нужных в файл {outfile_sj_del}", "*" * 10, "\n")
        write_vac_to_outfile(Connector.all_connectors[sj.filename].delete(query_del), outfile_sj_del)
        print("\n", "*" * 10, f"Данные удалены. Нужные данные в файле {outfile_sj_del}", "*" * 10, "\n")

    del_temp_json(hh.filename)
    del_temp_json(sj.filename)

    return True

if __name__ == "__main__":
    starter()