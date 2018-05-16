# ---------------------------
# -     Ryan Williamson     -
# - Advanced Higher Project -
# ---------------------------

# Imports
import GUI
import microbit
import tkinter
import threading
import importlib
import sys

#Variables

fileloadclose = True
simulationclose = True

#Functions
"""This function destroys the File Load GUI window"""
def CloseFileLoad():
    global fileloadclose
    fileloadclose = False
    root.destroy()

"""This function destroys the Simulation GUI window"""
def CloseSimulationWindow():
    global simulationclose
    simulationclose = False
    root.destroy()

"""This function runs the code in the file chosen by the user"""
def importFunction():
    # If file has not been run before run it
    # If the file has been run rerun it
    if 'run' not in sys.modules:
        import run
    else:
        import run
        run = importlib.reload(run)

#Main code

# First window - displayed on start
root = tkinter.Tk()
MainWindow = GUI.FileLoadGUI(root)
root.protocol("WM_DELETE_WINDOW", CloseFileLoad)
root.mainloop()

# Second window - displayed when first window closed
if (fileloadclose):
    while simulationclose:
        # Initial Simulation setup
        microbit.reset_simulation = False
        microbit.panic_mode = False
        root = tkinter.Tk()
        SimulationWindow = GUI.SimulationGUI(root)
        root.protocol("WM_DELETE_WINDOW", CloseSimulationWindow)
        microbit._initTime()
        # This allows the GUI to update on a regular schedule
        root.after(0, SimulationWindow.UpdateMicrobit, root)
        # This allows the code to be simulated to be run independantly
        runthread = threading.Thread(target=importFunction)
        runthread.daemon = True
        runthread.start()
        root.mainloop()
