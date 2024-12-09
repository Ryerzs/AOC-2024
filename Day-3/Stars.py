import time

def day_():
    path = "data.txt"
    #path = "test-data.txt"

    start_time = time.perf_counter()
    data = get_data(path)

    time1 = time.perf_counter()

    ans1 = star1(data)
    time2 = time.perf_counter()

    ans2 = star2(data)
    time3 = time.perf_counter()

    data = get_data("data_brute2.txt")

    ans3 = star3(data)
    #time3 = time.perf_counter()

    load_time = time1 - start_time
    star1_time = time2 - time1
    star2_time = time3 - time2
    if 1:
        print(f'Load time: {load_time}')
        print(f'Star 1 time: {star1_time}')
        print(f'Star 2 time: {star2_time}')
        print(f'Star 1 answer: {ans1}')
        print(f'Star 2 answer: {ans2}')
        print(f'Star 3 answer: {ans3}')

def get_data(path):
    data = [""]
    with open(path) as f:
        rows = f.read().splitlines()
        for row in rows:
            print(row)
            data[0] = data[0] + row
    return data
    
def star1(data):
    total = 0
    for line in data:
        mul = line.split("mul(")
        for m in mul:
            potential = m.split(")")[0].split(",")
            if len(potential) < 2:
                continue
            if not potential[0].isdigit() or not potential[1].isdigit():
                continue
            total += int(potential[0])*int(potential[1])
    return total

def star3(data):
    total = 0
    for line in data:
        total += get_mult_from_string(line)
    return total

def star2(data):
    total = 0
    for line in data:
        do = line.split("do()")
        for d in do:
            l = d.split("don't()")[0]
            total += get_mult_from_string(l)
    return total

def get_mult_from_string(s:str) -> int:
    total = 0
    mul = s.split("mul(")
    # print(l)
    for m in mul:
        potential = m.split(")")[0].split(",")
        #print(potential)
        if len(potential) != 2:
            continue
        if not potential[0].isdigit() or not potential[1].isdigit():
            continue
        total += int(potential[0])*int(potential[1])
    return total

def main():
    import cProfile
    import pstats
    with cProfile.Profile() as pr:
        day_()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    stats.dump_stats(filename = 'profiling.prof')

if __name__ == '__main__':
    main()