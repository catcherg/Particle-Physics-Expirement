import dudraw
import random

# Constants used when first starting the elements 
EMPTY = 0
SAND = 1
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FLOOR = 2
WATER = 3


# Function that makes the list
def create_world(canvas_size_x: int) -> list[list]:
    """
    Description of function: function that creates the main list used for the pixels 
    Parameters: canvas_size_x
    Return: the list called sandlist
    """
    listofsand = [[EMPTY for col in range(canvas_size_x)] for row in range(canvas_size_x)]
    return listofsand


# Function to clear the canvas when drawing the world
def draw_world():
    """
    Description of function: Clears the screen to white
    Parameters: None
    Return: None 
    """
    dudraw.clear(dudraw.WHITE)


# Function to place a particle of sand at a given position
def place_sand(sandlist: list[list], x: int, y: int) -> None:
    """
    Description of function: Places a particle of sand at a given position 
    Parameters: Sandlist, x coordinate, y coordinate
    Return: None
    """
    if (sandlist[125 - y][x] == EMPTY):
        # if nothing there then draws the sand particles in yellow
        sandlist[125 - y][x] = SAND
        dudraw.set_pen_color(dudraw.YELLOW)
        dudraw.filled_square(x, y, 0.5)


# Function to place water into spots where there is none already
def place_water(sandlist: list[list], x: int, y: int) -> None:
    """
    Description of function: Places water into spots where there is none already
    Parameters: sandlist, x coordinate, y coordinate
    Return:None
    """
    if (sandlist[125 - y][x] == EMPTY):
        # if there is nothing there then draws water particles in the color blue
        sandlist[125 - y][x] = WATER
        dudraw.set_pen_color(dudraw.BOOK_LIGHT_BLUE)
        dudraw.filled_square(x, y, 0.5)


# Function to place floor particles 
def place_floor(sandlist: list[list], x: int, y: int) -> None:
    """
    Description of function: Places the particles that make the floor 
    Parameters: Sandlist, x coordinate, y coordinate
    Return: None 
    """
    if (0 <= 125 - y < len(sandlist)) and (0 <= x + 1 < len(sandlist[0])) and (0 <= 125 - y - 1 < len(sandlist)) and (0 <= 125 - y + 1 < len(sandlist)):
        # Check if the indices are within the bounds of the sandlist

        if (sandlist[125 - y][x] == EMPTY) and (sandlist[125 - y][x + 1] == EMPTY) and (sandlist[125 - y - 1][x] == EMPTY) and (sandlist[125 - y + 1][x] == EMPTY):
            # Places floor particles only if all positions are empty

            # Fill the area with floor particles
            for i in range(-1, 2):
                for j in range(-1, 2):
                    sandlist[125 - y + i][x + j] = FLOOR

            dudraw.set_pen_color(dudraw.BLACK)  # Change line color to black
            # Draw filled squares for the area
            for i in range(-1, 2):
                for j in range(-1, 2):
                    dudraw.filled_square(x + j, y + i, 0.5)


# Function that erases pixels
def erase(sandlist: list[list], x: int, y: int) -> None:
    """
    Description of function: Function that erases pixels already drawn 
    Parameters: Sandlist, x coordinate, y coordinate 
    Return: None 
    """
    if (sandlist[125 - y][x] != EMPTY):
        # if a particle is present it will make all four of the positions become empty 
        sandlist[125 - y][x] = EMPTY
        sandlist[125 - y][x + 1] = EMPTY
        sandlist[125 - y - 1][x] = EMPTY
        sandlist[125 - y - 1][x + 1] = EMPTY
        dudraw.set_pen_color(dudraw.WHITE)  # Change line color to white

        # redraws them all to be the background color white
        dudraw.filled_square(x, y, 0.5)
        dudraw.filled_square(x + 1, y, 0.5)
        dudraw.filled_square(x, y + 1, 0.5)
        dudraw.filled_square(x + 1, y + 1, 0.5)


# function that traverses through each pixel and checks if its making its way downwards. It helps makes the particles flow
def advance_world(sandlist: list[list], canvas_size_x: int) -> None:
    """
    Description of function: Function that traverses through each pixel and checks if its making its way downwards. It also helps
    with the flowing movement of the pixels 
    Parameters: Sandlist, canvas_size_x
    Return: None
    """
    for row_index in range(len(sandlist)):

        row = (canvas_size_x - row_index - 1)  # traverses through the entire list backwards. Subtracting one allows it to sit on a pixel

        for col_index in range(len(sandlist[0])):
            if sandlist[row][col_index] == SAND:
                if (row < len(sandlist) - 1) and (sandlist[row + 1][col_index] == EMPTY) and (
                        sandlist[row + 1][col_index] != FLOOR):
                    # makes sure that its less than the range of sandlist
                    # checks if the pixel below is empty 
                    # checks if its not the floor underneath the original pixel

                    swap_part(sandlist, row, col_index, (row + 1), col_index)
                elif (row < len(sandlist) - 1) and (sandlist[row + 1][col_index + 1] == EMPTY) and (
                        sandlist[row + 1][col_index + 1] != FLOOR):
                    # makes sure that its less than the range of sandlist
                    # checks if the bottom most right is empty 
                    # checks if the bottom most right is not floor 

                    swap_part(sandlist, row, col_index, (row + 1), col_index + 1)
                    # moves it to the right 

                elif (row < len(sandlist) - 1) and (sandlist[row + 1][col_index - 1] == EMPTY) and (
                        sandlist[row + 1][col_index] != FLOOR):
                    # makes sure that its less than the range of sandlist
                    # checks if the bottom left is empty 
                    # makes sure bottom left is not floor
                    swap_part(sandlist, row, col_index, (row + 1), col_index - 1)
                    # moves it to the left 

            elif sandlist[row][col_index] == WATER:

                if (row < len(sandlist) - 1) and (sandlist[row + 1][col_index] == EMPTY) and (
                        sandlist[row + 1][col_index] != FLOOR):
                    # checks to make sure its less than the range of sandlist
                    # checks if the next row is empty 
                    # checks if the one below it is not equal to floor 
                    swap_part(sandlist, row, col_index, (row + 1), col_index)
                else:
                    randomdirection = random.choice((-1, 1))
                    if (randomdirection == -1) and (row < len(sandlist) - 1) and (
                            sandlist[row][col_index - 1] == EMPTY) and (sandlist[row][col_index - 1] != FLOOR):
                        # chooses a random direction and continues in the direction
                        # goes to the corresponding direction if it is empty and not floor
                        swap_part(sandlist, row, col_index, (row), col_index - 1)
                        # swaps and goes left

                    elif (randomdirection == 1) and (row < len(sandlist) - 1) and (
                            sandlist[row][col_index + 1] == EMPTY) and (sandlist[row][col_index + 1] != FLOOR):
                        # if left go left and vice versa 
                        swap_part(sandlist, row, col_index, (row), col_index + 1)
                        # swaps and goes right
def advance_world(sandlist: list[list], canvas_size_x: int) -> None:
    """
    Moves particles (sand and water) down the grid, simulating their movement.
    """
    for row_index in range(len(sandlist)):

        row = (canvas_size_x - row_index - 1)

        for col_index in range(len(sandlist[0])):
            if sandlist[row][col_index] == SAND:
                if (row < len(sandlist) - 1) and (sandlist[row + 1][col_index] == EMPTY) and (
                        sandlist[row + 1][col_index] != FLOOR):
                    swap_part(sandlist, row, col_index, (row + 1), col_index)
                elif (row < len(sandlist) - 1) and (col_index < len(sandlist[0]) - 1) and (sandlist[row + 1][col_index + 1] == EMPTY) and (
                        sandlist[row + 1][col_index + 1] != FLOOR):
                    swap_part(sandlist, row, col_index, (row + 1), col_index + 1)

                elif (row < len(sandlist) - 1) and (col_index > 0) and (sandlist[row + 1][col_index - 1] == EMPTY) and (
                        sandlist[row + 1][col_index] != FLOOR):
                    swap_part(sandlist, row, col_index, (row + 1), col_index - 1)

            elif sandlist[row][col_index] == WATER:

                if (row < len(sandlist) - 1) and (sandlist[row + 1][col_index] == EMPTY) and (
                        sandlist[row + 1][col_index] != FLOOR):
                    swap_part(sandlist, row, col_index, (row + 1), col_index)
                else:
                    randomdirection = random.choice((-1, 1))
                    if (randomdirection == -1) and (col_index > 0) and (row < len(sandlist) - 1) and (
                            sandlist[row][col_index - 1] == EMPTY) and (sandlist[row][col_index - 1] != FLOOR):
                        swap_part(sandlist, row, col_index, (row), col_index - 1)

                    elif (randomdirection == 1) and (col_index < len(sandlist[0]) - 1) and (row < len(sandlist) - 1) and (
                            sandlist[row][col_index + 1] == EMPTY) and (sandlist[row][col_index + 1] != FLOOR):
                        swap_part(sandlist, row, col_index, (row), col_index + 1)


# traverses through the list backwards and changes the colors of the pixels 
def updatepixel(sandlist: list[list], row: int, col: int) -> None:
    """
    Description of function: Traverses through the list backwards and changes the colors of the pixels 
    Parameters: Sandlist, row , col 
    Return: None
    """
    lengthlist = len(sandlist) - row
    # traverse through sandlist backwards 

    if sandlist[row][col] == SAND:
        # makes the sand yellow 
        dudraw.set_pen_color(dudraw.YELLOW)
        dudraw.filled_square(col, lengthlist, 0.5)

    elif sandlist[row][col] == EMPTY:
        # makes the background white
        dudraw.set_pen_color(dudraw.WHITE)
        dudraw.filled_square(col, lengthlist, 0.5)

    elif sandlist[row][col] == FLOOR:
        # makes the floor black
        dudraw.set_pen_color(dudraw.BLACK)
        dudraw.filled_square(col, lengthlist, 0.5)
        dudraw.filled_square(col + 1, lengthlist, 0.5)
        dudraw.filled_square(col, lengthlist + 1, 0.5)
        dudraw.filled_square(col + 1, lengthlist + 1, 0.5)

    elif sandlist[row][col] == WATER:
        # makes the water blue
        dudraw.set_pen_color(dudraw.BOOK_LIGHT_BLUE)
        dudraw.filled_square(col, lengthlist, 0.5)


# swapping the particles 
def swap_part(sandlist: list[list], row1: int, col1: int, row2: int, col2: int) -> None:
    """
    Description of function: Swaps the particles with each other 
    Parameters: Sandist, row1, col1, row2, col2
    Return: None
    """
    pixel1 = sandlist[row1][col1]
    sandlist[row1][col1] = sandlist[row2][col2]  # swapping the original pixel with the one below it 
    sandlist[row2][col2] = pixel1  # swaps next pixel with the original pixel 

    updatepixel(sandlist, row1, col1)  # sends the new value to update the pixel to change the color and value
    updatepixel(sandlist, row2, col2)  # sends the new value to update the pixel to change the color and value


# Main function with the animation loop and associates keys with water, sand, etc.
def main():

    worldsize = 250
    canvas_size_x = int((worldsize / 2))
    canvas_size_y = int((worldsize / 2))

    dudraw.set_canvas_size(canvas_size_x * 5, canvas_size_y * 5)
    dudraw.set_x_scale(0, canvas_size_x)
    dudraw.set_y_scale(0, canvas_size_y)

    sandlist = create_world(canvas_size_x)

    draw_world()

    key = 's'

    while key != 'q':
        if dudraw.mouse_is_pressed():
            if key == 's':
                x = int(dudraw.mouse_x() + random.randint(-5, 5))
                y = int(dudraw.mouse_y())

                dudraw.set_pen_color(dudraw.WHITE)
                dudraw.filled_rectangle(5, 120, 50, 50)

                dudraw.set_pen_color(dudraw.BLACK)
                dudraw.set_font_size(50)
                dudraw.text(15, 120, "sand")

                place_sand(sandlist, x, y)

            if key == 'f':
                x = int(dudraw.mouse_x())
                y = int(dudraw.mouse_y())

                dudraw.set_pen_color(dudraw.WHITE)
                dudraw.filled_rectangle(5, 120, 50, 50)

                dudraw.set_pen_color(dudraw.BLACK)
                dudraw.set_font_size(50)
                dudraw.text(15, 120, "floor")

                place_floor(sandlist, x, y)

            if key == 'w':
                x = int(dudraw.mouse_x() + random.randint(-5, 5))
                y = int(dudraw.mouse_y())

                dudraw.set_pen_color(dudraw.WHITE)
                dudraw.filled_rectangle(5, 120, 50, 50)

                dudraw.set_pen_color(dudraw.BLACK)
                dudraw.set_font_size(50)
                dudraw.text(15, 120, "water")

                place_water(sandlist, x, y)

            if key == 'e':
                x = int(dudraw.mouse_x())
                y = int(dudraw.mouse_y())

                dudraw.set_pen_color(dudraw.WHITE)
                dudraw.filled_rectangle(5, 120, 50, 50)

                dudraw.set_pen_color(dudraw.BLACK)
                dudraw.set_font_size(50)
                dudraw.text(15, 120, "erase")

                erase(sandlist, x, y)

        advance_world(sandlist, canvas_size_x)

        if dudraw.has_next_key_typed():
            key = dudraw.next_key_typed()

        dudraw.show(5)


if __name__ == "__main__":
    main()
