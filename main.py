from engine_classes import*
from jobs_classes import*
from funcs_in_main import*
from data_structures import*


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

    hh_engine = HH(quantity_vac, key_word)
    sj_engine = SuperJob(quantity_vac, key_word)
    range_hh = quantity_vac // hh_engine.per_page + 1
    range_sj = quantity_vac // sj_engine.per_page + 1

    stack_hh_all = StackVacancies()
    stack_sj_all = StackVacancies()

    print("\n", "*"*10, "Парсинг данных с сайта hh.ru", "*"*10, "\n")
    for page in range(1, range_hh):
        hh_engine.get_request(page)

    data_hh = Connector.all_connectors[hh_engine.filename_json].connect()
    print("\n", "*" * 10, "Форматирование данных с сайта hh.ru", "*" * 10, "\n")
    add_to_structure(HHVacancy, stack_hh_all, data_hh, hh_engine.filename_json, quantity=quantity_vac)

    outfile_hh = f"HH-vacancies-{hh_engine.key_word}.csv"
    print("\n", "*" * 10, f"Загрузка данных в файл {outfile_hh}", "*" * 10, "\n")
    write_vac_to_outfile(stack_hh_all.to_list(), outfile_hh, HHVacancy.get_count_of_vacancy(hh_engine.filename_json))
    print("\n", "*" * 10, f"Данные загружены в файл {outfile_hh}", "*" * 10, "\n")


    print("\n", "*" * 10, "Парсинг данных с сайта superjob.ru", "*" * 10, "\n")
    for page in range(1, range_sj):
        sj_engine.get_request(page)

    data_sj = Connector.all_connectors[sj_engine.filename_json].connect()
    print("\n", "*" * 10, "Форматирование данных с сайта superjob.ru", "*" * 10, "\n")
    add_to_structure(SJVacancy, stack_sj_all, data_sj, sj_engine.filename_json, quantity=quantity_vac)

    outfile_sj = f"SJ-vacancies-{sj_engine.key_word}.csv"
    print("\n", "*" * 10, f"Загрузка данных в файл {outfile_sj}", "*" * 10, "\n")
    write_vac_to_outfile(stack_sj_all.to_list(), outfile_sj, SJVacancy.get_count_of_vacancy(sj_engine.filename_json))
    print("\n", "*" * 10, f"Данные загружены в файл {outfile_sj}", "*" * 10, "\n")

    print(f"Вы можете произвести с выгруженными данными сортировку всех вакансий по зарплате (для этого введите 1) "
          f"или выгрузить ТОП-количество самых высокооплачиваемых вакансий (для этого введите 2) \n"
          f"или отобрать из файла только вакансии с определенным опытом работы (для этого введите 3) \n"
          f"или удалить из файла только вакансии с определенным опытом работы (для этого введите 4)"
          f"Для выхода из программы наберите stop \n")

    additionals = input("Сортировка (1) / ТОП-вакансий (2) / отбор по опыту (3) / удаление по опыту (4) "
                        "Введите 1, 2, 3 или 4 [1]: ")
    orders_sorting = {"1": "desc", "2": "asc"}

    if additionals == "":
        additionals = "1"
    else:
        additionals = additionals.replace(" ", "")

    if additionals.lower() == "stop":
        return f"Программа завершена"

    if additionals == "1":
        order = input("По убыванию (1) или по возрастанию (2) сортировать вакансии? Ваш ответ [1]: ")
        if order == "":
            order = orders_sorting["1"]
        else:
            order = orders_sorting[order.replace(" ", "")]

        outfile_hh_sort = f"HH-sort-in-{order}-vacancies.csv"
        write_vac_to_outfile(sorting(stack_hh_all.to_list(), order), outfile_hh_sort, quantity_vac)
        print("\n", "*" * 10, f"Отсортированные вакансии в файле HH-sort-in-{order}-vacancies.csv", "*" * 10, "\n")

        outfile_sj_sort = f"SJ-sort-in-{order}-vacancies.csv"
        write_vac_to_outfile(sorting(stack_sj_all.to_list(), order), outfile_sj_sort, quantity_vac)
        print("\n", "*" * 10, f"Отсортированные вакансии в файле SJ-sort-in-{order}-vacancies.csv", "*" * 10, "\n")


    elif additionals == "2":
        top_count = input("Введите количество ТОП-вакансий, которые нужно вывести [30]: ")
        if top_count == "":
            top_count = 30
        else:
            top_count = int(top_count.replace(" ", ""))

        outfile_hh_top = f"HH-TOP-{top_count}-vacancies.csv"
        top_vacancies_hh = get_top(stack_hh_all.to_list(), top_count, orders_sorting["1"])
        write_vac_to_outfile(top_vacancies_hh, outfile_hh_top, top_count)
        print("\n", "*" * 10, f"ТОП-{top_count} вакансий загружены в файл {outfile_hh_top}", "*" * 10, "\n")

        outfile_sj_top = f"SJ-TOP-{top_count}-vacancies.csv"
        top_vacancies_sj = get_top(stack_sj_all.to_list(), top_count, orders_sorting["1"])
        write_vac_to_outfile(top_vacancies_sj, outfile_sj_top, top_count)
        print("\n", "*" * 10, f"ТОП-{top_count} вакансий загружены в файл {outfile_sj_top}", "*" * 10, "\n")


    elif additionals == "3":

        sel_exper = input(f"ОТБОР ВАКАНСИЙ ПО ОПЫТУ РАБОТЫ \n"
                           f"Значения поля опыта: 1 = 'Нет опыта', 2 = 'от 1 года до 3 лет', 3 = 'от 3 до 6 лет', 4 = 'более 6 лет' \n"
                           f"Введите значение опыта 1, 2, 3 или 4, по которым нужно отфильтровать вакансии [1: 'Нет опыта']: ")

        contain_exper = {"1": "нет опыта", "2": "от 1 года до 3 лет", "3": "от 3 до 6 лет", "4": "более 6 лет"}

        if sel_exper.replace(" ", "") == "":
            sel_exper = "нет опыта"
        else:
            sel_exper = contain_exper[sel_exper.replace(" ", "")]

        contain_id_exper = {"нет опыта": "noExperience", "от 1 года до 3 лет": "between1And3",
                            "от 3 до 6 лет": "between3And6", "более 6 лет": "moreThan6"}
        id_sel_exper = contain_id_exper[sel_exper]

        query_sel = {"experience": sel_exper}

        outfile_hh_select = f"HH-select-vacancies-for-{id_sel_exper}.csv"
        print("\n", "*" * 10, f"Отбор данных в файл {outfile_hh_select}", "*" * 10, "\n")
        selecting_json_hh = Connector.all_connectors[hh_engine.filename_json].select(query_sel)
        ll_hh_selecting = LinkedListVacancies()
        add_to_structure(HHVacancy, ll_hh_selecting, selecting_json_hh, hh_engine.filename_json)
        write_vac_to_outfile(ll_hh_selecting.to_list(), outfile_hh_select, HHVacancy.get_count_of_vacancy(hh_engine.filename_json))
        print("\n", "*" * 10, f"Селективные данные в файле {outfile_hh_select}", "*" * 10, "\n")

        outfile_sj_select = f"SJ-select-vacancies-for-{id_sel_exper}.csv"
        print("\n", "*" * 10, f"Отбор данных в файл {outfile_sj_select}", "*" * 10, "\n")
        selecting_json_sj = Connector.all_connectors[sj_engine.filename_json].select(query_sel)
        ll_sj_selecting = LinkedListVacancies()
        add_to_structure(SJVacancy, ll_sj_selecting, selecting_json_sj, hh_engine.filename_json)
        write_vac_to_outfile(ll_sj_selecting.to_list(), outfile_sj_select, SJVacancy.get_count_of_vacancy(sj_engine.filename_json))
        print("\n", "*" * 10, f"Селективные данные в файле {outfile_sj_select}", "*" * 10, "\n")

        search_vacancy(ll_hh_selecting, ll_sj_selecting)

    elif additionals == "4":

        del_exper = input(f"УДАЛЕНИЕ ВАКАНСИЙ ПО ОПЫТУ РАБОТЫ \n"
            f"Значения поля опыта: 1 = 'Нет опыта', 2 = 'от 1 года до 3 лет', 3 = 'от 3 до 6 лет', 4 = 'более 6 лет' \n"
            f"Введите значение опыта 1, 2, 3 или 4, по которым нужно удалять вакансии [1: 'Нет опыта']: ")

        contain_exper = {"1": "нет опыта", "2": "от 1 года до 3 лет", "3": "от 3 до 6 лет", "4": "более 6 лет"}
        if del_exper.replace(" ", "") == "":
            del_exper = "нет опыта"
        else:
            del_exper = contain_exper[del_exper.replace(" ", "")]

        contain_id_exper = {"нет опыта": "noExperience", "от 1 года до 3 лет": "between1And3",
                            "от 3 до 6 лет": "between3And6", "более 6 лет": "moreThan6"}
        id_del_exper = contain_id_exper[del_exper]

        query_del = {"experience": del_exper}

        outfile_hh_del = f"HH-delete-vacancies-for-{id_del_exper}.csv"
        print("\n", "*" * 10, f"Удаление ненужных данных и загрузка нужных в файл {outfile_hh_del}", "*" * 10, "\n")
        without_deleting_json_hh = Connector.all_connectors[hh_engine.filename_json].delete(query_del)
        ll_hh_without_deleting = LinkedListVacancies()
        add_to_structure(HHVacancy, ll_hh_without_deleting, without_deleting_json_hh, hh_engine.filename_json)
        write_vac_to_outfile(ll_hh_without_deleting.to_list(), outfile_hh_del, HHVacancy.get_count_of_vacancy(hh_engine.filename_json))
        print("\n", "*" * 10, f"Данные удалены. Нужные данные в файле {outfile_hh_del}", "*" * 10, "\n")

        outfile_sj_del = f"SJ-delete_vacancies-for-{id_del_exper}.csv"
        print("\n", "*" * 10, f"Удаление ненужных данных и загрузка нужных в файл {outfile_sj_del}", "*" * 10, "\n")
        without_deleting_json_sj = Connector.all_connectors[sj_engine.filename_json].delete(query_del)
        ll_sj_without_deleting = LinkedListVacancies()
        add_to_structure(SJVacancy, ll_sj_without_deleting, without_deleting_json_sj, hh_engine.filename_json)
        write_vac_to_outfile(ll_sj_without_deleting.to_list(), outfile_sj_del, SJVacancy.get_count_of_vacancy(sj_engine.filename_json))
        print("\n", "*" * 10, f"Данные удалены. Нужные данные в файле {outfile_sj_del}", "*" * 10, "\n")

        search_vacancy(ll_hh_without_deleting, ll_sj_without_deleting)

    del_temp_json(hh_engine.filename_json)
    del_temp_json(sj_engine.filename_json)

    return True

if __name__ == "__main__":
    starter()