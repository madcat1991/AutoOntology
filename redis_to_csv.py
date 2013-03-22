#coding: utf-8

"""
Скрипт для сбора данных из редис в csv
"""
import argparse
import csv
from redis import Redis

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", dest="output_file", type=str, required=True,
                        help="csv, в который пишется результат")
    parser.add_argument("-s", "--host", dest="host", default="localhost", type=str,
                        help="Хост на котором находится Redis. По умолчанию 'localhost'")
    parser.add_argument("-p", "--port", dest="port", default=6379, type=int,
                        help="Порт на котором находится Redis. По умолчанию 6379")
    parser.add_argument("-d", "--db", dest="db", default=0, type=int,
                        help="БД в редисе. По умолчанию - 0")

    args = parser.parse_args()
    rd = Redis(host=args.host, port=args.port, db=args.db)

    with open(args.output_file, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="|")
        for key in rd.keys():
            csv_writer.writerow([key, rd.get(key)])
