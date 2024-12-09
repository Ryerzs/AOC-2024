import time
from collections import deque
# import numpy as np
import heapq

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
    file = []
    space = []
    with open(path) as f:
        is_file = True
        rows = f.read().splitlines()
        for row in rows:
            for c in row:
                if is_file:
                    file.append(int(c))
                    is_file = False
                else:
                    space.append(int(c))
                    is_file = True
    return [file, space]
    
def star1(data):
    checksum = 0
    list_format = []
    empty_indices = deque()
    occupied_indices = deque()
    file, space = data[0], data[1]
    running_index = 0
    for i, number in enumerate(file):
        for j in range(number):
            list_format.append(i)
            occupied_indices.append(running_index)
            running_index += 1
        if len(space) <= i:
            continue
        for j in range(space[i]):
            list_format.append(None)
            empty_indices.append(running_index)
            running_index += 1
    # print(list_format)
    ind = empty_indices.popleft()
    file_index = occupied_indices.pop()
    while empty_indices and ind < file_index:
        list_format[ind] = list_format[file_index]
        list_format[file_index] = None
        ind = empty_indices.popleft()
        file_index = occupied_indices.pop()
    # print(list_format)
    for i, number in enumerate(list_format):
        if number is not None:
            checksum += i * list_format[i]
    return checksum

def star2(data):
    checksum = 0
    list_format = []
    occupied_indices = deque()
    file, space = data[0], data[1]
    running_index = 0
    space_look_up = []
    for i in range(10):
        l = []
        heapq.heapify(l)
        space_look_up.append(l)
    for i, number in enumerate(file):
        for _ in range(number):
            list_format.append(i)
        occupied_indices.append((running_index,number))
        running_index += number
        if len(space) <= i:
            continue
        space_len = space[i]
        if space_len == 0:
            continue
        for j in range(space_len):
            list_format.append(None)
        heapq.heappush(space_look_up[space_len], running_index)
        running_index += space_len
    # print_list(list_format)
    while occupied_indices:
        file_info = occupied_indices.pop()
        file_index, file_len = file_info[0], file_info[1]
        space_index, space_len = get_space_index(file_len, file_index, space_look_up)
        if space_index is None:
            continue
        for i in range(file_len):
            list_format[i+space_index] = list_format[i+file_index]
            list_format[i+file_index] = None
        # print_list(list_format)
        new_space = space_len-file_len
        if new_space == 0:
            continue
        heapq.heappush(space_look_up[space_len-file_len], space_index + file_len)
    # print_list(list_format)
    for i, number in enumerate(list_format):
        if number is None:
            continue
        checksum += i * list_format[i]
    return checksum

def print_list(l):
    output = ""
    for el in l:
        if el is None:
            output = output + '.'
        else:
            output = output + str(el)
    print(output)

def get_space_index(number, file_index, space_look_up):
    ind = file_index
    smallest = 0
    for i in range(number, 10):
        if len(space_look_up[i]) == 0:
            continue
        temp_ind = heapq.heappop(space_look_up[i])
        if temp_ind < ind:
            if smallest != 0:
                heapq.heappush(space_look_up[smallest], ind)
            ind = temp_ind
            smallest = i
        else:
            heapq.heappush(space_look_up[i], temp_ind)
    if ind == file_index:
        return None, None
    return ind, smallest


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