#coding: utf-8
import argparse

import math
from cluster import get_clusters, simple_link_proximity, complete_link_proximity


METHODS = {
    "SIMPLE_LINK": simple_link_proximity,
    "COMPLETE_LINK": complete_link_proximity
}


def prepare_data(file_path, min_count, min_adj_count, delimiter="|"):
    """Читает файл, содержащий набор прилаг + существительное и собирает словарь следующего типа:
    {сущ1: {прилаг1: ln(кол-во встреч), прилаг2: ln(кол-во встре),...}, ...}

    Берутся только комбинации, которые встречаются не менее min_count раз.
    Из всех существительных, оставляются только те, у которых количество связных прилагательных
    не менее min_adj_count
    """
    res = {}
    f = open(file_path, "r")
    for line in f:
        parts = line.strip().split(delimiter)
        if len(parts) >= 2:
            try:
                count = int(parts[-1])
            except TypeError:
                continue

            if count > min_count:
                #на случай, если внутри был разделитель
                phrase = delimiter.join(parts[:-1])
                phrase_parts = phrase.split()
                if len(phrase_parts) == 2:
                    adj, noun = phrase_parts
                    res.setdefault(noun, {})
                    res[noun][adj] = math.log(count)
    for noun in res.keys():
        if len(res[noun]) < min_adj_count:
            res.pop(noun)
    return res


def word_module(word_dict):
    res = 0
    for key, value in word_dict.items():
        res += value * value
    return math.sqrt(res)


def cosine_similarity(firs_noun_dict, second_noun_dict):
    up = 0.0
    for key in firs_noun_dict:
        if key in second_noun_dict:
            up += firs_noun_dict[key] * second_noun_dict[key]
    if up > 0:
        return up / (word_module(firs_noun_dict) * word_module(second_noun_dict))
    return 0.0


def get_nouns_similarity_matrix(data_dict):
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
            first_noun_dict = data_dict[keys[i]]
            second_noun_dict = data_dict[keys[j]]
            cos_sim = cosine_similarity(first_noun_dict, second_noun_dict)
            matrix[i][j] = matrix[j][i] = cos_sim

    return keys, matrix


if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(10000)

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--csv-file", dest="csv_file_path", type=str, required=True,
                        help="Путь до файла с csv")
    parser.add_argument("-d", "--dot-file", dest="dot_file_path", type=str, required=True,
                        help="Файл в который будет сохранено dot-представление кластера")
    parser.add_argument("-t", "--min-count", dest="min_count", type=int, default=1,
                        help="Берутся только комбинации, количества встреч которых не меньше введенного значения."
                             "По умолчанию 1")
    parser.add_argument("-a", "--min-adj-count", dest="min_adj_count", type=int, default=5,
                        help="Рассматриваюся только существительные, количество связных прилагательных у которых, "
                             "не меньше введеного значения. По умолчанию 5")
    parser.add_argument("-m", "--method", dest="method", type=str, choices=METHODS.keys(), default="COMPLETE_LINK",
                        help="Метод кластеризации")

    args = parser.parse_args()

    data_dict = prepare_data(args.csv_file_path, args.min_count, args.min_adj_count)
    keys_list, matrix = get_nouns_similarity_matrix(data_dict)
    cluster = get_clusters(matrix, METHODS[args.method])

    f = open(args.dot_file_path, "w")
    f.write(cluster.get_dot_graph_str(keys_list))
    f.close()
