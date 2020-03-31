import numpy as np
import draw
import moves
from os import remove
from completeCube import complete, complete_hash
from itertools import product
import imageio
from pygifsicle import optimize
from time import clock

POSSIBLE_MOVES = "rRlLuUdDfFbB"

def hash_cube(cube):
    hash_string = [x for x in np.nditer(cube)]
    return hash_string

def calc_cycle_num_from_string(move_string):
    count = 0
    cube = complete
    current_hash = ""
    while current_hash != complete_hash:
        count+=1
        for move in move_string:
            cube = moves.moves[move](cube)
        current_hash = hash_cube(cube)
    return count

def make_instructions(starting_instruction=None, start_length=1, max_length=0):
    while start_length != max_length:
        for count, x in enumerate(product(POSSIBLE_MOVES, repeat=start_length)):
            if starting_instruction:
                if count % 10000 == 0:
                    print(f"Getting Ready For New Instructions {count}", end='\r')
                if ''.join(x) == starting_instruction:
                    print("\nMaking New Instructions")
                    starting_instruction = None
            else:
                yield ''.join(x)
        start_length+=1

def make_images_from_string(move_string):
    cycle_count = 0
    move_count = 0
    filenames = []
    cube = complete
    current_hash = ""
    draw.draw_cube(cube,f"output/{move_string}_{move_count:06}.png")
    filenames.append(f"output/{move_string}_{move_count:06}.png")
    move_count+=1
    draw.draw_cube(cube,f"output/{move_string}_{move_count:06}.png")
    filenames.append(f"output/{move_string}_{move_count:06}.png")
    while current_hash != complete_hash:
        cycle_count+=1
        for move in move_string:
            move_count+=1
            cube = moves.moves[move](cube)
            draw.draw_cube(cube,f"output/{move_string}_{move_count:06}.png")
            filenames.append(f"output/{move_string}_{move_count:06}.png")
        current_hash = hash_cube(cube)
    return filenames
    
def make_gif_from_string(move_string):
    filenames = make_images_from_string(move_string)
    with imageio.get_writer(f'output/{move_string}.gif', mode='I', fps=3) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image,)
    optimize(f'output/{move_string}.gif')
    for filename in filenames:
        remove(filename)
    return f'output/{move_string}.gif'

def compute_cycles_sequence(resume_work=True, max_length=0, redundancy=False):
    count=0
    instruct = ""
    print("Script started! Press ctrl+c to stop!")
    try:
        if(resume_work):
            with open("output.log",'r') as f:
                for line in f:
                    if count % 10000 == 0:
                        print(f"Reading Past Instructions From Log {count}", end='\r')
                    instruct, _ = line.split("\t")
                    count+=1
                print("\nDone Reading.")
        else:
            remove("output.log")
    except FileNotFoundError:
        pass
    with open("output.log",'a') as f:
        for count, x in enumerate(make_instructions(instruct, max_length=max_length), start=count):
            if redundancy or not is_instruction_redundant(x):
                result = calc_cycle_num_from_string(x)
            else:
                result = "Redundant"
            if count % 100 == 0:
                f.flush()
                print(f"{x}\t{count}\t{result}")
            f.write(f"{x}\t{result}\n")

def minimize_instruction_string(move_string):
    while True:
        cube = complete
        hash_table = [(complete_hash)]
        for move_index, move in enumerate(move_string):
            cube = moves.moves[move](cube)
            current_hash = hash_cube(cube)
            try:
                key = hash_table.index((current_hash))
                move_string = move_string[:key] + move_string[move_index+1:]
                break
            except ValueError:
                hash_table.append((current_hash))
        else:
            break
    return move_string

def is_instruction_redundant(move_string):
    cube = complete
    hash_table = [(complete_hash)]
    for move_index, move in enumerate(move_string):
        cube = moves.moves[move](cube)
        current_hash = hash_cube(cube)
        if current_hash in hash_table:
            return True
        else:
            hash_table.append((current_hash))
    return False

def get_highest_cycle_number_from_log():
    highest = ("",0)
    count = 0
    with open("output.log",'r') as f:
        for line in f:
            instruct, cycles = line.split("\t")
            count += 1
            if cycles == "Redundant\n":
                continue
            cycles = int(cycles)
            if cycles > highest[1]:
                highest = (instruct, cycles)
    return (highest[0], highest[1], count)

if __name__ == "__main__":
    try:
        compute_cycles_sequence(redundancy=True)
    except KeyboardInterrupt:
        print(get_highest_cycle_number_from_log())