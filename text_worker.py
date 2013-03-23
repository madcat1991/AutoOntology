#coding: utf-8
from Queue import Queue

import argparse
import codecs

from redis import Redis
from pymorphy import get_morph
from gatherer import Gatherer
from writer import RdWriter


def data_gathering(file_path, morph, rd, number_of_threads=2):
    """На каждой итерации возвращает список полученных из одной строки комбинаций прилаг + сущ.
    Элемент списка кортеж (прилагательное, существительно).
    Прилагательное и существительное приведены к нормальной форме

    :param file_path: путь до файла с данными. Файл должен быть в формате UTF-8
    :param morph: морфология
    """

    put_queue = Queue()
    get_queue = Queue()

    threads = []

    #поток на получение
    receive_thread = RdWriter(rd=rd, receive_queue=get_queue)
    receive_thread.start()
    threads.append(receive_thread)

    #потоки на обработку
    for index in range(number_of_threads):
        gatherer = \
            Gatherer(receive_queue=put_queue, send_queue=get_queue, morph=morph, name="thread_%s" % index)
        gatherer.start()
        threads.append(gatherer)

    f = codecs.open(file_path, encoding='utf-8')
    for line in f:
        put_queue.put(line)

    # ждем на завершение
    for thread in threads:
        thread.join()

    print "I have finished, my Master"


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

    data_gathering(args.file_path, morph, rd)

    rd.save()
