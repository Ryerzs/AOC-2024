import time

def day_():
    path = "data.txt"
    # path = "test-data.txt"

    start_time = time.perf_counter()
    width, height, data = get_data(path)

    time1 = time.perf_counter()

    ans1 = star1(width, height, data)
    time2 = time.perf_counter()

    ans2 = star2(width, height, data)
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
    data = {}
    width = 0
    height = 0
    with open(path) as f:
        rows = f.read().splitlines()
        height = len(rows)
        width =  len(rows[0])
        for i, row in enumerate(rows):
            for j, c in enumerate(row):
                if c != '.':
                    add_char_to_data(c, i, j, data)
            # print(row)
            # data.append(row)
    return width, height, data

def add_char_to_data(c, i, j, data):
    if c not in data:
        data[c] = [(i,j)]
    else:
        data[c].append((i,j))
    
def star1(width, height, data):
    antinode_locations = set()
    print(width, height, data)
    for frequency in data.values():
        all_pairs = get_all_pairs(frequency)
        print(len(all_pairs))
        for (p1, p2) in all_pairs:
            distance_vec = get_distance(p1,p2)
            # print(distance_vec)
            next_1 = add_vec(p2,distance_vec)
            next_2 = sub_vec(p1,distance_vec)
            if in_bounds(next_1, width, height):
                antinode_locations.add(next_1)
            if in_bounds(next_2, width, height):
                antinode_locations.add(next_2)
    # print(antinode_locations)
    # recreate_map(width, height, data, antinode_locations)
    return len(antinode_locations)

def recreate_map(width, height, data, antinode_locations):
    for i in range(height):
        row = []
        for j in range(width):
            frequency = is_at_frequency((i,j), data)
            if ((i,j) in antinode_locations) and (frequency is None):
            # if ((i,j) in antinode_locations):
                # print('huh')
                row.append('#')
            elif frequency != None:
                # print(frequency)
                row.append(frequency)
            else:
                row.append('.')
        print(''.join(row))



def is_at_frequency(p, data):
    for f, pos in data.items():
        if p in pos:
            return f
    return None

def get_all_pairs(frequency:list[tuple]):
    pairs = []
    for i in range(len(frequency)):
        for j in range(i+1, len(frequency)):
            pairs.append((frequency[i], frequency[j]))
    return pairs

def get_distance(p1, p2):
    return (p2[0]-p1[0], p2[1]-p1[1])

def add_vec(p, distance_vec):
    return (p[0] + distance_vec[0], p[1] + distance_vec[1])

def sub_vec(p, distance_vec):
    return (p[0] - distance_vec[0], p[1] - distance_vec[1])

def in_bounds(p, width, height):
    if p[0]>=0 and p[1]>=0 and p[0]<height and p[1] < width:
        return True
    return False

def star2(width, height, data):
    antinode_locations = set()
    print(width, height, data)
    for frequency in data.values():
        all_pairs = get_all_pairs(frequency)
        # print(len(all_pairs))
        for (p1, p2) in all_pairs:
            distance_vec = get_distance(p1,p2)
            # print(distance_vec)
            points = get_points_on_line(p1, distance_vec, width, height)
            for point in points:
                antinode_locations.add(point)
    # print(antinode_locations)
    recreate_map(width, height, data, antinode_locations)
    return len(antinode_locations)

def get_points_on_line(p, dist, width, height):
    points = []
    (y_0, x_0), (b,a) = p, dist
    b *= a//abs(a)
    a *= a//abs(a)
    X = []
    start_i = 0
    for i in range(-width//a-1, width//a+1):
        new_x = i*a+x_0
        if new_x >= 0 and new_x < width:
            X.append(new_x)
        if i == 0:
            start_i = -len(X)+1
    for x in X:
        new_y = y_0 + b*start_i
        if new_y >= 0 and new_y < height:
            points.append((new_y, x))
        start_i += 1
    return points



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