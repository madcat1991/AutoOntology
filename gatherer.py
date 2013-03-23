#coding: utf-8
from Queue import Empty
from threading import Thread
import itertools
from time import sleep
from nltk import sent_tokenize, word_tokenize, pos_tag, RegexpParser


SIMPLE_GRAMMAR = u"CHUNK :{<JJ.*>+ <N.*>}"
COMPLEX_GRAMMAR = u"""
    REL: {<,><CC>}
    REL: {<,> | <CC>}
    NOUN: {<N.*>(<REL><N.*>)*}
    ADJECTIVE: {<JJ.*>(<REL><JJ.*>)*}
    CHUNK: {<ADJECTIVE><NOUN>}
"""


class Gatherer(Thread):
    def __init__(self, *args, **kwargs):
        self.receive_queue = kwargs.pop("receive_queue")
        self.send_queue = kwargs.pop("send_queue")
        self.morph = kwargs.pop("morph")
        self.chunk_parser = RegexpParser(COMPLEX_GRAMMAR)
        super(Gatherer, self).__init__(*args, **kwargs)

    def get_adj_noun_list_from_chunk(self, chunk_subtree):
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

    def normilize_adj_noun_list(self, adj_noun_list, morph):
        """Приводит к нормально форме список кортжей (прилагательное, существительно)
        """
        res = []
        for adj, noun in adj_noun_list:
            normalized_adj = morph.normalize(adj.upper())
            normalized_noun = morph.normalize(noun.upper())
            if isinstance(normalized_adj, set):
                normalized_adj = normalized_adj.pop()
            if isinstance(normalized_noun, set):
                normalized_noun = normalized_noun.pop()
            res.append((normalized_adj, normalized_noun))
        return res

    def run(self):
        while True:
            try:
                line = self.receive_queue.get(block=True, timeout=5)
            except Empty:
                print "%s has finished" % self.name
                break

            for sentence in sent_tokenize(line):
                sentence = sentence.strip()
                if sentence:
                    tokens = word_tokenize(sentence)

                    tagged_tokens = pos_tag(tokens)
                    tree = self.chunk_parser.parse(tagged_tokens)
                    for subtree in tree.subtrees():
                        if subtree.node == u"CHUNK":
                            adj_noun_list = self.get_adj_noun_list_from_chunk(subtree)
                            normalized_adj_noun_list = self.normilize_adj_noun_list(adj_noun_list, self.morph)
                            self.send_queue.put(normalized_adj_noun_list)
