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
    data = [[],[]]
    with open(path) as f:
        rows = f.read().splitlines()
        for row in rows:
            row = list(map(int, row.split("   ")))
            #print(row)
            data[0].append(row[0])
            data[1].append(row[1])
        #print(data)
    return data
    
def star1(data):
    data[0].sort()
    data[1].sort()
    data2 = zip(data[0], data[1])
    d = sum([abs(e1-e2) for (e1,e2) in data2])
    #print(d)
    return d

def star2(data):
    total = 0
    count_left = count_map(data[0])
    count_right = count_map(data[1])
    for number, count in count_left.items():
        if number not in count_right:
            continue
        total += number*count*count_right[number]
    return total

def count_map(l:list[int]) -> dict:
    count_dict = {}
    for number in l:
        if number not in count_dict:
            count_dict[number] = 1
        else:
            count_dict[number] += 1
    return count_dict

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