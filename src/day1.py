import os

def get_shift(instruction_str):
    """
    Input
    -----
    instruction_str : string
        L or R followed by integer value
    Output
    ------
    int
        Rotation value (+ve for clockwise)
    """
    rotation_dir = (-1) ** (instruction_str[0] == "L")
    return rotation_dir * int(instruction_str[1:])

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day1.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    instructions = file.readlines()
instructions = [get_shift(instruction_txt.strip()) for instruction_txt in instructions]
dial_pos = [50]
zero_passes = 0
zp_track = [0]
for shift in instructions:
    next_pos = dial_pos[-1]+shift
    times_passed_zero = next_pos//100
    zero_passes += (abs(times_passed_zero) +
     int(next_pos %100 == 0 and times_passed_zero <= 0) -
      int(dial_pos[-1] == 0 and times_passed_zero < 0))
    dial_pos.append(next_pos%100)
print("Part 1: ", dial_pos.count(0))
print("Part 2: ", zero_passes)
