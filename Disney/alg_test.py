import algorithm_wada
import alg_util



if __name__ == '__main__':
    ipso = algorithm_wada.IPSO(16, 0.2, 0.3, i=1000)
    route, time = alg_util.wrapper_alg(ipso, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv')
    print('route:', route)
    print('time:', time)

    ga = algorithm_wada.GA(256, 32, 1.0, 1.0, i=1000)
    route, time = alg_util.wrapper_alg(ipso, './Disney/attractions_distances_2.csv', './wait_time_data_20221105.csv')
    print('route:', route)
    print('time:', time)
    