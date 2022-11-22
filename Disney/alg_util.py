import copy
from functools import reduce
import numpy as np
from typing import Tuple
import alg_wada



def wrapper_alg(fc, source_dist: str, source_wait: str, tspts_flg) -> Tuple[list[int], int]:
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
    print("no_list:", no_list)
    print("in_list:", in_list)

    dist = [[dist[i][j] for j in in_list] for i in in_list]
    wait = [wait[i] for i in in_list]
    assert -1 not in reduce(lambda accum, x: accum + x, dist, []), 'distに-1が存在'
    assert [-1 for _ in range(len(wait[0]))] not in wait, 'waitに-1のみの行が存在'
    assert dist == [[dist[i][j] for i in range(len(dist))] for j in range(len(dist))], 'distが対称行列でない'

    # m -> minに80m/minで変換後、小数点以下切り上げ
    dist = [[(x+79) // 80 for x in l] for l in dist]

    # tspts_flgがTrueなら待ち時間を考慮する
    if tspts_flg:
        route, time = wrapper_tspts(fc, dist, wait)
    else:
        route, time = wrapper_tsp(fc, dist, wait)

    # バックエンドに渡すために頂点番号を変更
    vertex_mapping_list = [in_list[i] for i in range(len(in_list))]
    route = [vertex_mapping_list[x] for x in route]

    return (route, time)


def wrapper_tspts(fc, dist: list[list[int]], wait: list[list[int]]) -> Tuple[list[int], int]:
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
    # np.random.seed(28)
    # ipso = IPSO(16, 0.2, 0.3, i=1000)
    # route, time = ipso.fit(n, dist, new_wait_2)

    # ga
    # ga = GA(256, 32, 1.0, 1.0, i=1000)
    # route, time = ga.fit(27, dist, new_wait_2)
    route, time = fc.fit(n, dist, new_wait_2)

    # -1を通っていないか検証
    now_time = 0
    for i in range(n):
        if wait_2[route[i]][now_time] == -1:
            raise AssertionError('-1を通っている')
        now_time += new_wait_2[route[i]][now_time]
        now_time += dist[route[i]][route[(i+1)%n]]

    print(route, time)

    # 閉園時間を過ぎていたらメッセージ
    if time > len(new_wait_2[0]) // 2:
        print("閉園時間を過ぎている")
        time *= -1
    
    return (route, time)


def wrapper_tsp(fc, dist: list[list[int]], wait: list[list[int]]) -> Tuple[list[int], int]:
    n = len(wait)
    new_wait = copy.deepcopy(wait)
    # -1の時に訪れたら前後の値の平均値で補間（一方しかないならその値を使う）、小数点以下は切り上げ
    for i in range(n):
        front = None
        for j in range(len(wait[i])):
            if wait[i][j] != -1:
                front = wait[i][j]
            elif front != None:
                new_wait[i][j] = front

        back = None
        for j in range(len(wait[i])-1, -1, -1):
            if wait[i][j] != -1:
                back = wait[i][j]
            elif back != None:
                if new_wait[i][j] != -1:
                    new_wait[i][j] = (new_wait[i][j] + back + 1) // 2
                else:
                    new_wait[i][j] = back

    # 15倍にする
    new_wait_2 = [[] for _ in range(n)]
    for i in range(n):
        new_wait_2[i] = reduce(lambda accum, x: accum + [x for _ in range(15)], new_wait[i], [])

    # 巡回セールスマン問題のアルゴリズム
    route = fc.fit(n, dist)

    # mi_timeとmi_routeを計算（先頭アトラクションと逆順を考慮）
    rev_route = list(reversed(route))
    mi_route = None
    mi_time = 2 ** 30
    for s in range(n):
        time = 0
        rev_time = 0
        for i in range(n):
            time += new_wait_2[route[(s+i)%n]][time]
            time += dist[route[(s+i)%n]][route[(s+i+1)%n]]
            rev_time += new_wait_2[rev_route[(s+i)%n]][rev_time]
            rev_time += dist[rev_route[(s+i)%n]][rev_route[(s+i+1)%n]]
        if time < mi_time:
            mi_route = route[s:] + route[:s]
            mi_time = time
        if rev_time < mi_time:
            mi_route = rev_route[s:] + rev_route[:s]
            mi_time = rev_time

    print(mi_route, mi_time)

    # 閉園時間を過ぎていたらメッセージ
    if mi_time > len(new_wait_2[0]):
        print("閉園時間を過ぎている")
        mi_time *= -1

    return (mi_route, mi_time)


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
