# ---------------------------
# -     Ryan Williamson     -
# - Advanced Higher Project -
# ---------------------------

# Imports

import time
import copy
import array
import math
import random
import os
from tkinter import messagebox
import LLQueue
import LinkedList

# Global Variables

start_time = None
reset_simulation = False
panic_mode = False

# Functions

""" Initialise the start_time, used for running_time function """
def _initTime():
    global start_time
    start_time = round(time.process_time() * 1000)

""" Panic function used to stop all code execution during runtime"""
def panic():
    global panic_mode
    panic_mode = True

""" Reset function used to reset the simulation of the board """
def reset():
    global reset_simulation
    reset_simulation = True

""" Stops execution of program for n milliseconds """
def sleep(n):
    print("Zzzz...")
    time.sleep(n / 1000.0)

""" Returns the elapsed time since last reset or startup """
def running_time():
    print("Get running time")
    elapsedtime = round(time.clock() * 1000 - start_time)
    print("%s" % str(elapsedtime))
    return elapsedtime

"""This function cannot be simulated properly"""
def temperature():
    messagebox.showerror("Not Supported",
                         "Temperature function not supported in the simulator")
    quit()

# Classes

"""
This class contains all of the method and variables for
button a and button b
This class does not inherit from another class
"""
class Button:

    """Button Constructor"""
    def __init__(self):
        self.NumberOfPresses = 0
        self.currentlypressed = False
        self.waspressed = False

    """
    This function returns a boolean of if the button
    is currently being held
    """
    def is_pressed(self):
        return self.currentlypressed

    """
    This function returns a boolean of if the button has been pressed
    since the last time the function was called
    This function also resets the waspressed to False
    """
    def was_pressed(self):
        temp = self.waspressed
        self.waspressed = False
        return temp

    """
    This function returns an integer of the number of button
    presses since the last time this function was called
    This function reset the NumberOfPresses to zero
    """
    def get_presses(self):
        temp = self.NumberOfPresses
        self.NumberOfPresses = 0
        return temp

"""
This class contains all of the functionality for Images, including
pre-existing and custom created Images.
This class does not inherit from another class
"""
class Image:
    """
    Class Constructor 1- (string)
    Class Constructor 2- (width, height, buffer)
    """
    def __init__(self, *args):
        self.width = 0
        self.height = 0
        # If using constructor 1
        if len(args) == 1:
            self.ImageGrid = [[0 for y in range(5)]for x in range(5)]
            # Convert the string into a usable format
            tempstring = args[0].replace(':', '')
            imagestring = tempstring.replace('\n', '')
            if len(imagestring) != 25:
                messagebox.showerror("String not long enough",
                                     "String given is not long enough.")
                os._exit(0)
            self.width = 5
            self.height = 5
            # Set the ImageGrid to the values in the string
            for i in range(25):
                y = int(i / 5)
                x = i % 5
                self.set_pixel(x, y, int(imagestring[i]))
        # If using constructor 2
        else:
            self.ImageGrid = [[0 for y in range(args[1])]for x in range(args[0])]
            self.width = args[0]
            self.height = args[1]
            # If a buffer array is provided fill ImageGrid
            if self.width > 5 or self.height > 5:
                messagebox.showerror("Invalid parameters",
                                     "Width or Height is too large")
                os._exit(0)
            if len(args) == 3:
                for i in range(self.width*self.height):
                    y = int(i/self.width)
                    x = i % self.width
                    self.set_pixel(x, y, args[2][i])
                

    """
    This function will return a compact string representation of
    the object
    Format: Image('xxxxx:xxxxx:xxxxx:xxxxx:xxxxx:')
    """
    def __repr__(self):
        outputstring = "Image('"
        for y in range(self.height):
            for x in range(self.width):
                # Concatenate outputstring with the pixel value
                outputstring = outputstring + str(self.get_pixel(x, y))
            outputstring = outputstring + ":"
        outputstring = outputstring + "')"
        print(outputstring)
        return outputstring

    """
    This function will return a readable string representation of
    the object
    Format: Image(9 'xxxxx:'9 'xxxxx:'9 'xxxxx:'9 'xxxxx:'9 'xxxxx:'9)
    """
    def __str__(self):
        outputstring = "Image(9"
        for y in range(self.height):
            outputstring = outputstring + " '"
            for x in range(self.width):
                # Concatenate outputstring with the pixel value
                outputstring = outputstring + str(self.get_pixel(x, y))
            outputstring = outputstring + ":'9"
        outputstring = outputstring + ")"
        print(outputstring)
        return outputstring

    """
    This function overloads the additon operator
    Adds the brightnesses of the two images that are being added
    returns the resultant image
    """
    def __add__(self, other):
        # The image sizes must match
        if self.width != other.width or self.height != other.height:
            messagebox.showerror("Unmatched width or height",
                                 "width or height of the two images does not"
                                 "match")
            os._exit(0)
        else:
            # Create new image to put the new pixel values in
            image = Image(self.width, self.height)
            for i in range(self.width*self.height):
                y = int(i / self.width)
                x = i % self.width
                # Obtains value from the two image pixel values at this
                # position and caps the value at 9
                value = int(self.get_pixel(x, y) + int(other.get_pixel(x, y)))
                value = self._cap(value, 9)
                image.set_pixel(x, y, value)
            return image

    """
    This function overloads the multiplication operator
    Multiplys the brightness of every pixel in the image and returns
    the resultant image
    """
    def __mul__(self, n):
        # Create new image to put new pixel values into
        image = Image(self.width, self.height)
        for i in range(self.width*self.height):
            y = int(i / self.width)
            x = i % self.width
            # Multiplys the value and caps it at 9
            value = int(self.get_pixel(x, y)) * n
            value = self._cap(value, 9)
            image.set_pixel(x, y, value)
        return image

    """
    This function caps the value passed into the function
    """
    def _cap(self,value, maxval):
        if value > maxval:
            return maxval
        return math.ceil(value)

    """
    This function converts an image that is not 5x5 to a format
    that can be displayed on the displaygrid by padding 0's onto the image
    """
    def OutputFormat(self):
        if self.width != 5 or self.height != 5:
            outputstring = ""
            missingwidth = 5 - self.width
            missingheight = 5 - self.height
            for y in range(self.height):
                for x in range(self.width):
                    outputstring = outputstring + str(self.get_pixel(x, y))
                # This loop is for padding empty columns
                for x in range(missingwidth):
                    outputstring = outputstring + '0'
            # This pads for empty rows
            for y in range(missingheight):
                for x in range(5):
                    outputstring = outputstring + '0'
            return Image(outputstring)
        else:
            return self

    """returns width"""
    def width(self):
        return self.width

    """returns height"""
    def height(self):
        return self.height

    """Sets the pixel at x, y if x and y are within the range"""
    def set_pixel(self, x, y, value):
        if x < self.width and y < self.height and x >= 0 and y >= 0:
            if int(value) > 9 or int(value) < 0:
                messagebox.showerror("incorrect value", "Value must be between 0 and 9")
                os._exit(0)
            self.ImageGrid[x][y] = int(value)

    """Returns the pixel at x, y if x and y are within the range"""
    def get_pixel(self, x, y):
        if x < self.width and y < self.height and x >= 0 and y >= 0:
            return self.ImageGrid[x][y]

    """
    This function returns the image with all pixels shifted
    to the left by n pixels
    """
    def shift_left(self, n):
        # Creates a new image to store the shifted pixels in
        shiftImage = Image(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                # If the pixel at x+n is not empty shift that pixel
                # to x
                if self.get_pixel(x+n, y) != None:
                    shiftImage.set_pixel(x, y, self.get_pixel(x+n, y))
                else:
                    shiftImage.set_pixel(x, y, 0)
        return shiftImage

    """
    This function returns the image with all pixels shifted
    to the right by n pixels
    """
    def shift_right(self, n):
        return self.shift_left(-n)

    """
    This function returns the image with all pixels shifted
    up by n pixels
    """
    def shift_up(self, n):
        # Creates a new image to store the shifted pixels in
        shiftImage = Image(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                # If the pixel at y+n is not empty shift that pixel
                # to y
                if self.get_pixel(x, y+n) != None:
                    shiftImage.set_pixel(x, y, self.get_pixel(x, y+n))
                else:
                    shiftImage.set_pixel(x, y, 0)
        return shiftImage

    """
    This function returns the image with all pixels shifted
    down by n pixels
    """
    def shift_down(self, n):
        return self.shift_up(-n)

    """
    This function crops the image to a rectangle of width w, height h
    starting at position x, y
    If the rectangle is outwith the image then fill those spots with zero's
    """
    def crop(self, x, y, w, h):
        cropImage = Image(w, h)
        if w < 0 or h < 0:
            return cropImage
        for yy in range(h):
            for xx in range(w):
                # Boundary checks
                if xx+x >= self.width or yy+y >= self.height:
                    cropImage.set_pixel(xx, yy, 0)
                elif xx+x < 0 or yy+y < 0:
                    cropImage.set_pixel(xx, yy, 0)
                else:
                    # Add pixels to cropped image
                    cropImage.set_pixel(xx, yy, self.get_pixel(xx+x, yy+y))
        return cropImage

    """Returns a complete copy of the image with a seperate object reference"""
    def copy(self):
        return copy.deepcopy(self)

    """Returns a new image with each LED value equal to (9 - value)"""
    def invert(self):
        bufferstr = ""
        for i in range(self.width*self.height):
            y = int(i / self.width)
            x = i % self.width
            bufferstr = bufferstr + str(9 - self.get_pixel(x, y)) # This inverts the value
        # Return new Image with the inverted values as the inital buffer
        return Image(self.width, self.height, bufferstr)
            
    """Fills all pixel values with the same value"""
    def fill(self, value):
        for i in range(self.width*self.height):
            y = int(i / self.width)
            x = i % self.width
            self.set_pixel(x, y, value)

    """
    blit function removed for now as it does not seem to function in the
    microbit environment
    def blit(self, src, x, y, w, h, xdest=0, ydest=0):
        print("This is the blit function")
    """

# This sets up all of the pre-existing Images
Image.HEART = Image("09090:99999:99999:09990:00900")
Image.HEART_SMALL = Image("00000:09090:09990:00900:00000")
Image.HAPPY = Image("00000:09090:00000:90009:09990")
Image.SMILE = Image("00000:00000:00000:90009:09990")
Image.SAD = Image("00000:09090:00000:09990:90009")
Image.CONFUSED = Image("00000:09090:00000:09090:90909")
Image.ANGRY = Image("90009:09090:00000:99999:90909")
Image.ASLEEP = Image("00000:99099:00000:09990:00000")
Image.SURPRISED = Image("09090:00000:00900:09090:00900")
Image.SILLY = Image("90009:00000:99999:00909:00999")
Image.FABULOUS = Image("99999:99099:00000:09090:09990")
Image.MEH = Image("09090:00000:00090:00900:09000")
Image.YES = Image("00000:00009:00090:90900:09000")
Image.NO = Image("90009:09090:00900:09090:90009")
Image.CLOCK12 = Image("00900:00900:00900:00000:00000")
Image.CLOCK11 = Image("09000:09000:00900:00000:00000")
Image.CLOCK10 = Image("00000:99000:00900:00000:00000")
Image.CLOCK9 = Image("00000:00000:99900:00000:00000")
Image.CLOCK8 = Image("00000:00000:00900:99000:00000")
Image.CLOCK7 = Image("00000:00000:00900:09000:09000")
Image.CLOCK6 = Image("00000:00000:00900:00900:00900")
Image.CLOCK5 = Image("00000:00000:00900:00090:00090")
Image.CLOCK4 = Image("00000:00000:00900:00099:00000")
Image.CLOCK3 = Image("00000:00000:00999:00000:00000")
Image.CLOCK2 = Image("00000:00099:00900:00000:00000")
Image.CLOCK1 = Image("00090:00090:00900:00000:00000")
Image.ALL_CLOCKS = [Image.CLOCK12, Image.CLOCK1, Image.CLOCK2, Image.CLOCK3,
                    Image.CLOCK4, Image.CLOCK5, Image.CLOCK6, Image.CLOCK7,
                    Image.CLOCK8, Image.CLOCK9, Image.CLOCK10, Image.CLOCK11]
Image.ARROW_N = Image("00900:09990:90909:00900:00900")
Image.ARROW_NE = Image("00999:00099:00909:09000:90000")
Image.ARROW_E = Image("00900:00090:99999:00090:00900")
Image.ARROW_SE = Image("90000:09000:00909:00099:00999")
Image.ARROW_S = Image("00900:00900:90909:09990:00900")
Image.ARROW_SW = Image("00009:00090:90900:99000:99900")
Image.ARROW_W = Image("00900:09000:99999:09000:00900")
Image.ARROW_NW = Image("99900:99000:90900:00090:00009")
Image.ALL_ARROWS = [Image.ARROW_N, Image.ARROW_NE, Image.ARROW_E, Image.ARROW_SE,
                    Image.ARROW_S, Image.ARROW_SW, Image.ARROW_W, Image.ARROW_NW]
Image.TRIANGLE = Image("00000:00900:09090:99999:00000")
Image.TRIANGLE_LEFT = Image("90000:99000:90900:90090:99999")
Image.CHESSBOARD = Image("09090:90909:09090:90909:09090")
Image.DIAMOND = Image("00900:09090:90009:09090:00900")
Image.DIAMOND_SMALL = Image("00000:00900:09090:00900:00000")
Image.SQUARE = Image("99999:90009:90009:90009:99999")
Image.SQUARE_SMALL = Image("00000:09990:09090:09990:00000")
Image.RABBIT = Image("90900:90900:99990:99090:99990")
Image.COW = Image("90009:90009:99999:09990:00900")
Image.MUSIC_CROTCHET = Image("00900:00900:00900:99900:99900")
Image.MUSIC_QUAVER = Image("00900:00990:00909:99900:99900")
Image.MUSIC_QUAVERS = Image("09999:09009:09009:99099:99099")
Image.PITCHFORK = Image("90909:90909:99999:00900:00900")
Image.XMAS = Image("00900:09990:00900:09990:99999")
Image.PACMAN = Image("09999:99090:99900:99990:09999")
Image.TARGET = Image("00900:09990:99099:09990:00900")
Image.TSHIRT = Image("99099:99999:09990:09990:09990")
Image.ROLLERSKATE = Image("00099:00099:99999:99999:09090")
Image.DUCK = Image("09900:99900:09999:09990:00000")
Image.HOUSE = Image("00900:09990:99999:09990:09090")
Image.TORTOISE = Image("00000:09990:99999:09090:00000")
Image.BUTTERFLY = Image("99099:99999:00900:99999:99099")
Image.STICKFIGURE = Image("00900:99999:00900:09090:90009")
Image.GHOST = Image("99999:90909:99999:99999:90909")
Image.SWORD = Image("00900:00900:00900:09990:00900")
Image.GIRAFFE = Image("99000:09000:09000:09990:09090")
Image.SKULL = Image("09990:90909:99999:09990:09990")
Image.UMBRELLA = Image("09990:99999:00900:90900:09900")
Image.SNAKE = Image("99000:99099:09090:09990:00000")

"""
This class contains all functions and variables for the 5x5 LED display
This class does not inherit from another class
"""
class Display:
    """Class Constructor"""
    def __init__(self):
        self.DisplayGrid = [[0 for y in range(5)]for x in range(5)]
        self.displayon = True
        # Converion array for character to image conversion
        self.ConversionArray = {
                    ' ' : "00000:00000:00000:00000:00000",
                    '!' : "09000:09000:09000:00000:09000",
                    '#' : "09090:99999:09090:99999:09090",
                    '$' : "09990:99009:09990:90099:09990",
                    '%' : "99009:90090:00900:09009:90099",
                    '&' : "09900:90090:09900:90090:09909",
                    '(' : "00900:09000:09000:09000:00900",
                    ')' : "09000:00900:00900:00900:09000",
                    '*' : "00000:09090:00900:09090:00000",
                    '+' : "00000:00900:09990:00900:00000",
                    ',' : "00000:00000:00000:00900:09000",
                    '-' : "00000:00000:09990:00000:00000",
                    '.' : "00000:00000:00000:09000:00000",
                    '/' : "00009:00090:00900:09000:90000",
                    '0' : "09900:90090:90090:90090:09900",
                    '1' : "00900:09900:00900:00900:09990",
                    '2' : "99900:00090:09900:90000:99990",
                    '3' : "99990:00090:00900:90090:09900",
                    '4' : "00990:09090:90090:99999:00090",
                    '5' : "99999:90000:99990:00009:99990",
                    '6' : "00090:00900:09990:90009:09990",
                    '7' : "99999:00090:00900:09000:90000",
                    '8' : "09990:90009:09990:90009:09990",
                    '9' : "09990:90009:09990:00900:09000",
                    ':' : "00000:09000:00000:09000:00000",
                    ';' : "00000:00900:00000:00900:09000",
                    '<' : "00090:00900:09000:00900:00090",
                    '=' : "00000:09990:00000:09990:00000",
                    '>' : "09000:00900:00090:00900:09000",
                    '?' : "09990:90009:00990:00000:00900",
                    '@' : "09990:90009:90909:90099:09900",
                    'A' : "09900:90090:99990:90090:90090",
                    'B' : "99900:90090:99900:90090:99900",
                    'C' : "09990:90000:90000:90000:09990",
                    'D' : "99900:90090:90090:90090:99900",
                    'E' : "99990:90000:99900:90000:99990",
                    'F' : "99990:90000:99900:90000:90000",
                    'G' : "09990:90000:90099:90009:09990",
                    'H' : "90090:90090:99990:90090:90090",
                    'I' : "99900:09000:09000:09000:99900",
                    'J' : "99999:00090:00090:90090:09900",
                    'K' : "90090:90900:99000:90900:90090",
                    'L' : "90000:90000:90000:90000:99990",
                    'M' : "90009:99099:90909:90009:90009",
                    'N' : "90009:99009:90909:90099:90009",
                    'O' : "09900:90090:90090:90090:09900",
                    'P' : "99900:90090:99900:90000:90000",
                    'Q' : "09900:90090:90090:09900:00990",
                    'R' : "99900:90090:99900:90090:90009",
                    'S' : "09990:90000:09900:00090:99900",
                    'T' : "99999:00900:00900:00900:00900",
                    'U' : "90090:90090:90090:90090:09900",
                    'V' : "90009:90009:90009:09090:00900",
                    'W' : "90009:90009:90909:99099:90009",
                    'X' : "90090:90090:09900:90090:90090",
                    'Y' : "90009:09090:00900:00900:00900",
                    'Z' : "99990:00900:09000:90000:99990",
                    '[' : "09990:09000:09000:09000:09990",
                    '\\' : "90000:09000:00900:00090:00009",
                    ']' : "09990:00090:00090:00090:09990",
                    '^' : "00900:09090:00000:00000:00000",
                    '_' : "00000:00000:00000:00000:99999",
                    '`' : "09000:00900:00000:00000:00000",
                    'a' : "00000:09990:90090:90090:09999",
                    'b' : "90000:90000:99900:90090:99900",
                    'c' : "00000:09990:90000:90000:09990",
                    'd' : "00090:00090:09990:90090:09990",
                    'e' : "09900:90090:99900:90000:09990",
                    'f' : "00990:09000:99900:09000:09000",
                    'g' : "09990:90090:09990:00090:09900",
                    'h' : "90000:90000:99900:90090:90090",
                    'i' : "09000:00000:09000:09000:09000",
                    'j' : "00090:00000:00090:00090:09900",
                    'k' : "90000:90900:99000:90900:90090",
                    'l' : "09000:09000:09000:09000:00990",
                    'm' : "00000:99099:90909:90009:90009",
                    'n' : "00000:99900:90090:90090:90090",
                    'o' : "00000:09900:90090:90090:09900",
                    'p' : "00000:99900:90090:99900:90000",
                    'q' : "00000:09990:90090:09990:00090",
                    'r' : "00000:09990:90000:90000:90000",
                    's' : "00000:00990:09000:00900:99000",
                    't' : "09000:09000:09990:09000:00999",
                    'u' : "00000:90090:90090:90090:09999",
                    'v' : "00000:90009:90009:09090:00900",
                    'w' : "00000:90009:90009:90909:99099",
                    'x' : "00000:90090:09900:09900:90090",
                    'y' : "00000:90009:09090:00900:99000",
                    'z' : "00000:99990:00900:09000:99990",
                    '{' : "00990:00900:09900:00900:00990",
                    '|' : "09000:09000:09000:09000:09000",
                    '}' : "99000:09000:09900:09000:99000",
                    '~' : "00000:00000:09900:00099:00000"
                }

    """Returns the pixel value at position x and y"""
    def get_pixel(self, x, y):
        return self.DisplayGrid[x][y]

    """Sets the pixel value at position x and y"""
    def set_pixel(self, x, y, value):
        if int(value) > 9 or int(value) < 0:
            messagebox.showerror("incorrect value",
                                 "Value must be between 0 and 9")
            os._exit(0)
        self.DisplayGrid[x][y] = int(value)

    """Sets all pixels to display value 0"""
    def clear(self):
        self.DisplayGrid = [[0 for y in range(5)] for x in range(5)]

    """
    This function has different functionality based on the parameters
    If an image is passed in as displayable then the image is displayed
    If an array of images is passed then each image is displayed with a delay
    between them
    If a string is passed in then each character is converted to an image then
    displayed with a delay between each character
    """
    def show(self, displayable, delay=400, wait=True, loop=False, clear=False):
        if isinstance(displayable, Image):
            self.DisplayGrid = displayable.OutputFormat().ImageGrid
        else:
            # Looping and background animation are not supported
            if (not (wait) or loop):
                messagebox.showerror("Not Supported",
                                     "Looping and not waiting are not supported in this simulator")
                os._exit(0)
            for item in displayable:
                if isinstance(item, Image):
                    self.DisplayGrid = item.OutputFormat().ImageGrid
                else:
                    value = self.ConversionArray.get(item, None) # Convert string to image
                    if value != None:
                        # Convert the character to an image then set display to the image
                        self.DisplayGrid = Image(value).OutputFormat().ImageGrid
                sleep(delay)
            if clear:
                self.clear()

    """
    This function works similar to show for text except it scrolls through
    column by column
    This implementation only works with monospace and does not support
    background animation or looping
    """
    def scroll(self, string, delay=150, wait=True, loop=False, monospace=True):
        if (not (wait) or loop):
            messagebox.showerror("Not Supported",
                                 "Looping and not waiting are not supported in this simulator")
            os._exit(0)
        if not(monospace):
            messagebox.showerror("Not Supported",
                                 "Only monospace is supported in this simulator")
            os._exit(0)
        if monospace:
            # Creates an image to store current display state
            currentImg = Image(5, 5)
            # Loops for every character
            for item in string:
                # Get character image string
                char = self.ConversionArray.get(item, None) # Convert char to image string
                if char != None:
                    # Create an image from character string
                    charImg = Image(char)
                    # Each character has a width of 5
                    for i in range(5):
                        # Takes 1x5 slice of the character image
                        imgSection = charImg.crop(i, 0, 1, 5)
                        # Move along the current display state
                        currentImg = currentImg.shift_left(1)
                        # Add the slice to the current display state
                        currentImg = currentImg + imgSection.OutputFormat().shift_right(4)
                        display.show(currentImg)
                        sleep(delay)
                    currentImg = currentImg.shift_left(1)



    """Sets the displayon boolean to true"""
    def on(self):
        self.displayon = True

    """Sets the displayon boolean to False"""
    def off(self):
        self.displayon = False

    """Returns a boolean value displayon"""
    def is_on(self):
        return self.displayon

"""
This class contains all of the functionality for the acclerometer
sub-system including the gesture system
This class does not inherit from another class
"""
class Accelerometer:

    """Class Constructor"""
    def __init__(self):
        self.accelerometerdict = {'x' : 0, 'y' : 0, 'z' : 0}
        self.currentgesture = None
        self.gesturelist = [
            "up",
            "down",
            "left",
            "right",
            "face up",
            "face down",
            "freefall",
            "3g",
            "6g",
            "8g",
            "shake"
        ]
        # Gesture History is a Queue
        self.gesturehistory = LLQueue.Queue()
        # Previous gesture is a linked list
        self.wasgesturelist = LinkedList.LinkedList()

    """Returns the value linked with x in the dictionary"""
    def get_x(self):
        return self.accelerometerdict['x']

    """Returns the value linked with y in the dictionary"""
    def get_y(self):
        return self.accelerometerdict['y']

    """Returns the value linked with z in the dictionary"""
    def get_z(self):
        return self.accelerometerdict['z']

    """Return a tuple of all the accelerometer values"""
    def get_values(self):
        return (self.get_x(), self.get_y(), self.get_z())

    """Returns the currently executed gesture"""
    def current_gesture(self):
        return self.currentgesture

    """
    Returns a boolean to check if the current gesture matches
    the gesture name passe into
    """
    def is_gesture(self, name):
        return self.currentgesture == name

    """
    Returns a boolean based on if the gesture name passed in was used
    since the last function call
    Also clears the wasgesture Linked List
    """
    def was_gesture(self, name):
        found = self.wasgesturelist.Search(name)
        self.wasgesturelist.Clear()
        return found

    """
    Returns a tuple of gestures used in runtime as a First in First Out
    Therefore a queue was used to store this
    """
    def get_gestures(self):
        return self.gesturehistory.convertToTuple()
        
# These are the pre-built object instances for the microbit
button_a = Button()
button_b = Button()
display = Display()
accelerometer = Accelerometer()
