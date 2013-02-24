#coding: utf-8

import argparse
import codecs
import itertools

from nltk import pos_tag, sent_tokenize, word_tokenize, RegexpParser


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


def normilize_adj_noun_list(adj_noun_list):
    """Приводит к нормально форме список кортжей (прилагательное, существительно)
    """
    pass


def gather_data(file_path, grammar=COMPLEX_GRAMMAR):
    """Собирает данные из файла

    :param file_path: путь до файла с данными. Файл должен быть в формате UTF-8
    """
    chunk_parser = RegexpParser(grammar)
    f = codecs.open(file_path, encoding='utf-8')
    for line in f:
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
                        adj_noun_normilized_list = normilize_adj_noun_list(adj_noun_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", dest="file_path", type=str, required=True,
                        help="Файл из которого будет браться текст")

    args = parser.parse_args()

    gather_data(args.file_path)