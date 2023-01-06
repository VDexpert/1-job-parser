import csv

def write_vac_to_outfile(vacancies, filename, quantity):
    with open(filename, "w", encoding="utf-8") as f:
        count = 0
        for vac in vacancies:
            count += 1
            file_writer = csv.writer(f)
            if count == 1:
                file_writer.writerow([f"Всего вакансий в документе: {quantity}"])
                continue
            file_writer.writerow([str(vac)])

if __name__ == "__main__":
    write_vac_to_outfile([10, 20, 30, 40, 50], "test.csv", 100)