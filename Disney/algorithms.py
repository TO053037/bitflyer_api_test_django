import copy
from functools import reduce
import numpy as np
from typing import Tuple



# globalだけでなくlobalにも対応
class IPSO():

    def __init__(self, m: int, c1: float, c2: float, k: int=-1, i: int=1000):
        self.m = m
        self.c1 = c1
        self.c2 = c2
        self.k = m-1 if k == -1 else k
        self.iter = i
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
        # for i in range(len(path) - 1):
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

    def fit(self, n: int, dist: list[list[int]], wait: list[list[int]]):
        self.n = n
        self.dist = dist
        self.wait = wait

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
            if (i+1) % 100 == 0:
                print("-"*100)
                print("iter:", (i+1))
                route, time = self.best_route_time()
                print("route:", route)
                print("time:", time)

        # 8
        return self.best_route_time()


class GA():

    def __init__(self, m: int, e: int, cr: float, mr: float, i: int):
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
        # イテレーション
        self.iter = i
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

    def update_x(self):
        pass

    def local_search(self):
        pass
    
    # indはxs[ind]
    def mutate(self, ind: int):
        pass

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
        # for i in range(self.m // 2):
            s1 = copy.deepcopy(self.xs[samples[2*i]])
            s2 = copy.deepcopy(self.xs[samples[2*i + 1]])
            if np.random.random() < self.crate:
                s1, s2 = self.CX3(s1, s2)
            # while np.random.random() < self.mrate:
            #     s1 = self.UOM(s1)
            # while np.random.random() < self.mrate:
            #     s2 = self.UOM(s2)
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

    # x = [D, E, I, M, P, S, U, W]
    # y = [M, E, I, S, W, P, U, D]
    # NRは単にyを返しているため交叉オペレータとしては意味をなさない
    def NR(self, ind1: int, ind2: int):
        new_path = copy.deepcopy(self.xs[ind1])
        while True:
            if self.xs[ind1] == self.xs[ind2]:
                break

            best_time = self.INF
            best_path = None
            # xのi番目の要素をyがある位置の要素とswap
            for i in range(self.n):
                if self.xs[ind1][i] == self.xs[ind2][i]:
                    continue

                for j in range(self.n):
                    if self.xs[ind2][j] == self.xs[ind1][i]:
                        tmp = copy.deepcopy(self.xs[ind1])
                        tmp[i] = self.xs[ind1][j]
                        tmp[j] = self.xs[ind1][i]
                        tmp_time = self.calc_time(tmp)
                        if tmp_time < best_time:
                            best_time = tmp_time
                            best_path = copy.deepcopy(tmp)
                        break

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
        # child_flg = True
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
                    # child_flg ^= True
                    break

        return (child1, child2)

    def SR(self, ind1: int, ind2: int):
        pass

    def fit(self, n: int, dist: list[list[int]], wait: list[list[int]]) -> Tuple[list[int], int]:
        self.n = n
        self.dist = dist
        self.wait = wait

        self.xs = [list(np.random.permutation(self.n)) for _ in range(self.m)]

        for i in range(self.iter):
            self.selection()
            if i == 0 or (i+1) % 100 == 0:
                print("-"*100)
                print("generation:", (i+1))
                print("route:", self.best_route)
                print("time:", self.best_time)

        return (self.best_route, self.best_time)


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
    assert dist == [[dist[i][j] for i in range(len(dist))] for j in range(len(dist))], 'distが対称行列でない'

    # m -> minに80m/minで変換後、小数点以下切り上げ
    dist = [[(x+79) // 80 for x in l] for l in dist]
    wrapper_ipso(dist, wait)

def wrapper_ipso(dist: list[list[int]], wait: list[list[int]]) -> Tuple[list[int], int]:
    n = len(wait)
    new_wait = copy.deepcopy(wait)
    # -1の時に訪れたらペナルティ
    for i in range(n):
        max_i = max(wait[i])
        for j in range(len(wait[i])):
            if wait[i][j] == -1:
                new_wait[i][j] = 2 * max_i + 30

    # 消費時間の平均で12時間追加して倍にする
    for i in range(n):
        mean_i = sum(wait[i]) // len(wait[0])
        new_wait[i] += [mean_i for _ in range(len(wait[0]))]

    # 15倍にする
    wait_2 = [[] for _ in range(n)]
    new_wait_2 = [[] for _ in range(n)]
    for i in range(n):
        wait_2[i] = reduce(lambda accum, x: accum + [x for _ in range(15)], wait[i], [])
        new_wait_2[i] = reduce(lambda accum, x: accum + [x for _ in range(15)], new_wait[i], [])

    # ipso
    np.random.seed(28)
    ipso = IPSO(16, 0.2, 0.3, i=1000)
    route, time = ipso.fit(n, dist, new_wait_2)

    # ga
    # ga = GA(256, 32, 1.0, 1.0, i=1000)
    # route, time = ga.fit(27, dist, new_wait_2)

    # -1を通っていないか検証
    now_time = 0
    for i in range(n):
        if wait_2[route[i]][now_time] == -1:
            raise AssertionError('-1を通っている')
        now_time += new_wait_2[route[i]][now_time]
        now_time += dist[route[i]][route[(i+1)%n]]

    print(route, time)
    
    return (route, time)


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
    # wrapper_alg('./Disney/attractions_distances.csv', './wait_time_data_20221105.csv')
    wrapper_alg('./Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv')