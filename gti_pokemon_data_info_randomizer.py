import sys, random

gti_valid_moves_file = open("gti_valid_moves", "r")
valid_moves = []
for x in gti_valid_moves_file:
    valid_moves.append(int(x, base=16).to_bytes(2, byteorder='little'))
gti_valid_moves_file.close()

gti_valid_abilities_file = open("gti_valid_abilities", "r")
valid_abilities = []
for x in gti_valid_abilities_file:
    valid_abilities.append(int(x, base=16))
gti_valid_abilities_file.close()

movements = [0b1011, 0b10011, 0b1000011, 0b11011, 0b1001011, 0b1010011, 0b11]
# water, lava, fly, combinations

types = ["None", "Normal", "Grass", "Fire", "Water", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "No type"]

pokemon_ids = [x for x in range(0x1, 0x9E)]
pokemon_ids.append(0xBE) # Substitute
pokemon_ids.remove(0x14) # Lugia
pokemon_ids.remove(0x15) # Ho-Oh
pokemon_ids.remove(0x95) # Reshiram
pokemon_ids.remove(0x96) # Zekrom
pokemon_ids.remove(0x98) # Kyurem
pokemon_ids.remove(0x9C) # Kyurem (White)
pokemon_ids.remove(0x9D) # Kyurem (Black)

input_file = input("Path to input pokemon_data_info.bin file: ")
file = open(input_file, "rb")
data = bytearray(file.read())

entry = 0
size_of_entry = 0xE0

chosen_seed = input("Enter seed: ")
random.seed(chosen_seed)

all_evolutions = input("Randomize all evolution slots for all Pokémon? y/n: ")
if all_evolutions == "y":
    all_evolutions = True
else:
    all_evolutions = False

learnable_TMs = 0x0
moves = 0x10
levelups = 0x44
movement = 0x60
evolution = 0x7C
abilities = 0xD8
types = 0xDB

while entry < 0xF6: # amount of entries
    learnable_TMs += size_of_entry # size of each entry
    moves += size_of_entry
    levelups += size_of_entry
    movement += size_of_entry
    evolution += size_of_entry
    abilities += size_of_entry
    types += size_of_entry
    entry += 1

    for x in range(0xF):
        data[learnable_TMs+x] = random.randint(0x00, 0xFF)

    for x in range(0, 56, 2):
        data[moves+x:moves+x+2] = random.choice(valid_moves)

    for x in range(28):
        if x == 0:
            data[levelups+x] = 1
        else:
            data[levelups+x] = random.randint(1, 100)

    data[movement] = random.choice(movements)


    add = 0

    for x in range(7):
        data[evolution+add+0x2] = random.choice(pokemon_ids)
        data[evolution+add+0x4] = 0x00 # always evolve without item
        data[evolution+add+0x8] = 0x00 # always evolve without friendship?
        data[evolution+add+0xA] = random.randint(1, 100)
        data[evolution+add+0xB] = 0x01 # always evolve by level
        if all_evolutions:
         add += 0xC
        # currently doesn't change all of Eevee's evolutions without giving everyone tons of overlapping evolutions

    data[abilities] = random.choice(valid_abilities)
    data[abilities+1] = random.choice(valid_abilities)

    data[types] = random.randint(1, 17)
    data[types+1] = random.randint(0, 17) # should I make it so you never get the same type twice?


file.close()

output_file = input("Output file path: ")
file = open(output_file, "wb")
file.write(data)
file.close()
