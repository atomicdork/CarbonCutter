"""
    The point of this program is to take general
    Requests from the user and turn it into G-Code
    for the arduino
"""
from doctest import master
import tkinter as tk
import tkinter.ttk as ttk
import data_functions
import sample_functions


window = tk.Tk()
window.title("Design Config.")
window.resizable(width=False, height=False)

save_var = {
    "Dx Value" : tk.StringVar(),
    "Dy Value" : tk.StringVar(),
    "Height" : tk.StringVar(),
    "Layers" : tk.StringVar(),
    "Number of samples" : tk.StringVar(),
    "Sample Size" : tk.StringVar(),
    "Cross-ply" : tk.IntVar()
}

"""
    All the functions
"""
def handle_keypress(event):
    """Print the character associated to the key pressed"""
    print(event.char)

def submit():
    tempDict = {}

    for key in save_var:
        var = save_var[key].get()
        # Add to dictionary
        tempDict[key] = var

        print(f"{key} is {var}")

        var = save_var[key].set("")
        
    tempDict["Sample Size"] = samp_value.get()
    var = tempDict["Sample Size"]
    print(f"Sample Size is {var}")
    # Save the dict
    data_functions.save_to_CSV(list(save_var.keys()),tempDict)
    data_functions.clean_csv()

def cross_ply_on():
    print("Cross-ply is ", save_var["Cross-ply"].get())

window.bind("<Key>", handle_keypress)

# Creates a title frame to introduce the frame
frm_title = ttk.Frame()
main_lbl = ttk.Label(master=frm_title, text="Please enter your desired dimensions. \nPress submit to get a preview")
main_lbl.pack()
frm_title.pack()

# List of field labels
labels = [
    "Dx Value",
    "Dy Value",
    "Height",
    "Layers", # Also called Piles
    "Number of samples",
    "Sample Size",
    "Cross-ply"
]

# List of field labels
default_val = {
    "Dx Value":17.5,
    # "Dy Value",
    "Height":2.5,
    "Layers":8, # Also called Piles
    # "Sample Size"
}

# List of sample sizes
samp_size = [
    "17.5mm x 120mm",
    "20mm x 120mm",
    "100mm x 150mm"
]

# Create a new frame `frm_form` to contain the Label
# and Entry widgets for entering address information
frm_form = ttk.Frame(relief=tk.SUNKEN, borderwidth=3)
# Pack the frame into the window
frm_form.pack()

# Loop over the list of field labels
for idx, text in enumerate(labels):
    # Create a Label widget with the text from the labels list
    label = ttk.Label(master=frm_form, text=text)
    # Create Options Widget is option is sample size
    if text == "Sample Size":
        samp_value=tk.StringVar(frm_form)
        samp_value.set(samp_size[0])

        entry = tk.OptionMenu(frm_form, samp_value, *samp_size)
    elif text == "Cross-ply":
        entry = ttk.Checkbutton(frm_form, text="Select to create cross-ply sample", variable=save_var[text], onvalue=1, offvalue=0, command=cross_ply_on)
        
    else:
        # Create an Entry widget
        entry = ttk.Entry(master=frm_form, textvariable=save_var[text], width=50)

        #Checks if a default value is provided and if so adds it
        if text in default_val.keys():
            entry.insert(0,default_val[text])
    
    # Use the grid geometry manager to place the Label and
    # Entry widgets in the row whose index is idx
    label.grid(row=idx, column=0, sticky="e")
    entry.grid(row=idx, column=1, sticky='w')

# Create a new frame `frm_buttons` to contain the
# Submit and Clear buttons. This frame fills the 
# whole window in the horizontal direction and has
# 5 pixels of horizontal and vertical padding.
frm_buttons = tk.Frame()
frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

# Create the "Submit" button and pack it to the
# right side of `frm_buttons`
btn_submit = tk.Button(master=frm_buttons, text="Submit", command=submit)
btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

# Create the "Clear" button and pack it to the
# right side of `frm_buttons`
btn_clear = tk.Button(master=frm_buttons, text="Clear")
btn_clear.pack(side=tk.RIGHT, ipadx=10)

# Start the application
window.mainloop()