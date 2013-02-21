#coding: utf-8

import argparse
import codecs

from nltk import pos_tag, sent_tokenize, word_tokenize, RegexpParser


SIMPLE_GRAMMAR = u"CHUNK :{<JJ.*>+ <N.*>}"
COMPLEX_GRAMMAR = u"""
    REL: {<,><CC>}
    REL: {<,> | <CC>}
    NOUN: {<N.*>(<REL><N.*>)*}
    ADJECTIVE: {<JJ.*>(<REL><JJ.*>)*}
    CHUNK: {<ADJECTIVE><NOUN>}
"""


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
                #import ipdb; ipdb.set_trace()
                print sentence
                print unicode(tree)
                for subtree in tree.subtrees():
                    if subtree.node == u"CHUNK":
                        print unicode(subtree)
                print '\n'



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", dest="file_path", type=str, required=True,
                        help="Файл из которого будет браться текст")

    args = parser.parse_args()

    gather_data(args.file_path)