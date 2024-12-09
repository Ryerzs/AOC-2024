import time

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
            s, instr = row.split(': ')
            s = int(s)
            instr = [int(n) for n in instr.split(' ')]
            data.append((s, instr))
    return data
    
def star1(data):
    total = 0
    for result, instructions in data:
        combinations = []
        for instr in instructions:
            if len(combinations) == 0:
                combinations = [instr]
                continue
            mult = [el*instr for el in combinations]
            add  = [el+instr for el in combinations]
            combinations = add + mult 

        if result in combinations:
            total += result
    return total

def star2(data):
    total = 0
    for result, instructions in data:
        length = len(instructions)
        combinations_forward = [instructions[0]]
        combinations_backward = [result]
        # for i in range(1, length//2):
        #     instr = instructions[i]
        #     mult = []
        #     add = []
        #     concat = []
        #     for el in combinations_forward:
        #         mult.append(el*instr)
        #         add.append(el+instr)
        #         concat.append(concat_func(el,instr))
        #     combinations_forward = add + mult + concat
        # for i in range(length-length//2):
        for i in range(length-1):
            instr = instructions[length-i-1]
            mult = []
            add = []
            concat = []
            for el in combinations_backward:
                if el%instr == 0:
                    mult.append(el//instr)
                if el-instr >= 0:
                    add.append(el-instr)
                if is_concatenation(el,instr):
                    # print(instr)
                    concat.append(remove_end(el,len(str(instr))))
            combinations_backward = add + mult + concat
            # print(combinations_backward)

        # if result in set(combinations_forward).intersection(set(combinations_backward)):
        # print(result, combinations_backward)
        if instructions[0] in combinations_backward:
            total += result
    return total

def is_concatenation(n1,n2):
    s1 = str(n1)
    s2 = str(n2)
    l1 = len(s1)
    l2 = len(s2)
    if l2 >= l1:
        # print(l1, l2)
        return False
    if s1[(l1-l2):] == s2:
        return True
    return False

def remove_end(number, i):
    # print(number, i)
    s = str(number)
    return int(s[:-i])

def concat_func(n1, n2):
    return int(str(n1) + str(n2))

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