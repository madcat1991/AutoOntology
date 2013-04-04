#coding: utf-8

"""
Скрипт для слияния двух csv-файлов с данными. На данный момент упрощенная версия, которая работает со словарем
"""
import argparse
import csv


def merge_csv(first_csv_path, second_csv_path, result_csv_path, delimiter="|"):
    """Сливает два csv-файла с данными в один.
    У всех файлов должен быть один тип представления: obj | param | count
    """
    res = {}

    first_csv = open(first_csv_path, "r")
    reader = csv.reader(first_csv, delimiter=delimiter)
    for row in reader:
        key = (row[0], row[1])
        res.setdefault(key, 0)
        res[key] += int(row[2])
    first_csv.close()

    second_csv = open(second_csv_path, "r")
    reader = csv.reader(second_csv, delimiter=delimiter)
    for row in reader:
        key = (row[0], row[1])
        res.setdefault(key, 0)
        res[key] += int(row[2])
    second_csv.close()

    result_csv = open(result_csv_path, "w")
    writer = csv.writer(result_csv, delimiter=delimiter)
    for key, value in res.items():
        writer.writerow([key[0], key[1], value])
    result_csv.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт для слияния двух csv-файлов с данными. "
                                                 "У файлов должен быть один тип представления: obj | param | count")

    parser.add_argument("-f", "--first-csv", dest="first_csv", type=str, required=True,
                        help="Первый csv-файл")
    parser.add_argument("-s", "--second-csv", dest="second_csv", type=str, required=True,
                        help="Второй csv-файл")
    parser.add_argument("-r", "--result-csv", dest="result_csv", type=str, required=True,
                        help="Результат")

    args = parser.parse_args()
    merge_csv(args.first_csv, args.second_csv, args.result_csv)
