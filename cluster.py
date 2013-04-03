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
            res.append('"%s" -- "%s";' % (self.get_title(keys), self.A.get_title(keys)))
            if self.A.A or self.A.B:
                res += self.A.get_list_of_edges(keys)
        if self.B:
            res.append('"%s" -- "%s";' % (self.get_title(keys), self.B.get_title(keys)))
            if self.B.A or self.B.B:
                res += self.B.get_list_of_edges(keys)
        return res

    def get_dot_graph_str(self, keys):
        return "graph cluster {\n%s\n}" % '\n'.join(self.get_list_of_edges(keys))


def new_proximity(cluster_matrix, A_index, B_index, Q_index, alpha_A=0.5, alpha_B=0.5, beta=0.0, gamma=-0.5):
    """Формула Ланса Вильямса адаптированная в умолчальных настройках
    под Complete Link для косинусной меры
    """
    res = alpha_A * cluster_matrix[A_index][Q_index] + \
        alpha_B * cluster_matrix[B_index][Q_index] + \
        beta * cluster_matrix[A_index][B_index] + \
        gamma * abs(cluster_matrix[A_index][Q_index] - cluster_matrix[B_index][Q_index])

    return res


def complete_link_proximity(cluster_matrix, A_index, B_index, Q_index):
    return new_proximity(cluster_matrix, A_index, B_index, Q_index, 0.5, 0.5, 0, -0.5)


def single_link_proximity(cluster_matrix, A_index, B_index, Q_index):
    return new_proximity(cluster_matrix, A_index, B_index, Q_index, 0.5, 0.5, 0, 0.5)


def get_clusters(matrix, clustering_method):
    """Извлечение кластеров.

    :param matrix: матрица весов
    :param clustering_method: метод кластеризации
    """
    clusters = [Cluster(index=index) for index in range(len(matrix))]
    clusters_matrix = matrix

    while len(clusters) > 2:
        cluster_len = len(clusters)
        print "Clusters left %s" % cluster_len

        best_value = 0
        best_i = best_j = 0
        for i in range(cluster_len):
            #оптимизация
            for j in range(i + 1, cluster_len):
                if i != j:
                    if clusters_matrix[i][j] > best_value:
                        best_value = clusters_matrix[i][j]
                        best_i, best_j = i, j

        print "Results got. Start to update cluster matrix"

        #вначале надо сделать pop большего индекса
        if best_j > best_i:
            best_i, best_j = best_j, best_i

        #работа со списком класетров
        A = clusters.pop(best_i)
        B = clusters.pop(best_j)
        R = Cluster(A=A, B=B)
        clusters.append(R)

        #работа с матрицей
        new_row = [0] * (len(clusters_matrix) + 1)
        new_row[-1] = 1.0
        for index, row in enumerate(clusters_matrix):
            p = clustering_method(clusters_matrix, best_i, best_j, index)
            #колонка
            row.append(p)
            #ряд
            new_row[index] = p

        clusters_matrix.append(new_row)

        #очистка
        for row in clusters_matrix:
            row.pop(best_i)
            row.pop(best_j)

        #очистка
        clusters_matrix.pop(best_i)
        clusters_matrix.pop(best_j)

    if len(clusters) == 2:
        res = Cluster(A=clusters[0], B=clusters[1])
    elif len(clusters) == 1:
        res = clusters[0]
    else:
        res = None

    return res
