import cs50

print("Height: ", end="")
height = cs50.get_int()

while(height < 0 or height > 23):
    print("Height: ", end="")
    height = cs50.get_int()

total_space = height + 1

for i in range(height):
    number_of_hash = i + 2;
    for j in range(total_space - number_of_hash):
        print(" ", end="")
    for k in range(number_of_hash):
        print("#", end="")
    print("")