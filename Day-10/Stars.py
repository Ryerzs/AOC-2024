import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
from collections import deque

def day_():
    year = int(os.getcwd().split('\\')[-2][-4:]) 
    day = int(__file__.split('\\')[-2].split('-')[1].split('.')[0])
    puzzle = Puzzle(year=year, day=day) 
    submit_a = "a" in sys.argv
    submit_b = "b" in sys.argv
    example = "e" in sys.argv

    if (submit_a or submit_b) and example:
        print("Cannot submit examples")
        return

    raw_data = puzzle.input_data
    if example:
        print("Using example")
        #use 'aocd year day --example' to get the example data
        with open('test-data.txt', 'r') as f:
            raw_data = f.read()
            
    start_time = time.perf_counter()
    data = format_data(raw_data)

    time1 = time.perf_counter()

    ans1 = star1(data)
    time2 = time.perf_counter()

    ans2 = star2(data)
    time3 = time.perf_counter()

    load_time = time1 - start_time
    star1_time = time2 - time1
    star2_time = time3 - time2

    if submit_a:
        print("Submitting star 1")
        puzzle.answer_a = ans1
    if submit_b:
        print("Submitting star 2")
        puzzle.answer_b = ans2
    if 1:
        print(f'Load time: {load_time}')
        print(f'Star 1 time: {star1_time}')
        print(f'Star 2 time: {star2_time}')
        print(f'Star 1 answer: {ans1}')
        print(f'Star 2 answer: {ans2}')

def format_data(raw):
    data = []
    for row in raw.splitlines():
        data.append(row)
    height = len(data)
    width = len(data[0])
    adj_matrix = {}
    node_values = {}
    start_nodes = deque([])
    end_nodes = deque([])
    for j in range(width):
        for i in range(height):
            # Create all connections between nodes
            current_node = (i,j)
            adjecent_nodes = get_adjecent_nodes(i,j, height, width)
            for p in adjecent_nodes:
                add_to_adj_matrix(current_node, p, adj_matrix)
            # Add node value to lookup table
            node_values[current_node] = int(data[i][j])
            # Start and end nodes
            if node_values[current_node] == 0:
                start_nodes.append((i,j))
            elif node_values[current_node] == 9:
                end_nodes.append((i,j))
    return [adj_matrix, node_values, start_nodes, end_nodes]
    
def star1(data):
    total = 0
    [adj_matrix, node_values, start_nodes, end_nodes] = data
    for start in start_nodes:
        total += dijkstra_typ(start, adj_matrix, node_values, end_nodes, part1=True)

    return total
def dijkstra_typ(start, adj_matrix, node_values, end_nodes, part1) -> int:
    total = 0
    unexplored = deque([start])
    found = []
    while unexplored:
        node = unexplored.popleft()
        current_node_value = node_values[node]
        for neighbor in adj_matrix[node]:
            if node_values[neighbor] != current_node_value + 1:
                continue

            if neighbor in end_nodes and neighbor not in found:
                if part1:
                    found.append(neighbor)
                total += 1
            else:
                unexplored.append(neighbor)
    return total

def get_adjecent_nodes(i,j,height,width) -> list[tuple]:
    potential_nodes = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]
    valid_neighbors = []
    for p in potential_nodes:
        if p[0]>=0 and p[0] < height and p[1]>=0 and p[1] < width:
            valid_neighbors.append(p)
    return valid_neighbors

def add_to_adj_matrix(p1, p2, adj_matrix):
    if p1 not in adj_matrix:
        adj_matrix[p1] = set([p2])
    else:
        adj_matrix[p1].add(p2)
    if p2 not in adj_matrix:
        adj_matrix[p2] = set([p1])
    else:
        adj_matrix[p2].add(p1)

def star2(data):
    total = 0
    [adj_matrix, node_values, start_nodes, end_nodes] = data
    for start in start_nodes:
        total += dijkstra_typ(start, adj_matrix, node_values, end_nodes, part1=False)
    return total

def main():
    import cProfile
    import pstats
    with cProfile.Profile() as pr:
        day_()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    day = int(__file__.split('\\')[-2].split('-')[1].split('.')[0])
    stats.dump_stats(filename = f'profiling{day}.prof')

# run with `py day_n.py -- a b` to submit both stars for day n
if __name__ == '__main__':
    main()