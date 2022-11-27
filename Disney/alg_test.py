import numpy as np

import alg_util
import alg_wada



if __name__ == '__main__':
    # ipso = alg_wada.IPSO(16, 0.2, 0.3, display_flg=True)
    # route, time = alg_util.wrapper_alg(ipso, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv', True)
    # print('route:', route)
    # print('time:', time)

    ga = alg_wada.GA(32, 4, 1.0, 1.0, c_alg='CX')
    route, time = alg_util.wrapper_alg(ga, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv', True)
    print('route:', route)
    print('time:', time)

    # test_tsp = alg_wada.TEST_TSP()
    # route, time = alg_util.wrapper_alg(test_tsp, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv', False)
    # print('route:', route)
    # print('time:', time)

    # for i in range(10):
    #     ipso = alg_wada.IPSO(16, 0.2, 0.3, seed=i, display_flg=False)
    #     route, time = alg_util.wrapper_alg(ipso, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv', True)
    #     print('route:', route)
    #     print('time:', time)
