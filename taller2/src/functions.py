import statistics

r = [10, 10, 10, 1.1511, 1.4250, 1.5712, 1.6563, 1.7110, 1.7491, 1.7770,
    1.7984, 1.8153, 1.8290, 1.8403, 1.8498, 1.8579, 1.8649, 1.8710, 1.8764, 1.8811,
    1.8853, 1.8891, 1.8926, 1.8957, 1.8985, 1.9011, 1.9035, 1.9057, 1.9078, 1.9096,
    1.9114] # Modified Thompson Values


def get_outliers(data):
    res = [True] * len(data)
    enumerated_data = [(d,n) for (n,d) in enumerate(data)]
    enumerated_data = list(filter(lambda e : e[0] >= 0, enumerated_data))
    enumerated_data.sort()
    there_are_outliers = True
    while there_are_outliers:
        there_are_outliers = False
        data = [e[0] for e in enumerated_data]
        s = statistics.stdev(data)
        m = statistics.mean(data)
        threshold = s*r[len(data)]
        left_posible_outlier_deviation = abs(data[0]-m)
        right_posible_outlier_deviation = abs(data[-1]-m)
        if left_posible_outlier_deviation < right_posible_outlier_deviation:
            if threshold < right_posible_outlier_deviation:
                enumerated_data.pop(-1)
                there_are_outliers = True
        else:
            if threshold < left_posible_outlier_deviation:
                enumerated_data.pop(0)
                there_are_outliers = True
    for (_,n) in enumerated_data:
        res[n] = False
    return res