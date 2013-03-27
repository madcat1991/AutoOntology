#coding: utf-8

#значение для автоинкремента
autoincrement_value = -1


def get_id():
    global autoincrement_value
    autoincrement_value += 1
    return autoincrement_value


class Cluster(object):
    """Класс обозначающий один кластер
    """
    def __init__(self, index=None, A=None, B=None):
        # подкластеры, структура-та иерархическая
        self.A = A
        self.B = B
        self.index = index
        self.name = "C%s" % get_id()

    def get_title(self, keys):
        return keys[self.index] if self.index is not None else self.name

    def get_list_of_edges(self, keys):
        res = []
        if self.A:
            res.append("%s -- %s;" % (self.get_title(keys), self.A.get_title(keys)))
            if self.A.A or self.A.B:
                res += self.A.get_list_of_edges(keys)
        if self.B:
            res.append("%s -- %s;" % (self.get_title(keys), self.B.get_title(keys)))
            if self.B.A or self.B.B:
                res += self.B.get_list_of_edges(keys)
        return res

    def get_dot_graph_str(self, keys):
        return "graph cluster {\n%s\n}" % '\n'.join(self.get_list_of_edges(keys))


def proximity(matrix, R, Q, alpha_A=0.5, alpha_B=0.5, beta=0.0, gamma=-0.5):
    """Формула Ланса Вильямса адаптированная в умолчальных настройках
    под Complete Link для косинусной меры
    """
    if R.A and R.B:
        #стандартный, сложный случай
        res = alpha_A * proximity(matrix, R.A, Q) + alpha_B * proximity(matrix, R.B, Q) + \
            beta * proximity(matrix, R.A, R.B) + \
            gamma * abs(proximity(matrix, R.A, Q) - proximity(matrix, R.B, Q))
    elif Q.A and Q.B:
        #стандартный простой случай
        res = proximity(matrix, Q, R)
    else:
        res = matrix[R.index][Q.index]
    return res


def get_clusters(matrix):
    clusters = [Cluster(index=index) for index in range(len(matrix))]

    while len(clusters) > 2:
        cluster_len = len(clusters)

        best_value = 0
        best_i = best_j = 0
        for i in range(cluster_len):
            #оптимизация
            for j in range(i + 1, cluster_len):
                if i != j:
                    p = proximity(matrix, clusters[i], clusters[j])
                    if p > best_value:
                        best_value = p
                        best_i, best_j = i, j

        #вначале надо сделать pop большего индекса
        if best_j > best_i:
            best_i, best_j = best_j, best_i
        A = clusters.pop(best_i)
        B = clusters.pop(best_j)
        clusters.append(Cluster(A=A, B=B))

    if len(clusters) == 2:
        res = Cluster(A=clusters[0], B=clusters[1])
    elif len(clusters) == 1:
        res = clusters[0]
    else:
        res = None

    return res
