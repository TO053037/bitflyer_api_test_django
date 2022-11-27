import copy
from time import time as timestamp
from typing import Tuple

import numpy as np



# globalだけでなくlobalにも対応
class IPSO():

    def __init__(self, m: int, c1: float, c2: float, k: int=-1, max_time: float=1.8, seed: int=28, display_flg: bool=True):
        self.m = m
        self.c1 = c1
        self.c2 = c2
        self.k = m-1 if k == -1 else k
        self.max_time = max_time
        self.seed = seed
        self.display_flg = display_flg
        self.n = None
        self.dist = None
        self.wait = None
        self.xs = None
        self.ps = None
        self.p_time = None
        self.ls = None
        self.l_time = None
        self.INF = 2 ** 30

    # スタートとゴールを入口にするという改良の余地あり
    def calc_time(self, path: list[int]) -> int:
        time = 0
        for i in range(len(path)):
            time += self.wait[path[i]][time]
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
                xdashdash = copy.deepcopy(candidate)
        # 5
        xdashdashdash = []
        mi = self.INF
        for i in range(self.n - len(ldash)):
            candidate = xdashdash[:lind] + ldash + xdashdash[lind:]
            c_time = self.calc_time(candidate)
            if c_time < mi:
                mi = c_time
                xdashdashdash = copy.deepcopy(candidate)
            xdashdash = xdashdash[1:] + [xdashdash[0]]

        self.xs[num] = copy.deepcopy(xdashdashdash)

        if mi < self.p_time[num]:
            self.p_time[num] = mi
            self.ps[num] = copy.deepcopy(xdashdashdash)

    def best_route_time(self) -> Tuple[list[int], int]:
        mi_ind = np.argmin(np.array(self.p_time))

        return (self.ps[mi_ind], self.p_time[mi_ind])

    def fit(self, n: int, dist: list[list[int]], wait: list[list[int]]) -> Tuple[list[int], int]:
        np.random.seed(self.seed)
        self.n = n
        self.dist = dist
        self.wait = wait

        # 1
        self.xs = [list(np.random.permutation(self.n)) for _ in range(self.m)]
        self.init_p_l()

        # 7
        # 終了条件には工夫の余地がある
        route, time = self.best_route_time()
        if self.display_flg:
            print("initial_route:", route)
            print("initial_time:", time)

        start_time = timestamp()
        i = 0
        while timestamp() - start_time < self.max_time:
            # 2, 3, 4, 5
            for j in range(self.m):
                self.update_x_p(j)
            # 6
            self.update_lbest()
            if self.display_flg and (i+1) % 20 == 0:
                route, time = self.best_route_time()
                print("-"*100)
                print("iter:", (i+1))
                print("route:", route)
                print("time:", time)
            i += 1

        # 8
        return self.best_route_time()


class GA():

    def __init__(self, m: int, e: int, cr: float, mr: float, c_alg: str, max_time: float=1.8, seed: int=28, display_flg: bool=True):
        # データ数
        self.n = None
        # 遺伝子数
        self.m = m
        # エリート数
        self.elite = e
        # 交叉確率
        self.crate = cr
        # 突然変異確率
        self.mrate = mr
        # 交叉アルゴリズム
        self.c_alg = c_alg
        # イテレーション
        self.max_time = max_time
        # seed値
        self.seed = seed
        # 途中経過を表示するか
        self.display_flg = display_flg
        self.dist = None
        self.wait = None
        self.xs = None
        self.INF = 2 ** 30
        self.best_time = self.INF
        self.best_route = None

    def calc_time(self, path: list[int]) -> int:
        time = 0
        # for i in range(len(path) - 1):
        for i in range(len(path)):
            time += self.wait[path[i]][time]
            time += self.dist[path[i]][path[(i+1)%len(path)]]
        
        return time

    def norm_softmax(self, l: list[int]):
        mean = np.mean(l)
        std = np.sqrt(np.var(l))
        if std == 0:
            print("*"*100)
            return [1.0 / self.m for _ in range(self.m)]
        l2 = [(x - mean) / std for x in l]
        su = 0
        for x in l2:
            su += np.exp(x)
    
        return [np.exp(x) / su for x in l2]

    # ルーレット選択
    def selection(self):
        # 最適タイム、最適ルートを保存
        time_list = [self.calc_time(x) for x in self.xs]
        mi_ind = np.argmin(time_list)
        if time_list[mi_ind] < self.best_time:
            self.best_time = time_list[mi_ind]
            self.best_route = copy.deepcopy(self.xs[mi_ind])

        minus_time_list = [-t for t in time_list]
        p_list = self.norm_softmax(minus_time_list)
        samples = np.random.choice(a=list(range(self.m)), size=self.m, p=p_list)
        argsorted_time = np.argsort(time_list)
        next_generation = [self.xs[argsorted_time[i]] for i in range(self.elite)]

        for i in range((self.m - self.elite) // 2):
            s1 = copy.deepcopy(self.xs[samples[2*i]])
            s2 = copy.deepcopy(self.xs[samples[2*i + 1]])
            if np.random.random() < self.crate:
                if self.c_alg == 'CX':
                    s1, s2 = self.CX(s1, s2)
                elif self.c_alg == 'CX2':
                    s1, s2 = self.CX2(s1, s2)
                elif self.c_alg == 'CX3':
                    s1, s2 = self.CX3(s1, s2)
                else:
                    raise ValueError('存在しない交叉アルゴリズムを指定している')
            if np.random.random() < self.mrate:
                s1 = self.UOM(s1)
            if np.random.random() < self.mrate:
                s2 = self.UOM(s2)

            next_generation.append(s1)
            next_generation.append(s2)

        self.xs = copy.deepcopy(next_generation)

    # indはxs[ind]
    def UOM(self, path: list[int]):
        r1, r2 = np.random.choice(self.n, size=2, replace=False)
        tmp = copy.deepcopy(path)
        tmp[r1] = path[r2]
        tmp[r2] = path[r1]

        return tmp

    # サイクルを先頭ではなくランダムに決めることもできる
    def CX(self, path1: list[int], path2: list[int]) -> Tuple[list[int], list[int]]:
        child1 = [0 for _ in range(self.n)]
        child2 = [0 for _ in range(self.n)]
        seen_flg = [False for _ in range(self.n)]
        child_flg = True
        # key: 数字, value: インデックス
        num_to_index = {num:i for (i, num) in enumerate(path1)}
        for i in range(self.n):
            if seen_flg[i] == True:
                continue

            ind = i
            while True:
                seen_flg[ind] = True

                if child_flg:
                    child1[ind] = path1[ind]
                    child2[ind] = path2[ind]
                else:
                    child1[ind] = path2[ind]
                    child2[ind] = path1[ind]
                ind = num_to_index[path2[ind]]

                if ind == i:
                    child_flg ^= True
                    break

        return (child1, child2)

    # サイクルを先頭ではなくランダムに決めることもできる
    def CX2(self, path1: list[int], path2: list[int]) -> Tuple[list[int], list[int]]:
        child1 = [0 for _ in range(self.n)]
        child2 = [0 for _ in range(self.n)]
        seen_flg = [False for _ in range(self.n)]
        # key: 数字, value: インデックス
        num_to_index = {num:i for (i, num) in enumerate(path1)}
        rand = np.random.randint(0, self.n)

        ind = rand
        while True:
            seen_flg[ind] = True
            child1[ind] = path2[ind]
            child2[ind] = path1[ind]
            ind = num_to_index[path2[ind]]

            if ind == rand:
                break

        for i in range(self.n):
            if not seen_flg[i]:
                child1[i] = path1[i]
                child2[i] = path2[i]

        return (child1, child2)

    def CX3(self, path1: list[int], path2: list[int]) -> Tuple[list[int], list[int]]:
        child1 = [0 for _ in range(self.n)]
        child2 = [0 for _ in range(self.n)]
        seen_flg = [False for _ in range(self.n)]
        # key: 数字, value: インデックス
        num_to_index = {num:i for (i, num) in enumerate(path1)}
        for i in range(self.n):
            if seen_flg[i] == True:
                continue

            ind = i
            child_flg = np.random.random() < 0.5
            while True:
                seen_flg[ind] = True

                if child_flg:
                    child1[ind] = path1[ind]
                    child2[ind] = path2[ind]
                else:
                    child1[ind] = path2[ind]
                    child2[ind] = path1[ind]
                ind = num_to_index[path2[ind]]

                if ind == i:
                    break

        return (child1, child2)

    def fit(self, n: int, dist: list[list[int]], wait: list[list[int]]) -> Tuple[list[int], int]:
        np.random.seed(self.seed)
        self.n = n
        self.dist = dist
        self.wait = wait

        self.xs = [list(np.random.permutation(self.n)) for _ in range(self.m)]

        start_time = timestamp()
        i = 0
        while timestamp() - start_time < self.max_time:
            self.selection()
            if self.display_flg and (i == 0 or (i+1) % 20 == 0):
                print("-"*100)
                print("generation:", (i+1))
                print("route:", self.best_route)
                print("time:", self.best_time) 
            i += 1

        return (self.best_route, self.best_time)


class TEST_TSP():

    def __init__(self):
        pass

    def fit(self, n: int, dist: list[list[int]]) -> list[int]:
        return [i for i in range(n)]
