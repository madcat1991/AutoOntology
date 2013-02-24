#coding: utf-8


def f_one_score(precision, recall):
    """Вычисления F1 меры

    :param precision: точность
    :param recall: полнота
    """
    return 2.0 * precision * recall / (precision + recall)
