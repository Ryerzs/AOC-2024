import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
from collections import Counter, deque

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
    data = Counter()
    for row in raw.splitlines():
        for c in row.split(' '):
            data[c] += 1
    return data
    
def star1(data):
    n = 25
    stones = blink(data, n)

    total = sum([number for number in stones.values()])
    return total

def star2(data):
    n = 75
    stones = blink(data, n)

    total = sum([number for number in stones.values()])
    return total

def blink(data, n):
    stones = data.copy()
    for i in range(n):
        next_stones = Counter()
        for stone, number in stones.items():
            if len(stone) % 2 == 0:
                s1 = str(int(stone[:len(stone)//2]))
                s2 = str(int(stone[len(stone)//2:]))
                next_stones[s1] += number
                next_stones[s2] += number
            elif int(stone) == 0:
                next_stones['1'] += number
            else:
                next_stones[str(int(stone)*2024)] += number
        stones = next_stones.copy()
    return stones

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