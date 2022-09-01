# CarbonCutter

This is the read me file explaining how to operate the robot and select the desired pattern

## Setup

- Install the grbl-with-solenoid-Z-axis-for-2D-plotter-master library on the arduino
- Install [GRBL plotter](https://grbl-plotter.de/) on the computer

## Create desired samples

### GUI

- Open designsetting.py and run the program
- Enter all of the desired samples into the GUI
- All of the samples entered will be saved to the CSV
- Every sample in the CSV will be placed on the Sheets layer by layer
- There is no error catching so ensure all of the samples fit into the 300 by 330 sheet

> Note: the cross ply check does not work yet the implementation will just rquire each sheet to be rotated and then stacked

### Generate g-code

- Open the svg_draw_funct.py file and run it.
- Check the g-code and pattern by opening the svg files
- the txt file of the same name will say what each ply corrisponds too

## Robot setup 

- Connect the 3.5mm terminals to the power supply +ve into the red terminals and black to ground
- Connect the servo USB to the wall socket
- Connect the arduio to the computer
- Using the jig align the sheet of prepreg to the corner

## Printing

- Upload the first layer to the GRBL plotter program
- Run the homing process
- Press run
- repeat for each layer

## Calabration
- Done manually by typeing the commands into the arduino serial console
