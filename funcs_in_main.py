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

def push_to_stack_by_init_vacancy(class_of_vacancy, stack, data, filename, quantity=None):
    limiter = 0
    count_vac = 0
    for vac in data:
        limiter += 1
        count_vac += 1
        stack.push(class_of_vacancy(name=vac["name"], href=vac["href"], company=vac["company"], experience=vac["experience"],
                              salary=vac["salary"], description=vac["description"], filename=filename,
                              count_vac=count_vac))
        if limiter == quantity:
            break