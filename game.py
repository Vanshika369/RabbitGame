import random
import msvcrt
import os
import copy
from collections import deque
import itertools

while True:
 
    print("Instructions:")
    print("Press Enter to play the game; Press any other key to Quit.")
    print("Repeat the same after every play.")
 
    if msvcrt.getch().decode('utf-8') != '\r':
        break
 
    grid_size = int(input("Enter grid size: "))
    number_of_carrots = int(input("Enter number of carrots: "))
    number_of_holes = int(input("Enter number of holes: "))
 
    def create_grid(n):
        grid = [['-' for _ in range(n)] for _ in range(n)]
        return grid
 
    def placeCarrotsAndHoles(grid, n, m):
        carrots = 0
        holes = 0
        while carrots < n:
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, grid_size - 1)
            if grid[row][col] == "-":
                grid[row][col] = 'c'
                carrots += 1
 
        while holes < m:
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, grid_size - 1)
            if grid[row][col] == "-":
                grid[row][col] = 'O'
                holes += 1
 
        while True:
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, grid_size - 1)
            if grid[row][col] == "-":
                rabbit = 'r'
                grid[row][col] = rabbit
                return rabbit, row, col
 
    def print_grid(grid):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in grid:
            print(' '.join(row))
 
    def move_rabbit(grid, direction, rabbit, rabbit_row, rabbit_col):
        new_row, new_col = rabbit_row, rabbit_col
 
        if direction == 'w' and rabbit_row > 0:
            new_row -= 1
        elif direction == 's' and rabbit_row < grid_size - 1:
            new_row += 1
        elif direction == 'a' and rabbit_col > 0:
            new_col -= 1
        elif direction == 'd' and rabbit_col < grid_size - 1:
            new_col += 1
 
        if grid[new_row][new_col] == '-':
            grid[rabbit_row][rabbit_col] = '-'
            rabbit_row, rabbit_col = new_row, new_col
            grid[rabbit_row][rabbit_col] = rabbit
 
        return rabbit, rabbit_row, rabbit_col
 
    def get_key():
        return msvcrt.getch().decode('utf-8')
 
    # Main game loop
    grid = create_grid(grid_size)
    rabbit, rabbit_row, rabbit_col = placeCarrotsAndHoles(grid, number_of_carrots, number_of_holes)
    copy_grid = copy.deepcopy(grid)
    copy_rabbit_row = rabbit_row
    copy_rabbit_col = rabbit_col
    print_grid(grid)
 
    def pick_carrot(grid, rabbit, rabbit_row, rabbit_col):
        moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        for dr, dc in moves:
            new_row, new_col = rabbit_row + dr, rabbit_col + dc
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] == 'c':
                rabbit = 'R'
                grid[new_row][new_col] = rabbit
                grid[rabbit_row][rabbit_col] = '-'
                return rabbit, new_row, new_col
        return rabbit, rabbit_row, rabbit_col
 
    def place_carrot(grid, rabbit_row, rabbit_col):
        moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        for dr, dc in moves:
            new_row, new_col = rabbit_row + dr, rabbit_col + dc
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] == 'O':
                return True
        return False
 
    def jump_hole(grid, rabbit, rabbit_row, rabbit_col):
        moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        for dr, dc in moves:
            new_row, new_col = rabbit_row + dr, rabbit_col + dc
            nr, nc = rabbit_row + dr * 2, rabbit_col + dc * 2
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == '-' and grid[new_row][new_col] == 'O':
                grid[nr][nc] = rabbit
                grid[rabbit_row][rabbit_col] = '-'
                return rabbit, nr, nc
        return rabbit, rabbit_row, rabbit_col
 
    def optimalSimulation(grid):
        def distance(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        
        def is_valid_move(grid, start, end):
            r_start, c_start = start
            r_end, c_end = end
            
            # Check if there are any obstacles between start and end
            if r_start == r_end:
                for c in range(min(c_start, c_end) + 1, max(c_start, c_end)):
                    if grid[r_start][c] != '-':
                        return False
            elif c_start == c_end:
                for r in range(min(r_start, r_end) + 1, max(r_start, r_end)):
                    if grid[r][c_start] != '-':
                        return False
            return True
 
        def find_shortest_path(grid):
            rows, cols = len(grid), len(grid[0])
            rabbit_pos = None
            carrots = []
            holes = []
            
            for r in range(rows):
                for c in range(cols):
                    if grid[r][c] == 'r':
                        rabbit_pos = (r, c)
                    elif grid[r][c] == 'c':
                        carrots.append((r, c))
                    elif grid[r][c] == 'O':
                        holes.append((r, c))
 
            shortest_distance = float('inf')
            shortest_path = None
 
            # Iterate through all possible combinations of picking a carrot and dropping it in a hole
            for carrot, hole in itertools.product(carrots, holes):
                total_distance = distance(rabbit_pos, carrot) + distance(carrot, hole)
                
                # Check if the path between rabbit, carrot, and hole is valid
                if is_valid_move(grid, rabbit_pos, carrot) and is_valid_move(grid, carrot, hole):
                    if total_distance < shortest_distance:
                        shortest_distance = total_distance
                        shortest_path = (carrot, hole)
 
            return rabbit_pos, shortest_path, shortest_distance
 
        rabbit_pos, shortest_path, shortest_distance = find_shortest_path(grid)
 
        def print_grid(grid):
            for row in grid:
                print(' '.join(row))
 
        def move_rabbit_to_point(grid, start, end):
            r_start, c_start = start
            r_end, c_end = end
            grid[r_start][c_start] = '-'  # Clear rabbit's current position
            grid[r_end][c_end] = 'r'      # Move rabbit to new position
 
        print("\nPrinting Optimal Emulation\n")
        print("Rabbit starting position:", rabbit_pos)
        print("Optimal path (Carrot, Hole):", shortest_path)
        print("Shortest distance:", shortest_distance)
        print("Initial Grid:")
        print("\n")
        print_grid(grid)
 
 
        # Move the rabbit to the carrot
        move_rabbit_to_point(grid, rabbit_pos, shortest_path[0])
        grid[shortest_path[0][0]][shortest_path[0][1]] = 'R'
        print("\nAfter moving to carrot:")
        print_grid(grid)
 
        # Move the rabbit to the hole
        move_rabbit_to_point(grid, shortest_path[0], shortest_path[1])
        grid[shortest_path[1][0]][shortest_path[1][1]] = 'R'
        print("\nAfter dropping carrot in hole:")
        print_grid(grid)
 
 
 
    while True:
        move = get_key()
        if move == 'q':
            break
        elif move in ['w', 's', 'a', 'd']:
            rabbit, rabbit_row, rabbit_col = move_rabbit(
                grid, move, rabbit, rabbit_row, rabbit_col)
            print_grid(grid)
        elif move == 'p' and rabbit == 'r':
            rabbit, rabbit_row, rabbit_col = pick_carrot(
                grid, rabbit, rabbit_row, rabbit_col)
            print_grid(grid)
        elif move == 'p' and rabbit == 'R':
            if (place_carrot(grid, rabbit_row, rabbit_col) == True):
                optimalSimulation(copy_grid)
                break
        elif move == 'j':
            rabbit, rabbit_row, rabbit_col = jump_hole(
                grid, rabbit, rabbit_row, rabbit_col)
            print_grid(grid)