import alg_wada
import alg_util
import numpy as np



if __name__ == '__main__':
    # np.random.seed(28)
    # ipso = alg_wada.IPSO(16, 0.2, 0.3, i=1000, display_flg=False)
    # route, time = alg_util.wrapper_alg(ipso, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv', True)
    # print('route:', route)
    # print('time:', time)

    # np.random.seed(28)
    # ga = alg_wada.GA(256, 32, 1.0, 1.0, i=1000)
    # route, time = alg_util.wrapper_alg(ipso, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv', True)
    # print('route:', route)
    # print('time:', time)

    # test_tsp = alg_wada.TEST_TSP()
    # route, time = alg_util.wrapper_alg(test_tsp, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv', False)
    # print('route:', route)
    # print('time:', time)

    for i in range(10):
        np.random.seed(i)
        ipso = alg_wada.IPSO(16, 0.2, 0.3, i=1000, display_flg=False)
        route, time = alg_util.wrapper_alg(ipso, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv', True)
        print('route:', route)
        print('time:', time)
