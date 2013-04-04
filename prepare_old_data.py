#coding: utf-8
import argparse
import csv


def prepare(old_file_path, new_file_path, get_columns_func, delimiter="|", text_column=1, count_column=2):
    file_to_read = open(old_file_path, "r")
    file_to_write = open(new_file_path, "w")

    reader = csv.reader(file_to_read, delimiter=delimiter)
    writer = csv.writer(file_to_write, delimiter="|")

    for row in reader:
        data = get_columns_func(row, text_column, count_column)
        if data:
            writer.writerow(data)

    file_to_read.close()
    file_to_write.close()


def get_columns_for_row(row, text_column, count_column, words_count_limit):
    text = row[text_column].strip()

    text_parts = text.split()
    if len(text_parts) == words_count_limit:
        count = row[count_column]
        left_part = text_parts[0]
        right_part = " ".join(text_parts[1:])
        return [left_part, right_part, count]
    return None


def get_columns_for_verb(row, text_column, count_column):
    return get_columns_for_row(row, text_column, count_column, 3)


def get_columns_for_noun(row, text_column, count_column):
    return get_columns_for_row(row, text_column, count_column, 2)


METHODS = {
    "VERB": get_columns_for_verb,
    "NOUN": get_columns_for_noun,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--file-to-read", dest="read_file_path", type=str, required=True,
                        help="Файл из которого будут читаться данные")
    parser.add_argument("-w", "--file-to-write", dest="write_file_path", type=str, required=True,
                        help="Файл в который будет писаться результат")
    parser.add_argument("-d", "--delimiter", dest="delimiter", type=str, default="|",
                        help="Разделитель в файле, из которого производится чтение. По умолчанию - '|'")
    parser.add_argument("-t", "--text_column", dest="text_column", default=0, type=int,
                        help="Колонка с текстом. По умолчанию 0")
    parser.add_argument("-c", "--count_column", dest="count_column", default=1, type=int,
                        help="Колонка с количеством. По умолчанию 1")
    parser.add_argument("-m", "--method", dest="method", default="VERB", type=str, choices=METHODS.keys(),
                        help="Метод разбора. По умолчанию VERB")

    args = parser.parse_args()
    prepare(args.read_file_path, args.write_file_path, METHODS[args.method],
            args.delimiter, args.text_column, args.count_column)
