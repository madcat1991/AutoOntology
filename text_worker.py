#coding: utf-8

import argparse
import itertools

from nltk import pos_tag, sent_tokenize, word_tokenize, RegexpParser
from redis import Redis
from pymorphy import get_morph


SIMPLE_GRAMMAR = u"CHUNK :{<JJ.*>+ <N.*>}"
COMPLEX_GRAMMAR = u"""
    REL: {<,><CC>}
    REL: {<,> | <CC>}
    NOUN: {<N.*>(<REL><N.*>)*}
    ADJECTIVE: {<JJ.*>(<REL><JJ.*>)*}
    CHUNK: {<ADJECTIVE><NOUN>}
"""


def get_adj_noun_list_from_chunk(chunk_subtree):
    """Вытаскивает из chunk наборы: прилаг + существительное
    """
    adjectives = []
    nouns = []
    for s in chunk_subtree.leaves():
        word, tag = s
        if tag and tag[0] == "J":
            adjectives.append(word)
        elif tag and tag[0] == "N":
            nouns.append(word)

    result = []
    #находим все комбинации
    for adj_noun in itertools.product(adjectives, nouns):
        result.append(adj_noun)
    return result


def normilize_adj_noun_list(adj_noun_list, morph):
    """Приводит к нормально форме список кортжей (прилагательное, существительно)
    """
    res = []
    for adj, noun in adj_noun_list:
        normilized_adj = morph.normalize(adj.upper())
        normilized_noun = morph.normalize(noun.upper())
        if isinstance(normilized_adj, set):
            normilized_adj = normilized_adj.pop()
        if isinstance(normilized_noun, set):
            normilized_noun = normilized_noun.pop()
        res.append((normilized_adj, normilized_noun))
    return res


def data_gathering_iterator(file_path, morph, grammar=COMPLEX_GRAMMAR):
    """На каждой итерации возвращает список полученных из одной строки комбинаций прилаг + сущ.
    Элемент списка кортеж (прилагательное, существительно).
    Прилагательное и существительное приведены к нормальной форме

    :param file_path: путь до файла с данными. Файл должен быть в формате UTF-8
    :param morph: морфология
    """
    chunk_parser = RegexpParser(grammar)
    f = open(file_path, "r")

    for line in f:
        try:
            line = line.decode('utf-8')
        except UnicodeDecodeError:
            continue
        line = line.strip()
        #разбиваем на предложения
        for sentence in sent_tokenize(line):
            sentence = sentence.strip()
            if sentence:
                tokens = word_tokenize(sentence)

                tagged_tokens = pos_tag(tokens)
                tree = chunk_parser.parse(tagged_tokens)
                for subtree in tree.subtrees():
                    if subtree.node == u"CHUNK":
                        adj_noun_list = get_adj_noun_list_from_chunk(subtree)
                        yield normilize_adj_noun_list(adj_noun_list, morph)


def get_data_and_statistic(file_path, morph, rd):
    for adj_noun_list in data_gathering_iterator(file_path, morph):
        for adj_noun in adj_noun_list:
            adj_noun_str = u" ".join(adj_noun)
            rd.incr(adj_noun_str, 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", dest="file_path", type=str, required=True,
                        help="Файл из которого будет браться текст")
    parser.add_argument("-m", "--morph_dir", dest="morph_dir", type=str, required=True,
                        help="Директория в которой лежат словари pymorphy")
    parser.add_argument("-s", "--host", dest="host", default="localhost", type=str,
                        help="Хост на котором находится Redis. По умолчанию 'localhost'")
    parser.add_argument("-p", "--port", dest="port", default=6379, type=int,
                        help="Порт на котором находится Redis. По умолчанию 6379")
    parser.add_argument("-d", "--db", dest="db", default=0, type=int,
                        help="БД в редисе. По умолчанию - 0")

    args = parser.parse_args()
    morph = get_morph(args.morph_dir)
    rd = Redis(host=args.host, port=args.port, db=args.db)
    rd.flushdb()

    get_data_and_statistic(args.file_path, morph, rd)

    rd.save()
