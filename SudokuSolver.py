#Defines lists
vertical = []
box = []
horizontal = []


# Feeds the sudoku into the horizontal list.
# Makes integers out of the strings in the end.
def horizontal_list_filler():
    f = open('Pussel.csv')
    pussellist = []
    for line in f:
        pussellist.append(line.split(','))

    for i in range(0,9):
        horizontal.append(pussellist[0][i*9:(i+1)*9])
    
    for i in range(0,9):
        for j in range(0,9):
            horizontal[i][j] = int(horizontal[i][j])

    f.close()

    return horizontal


# Makes a 2D-list filled with zeros
def zerolistMaker():
    listOfZeros = [[0] * 9] * 9
    return listOfZeros


# Fills in the vertical lane called for
def vertical_list_filler(i):
    return_List = []
    for j in range(0,9):
        return_List.append(horizontal[j][i])
    return return_List


# Fills in all the vertical lanes with the values form the horzontal lanes.
def fill_in_vertical():
    for i in range(0,9):
        vertical.append(vertical_list_filler(i))
    return vertical


# Fills in the box requested with appropiate values from the horizontal list.
def fill_a_box(k,l):
    return_List = []
    for i in range(0,3):
        for j in range(0,3):
            return_List.append(horizontal[i+l][j+k])
    return return_List

# Fills in boxes with values
def fill_in_box():
    box = []
    for vertical_boxes in range(0,3):
        for horizontal_boxes in range(0,3):
            box.append(fill_a_box(horizontal_boxes*3,vertical_boxes*3))
    return box


# Checks for a solution 3x3box by 3x3box. Starts from top left, contiues to top right, goes down one step and starts from the left again until it reaches the last box.
# The same logic applies inside the boxes to find a missing number(0) and trying to resolve it.
# When the function has found missing number it will check what numbers(1-9) are missing inside the box.
# It takes the first number it finds that is missing in the box and matches it to the vertical and horizontal lane.
# If there is no match it will continue to look for other zeros in the box and match the number against their vertical and horizontal lane.
# If there is a match it will continue to look for more zeros in the box and repeat the process until it has gone through numbers 1-9.
# If this process goes all the way through with one number it will apply it to the space where it first checked.
# If the process dosnt go all the way through with the number it will check the next one and in the end jump to the next space to repeat the process.
# This process goes through all the 9x9 spaces in the soduko one time and there might be missing numbers that wasnt resolved but will be in the next time the function is called. 
def check_for_solution(i,j):
    possible_box = []

    #Checks box for missing numbers
    for k in range(1,10):
        print(f"k={k}      i={i}")
        if k not in box[i]:
            possible_box.append(k)
            print(f'Possible box numbers: {possible_box}')
            # if the number isnt in the horizontal or vertical lane it continues
            print(f'k={k}   j={j}   j/3={int(j/3)}   i={i}   vertical_list={vertical[(j%3)+((i%3)*3)]}    horizontal_list={horizontal[(int(j/3))+(int(i/3)*3)]}')
            if k not in horizontal[(int(j/3))+(int(i/3)*3)] and k not in vertical[(j%3)+((i%3)*3)]:
                print("continue after horzontal and vertical check")
                for l in range(0,10):
                    if l != j:
                        print(f'l={l}')
                        if l == 9:
                            box[i][j] = k
                            print(f"BOX_CORDINATE[{i}][{j}] = k={k}")
                            return
                        elif box[i][l] == 0:
                            print(f"Check hori & verti blocking  l={l}  i={i}  vertical={((l%3))+((i%3)*3)}  horizontal_line={horizontal[int(l/3)]}  vertical_line={vertical[((l%3))+((i%3)*3)]}")
                            if k in horizontal[int(l/3)+(int(i/3)*3)] or k in vertical[((l%3))+((i%3)*3)]:
                                print(f"in this boxIndex={l} k={k} is blocked")
                            else:
                                break

# Goes through all the 3x3boxes and checks for any missing numbers(0). If there is then it calls the check_for_solution function.
def the_sudoku_solver():
    for i in range(0,9):
        for j in range(0,9):
            if box[i][j] == 0:
                print(f'checking this number: {box[i][j]} in cordinates {i}, {j}')
                check_for_solution(i,j)
                update()

# Update all the horizontal and vertical cordinates from the box cordinates.
def update():
    i = 0
    j = 0
    for g in range(0,3):
        for h in range(0,3):
            for e in range(0+(g*3),3+(g*3)):
                for d in range(0+(h*3),3+(h*3)):
                    horizontal[i][j] = box[e][d]
                    vertical[j][i] = horizontal[i][j]
                    j += 1
                    if j == 9:
                        j = 0
                        i += 1
    print("UPDATED HORIZONTAL and VERTICAL LINES:")
    print("Horizontal Lines:\n")
    for i in range(0, 9):
        print(f"{horizontal[i]}")
    print("\nVertical Lines:\n")
    for i in range(0, 9):
        print(f"{vertical[i]}")

#Checks if there are any zeros left in the sudoku. If there is then it sudoku_solver function. If not it prints the solved sudoku.
def check_if_solved():
    tries = 0
    not_completed = 1
    while not_completed != 0:
        not_completed = 0
        for i in range(0,9):
            if 0 in horizontal[i]:
                the_sudoku_solver()
                not_completed += 1
                tries += 1


    print(f"tries={tries}")
    print("Solved!")
    for i in range(0,9):
        print(horizontal[i])


# Fills in all the values for the 3x3boxes, horizontal lanes and vertical lanes.
horizontal = horizontal_list_filler()
vertical = fill_in_vertical()
box = fill_in_box()

check_if_solved()