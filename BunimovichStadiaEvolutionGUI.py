# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 13:56:14 2019
Stadia evoulution Viewer (GUI). Provides a GUI for the user to input
what they want to view. (Stadia View, Cylinder View, or Spherical View)
@author: Randy
"""

import Tkinter as tk
from Tkinter import StringVar, Label, Entry, OptionMenu, Menu, Message, Button
from MessageText import TEXT, ITERMESSAGE, PHIMESSAGE1, PHIMESSAGE2
from Plotter import plotter
from CoordinateConversion import mod2pi
import math

pi = math.pi

# Create a GUI window
master = tk.Tk()

## Create global variables (those in drop down menues) ##
constvar   = StringVar(master) # Which variable (theta/phi) is constant?
eRange     = StringVar(master) # Specifies a window for the other var to vary
samples    = StringVar(master) # Specifies the number of samples
sampleType = StringVar(master) # Specifies the sampling technique to be used
iterations = StringVar(master) # Specifies the number of iterations
start      = StringVar(master) # Specifies the iteration to start displaying

## Global entry varialbes
const = StringVar(master)
var   = StringVar(master)

## Global checkbox variables
c_check = StringVar()
s_check = StringVar()
b_check = StringVar()

# Set default values for the global variables (displayed on dropdowns)
constvar.set("constant variable")
eRange.set("sampled variable range")
samples.set("samples")
sampleType.set("sample method")
iterations.set("iterations")
start.set("first iteration")
# Make sure check boxes start unchecked
c_check.set(0)
s_check.set(0)
b_check.set(0)

## A function for displaying the "about" information under the help menu ##
## This uses the variable TEXT imported from helpAboutText.py ##
def about():
    help_window = tk.Toplevel(master) 
    help_window.geometry("1000x1000")
    help_window.title("About the Bunimovich Stadia Evolution Viewer")
          
    text = Message(help_window, text = TEXT, padx = 100)
    text.pack()
    
## A function for resetting all values to their default ##
def reset_all(): 
    # Clear the text entry boxes
    constVar_field.delete(0, tk.END)  
    samplVar_field.delete(0, tk.END)
    constvar.set("constant variable")
    eRange.set("sampled variable range")
    samples.set("samples")
    sampleType.set("sample method")
    iterations.set("iterations")
    start.set("first iteration")
    c_check.set(0)
    s_check.set(0)
    b_check.set(0)


## A function for ensuring the generate button can only be pressed when ##
## all fields have been filled in. ------------------------------------ ## 
def protectGenerate(*args):
    a = not (constvar.get()   == "constant variable")
    b = not (eRange.get()     == "sampled variable range")
    c = not (samples.get()    == "samples")
    d = not (sampleType.get() == "sample method")
    e = not (iterations.get() == "iterations")
    f = not (start.get()      == "first iteration")
    g = const.get()
    h = var.get()
    i = c_check.get() == '1' or s_check.get() == '1' or b_check.get() == '1'
    if a and b and c and d and e and f and g and h and i:
        generate_button.config(state = 'normal')
    else:
        generate_button.config(state = 'disabled')

## A function for ensuring that the text boxes supplying the values of ##
## theta and phi are float ------------------------------------------- ##        
def validate(action, index, value_if_allowed, prior_value, text, \
             validation_type, trigger_type, widget_name):
    # action=1 -> insert
    if(action=='1'):
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    else:
        return True
    
## A function for generating the visual output
def generate():
    ## Get the values of all variables ##
    cvar = constvar.get()        # Which variable is the constant one?
    sams = int(samples.get())    # Number of samples
    avg  = float(var.get())      # Average value of sampled variable
    eps  = eRange.get()          # Range of sampled variable
    para = float(const.get())    # Value of constant variable
    its  = int(iterations.get()) # Number of iterations
    star = int(start.get())      # First iteration to display to user
    styp = sampleType.get()      # Type of sampling method
    
    ## Set the view variables according to the check boxes make their default
    ## values an empty string.
    c,s,b = "","",""
    if c_check.get() == '1':
        c = "c"         # Indicates if cylinder view is checked.
    if s_check.get() == '1':
        s = "s"         # Indicates if spherical view is checked.
    if b_check.get() == '1':
        b = "b"         # Indicates if stadia view is checked.
    
    # get the eps value ready to pass to the plotter
    if eps == "pi/4":
        epsi = pi/4
    elif eps == "pi/16":
        epsi = pi/16
    elif eps == "pi/64":
        epsi = pi/64
    elif eps == "pi/256":
        epsi = pi/256
    elif eps == "pi/1024":
        epsi = pi/1024
    else:
        print "Invalid input from drop down menu"
    
    ## Make sure that the number of iterations and the first iteration to ##
    ## display are consistent ------------------------------------------- ##
    if its <= star:
        iteration_error_window = tk.Toplevel(master)
        iteration_error_window.geometry("300x150")
        iteration_error_window.title("ILLEGAL INPUT DETECTED")
          
        text = Message(iteration_error_window, text = ITERMESSAGE)
        text.pack()
        return False
    
    ## Make sure that theta is in the proper range ##    
    if cvar == "theta" and (para < 0 or para >= 2*pi):
        # para is a theta value and its outside of the [0,2pi) range.
        # Mod it into the [0,2pi) range.
        para = mod2pi(para)

    
    ## Make sure that phi is in the proper range ##
    if cvar == "phi" and (para <= -pi/2 or para >= pi/2):
        phi_error_window = tk.Toplevel(master)
        phi_error_window.geometry("400x300")
        phi_error_window.title("ILLEGAL INPUT DETECTED")
        
        text = Message(phi_error_window, text = PHIMESSAGE1)
        text.pack()
        return False
    ## Make sure that phi is in the proper range ##
    if cvar == "theta" and (avg - epsi <= -pi/2 or avg + epsi >= pi/2):
        phi_error_window = tk.Toplevel(master)
        phi_error_window.geometry("400x200")
        phi_error_window.title("ILLEGAL INPUT DETECTED")
        
        text = Message(phi_error_window, text = PHIMESSAGE2)
        text.pack()
        return False
    
    if plotter(cvar, sams, avg - epsi, avg + epsi, para, its+1, star, 2, \
                    styp, c + s + b):
        confirm_window = tk.Toplevel(master) 
        confirm_window.geometry("200x100")
        confirm_window.title("Success!")
        
        msg  = """
        Pdf(s) of the desired images were created 
        in the folder containing this application.
        """
        text = Message(confirm_window, text = msg, padx = 10)
        text.pack()

if __name__ == "__main__":
    
    # Set the size of the GUI window
    master.geometry("460x285")
    master.title("Bunimovich Stadia Evolution Viewer")
    
    ## Create a Menu ##
    menu = Menu(master)
    master.config(menu = menu)
    
    # Add help menu with an about option 
    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About...", command=about)
    
    ## WIDGETS ##
    # Labels for drop downs
    label_const   = Label(master, text = "Constant Variable: ")
    label_eRang   = Label(master, text = "Sampled Variable Range: ")
    label_samples = Label(master, text = "Number of Samples: ")
    label_samType = Label(master, text = "Sampling Method: ")
    label_iters   = Label(master, text = "Number of Iterations: ")
    label_startIt = Label(master, text = "First Iteration to Display: ")
    
    # Lables for text input boxes
    label_value_const   = Label(master, text = "Value of Constant Variable: ")
    lable_value_sampVar = Label(master, text = \
                                "Mean Value of Sampled Variable: ")
    
    ## Use the grid method to place the widgets ##
    label_const.grid(row = 0, column = 0)
    label_value_const.grid(row = 1, column = 0)
    lable_value_sampVar.grid(row = 2, column = 0)
    label_eRang.grid(row = 3, column = 0)
    label_samples.grid(row = 4, column = 0)
    label_samType.grid(row = 5, column = 0)
    label_iters.grid(row = 6, column = 0)
    label_startIt.grid(row = 7, column = 0)
    
    ## Create text entry boxes for getting theta and phi ##
    vcmd = (master.register(validate), '%d', '%i', '%P', '%s', '%S', '%v', \
                                       '%V', '%W')
    constVar_field = Entry(master, textvariable = const, validate = 'key', \
                           validatecommand = vcmd)
    samplVar_field = Entry(master, textvariable = var, validate = 'key', \
                           validatecommand = vcmd)
    
    # Place the text entry boxes on the window
    constVar_field.grid(row = 1, column = 2, ipadx = "20")
    samplVar_field.grid(row = 2, column = 2, ipadx = "20")
    
    ## Create the list of option for each drop down ##
    constVar_list = ["theta", "phi"]
    eRang_list = ["pi/4", "pi/16", "pi/64", "pi/256", "pi/1024"]
    samples_list = ["2", "5", "10", "20", "50", "100", "200", "500", "1000",\
                     "2000",  "5000",  "10000"]
    samType_list = ["even", "random"]
    iterations_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", \
                       "11", "12", "13", "14", "15"]
    start_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", \
                  "11", "12", "13", "14", "15"]
    ## Create drop down menues ##
    const_option   = OptionMenu(master, constvar, *constVar_list)
    eRang_option   = OptionMenu(master, eRange, *eRang_list)
    samples_option = OptionMenu(master, samples, *samples_list)
    samType_option = OptionMenu(master, sampleType, *samType_list)
    iterate_option = OptionMenu(master, iterations, *iterations_list)
    start_option   = OptionMenu(master, start, *start_list)
    
    # Place the drop down menues
    const_option.grid(row = 0, column = 2)
    eRang_option.grid(row = 3, column = 2)
    samples_option.grid(row = 4, column = 2)
    samType_option.grid(row = 5, column = 2)
    iterate_option.grid(row = 6, column = 2)
    start_option.grid(row = 7, column = 2)
    
    ## Create buttons ##
    clear_button    = Button(master, text = "Reset All", command = reset_all)
    generate_button = Button(master, text = "Generate", command = generate)
    quit_button     = Button(master, text = "Quit", command = master.destroy)
    
    # Place the buttons
    quit_button.grid(row = 8, column = 0)
    clear_button.grid(row = 8, column = 1)
    generate_button.grid(row = 8, column = 2)
    
    # Configure the generate_button to be disabled initially. It shall 
    # remain disabled until all fields are entered.
    generate_button.config(state = 'disabled')
    
    # Attach a trace to all varialbes. Use it to ensure that generate_button
    # can only be pressed when all fields are entered.
    constvar.trace("w", protectGenerate)
    eRange.trace("w", protectGenerate)
    samples.trace("w", protectGenerate)
    sampleType.trace("w", protectGenerate)
    iterations.trace("w", protectGenerate)
    start.trace("w", protectGenerate)
    const.trace("w", protectGenerate)
    var.trace("w", protectGenerate)
    
    ## Create check buttons to provide options to the user
    c_checkbutton = tk.Checkbutton(master, variable=c_check, \
                            text ='cylinder view', command=protectGenerate)
    s_checkbutton = tk.Checkbutton(master, variable=s_check, \
                            text ='spherical view', command=protectGenerate)
    b_checkbutton = tk.Checkbutton(master, variable=b_check, \
                            text ='stadia view', command=protectGenerate)
    
    # Place checkbuttons
    c_checkbutton.grid(row = 9, column = 0)
    s_checkbutton.grid(row = 9, column = 1)
    b_checkbutton.grid(row = 9, column = 2)
    
    master.mainloop()