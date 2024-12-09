import time

def day_():
    path = "data.txt"
    # path = "test-data.txt"

    start_time = time.perf_counter()
    data = get_data(path)
    arranged_numbers = create_arranged_numbers(data[0])

    time1 = time.perf_counter()

    ans1 = star1(data)
    time2 = time.perf_counter()

    ans3 = star3(arranged_numbers, data[0], data[1])
    ans2 = star2(data)
    print(ans3)
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


def create_arranged_numbers(rules):
    #Linked list of numbers
    list_index = {}
    for number, [_, greater] in rules.items():
        greatest_index = 0
        for l in greater:
            if l in list_index:
                greatest_index = max(greatest_index, list_index[l]+1)
        # print(greatest_index, number)
        add_value_to_list(number, greatest_index, list_index)

    sorted_list = [0]*len(list_index)
    # print(list_index)
    for n, index in list_index.items():
        sorted_list[index] = n
    print(sorted_list)
    return sorted_list

def add_value_to_list(n:int, index:int, list_index:dict):
    if index in list_index.values():
        #Recursion, less gooooo
        next_number = get_number_from_dict(index, list_index)
        list_index[n] = index
        add_value_to_list(next_number, index+1, list_index)
    else:
        list_index[n] = index

def get_number_from_dict(index:int, list_index:dict) -> int:
    for item, key in list_index.items():
        if key == index:
            return item


def get_data(path):
    rules = {}
    updates = []
    fetching_rules = True
    with open(path) as f:
        rows = f.read().splitlines()
        for row in rows:
            # print(row)
            if row == "":
                fetching_rules = False
                continue
            if fetching_rules:
                s = row.split("|")
                add_to_rules(s,rules)
            else:
                updates.append([int(n) for n in row.split(',')])
    return [rules, updates]

def add_to_rules(s, rules):
    n1, n2 = int(s[0]), int(s[1])
    if n1 not in rules:
        rules[n1] = [[n2], []]
    else:
        rules[n1][0].append(n2)
    if n2 not in rules:
        rules[n2] = [[], [n1]]
    else:
        rules[n2][1].append(n1)
    
def star1(data):
    total = 0
    rules, updates = data
    for update in updates:
        if is_valid_update(rules, update):
            total += update[(len(update)-1)//2]
    return total

def is_valid_update(rules:dict, update:list[int]) -> bool:
    valid = True
    for i in range(len(update)):
        current_number = update[i]
        for j in range(i+1, len(update)):
            n = update[j]
            if n in rules[current_number][1]:
                return False

    return valid

def star2(data):
    total = 0
    rules, updates = data
    for update in updates:
        if not is_valid_update(rules, update):
            fixed = fix_update(rules, update)
            # print(fixed)
            total += fixed[(len(fixed)-1)//2]
    return total

def star3(arranged_numbers, rules, updates):
    total = 0
    for update in updates:
        if not is_valid_update(rules, update):
            fixed = fix_update_2(arranged_numbers, update)
            total += fixed[(len(fixed)-1)//2]
    return total

def fix_update(rules:dict, update:list[int]) -> bool:
    #Bubbelsort ish
    current_index = 0
    updated = False
    while current_index < len(update)-1:
        updated = False
        current_number = update[current_index]
        number_index = current_index
        for j in range(current_index+1, len(update)):
            n = update[j]
            if n in rules[current_number][1]:
                # print(current_number, n)
                # print(update)
                update[number_index], update[j] = update[j], update[number_index]
                number_index = j
                updated = True
                # print(update)
                # print("***************************")
        if not updated:
            current_index += 1
    return update

def fix_update_2(arranged_numbers, update):
    fixed = [0]*len(update)
    order = []
    for number in update:
        index = get_number_from_list(arranged_numbers, number)
        order.append((index,number))
    order.sort(key=lambda x: x[0])
    # print(order)
    for i in range(len(order)):
        fixed[i] = order[i][1]
    return fixed

def get_number_from_list(arranged_numbers, number) -> int:
    for i, n in enumerate(arranged_numbers):
        if n == number:
            return i

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