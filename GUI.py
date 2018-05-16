# ---------------------------
# -     Ryan Williamson     -
# - Advanced Higher Project -
# ---------------------------

# Imports

import microbit
import tkinter
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import shutil
import os

# Classes
"""This is the class that all of the GUI window classes are derived from"""
class BaseGUI:
    """Initalise the window"""
    def init(self, root):
        self.root = root
        root.title("Micro:bit Simulator")
        root.resizable(0,0)

    """This function allows text to be inserted into a text field"""
    def InsertMethod(self, TextField, Message):
        TextField.configure(state='normal')
        TextField.insert(tkinter.END, Message+"\n")
        TextField.configure(state='disabled')

    """This function quits the program closing all windows"""
    def quit(self):
        quit()

    """This opens the help pdf file with the default pdf viewer program"""
    def openhelp(self):
        cwd = os.getcwd()
        os.system("start " + cwd + "\\Help\\Help.pdf")

"""
This is the class for the file load GUI
This class Inherits from BaseGUI
"""
class FileLoadGUI(BaseGUI):
    """This is the class constructor"""
    def __init__(self, root):
        BaseGUI.init(self, root)
        self.InitGUI(self.root)

    """This function sets up all the tkinter objects in the window"""
    def InitGUI(self, root):

        # Variables needed for buttons
        self.name = ""
        
        #Menubar GUI
        self.menubar = tkinter.Menu(root)
        self.menubar.add_command(label="Quit", command=super(FileLoadGUI, self).quit)
        self.menubar.add_command(label="Help", command=super(FileLoadGUI, self).openhelp)
        root.config(menu=self.menubar)

        #Frame setup
        self.outputframe = ttk.Frame(root, width=400, height = 100)
        self.outputframe.grid(row=0, column=0, columnspan=4, rowspan=2, padx=5, pady=5, sticky="N")
        self.outputframe.grid_propagate(False)

        #Output window and scrollbar
        self.scrollbar = ttk.Scrollbar(root, orient=tkinter.VERTICAL)

        self.output = tkinter.Text(self.outputframe, width=75, yscrollcommand=self.scrollbar.set)
        self.output.grid(row=0, column=0, columnspan=4, rowspan=2, sticky='N')

        self.scrollbar.config(command=self.output.yview)
        self.scrollbar.grid(row=0, column=4, rowspan=2, sticky="NS")

        #Separator
        self.separator = ttk.Separator(root, orient=tkinter.HORIZONTAL)
        self.separator.grid(row=3, column=0, columnspan=4, pady=(5, 25), sticky="EW")

        #File path label
        self.filepathlabel = ttk.Label(root, text="[dummy file path]", background="white")
        self.filepathlabel.grid(row=4, column=1, columnspan=2, pady=(0, 25), sticky="NSEW")

        #Browse Button
        self.browsebutton = ttk.Button(root, text="Browse", command=self.browse)
        self.browsebutton.grid(row=4, column=3, pady=(0, 25), sticky='NS')

        # Load file Button
        self.loadbutton = ttk.Button(root, text="Load File", command=self.loadfile)
        self.loadbutton.grid(row=5, column=2, pady=(0, 25), sticky='NS')

    """This function allows the selection of a file to be loaded later"""
    def browse(self):
        # Sets the selected file path to self.name
        self.name = askopenfilename(initialdir="H:/",
                                                  filetypes=(("Python File", "*.py"),
                                                             ("All Files", "*.*")),
                                                  title="Choose a file")
        # Make use of try statement in case the dialog is closed without of file selected
        try:
            # If the file is a python file
            if self.name.endswith('.py'):
                with open(self.name,'r') as File:
                    print(File.read())
                self.filepathlabel.config(text=self.name)
            else:
                BaseGUI.InsertMethod(self, self.output, "Not a python file")
        except:
            BaseGUI.InsertMethod(self, self.output, "No file selected or file non-readable")

    """
    This function loads the file and moves the program onto the simulation
    window
    """
    def loadfile(self):
        cwd = os.getcwd()
        # Attempt to copy the file to the program directory
        try:
            shutil.copy(self.name, cwd)
        except:
            # If the file cannot be copied then there is no file
            BaseGUI.InsertMethod(self, self.output, "No file selected to read")
            return
        # Get filename from file path
        filename = os.path.basename(self.name)
        # Remove old simulator code if it exists
        try:
            os.remove("%s\\run.py" % cwd)
        except:
            print("File does not already exist")
        # Renames the file to run.py
        os.rename("%s\\%s" % (cwd, filename),
                    "%s\\run.py" % cwd)
        # Closes the window
        self.root.destroy()
        

"""
This is the class for the Simulation GUI
This class Inherits from BaseGUI
"""
class SimulationGUI(BaseGUI):
    """Class constructor"""
    def __init__(self, root):
        BaseGUI.init(self, root)
        self.InitGUI(self.root)

    """This function sets up all the object in the tkinter window"""
    def InitGUI(self, root):

        #Menubar GUI
        self.menubar = tkinter.Menu(self.root)
        self.menubar.add_command(label="Exit", command=super(SimulationGUI, self).quit)
        self.menubar.add_command(label="Help", command=super(SimulationGUI, self).openhelp)
        root.config(menu=self.menubar)

        #Frame setup for holding micro:bit image, LED's, and buttons
        self.photoframe = tkinter.Frame(root, width=350, height=350)
        self.photoframe.grid(row=0, column=0, columnspan=3, padx=2, pady=10, sticky="NSEW")
        self.photoframe.grid_propagate(False)

        #Setup photo of micro:bit
        self.mbimage = tkinter.PhotoImage(file="Images/microbit.gif")
        self.mblabel = tkinter.Label(self.photoframe, image=self.mbimage)
        self.mblabel.grid(row=0, column=0)

        # Button Setup
        self.buttonimage = tkinter.PhotoImage(file="Images/Button.gif")
        self.mbbuttonframe = tkinter.Frame(self.photoframe, width=315, height=46, bg="black")
        self.mbbuttonframe.grid(row=0, column=0, columnspan=3,padx=(8, 16), pady=(120, 175))
        self.mbbuttonframe.grid_propagate(False)

        #Button A
        self.button_a = tkinter.Button(self.mbbuttonframe, image=self.buttonimage,
                                       width=39, height=39)
        self.button_a.bind('<ButtonPress-1>', self.APress)
        self.button_a.bind('<ButtonRelease-1>', self.ARelease)
        self.button_a.grid(row=0, column=0, padx=(0, 225), sticky="NESW")

        #Button B
        self.button_b = tkinter.Button(self.mbbuttonframe, image=self.buttonimage,
                                       width=39, height=39)
        self.button_b.bind('<ButtonPress-1>', self.BPress)
        self.button_b.bind('<ButtonRelease-1>', self.BRelease)
        self.button_b.grid(row=0, column=1, sticky="NESW")

        # Button A and B
        self.button_both = tkinter.Button(self.photoframe, image=self.buttonimage,
                                          width=39, height=39)
        self.button_both.bind('<ButtonPress-1>', self.BothPress)
        self.button_both.bind('<ButtonRelease-1>', self.BothRelease)
        self.button_both.grid(row=0, column=0, padx=(0, 0), pady=(302, 0))

        #Setup for LED
        self.ledframe = tkinter.Frame(self.photoframe, width=135, height=135, bg="black")
        self.ledframe.grid(row=0, column=0, columnspan=5, rowspan=5, padx=(115, 127), pady=(87, 155), sticky="NSEW")
        self.ledframe.grid_propagate(False)

        # Sets up the array for all of the LED images from 0 to 9
        self.ledimages = [None for i in range(10)]
        for i in range(0, 10):
            self.ledimages[i] = tkinter.PhotoImage(file="Images/LED%s.gif" % str(i))

        # Sets up canvas arrays
        self.ledcanvasarray = [None for i in range(25)]
        self.imageoncanvas = [None for i in range(25)]
        for i in range(0, 25):
            Row = int(i/5)
            Column = i%5
            self.ledcanvasarray[i] = tkinter.Canvas(self.ledframe, width=5, height=11)
            self.imageoncanvas[i] = self.ledcanvasarray[i].create_image(0, 0,
                                    image=self.ledimages[0], anchor=tkinter.NW)
            self.ledcanvasarray[i].grid(row=Row, column=Column, padx=(0, 19), pady=(0, 13))

        # Frame for Simulation Inputs and Buttons
        self.editorframe = tkinter.Frame(root, width=350, height=200)
        self.editorframe.grid(row=1, column=0, rowspan=6, columnspan=2)
        self.editorframe.grid_propagate(False)

        # Accelerometer X
        self.accelerometerlabel_x = tkinter.Label(self.editorframe, width=17,
                                                  text="Accelerometer X: ")
        self.accelerometerlabel_x.grid(row=0, column=0, sticky="EW", padx=(90, 0), pady=(0, 5))
        self.stringvarx = tkinter.StringVar()
        self.stringvarx.trace("w", self.AXChanged)
        self.stringvarx.set(str(microbit.accelerometer.get_x()))
        self.accelerometerinput_x = tkinter.Entry(self.editorframe, width=3,
                                                  textvariable=self.stringvarx)
        self.accelerometerinput_x.grid(row=0, column=1, sticky="EW", padx=(0, 15), pady=(0, 5))

        # Accelerometer Y
        self.accelerometerlabel_y = tkinter.Label(self.editorframe, width=17,
                                                  text="Accelerometer Y: ")
        self.accelerometerlabel_y.grid(row=1, column=0, sticky="EW", padx=(90, 0), pady=(0, 5))
        self.stringvary = tkinter.StringVar()
        self.stringvary.trace("w", self.AYChanged)
        self.stringvary.set(str(microbit.accelerometer.get_y()))
        self.accelerometerinput_y = tkinter.Entry(self.editorframe, width=3,
                                                  textvariable=self.stringvary)
        self.accelerometerinput_y.grid(row=1, column=1, sticky="EW", padx=(0, 15), pady=(0, 5))

        # Accelerometer Z
        self.accelerometerlabel_z = tkinter.Label(self.editorframe, width=17,
                                                  text="Accelerometer Z: ")
        self.accelerometerlabel_z.grid(row=2, column=0, sticky="EW", padx=(90, 0), pady=(0, 5))
        self.stringvarz = tkinter.StringVar()
        self.stringvarz.trace("w", self.AZChanged)
        self.stringvarz.set(str(microbit.accelerometer.get_z()))
        self.accelerometerinput_z = tkinter.Entry(self.editorframe, width=3,
                                                  textvariable=self.stringvarz)
        self.accelerometerinput_z.grid(row=2, column=1, sticky="EW", padx=(0, 15), pady=(0, 5))

        # Predefined Gesture Button
        self.pdgsbutton = ttk.Button(self.editorframe, text="Gestures", command=self.OpenPDGS)
        self.pdgsbutton.grid(row=3, column=0, sticky="NSEW", padx=(115, 0), pady=(0, 5))

        # Reset Gesture Button
        self.resetbutton = ttk.Button(self.editorframe, text="Reset", command=self.reset)
        self.resetbutton.grid(row=4, column=0, sticky="NSEW", padx=(115, 0), pady=(0, 5))

    """Function that occurs when the value for accelerometer x was changed"""
    def AXChanged(self, *args):
        # If accelerometer x was given a value
        if self.stringvarx.get() != '' and self.stringvarx.get().isdigit():
            microbit.accelerometer.accelerometerdict['x'] = self.stringvarx.get()
            print(microbit.accelerometer.get_values())

    """Function that occurs when the value for accelerometer y was changed"""
    def AYChanged(self, *args):
        # If accelerometer y was given a value
        if self.stringvary.get() != ''  and self.stringvary.get().isdigit():
            microbit.accelerometer.accelerometerdict['y'] = self.stringvary.get()
            print(microbit.accelerometer.get_values())

    """Function that occurs when the value for accelerometer z was changed"""
    def AZChanged(self, *args):
        # If accelerometer z was given a value
        if self.stringvarz.get() != ''  and self.stringvarz.get().isdigit():
            microbit.accelerometer.accelerometerdict['z'] = self.stringvarz.get()
            print(microbit.accelerometer.get_values())

    """A function that will handle any button being pressed"""
    def ButtonPress(self, button):
        button.currentlypressed = True
        button.waspressed = True
        button.NumberOfPresses += 1

    """A function that will handle any button being released"""
    def ButtonRelease(self, button):
        button.currentlypressed = False

    """Function that will run when Button A is pressed"""
    def APress(self, event):
        print("Press A")
        self.ButtonPress(microbit.button_a)

    """Function that will run when Button A is released"""
    def ARelease(self, event):
        print("Release A")
        self.ButtonRelease(microbit.button_a)

    """Function that will run when Button B is pressed"""
    def BPress(self, event):
        print("Press B")
        self.ButtonPress(microbit.button_b)

    """Function that will run when Button B is released"""
    def BRelease(self, event):
        print("Release B")
        self.ButtonRelease(microbit.button_b)

    """Function that will run when both buttons are pressed"""
    def BothPress(self, event):
        print("Press Both")
        self.ButtonPress(microbit.button_a)
        self.ButtonPress(microbit.button_b)

    """Function that will run when both buttons are released"""
    def BothRelease(self, event):
        print("Release Both")
        self.ButtonRelease(microbit.button_a)
        self.ButtonRelease(microbit.button_b)

    """This function will open the Gesture GUI window"""
    def OpenPDGS(self):
        print("Opens PDGS")
        # Links the Gesture window the the main window
        # so that if the main window is closed so is the gesture window
        self.gesturewindow = tkinter.Toplevel(self.root)
        self.app = GestureGUI(self.gesturewindow)

    """This function runs when the reset button is pressed"""
    def reset(self):
        print("reset")
        microbit.reset()

    """
    This function runs every 100 milliseconds
    The LED's are updated in this function
    If the reset flag has been set then the Simulation GUI is reset
    If the panic flag has been set the execution stops and
    Image.SAD is displayed
    """
    def UpdateMicrobit(self, root):
        # If the reset flag is set
        if microbit.reset_simulation:
            # Stop updating then destroy window
            root.after_cancel(self.afterid)
            microbit.display.clear()
            root.destroy()
        # If the panic flag is set
        if microbit.panic_mode:
            # Stop updating LED after display Image.SAD
            root.after_cancel(self.afterid)
            microbit.display.show(microbit.Image.SAD)
        # Update each LED to match what is in the display 2DArray
        for i in range(25):
            Col = int(i / 5)
            Row = i % 5
            if microbit.display.is_on():
                self.ledcanvasarray[i].itemconfig(self.imageoncanvas[i],
                                                  image=self.ledimages[int(microbit.display.get_pixel(Row, Col))])
            else:
                self.ledcanvasarray[i].itemconfig(self.imageoncanvas[i],
                                                  image=self.ledimages[0])
        # Schedule this function to run again in 100 milliseconds
        self.afterid = root.after(100, self.UpdateMicrobit, root)


"""
This is the class for the Gesture GUI
This class Inherits from BaseGUI
"""
class GestureGUI(BaseGUI):
    """Class constructor"""
    def __init__(self, root):
        BaseGUI.init(self, root)
        self.InitGUI(self.root)

    """This function sets up all objects in GestureGUI window"""
    def InitGUI(self, root):

        # Menubar GUI
        self.menubar = tkinter.Menu(self.root)
        self.menubar.add_command(label="Exit", command=super(GestureGUI, self).quit)
        self.menubar.add_command(label="Help", command=super(GestureGUI, self).openhelp)
        root.config(menu=self.menubar)

        #Setup for list of all gestures in micro:bit        
        self.gesturelist = microbit.accelerometer.gesturelist

        #Setup for drop down menu
        self.selectedgesture = tkinter.StringVar()
        self.selectedgesture.set(self.gesturelist[0])
        self.gesturemenu = ttk.OptionMenu(root, self.selectedgesture, self.gesturelist[0], *self.gesturelist)
        self.gesturemenu.config(width=13)
        self.gesturemenu.grid(row=0, column=0, sticky="EW", padx=10, pady=(15, 15))

        #Button to execute gesture
        self.gesturebutton = ttk.Button(root, text="Execute Gesture", command=self.ExecuteGesture)
        self.gesturebutton.grid(row=0, column=1, sticky="EW", padx=(0, 10), pady=(15, 15))

        self.stopbutton = ttk.Button(root, text="Stop Gesture", command=self.StopGesture)
        self.stopbutton.grid(row=0, column=2, sticky="EW", padx=(0, 10), pady=15)

    """This function is run when a gesture is executed"""
    def ExecuteGesture(self):
        Gesture = self.selectedgesture.get()
        microbit.accelerometer.currentgesture = Gesture
        microbit.accelerometer.gesturehistory.Enqueue(Gesture)
        microbit.accelerometer.wasgesturelist.Append(Gesture)

    """This function is run when a gesture is stopped"""
    def StopGesture(self):
        microbit.accelerometer.currentgesture = None
