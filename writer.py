#coding: utf-8
from Queue import Empty
from threading import Thread


class RdWriter(Thread):
    def __init__(self, *args, **kwargs):
        self.rd = kwargs.pop("rd")
        self.receive_queue = kwargs.pop("receive_queue")
        super(RdWriter, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            try:
                normalized_adj_noun_list = self.receive_queue.get(block=True, timeout=20)
            except Empty:
                print "RdWriter has finished"
                break

            for adj_noun in normalized_adj_noun_list:
                adj_noun_str = u" ".join(adj_noun)
                self.rd.incr(adj_noun_str, 1)