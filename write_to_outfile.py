import csv

def write_vac_to_outfile(vacancies, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for vac in vacancies:
            file_writer = csv.writer(f)
            file_writer.writerow([str(vac)])