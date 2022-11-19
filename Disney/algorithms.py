import copy
from functools import reduce
import numpy as np
from typing import Tuple



# globalだけでなくlobalにも対応
class IPSO():

    def __init__(self, m: int, c1: float, c2: float, k: int=-1, i: int=10):
        self.m = m
        self.c1 = c1
        self.c2 = c2
        self.k = m-1 if k == -1 else k
        self.iter = i
        self.n = None
        self.dist = None
        # self.wait = None
        self.xs = None
        self.ps = None
        self.p_time = None
        self.ls = None
        self.l_time = None
        self.INF = 2 ** 30

    # スタートとゴールを入口にするという改良の余地あり
    def calc_time(self, path: list[int]) -> int:
        time = 0
        # for i in range(len(path) - 1):
        for i in range(len(path)):
            # time += self.wait[path[i]][time]
            time += self.dist[path[i]][path[(i+1)%len(path)]]
        
        return time

    def update_lbest(self):
        if self.k == self.m - 1:
            mi_time = min(self.p_time)
            if mi_time < self.l_time[0]:
                self.l_time = [mi_time for _ in range(self.m)]
                mi_ind = np.argmin(np.array(self.p_time))
                self.ls = [self.ps[mi_ind] for _ in range(self.m)]

            return

        for i in range(self.m):
            front = i
            back = i
            mi = self.p_time[i]
            mi_ind = i
            for j in range(self.k // 2):
                front = (front + 1) % self.m
                back = (back - 1 + self.n) % self.m
                f_time = self.p_time[front]
                if mi > f_time:
                    mi = f_time
                    mi_ind = front
                b_time = self.p_time[back]
                if mi > b_time:
                    mi = b_time
                    mi_ind = back
            # self.l_time[i] = self.p_time[mi_ind]
            # self.ls[i] = self.ps[mi_ind]
            self.l_time[i] = copy.deepcopy(self.p_time[mi_ind])
            self.ls[i] = copy.deepcopy(self.ps[mi_ind])

        return

    def init_p_l(self):
        # self.ps = self.xs
        self.ps = copy.deepcopy(self.xs)
        self.p_time = [self.calc_time(p) for p in self.ps]
        self.l_time = [self.INF for _ in range(self.m)]
        self.ls = [[] for _ in range(self.m)]
        self.update_lbest()

    # def update_lbest(self):
    #     if self.k == m-1:
    #         mi_ind = np.argmin(np.array(calc_time(p) for p in self.ps))
    #         self.ls = [self.ps[mi_ind] for _ in range(self.n)]
    #         return

    #     times = [calc_time(p) for p in ps]
    #     for i in range(self.m):
    #         front = i
    #         back = i
    #         mi = self.calc_time(self.ps[i])
    #         mi_ind = i
    #         for j in range(k // 2):
    #             front = (front + 1) % self.n
    #             back = (back - 1 + self.n) % self.n
    #             f_time = self.calc_time(ps[front])
    #             if mi > f_time:
    #                 mi = f_time
    #                 mi_ind = front
    #             b_time = self.calc_time(ps[front])
    #             if mi > b_time:
    #                 mi = b_time
    #                 mi_ind = back
    #         self.ls[i] = self.ps[mi_ind]

    def update_x_p(self, num: int):
        # 1
        r1 = np.random.rand()
        r2 = np.random.rand()
        plen = int(self.c1 * r1 * self.n)
        llen = int(self.c2 * r2 * self.n)
        pind = np.random.randint(0, self.n - plen + 1)
        lind = np.random.randint(0, self.n - llen + 1)
        pdash = self.ps[num][pind:(pind+plen)]
        ldash = self.ls[num][lind:(lind+llen)]
        # 2
        pdashdash = [p for p in pdash if p not in ldash]
        # 3
        p_and_l = pdashdash + ldash
        xdash = [x for x in self.xs[num] if x not in p_and_l]
        # 4
        # 挿入場所を1つ増やせる、pdashを反対にできる
        xdashdash = []
        mi = self.INF
        for i in range(1, self.n - len(p_and_l)):
            candidate = xdash[:i] + pdashdash + xdash[i:]
            c_time = self.calc_time(candidate)
            if c_time < mi:
                mi = c_time
                # xdashdash = candidate
                xdashdash = copy.deepcopy(candidate)
        # 5
        xdashdashdash = []
        mi = self.INF
        for i in range(self.n - len(ldash)):
            candidate = xdashdash[:lind] + ldash + xdashdash[lind:]
            c_time = self.calc_time(candidate)
            if c_time < mi:
                mi = c_time
                # xdashdashdash = candidate
                xdashdashdash = copy.deepcopy(candidate)
            xdashdash = xdashdash[1:] + [xdashdash[0]]

        # self.xs[num] = xdashdashdash
        self.xs[num] = copy.deepcopy(xdashdashdash)

        if mi < self.p_time[num]:
            self.p_time[num] = mi
            # self.ps[num] = xdashdashdash
            self.ps[num] = copy.deepcopy(xdashdashdash)

    def best_route_time(self) -> Tuple[list[int], int]:
        mi_ind = np.argmin(np.array(self.p_time))

        return (self.ps[mi_ind], self.p_time[mi_ind])

    # def fit(self, n: int, dist: list[list[int]], wait: list[list[int]]):
    def fit(self, n: int, dist: list[list[int]]):
        self.n = n
        self.dist = dist
        # self.wait = wait

        # 1
        self.xs = [list(np.random.permutation(self.n)) for _ in range(self.m)]
        self.init_p_l()

        # 7
        # 終了条件には工夫の余地がある
        route, time = self.best_route_time()
        print("initial_route:", route)
        print("initial_time:", time)
        for i in range(self.iter):
            # 2, 3, 4, 5
            for j in range(self.m):
                self.update_x_p(j)
            # 6
            self.update_lbest()
            if (i+1) % 1 == 0:
                print("-"*100)
                print("iter:", (i+1))
                route, time = self.best_route_time()
                print("route:", route)
                print("time:", time)

        # 8
        return self.best_route_time()


def do_alg() -> int:
    dist = []
    with open('./wait_time_data_20221105.csv', 'r') as f:
        dist = f.read()


def wrapper_alg(source_dist: str, source_wait: str) -> Tuple[list[int], int]:
    dist = shape_dist(source_dist)
    wait = shape_wait(source_wait)
    wait = [[wait[i][j] for i in range(len(wait))] for j in range(len(wait[0]))]
    assert len(set((len(dist), len(wait), *(len(dist[i]) for i in range(len(dist)))))) == 1, 'distの行数、waitの行数、distの列数が異なる'

    no_dist_list = []
    for i in range(len(dist)):
        if dist[i][2] == -1:
            no_dist_list.append(i)

    no_wait_list = []
    for i in range(len(wait)):
        no_flg = True
        for x in wait[i]:
            if x != -1:
                no_flg = False
                break
        if no_flg:
            no_wait_list.append(i)

    no_list = sorted(no_dist_list + no_wait_list)
    in_list = [i for i in range(len(dist)) if i not in no_list]
    print(no_list)
    print(in_list)
    dist = [[dist[i][j] for j in in_list] for i in in_list]
    wait = [wait[i] for i in in_list]
    assert -1 not in reduce(lambda accum, x: accum + x, dist, []), 'distに-1が存在'
    assert [-1 for _ in range(len(wait[0]))] not in wait, 'waitに-1のみの行が存在'
    print(dist)
    # print('*'*100)
    # print(wait)

    # m -> minに120m/minで変換後、小数点以下切り上げ
    dist = [[(x+119) // 120 for x in l] for l in dist]

# def wrapper_ipso(dist: list[list[int]], wait: list[list[int]]) -> Tuple[list[int], int]:
#     new_wait = 
    


def shape_dist(source: str) -> list[list[int]]:
    dist = []
    with open(source, 'r') as f:
        dist = f.read().split('\n')
    dist = [x.split(',') for x in dist][:-1]
    dist = [[int(x) for x in l] for l in dist]

    return dist


def shape_wait(source: str) -> list[list[int]]:
    wait = []
    with open(source, 'r') as f:
        wait = f.read().split('\n')
    wait = [x.split(',') for x in wait][:-1]
    wait = [[int(x) for x in l] for l in wait]

    return wait


if __name__ == '__main__':
    wrapper_alg('./Disney/attractions_distances.csv', './wait_time_data_20221105.csv')