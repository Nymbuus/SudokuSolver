#Defines lists
vertical = []
box = []
horizontal = []


# Feeds the sudoku into the horizontal list.
# Makes integers out of the strings in the end.
# Returns a horizontal list with numbers from the unsolved sudoku.
#
#      - f = Cotains the file "Pussel.csv" which has the sudoku that will be solved.
#      - pussellist = This list contains the all the numbers as strings.
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


# Makes a 2D-list filled with zeros and returns it.
def zerolistMaker():
    listOfZeros = [[0] * 9] * 9
    return listOfZeros


# Fills in the vertical lane called for with the values form the horzontal lanes and returns it as a list.
def vertical_list_filler(i):
    return_List = []
    for j in range(0,9):
        return_List.append(horizontal[j][i])
    return return_List


# Fills in all the vertical lanes 
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
#
#      - box_number = Is the 3x3box which the function currently is checking.
#      - space_number = Is the space in the 3x3box which the functio currently is checking.
#      - number_check = Is the number that the function checks if it fits in the space.
#      - other_space_number = Is the other spaces in the 3x3box that the function is checking. Its checking if there is a missing number and
#                             if the number in the variable number_check is blocked in these spaces.
def check_for_solution(box_number,space_number):
    possible_box = []

    #Checks box for missing numbers
    for number_check in range(1,10):
        print(f"number_check={number_check}      box_number={box_number}")
        if number_check not in box[box_number]:
            possible_box.append(number_check)
            print(f'Possible box numbers: {possible_box}')
            # if the number isnt in the horizontal or vertical lane it continues
            print(f'number_check={number_check}   space_number={space_number}   space_number/3={int(space_number/3)}   box_number={box_number}   vertical_list={vertical[(space_number%3)+((box_number%3)*3)]}    horizontal_list={horizontal[(int(space_number/3))+(int(box_number/3)*3)]}')
            if number_check not in horizontal[(int(space_number/3))+(int(box_number/3)*3)] and number_check not in vertical[(space_number%3)+((box_number%3)*3)]:
                print("continue after horzontal and vertical check")
                for other_space_number in range(0,10):
                    if other_space_number != space_number:
                        print(f'other_space_number={other_space_number}')
                        if other_space_number == 9:
                            box[box_number][space_number] = number_check
                            print(f"BOX_CORDINATE[{box_number}][{space_number}] = number_check={number_check}")
                            return
                        elif box[box_number][other_space_number] == 0:
                            print(f"Check hori & verti blocking  other_space_number={other_space_number}  box_number={box_number}  vertical={((other_space_number%3))+((box_number%3)*3)}  horizontal_line={horizontal[int(other_space_number/3)]}  vertical_line={vertical[((other_space_number%3))+((box_number%3)*3)]}")
                            if number_check in horizontal[int(other_space_number/3)+(int(box_number/3)*3)] or number_check in vertical[((other_space_number%3))+((box_number%3)*3)]:
                                print(f"in this boxIndex={other_space_number} number_check={number_check} is blocked")
                            else:
                                break


# Goes through all the 3x3boxes and checks for any missing numbers(0). If there is then it calls the check_for_solution function and then update the sudokulists.
#
#      - box_number = Is the 3x3box which the function currently is checking.
#      - space_number = Is the space in the 3x3box which the functio currently is checking.
def the_sudoku_solver():
    for box_number in range(0,9):
        for box_space in range(0,9):
            if box[box_number][box_space] == 0:
                print(f'checking this number: {box[box_number][box_space]} in box {box_number}, {box_space}')
                check_for_solution(box_number,box_space)
                update()


# Update all the horizontal and vertical cordinates from the box cordinates.
#
#      - horizontal_lane = Horizontal lanes in the sudoku from top to bottom
#      - vertical_lane = Vertical lanes in the sudoku from left to right
#      - box_number = the number of the 3x3box in the sudoku, starts top left to top right then one down to the far left and repeat.
#      - space_number = the number of the space in the in the 3x3box. Uses the same logic to count spaces as the 3x3box.
#      - box_row = There are three rows of boxes in the sudoku and this is the variable that selects that.
#      - space_row = Same logic as box_row but in the 3x3box itself.
def update():
    horizontal_lane = 0
    vertical_lane = 0
    for box_row in range(0,3):
        for space_row in range(0,3):
            for box_number in range(0+(box_row*3),3+(box_row*3)):
                for space_number in range(0+(space_row*3),3+(space_row*3)):
                    horizontal[horizontal_lane][vertical_lane] = box[box_number][space_number]
                    vertical[vertical_lane][horizontal_lane] = horizontal[horizontal_lane][vertical_lane]
                    vertical_lane += 1
                    if vertical_lane == 9:
                        vertical_lane = 0
                        horizontal_lane += 1
    print("UPDATED HORIZONTAL and VERTICAL LINES:")
    print("Horizontal Lines:\n")
    for i in range(0, 9):
        print(f"{horizontal[i]}")
    print("\nVertical Lines:\n")
    for i in range(0, 9):
        print(f"{vertical[i]}")


# Checks if there are any zeros left in the sudoku. If there is then it sudoku_solver function. If not it prints the solved sudoku.
#
#      - tries = Is the amount of iterations through the_sudoku_solver function before the sudoku is solved
#      - not_completed = this increments if the_sudoku_solver is called and the while loop will continue if above 0.
#                        If the_sudoku_solver isnt called then the while loop ends.
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

# Solves the sudoku.
check_if_solved()