#coding: utf-8
import argparse

import math
from cluster import get_clusters


def prepare_data(file_path, min_log, delimiter="|"):
    """Читает файл, содержащий набор прилаг + существительное и собирает словарь следующего типа:
    {сущ1: {прилаг1: ln(кол-во встреч), прилаг2: ln(кол-во встре),...}, ...}
    Для существительного берутся только прилагательные чей логорифм от количества встреч > min_log
    """
    res = {}
    f = open(file_path, "r")
    for line in f:
        if line:
            parts = line.strip().split(delimiter)
            phrase_parts = parts[0].split()
            if len(phrase_parts) == 2:
                adj, noun = phrase_parts
                count = float(parts[1])
                if count > 0 and math.log(count) > min_log:
                    res.setdefault(noun, {})
                    res[noun][adj] = math.log(count)
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
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--csv-file", dest="csv_file_path", type=str, required=True,
                        help="Путь до файла с csv")
    parser.add_argument("-d", "--dot-file", dest="dot_file_path", type=str, required=True,
                        help="Файл в который будет сохранено dot-представление кластера")
    parser.add_argument("-t", "--min-log", dest="min_log", type=float, default=0,
                        help="Берутся только строки, логорифм от количества встреч которого больше введенного значения."
                             "По умолчанию 0")

    args = parser.parse_args()

    data_dict = prepare_data(args.csv_file_path, args.min_log)
    keys_list, matrix = get_nouns_similarity_matrix(data_dict)
    cluster = get_clusters(matrix)

    f = open(args.dot_file_path, "w")
    f.write(cluster.get_dot_graph_str(keys_list))
    f.close()
