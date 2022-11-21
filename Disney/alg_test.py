import alg_wada
import alg_util



if __name__ == '__main__':
    # ipso = alg_wada.IPSO(16, 0.2, 0.3, i=1000)
    # route, time = alg_util.wrapper_alg(ipso, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv', True)
    # print('route:', route)
    # print('time:', time)

    # ga = alg_wada.GA(256, 32, 1.0, 1.0, i=1000)
    # route, time = alg_util.wrapper_alg(ipso, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv', True)
    # print('route:', route)
    # print('time:', time)

    test_tsp = alg_wada.TEST_TSP()
    route, time = alg_util.wrapper_alg(test_tsp, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv', False)
    print('route:', route)
    print('time:', time)
