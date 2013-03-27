#coding: utf-8

#значение для автоинкремента
from Queue import Queue
from threading import Thread

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


class MyThread(Thread):
    def __init__(self, *args, **kwargs):
        self.matrix = kwargs.pop("matrix")
        self.get_queue = kwargs.pop("get_queue")
        self.put_queue = kwargs.pop("put_queue")
        super(MyThread, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            i, j, cluster_i, cluster_j = self.get_queue.get()
            p = proximity(self.matrix, cluster_i, cluster_j)
            self.put_queue.put((i, j, p))
            self.get_queue.task_done()


def get_clusters_proximity_matrix(matrix, clusters, number_of_threads=4):
    print "Start to build proximity matrix"
    task_queue = Queue()
    result_queue = Queue()

    for i in range(number_of_threads):
        t = MyThread(matrix=matrix, get_queue=task_queue, put_queue=result_queue)
        t.setDaemon(True)
        t.start()

    clusters_matrix = []
    cluster_len = len(clusters)
    for i in range(cluster_len):
        clusters_matrix.append([0.0] * cluster_len)
        #оптимизация
        for j in range(i + 1, cluster_len):
            if i != j:
                task_queue.put((i, j, clusters[i], clusters[j]))

        clusters_matrix[i][i] = 1.0

    task_queue.join()

    while not result_queue.empty():
        i, j, p = result_queue.get()
        clusters_matrix[i][j] = clusters_matrix[j][i] = p

    print "Proximity matrix built"
    return clusters_matrix


def get_clusters(matrix, number_of_threads=4):
    clusters = [Cluster(index=index) for index in range(len(matrix))]
    clusters_matrix = get_clusters_proximity_matrix(matrix, clusters, number_of_threads)

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
        clusters_matrix.pop(best_i)
        clusters_matrix.pop(best_j)

        new_row = [0] * (len(clusters_matrix) + 1)
        new_row[-1] = 1.0
        for index, row in enumerate(clusters_matrix):
            row.pop(best_i)
            row.pop(best_j)
            p = proximity(matrix, R, clusters[index])
            #колонка
            row.append(p)
            #ряд
            new_row[index] = p
        clusters_matrix.append(new_row)

    if len(clusters) == 2:
        res = Cluster(A=clusters[0], B=clusters[1])
    elif len(clusters) == 1:
        res = clusters[0]
    else:
        res = None

    return res
