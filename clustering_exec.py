#coding: utf-8
import argparse
import csv
import math
from cluster import get_clusters, single_link_proximity, complete_link_proximity


METHODS = {
    "SINGLE_LINK": single_link_proximity,
    "COMPLETE_LINK": complete_link_proximity
}


def prepare_data(file_path, min_value, min_param_count, obj_column=0, param_column=1, value_column=2, delimiter="|"):
    """Читает файл, содержащий набор объектов, параметров и их координат. Собирает словарь следующего типа:
    {obj1: {param1: ln(value1), param2: ln(value2),...}, ...}

    Берутся только параметры value которых не менее min_value.
    Из всех объектов, оставляются только те, у которых количество параметров не менее min_param_count
    """
    res = {}
    f = open(file_path, "r")
    reader = csv.reader(f, delimiter=delimiter)

    for row in reader:
        obj = row[obj_column]
        param = row[param_column]
        value = float(row[value_column])

        if value > min_value:
            #на случай, если внутри был разделитель
            res.setdefault(obj, {})
            res[obj][param] = math.log(value)

    for obj in res.keys():
        if len(res[obj]) < min_param_count:
            res.pop(obj)

    f.close()

    return res


def obj_length(obj_dict):
    res = 0
    for key, value in obj_dict.items():
        res += value * value
    return math.sqrt(res)


def cosine_similarity(firs_obj_dict, second_obj_dict):
    up = 0.0
    for key in firs_obj_dict:
        if key in second_obj_dict:
            up += firs_obj_dict[key] * second_obj_dict[key]
    if up > 0:
        return up / (obj_length(firs_obj_dict) * obj_length(second_obj_dict))
    return 0.0


def get_objects_similarity_matrix(data_dict):
    """не забываем, что матрица обратно симметричная
    """
    #легче работать с цифрами
    keys = data_dict.keys()
    keys_length = len(keys)

    matrix = []
    #вуаля симметричность
    for i in range(keys_length):
        matrix.append([0] * keys_length)
        for j in range(i + 1):
            first_obj_dict = data_dict[keys[i]]
            second_obj_dict = data_dict[keys[j]]
            cos_sim = cosine_similarity(first_obj_dict, second_obj_dict)
            matrix[i][j] = matrix[j][i] = cos_sim
    return keys, matrix


if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(10000)

    parser = argparse.ArgumentParser(description="Скрипт кластеризующий данные по входному csv-файлу вида: "
                                                 "obj | param | value")
    parser.add_argument("-c", "--csv-file", dest="csv_file_path", type=str, required=True,
                        help="Путь до csv-файла с данными")
    parser.add_argument("-d", "--dot-file", dest="dot_file_path", type=str, required=True,
                        help="Файл в который будет сохранено dot-представление кластера")
    parser.add_argument("-v", "--min-value", dest="min_value", type=int, default=1,
                        help="Берутся только параметры значения которых не меньше заданного. По умолчанию 1")
    parser.add_argument("-p", "--min-param-count", dest="min_param_count", type=int, default=5,
                        help="Рассматриваюся только объекты количество параметров у которых "
                             "не меньше заданного. По умолчанию 5")
    parser.add_argument("-m", "--method", dest="method", type=str, choices=METHODS.keys(), default="COMPLETE_LINK",
                        help="Метод кластеризации. По умолчанию COMPLETE_LINK")

    parser.add_argument("-o", "--obj_column", dest="obj_column", default=0, type=int,
                        help="Колонка с объектом. По умолчанию 0")
    parser.add_argument("-a", "--param_column", dest="param_column", default=1, type=int,
                        help="Колонка с параметром. По умолчанию 1")
    parser.add_argument("-l", "--value_column", dest="value_column", default=2, type=int,
                        help="Колонка со значением параметра. По умолчанию 2")
    parser.add_argument("--count_cpcc", dest="count_cpcc", help="Считать Cophenetic Correlation Coefficient",
                        action="store_true")

    args = parser.parse_args()

    data_dict = prepare_data(args.csv_file_path, args.min_value, args.min_param_count,
                             args.obj_column, args.param_column, args.value_column)
    keys_list, matrix = get_objects_similarity_matrix(data_dict)
    cluster = get_clusters(matrix, METHODS[args.method], args.count_cpcc)

    f = open(args.dot_file_path, "w")
    f.write(cluster.get_dot_graph_str(keys_list))
    f.close()
