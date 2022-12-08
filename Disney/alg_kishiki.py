import csv
import statistics
import copy
from copy import deepcopy
import math
import sys 
from typing import Tuple
import alg_util

#距離も考える


sys.setrecursionlimit(10000)

class HOGE:

    #平均を出す関数
    #average_list:[アトラクションの平均待ち時間]*n <-添字がアトラクション番号に対応する
    def average_fun(self,row_list1):
        average_list = [-1] * self.n
        sum_list = [0] * self.n
        length_list = [0] * self.n
        for i in range(len(row_list1)):
            for j in range(720):
                if row_list1[i][j] > 0:
                    sum_list[i] += row_list1[i][j]
                    length_list[i] += 1
        for i in range(len(sum_list)):
            if length_list[i] > 0:
                average_list[i] = sum_list[i]/length_list[i]
        return average_list



    

    #平均との差を出す関数
    #difference_list[i][j] : アトラクション(i)と時間（j）と平均との差を格納する
    #行がn個、列が７２０個　７２０は60*12の１２時間分のデータ
    
    def difference_fun(self,average_list1,row_list1):
        
        difference_list = [[-1]*720]*self.n
        sannsyou_taisaku_list=[0]*720

        for i in range(len(difference_list)):
            if i > 0:
                difference_list[i-1] = sannsyou_taisaku_list.copy()
            for j in range(len(difference_list[i])):
                if average_list1[i] == -1 or row_list1[i][j] == -1:
                    sannsyou_taisaku_list[j] = -1000
                else:
                    sannsyou_taisaku_list[j] = average_list1[i] - row_list1[i][j]
        difference_list[self.n -1] = sannsyou_taisaku_list.copy()   
        return difference_list


    #この関数では、difference_listからそのアトラクションのより平均との差が大きいアトラクションをリストに格納している
    #good_time_list [平均との差、時間（row＿listの添字）]*n ＜ー　一行目はアトラクション０の一番平均との差が大きい時間とその差を格納している
    def good_fun(self,difference_list1):
        good_time_list = [[-2000]*2]*self.n
        good_time_attraction_list=[[0]*2]
        for i in range(len(difference_list1)):
            for j in range(len(difference_list1[i])):      
                if difference_list1[i][j] > good_time_list[i][0]:
                    good_time_attraction_list = [difference_list1[i][j],j]
                    good_time_list[i] = good_time_attraction_list.copy() 
        return good_time_list


    #この関数では、good＿listからアトラクションの中の平均との差が一番大きいアトラクションを求め、best_moment_attractionに格納している
    #best_moment_attraction[平均との差、時間（row_listの添字）、アトラクショん（row＿listの添字）]
    def best_fun(self,good_time_list1):  
        best_moment_attraction = [[-10000]*3]       
        for i in range(len(good_time_list1)):
            if good_time_list1[i][0] > best_moment_attraction[0][0]:
                best_moment_attraction[0][0] = good_time_list1[i][0]     
                best_moment_attraction[0][1] = good_time_list1[i][1] 
                best_moment_attraction[0][2] = i
        return best_moment_attraction
            

    
    #この関数ではrouteを確定する関数
    #route_list　：　720個の格納できる領域を持つ、平均との差が大きいアトラクションを返す
    

    def route_fun(self,row_list_copy, route_list,row_list):
        
        global average_list
        global difference_list
        global good_time_list
        global best_moment_attraction
        average_list = self.average_fun(row_list_copy)
        difference_list = self.difference_fun(average_list,row_list_copy)
        good_time_list = self.good_fun(difference_list)       
        best_moment_attraction = self.best_fun(good_time_list)
        
        # print(row_list_copy)
        #print(row_list)
        # print(route_list)
        # print(best_moment_attraction)
        
        for i in range(8):
            route_list[i] = -1
        #route_listに入れることができるのかの確認
        #best_moment_attractionで求めたアトラクションとその時間に対して、元々埋めてあったアトラクションと時間がかぶらないようにするためのfor文
        #つまり、すでに確定しているアトラクションとダブルブッキングしないためのfor文
        #route_funは再帰関数であるのでroute_listはどんどん更新されてく
        #ダブルブッキングしそうであったら、そこのrow_listの内容を-1にして再帰
        #補足：route_listの中が０であるなら、そこの時間には入れる
        
        #print("ここは？")
        if best_moment_attraction[0][0] != -1000:
            for i in range(row_list[best_moment_attraction[0][2]][best_moment_attraction[0][1]]+8):
                if best_moment_attraction[0][1]+i >719:
                    break
                elif route_list[best_moment_attraction[0][1]+i] != 0 and best_moment_attraction[0][1] != -1 and best_moment_attraction[0][0] != -1000 :
                    row_list_copy[best_moment_attraction[0][2]][best_moment_attraction[0][1]]  =  -1
                    self.kakuninn = 1
                
                # print(best_moment_attraction)
                # print(route_list)
                    #print('aa')
        
        
                #print("ここ")
            if self.kakuninn != 1:
            #アトラクションが決まったら、そのアトラクションは乗らないのでrow_listのそのアトラクションの待ち時間を値を-1に変えている
            #さらにその時間や待っている時間に他のアトラクションに映ることもできないので、対応する時間も−１に変更してる
                for i in range(len(row_list_copy)):
                    for pp in range(len(row_list_copy[i])):
                        row_list_copy[best_moment_attraction[0][2]][pp]=-1
                        for j in range(row_list[best_moment_attraction[0][2]][best_moment_attraction[0][1]]):
                            row_list_copy[i][best_moment_attraction[0][1]+j] = -1
                    
                    
        
            #print("ここ２")          
            #route_listに行くアトラクションの番号を格納するfor文
            #最初に並ぶ時間には、route_listにアトラクション番号を格納する
            #それ以降（並んでいる時間）には-1を格納している
            #アトラクション番号が０である時は、100という風に格納している。これはroute_listは元々全て０で格納されていて区別ができないため
            #アトラクションの最高数は３６だから１００は大丈夫
                # print(best_moment_attraction)
        
            #     print(best_moment_attraction)
                for i in range(row_list[best_moment_attraction[0][2]][best_moment_attraction[0][1]]+8):
                    if best_moment_attraction[0][1] != -1:
                        if i == 0:
                            if best_moment_attraction[0][2] == 0:
                                route_list[best_moment_attraction[0][1]] = 100
                            else:
                                route_list[best_moment_attraction[0][1]] = best_moment_attraction[0][2]
                                # print(route_list[best_moment_attraction[0][1]])
                        elif best_moment_attraction[0][1] + i > 719:
                            break
                        else:
                            route_list[best_moment_attraction[0][1]+i] = -1
                    
                    
            #print("ラスト")
                # print(row_list[best_moment_attraction[0][2]][best_moment_attraction[0][1]])
                # print(route_list)
        
                    
            #best_moment_attractionが-1000で無い時は再帰
        
            #print(best_moment_attraction)
            # print(route_list)
            self.kakuninn = 0
            route_list = self.route_fun(row_list_copy,route_list,row_list)
            # print(route_list)
        return route_list



    

    
    def time_fun2(self,route_list,row_list,dist,entrance_dist):
        
        for i in range(len(route_list)):
            if route_list[i] != 0 and route_list[i] != -1:
                if route_list[i] == 100:
                    route_list[i] = 0
                self.m += row_list[route_list[i]][i]
                if route_list[i] == 0:
                    route_list[i] = 100
                # print(self.m)
                
        for i in range(len(route_list)):
            if route_list[i] != 0 and route_list[i] != -1:
                if route_list[i] == 100:
                    route_list[i] = 0
                if self.p ==0:
                    self.p = copy.copy(route_list[i])
                    self.a = route_list[i]
                    self.m += entrance_dist[self.p]
            
                else:
                    self.m += dist[route_list[i]][self.p]
                    # print(dist[route_list[i]][self.p])
                    # print(dist[route_list[i]][self.p]/80)
                    self.p = copy.copy(route_list[i])
                    # print(self.m)
                if route_list[i] ==0:
                    route_list[i] =100
        return self.m
    
    def route_syuusei_fun(self,route_list,route_syuusei_list):
        i = 0
        for i in range(len(route_list)):
            if route_list[i] != 0 and route_list[i] != -1:
                if route_list[i] == 100:
                    route_list[i] = 0
                route_syuusei_list.append(route_list[i])
                i+=1
        print(route_syuusei_list)
        if i != self.n:
            self.m = 10000000
        return route_syuusei_list, self.m
                
        
        
    def fit(self, n: int, dist: list[list[int]],row_list: list[list[int]],entrance_dist: list[int]) ->Tuple[list[int], int]:
        self.n = n
        
        # print(row_list[10])
        # print(row_list[23])
        # print(row_list[24])
        # print(row_list[25])
        # print(row_list[26])
        # print(n)
        self.route_syuusei_list = []
        self.difference_list = [[-1]*self.n]*720
        self.route_list = [0]*720
        self.m = 0
        self.p = 0
        self.a = 0
        self.kakuninn = 0
        self.row_list_copy = copy.deepcopy(row_list)
        self.route_list = self.route_fun(self.row_list_copy,self.route_list,row_list)
        
        self.m = self.time_fun2(self.route_list,row_list,dist,entrance_dist)
        self.route_list ,self.m= self.route_syuusei_fun(self.route_list,self.route_syuusei_list)
        return self.route_list,self.m
    
    
    
# hoge = HOGE()
# route,time= alg_util.wrapper_alg(hoge,'./Disney/attractions_distances_data.csv','./wait_time_data_20221105.csv',True)

