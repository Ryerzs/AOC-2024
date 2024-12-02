import time
from copy import deepcopy

def day_():
    path = "data.txt"
    # path = "test-data.txt"

    start_time = time.perf_counter()
    data = get_data(path)

    time1 = time.perf_counter()

    ans1 = star1(data)
    time2 = time.perf_counter()

    ans2 = star2(data)
    time3 = time.perf_counter()

    load_time = time1 - start_time
    star1_time = time2 - time1
    star2_time = time3 - time2
    if 1:
        print(f'Load time: {load_time}')
        print(f'Star 1 time: {star1_time}')
        print(f'Star 2 time: {star2_time}')
        print(f'Star 1 answer: {ans1}')
        print(f'Star 2 answer: {ans2}')

def get_data(path):
    data = []
    with open(path) as f:
        rows = f.read().splitlines()
        for row in rows:
            row = list(map(int, row.split(" ")))
            #print(row)
            data.append(row)
    return data
    
def star1(data):
    safe = 0
    for report in data:
        if safe_increase(report) or safe_decrease(report):
            safe +=1
    return safe

def safe_increase(l:list[int]) -> bool:
    for i in range(len(l)-1):
        if l[i] >= l[i+1]:
            return False
        if l[i] < l[i+1] - 3:
            return False
    return True

def safe_decrease(l:list[int]) -> bool:
    for i in range(len(l)-1):
        if l[i] <= l[i+1]:
            return False
        if l[i] > l[i+1] + 3:
            return False
    return True

def star2(data):
    safe = 0
    for report in data:
        if safe_dampener(report):
            safe +=1
    return safe

def safe_dampener(l:list[int]) -> bool:
    for j in range(len(l)):
        new_list = l[0:j] + l[(j+1):]
        if safe_increase(new_list) or safe_decrease(new_list):
            return True
    return False

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