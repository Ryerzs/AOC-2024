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
            # print(row)
            data.append(row)
    return data
    
def star1(data):
    total = 0
    total += find_in_grid("XMAS", data)
    total += find_in_grid("XMAS", reverse(data))
    total += find_in_grid("XMAS", vertical(data))
    total += find_in_grid("XMAS", reverse(vertical(data)))
    total += find_in_grid("XMAS", diagonal_right(data))
    total += find_in_grid("XMAS", reverse(diagonal_right(data)))
    total += find_in_grid("XMAS", diagonal_left(data))
    total += find_in_grid("XMAS", reverse(diagonal_left(data)))

    return total

def find_in_grid(s:str, grid:list[str]):
    total = 0
    for line in grid:
        total += find_in_string(s, line)
    return total

def find_in_string(s:str, line:str):
    if s in line:
        return len(line.split(s))-1
    return 0

def reverse(l:list[str]):
    data = []
    for line in l:
        data.append(line[::-1])
    return data

def vertical(l:list[str]):
    data = ["" for i in range(len(l[0]))]
    for line in l:
        for i in range(len(line)):
            data[i] = data[i] + line[i]
    return data

def diagonal_right(l:list[str]):
    # Assuming symmetric, otherwise I would need modolu
    data = []
    length = len(l[0])
    for j in range(length-3):
        diag1 = ""
        diag2 = ""
        for i in range(length):
            if i+j >= length:
                continue
            diag1 = diag1 + l[i+j][i]
            diag2 = diag2 + l[i][i+j]
        data.append(diag1)
        if j!=0:
            data.append(diag2)
    return data

def diagonal_left(l:list[str]):
    # Assuming symmetric, otherwise I would need modolu
    data = []
    length = len(l[0])
    for j in range(length-3):
        diag1 = ""
        diag2 = ""
        for i in range(length):
            if i+j >= length:
                continue
            diag1 = diag1 + l[length-1-i-j][i]
            diag2 = diag2 + l[length-1-i][i+j]
        data.append(diag1)
        if j!=0:
            data.append(diag2)
    return data

def star2(data):
    total = 0
    for j in range(1,len(data)-1):
        for i in range(1, len(data)-1):
            if data[i][j] == 'A':
                r1 = data[i-1][(j-1):(j+2)]
                r3 = data[i+1][(j-1):(j+2)]
                total += is_x_mas(r1,r3)
    return total

def is_x_mas(r1:str, r3:str) -> int:
    c1, c2 = r1[0], r1[2]
    c3, c4 = r3[0], r3[2]
    tot_M = count_char('M', [c1,c2,c3,c4])
    tot_S = count_char('S', [c1,c2,c3,c4])
    if tot_M != 2 or tot_S != 2:
        return 0 


    if (c1==c2 or c1==c3):
        return 1    
    else:
        return 0

def count_char(match_char, s:list[str]) -> int:
    tot = 0
    for char in s:
        if char == match_char:
            tot += 1
    return tot

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