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
    height = len(data)
    width = len(data[0])
    obstacles = []
    path_set = set()
    for i in range(height):
        for j in range(width):
            if data[i][j] == '^':
                start = (i,j)
            if data[i][j] == '#':
                obstacles.append((i,j))
    direction = (-1,0)
    path_set.add(start)
    
    while not at_edge(start, width, height):
        next_pos = (start[0] + direction[0], start[1] + direction[1])
        while next_pos in obstacles:
            direction = rotate_right(direction)
            next_pos = (start[0] + direction[0], start[1] + direction[1])
        start = next_pos
        path_set.add(start)

    return len(path_set)

def at_edge(pos, width, height) -> bool:
    if pos[0]<=0 or pos[1]<=0 or pos[0]>=height-1 or pos[1] >= width-1:
        return True
    return False

def rotate_right(direction):
    # (-1, 0) -> ( 0, 1)
    # ( 0, 1) -> ( 1, 0)
    # ( 1, 0) -> ( 0,-1)
    # ( 0,-1) -> (-1, 0)
    if direction[0] != 0:
        return (0, direction[0]*-1)
    else:
        return (direction[1], 0)


def star2(data):
    height = len(data)
    width = len(data[0])
    obstacles = []
    loop_possibility = set()
    path_set = set()
    for i in range(height):
        for j in range(width):
            if data[i][j] == '^':
                start = (i,j)
            if data[i][j] == '#':
                obstacles.append((i,j))
    direction = (-1,0)
    path_set.add((start, direction))
    
    while not at_edge(start, width, height):
        next_pos = (start[0] + direction[0], start[1] + direction[1])

        if line_of_sight_has_visited(start, rotate_right(direction), path_set, obstacles, width, height):
            # print(next_pos)
            loop_possibility.add(next_pos)

        while next_pos in obstacles:
            direction = rotate_right(direction)
            next_pos = (start[0] + direction[0], start[1] + direction[1])
            if line_of_sight_has_visited(start, rotate_right(direction), path_set, obstacles, width, height):
                # print(next_pos)
                loop_possibility.add(get_next_pos(start, rotate_right(direction)))
        start = next_pos
        path_set.add((start, direction))
    print(loop_possibility)
    return len(loop_possibility)

def get_next_pos(start, direction):
    return (start[0] + direction[0], start[1] + direction[1])

def line_of_sight_has_visited(start, direction, path_set, obstacles, width, height):
    next_pos = (start[0] + direction[0], start[1] + direction[1])
    while next_pos not in obstacles and not at_edge(next_pos, width, height):
        possible_obstruction = (next_pos, direction)
        if possible_obstruction in path_set:
            return True
        next_pos = (next_pos[0] + direction[0], next_pos[1] + direction[1])
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