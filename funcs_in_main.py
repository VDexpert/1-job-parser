import os
import csv


def del_temp_json(filename):
    path = os.path.abspath(filename)
    os.remove(path)

    return True

def write_vac_to_outfile(vacancies, filename, quantity):
    with open(filename, "w", encoding="utf-8") as f:
        count = 0
        for vac in vacancies:
            count += 1
            file_writer = csv.writer(f)
            if count == 1:
                file_writer.writerow([f"Всего вакансий в документе: {quantity}"])
                file_writer.writerow([str(vac)])
                continue
            file_writer.writerow([str(vac)])

def add_to_structure(class_of_vacancy, structure, data, filename, quantity=None):
    limiter = 0
    count_vac = 0

    if structure.__class__.__name__ == "StackVacancies":
        for vac in data:
            limiter += 1
            count_vac += 1
            structure.push(class_of_vacancy(name=vac["name"], href=vac["href"], company=vac["company"], experience=vac["experience"],
                                  salary=vac["salary"], description=vac["description"], filename=filename,
                                  count_vac=count_vac))
            if limiter == quantity:
                break
    elif structure.__class__.__name__ == "LinkedListVacancies":
        for vac in data:
            limiter += 1
            count_vac += 1
            structure.insert_end(class_of_vacancy(name=vac["name"], href=vac["href"], company=vac["company"], experience=vac["experience"],
                                  salary=vac["salary"], description=vac["description"], filename=filename,
                                  count_vac=count_vac))
            if limiter == quantity:
                break

def search_vacancy(ll_vac_hh, ll_vac_sj):
    print("ВЫВОД ПОДРОБНОГО ОПИСАНИЯ ИНТЕРЕСУЕМОЙ ВАКАНСИИ")
    dict_ll = {"HH": ll_vac_hh, "SJ": ll_vac_sj}
    while True:
        query = input("\nВведите, с какого сервиса вывести описание вакансии из последних двух файлов : <HH> или <SJ> \n"
                      "и через пробел введите номер интересуемой вакансии или введите <stop> для выхода из программы: ")

        if query.replace(" ", "") == "stop":
            print("\nПрограмма завершена")
            break

        if len(query.split()) != 2:
            print("\nЗапрос некорректен, повторите запрос\n")
            continue

        id_vac = int(query.split()[1])
        source = query.split()[0].upper()
        data = dict_ll[source].search_by_id(id_vac)
        print(f"\nПодробное описание вакансии № {id_vac} c последней выгрузки с сайта {source}: \n"
              f"{data}\n"
              f"{data.description}\n")



