import re
import math
import data_functions
import numpy as np



"""
    Class containing all a single ply#
    this lets it be placed anywhere on the printing surface
    Takes data from the Sample class

    It should be shifted down along Dy by length ID
"""
class Ply:
    
    def __init__(self, layer_position, samp_size, orientation=0):
        self.layer_position = layer_position
        self.width = samp_size[0]
        self.length = samp_size[1]
        self.h = 0
        self.ply_name = "ply" # This is just an id so it can be identified easier
        self.orientation = orientation # This can be 90 if it is the cross ply
        self.cut_start_points = [] # The top leftmost corner position This is relative [[x,y]]
       
    
    """
        Defines where the blade should push down
        This is relative without the buffer 
        This is for UNIDIRECTIONAL TODO make this cross-ply
        ply_count is the number of plys in the sample
        layer_position is used to create the offset as you move down plys
    """
    def cut_pos_in_ply(self, ID, H, Dx, Dy, ply_count):
        self.h = H
        xp_pos = 0
        yp_pos = 0
        
        # Segments per Dx is the ply_count
        number_in_width = self.width/Dx *ply_count
        number_in_length = (self.length/Dy) + 1

        for i in range(int(number_in_width)):
            xp_pos = (H*i)%self.width

            for j in range(int(number_in_length)):
                all_pos = (j*Dy)
                shift_from_x = ((i*ID)%Dy)
                shift_along = (round((self.layer_position)*ID+(i*ID))%Dy)
                yp_pos = all_pos+shift_along#+shift_from_x#+thing3
                
                if self.layer_position == 7 and xp_pos == 10:
                    pass
                    # print("here")
                # If yp_pos is greater than the length then the summation is too large
                if yp_pos > self.length:
                    break
                    
                else:
                    pos_save = [round(xp_pos,2), round(yp_pos,2)]
                    self.cut_start_points.append(np.array(pos_save))
                
        # Creates the label
        self.ply_name = f"y{Dy}h{H}lay{self.layer_position}"

        return self.cut_start_points

    """
        Generate global Ply position
    """
    def glob_pos_generate(self, start_pos=[0]):
        cnt = 0
        glob_pos_list = []

        for i in self.cut_start_points:
            if self.orientation == 0:
                x_pos = i[1]
                y_pos = i[0]
            elif self.orientation == 90:
                x_pos = i[0]
                y_pos = i[1]

            # print(x_pos, end=" ")
            # print(y_pos, end=" -> ")

            x_pos += start_pos[0] # Adjustst the cuts with the x start
            y_pos += start_pos[1]

            pos_save = [round(x_pos,2), round(y_pos,2)]
            glob_pos_list.append(np.array(pos_save))
            cnt += 1
            #
        return glob_pos_list

    """
        Draws the ply on a cairo surface with ply x and global x the same
        Based on the placement of the start position
    """   
    def draw_ply_line(self, context, start_pos):
        
        list_temp = self.glob_pos_generate(start_pos)
        no_dup_list = [list(pos) for pos in set(tuple(element) for element in list_temp)]
        sorted_list = (sorted(no_dup_list,key=lambda x : (x[1])))
        length_of_cuts = len(list_temp)
        start_color = 0
        # context.set_line_width(1)
        context.set_source_rgba(0,0,0,1)
        if start_pos[0] < 100:
            context.move_to(start_pos[0]-15,start_pos[1])
            context.line_to(start_pos[0]-15,start_pos[1]+2.5)


        for i in sorted_list: #TODO change this back to global?
            x_start_pos = i[0]
            y_start_pos = i[1]
            y_end_pos = y_start_pos + self.h
            # y_end_pos = y_start_pos
            
            start_color += 1
            context.move_to(x_start_pos,y_start_pos)
            context.line_to(x_start_pos,y_end_pos)
            context.stroke()
            context.set_line_width(0.5)
            
    """
        Creates a list of gcode entries in a list and writes it to a file 
    """
    def ply_gcode_write(self, file, start_pos):
        list_temp = self.glob_pos_generate(start_pos)
        # Turn it into a set so there are no duplicates
        no_dup_list = [list(pos) for pos in set(tuple(element) for element in list_temp)]
        sorted_list = (sorted(no_dup_list,key=lambda x : (x[1],x[0])))
        length_of_cuts = len(list_temp)
        pen_dwn = f"G90 G0 Z-2.000\n"
        pen_up = f"G90 G0 Z2.000\n"

        x_pos = start_pos[0]-15
        y_pos = start_pos[1]

        gcode_list = []

        if x_pos < 100:
            gcode_list.append(f"G1 X{x_pos} Y{y_pos} F1000\n{pen_dwn}{pen_up}")
        # gcode_list.append(string_temp)
          
        # context.set_line_width(1)
        for i in sorted_list: #TODO change this back to global?
            x_start_pos = i[0]
            y_start_pos = i[1]
            string_temp = f"G1 X{x_start_pos} Y{y_start_pos} F1000\n"
            gcode_list.append(string_temp)
            gcode_list.append(pen_dwn)
            gcode_list.append(pen_up)

        file.writelines(gcode_list)
        return gcode_list

    """
        Draws the outline of the ply sample
    """
    def draw_ply_outline(self, context, top_corner):
        start_pos = top_corner
        context.set_source_rgba(1, 0, 0, 1)
        context.set_line_width(0.04)
        if self.orientation == 90:
            context.rectangle(start_pos[0],start_pos[1],self.width,self.length)
        elif self.orientation == 0:
            context.rectangle(start_pos[0],start_pos[1],self.length,self.width)
        context.stroke()
        context.set_line_width(0.5)
   
"""
    Class containing all of the samples data
"""
class Sample:
    def __init__(self, data_row=-1):
        self.dx = 0
        self.dy = 0
        self.h = 0
        self.id = 0
        self.layers = 0
        self.sample_name = "name"
        self.samp_size = []
        self.ply_list = []

        # self.fill_sample()
        

    """
        Creates the sample from the provided file
    """
    def fill_sample(self, data_row=-1):
        dict_param = data_functions.get_csv_param("pattern_param_clean.csv")
        self.dx = dict_param[data_row]["Dx Value"]
        self.dy = dict_param[data_row]["Dy Value"]
        self.h = dict_param[data_row]["Height"]
        self.layers = int(dict_param[data_row]["Layers"])
        self.id = dict_param[data_row]["ID"]
        self.get_samp_size(dict_param[data_row]["Sample Size"])

        self.samp_name = f"x{self.dx}y{self.dy}h{self.h}"
        
        # With this data make the ply list
        self.make_ply()

        return dict_param[data_row]["Number of samples"]

    """
        Splits the sample size text
    """
    def get_samp_size(self, samp_size_txt):
        listTemp = re.findall("[-+]?(?:\d*\.\d+|\d+)", samp_size_txt)

        self.samp_size = [float(x) for x in listTemp]
        # Outputs the sample size as a list of [x, y]
        return self.samp_size       

    """
        Creates the list of Plys
    """         
    def make_ply(self):
        for i in range(int(self.layers)):
            ply_temp = Ply(i, self.samp_size) # this was i+1
            ply_temp.cut_pos_in_ply(self.id, self.h, self.dx, self.dy, self.layers)
            self.ply_list.append(ply_temp)


"""
    Class to contain all of the plys that wish to be printed
    This will draw the global SVG image
"""
class CuttingField:
    def __init__(self):
        self.BUFFER = 20 # This is needed at each side of the samples
        self.CUT_WIDTH = 10 # This is the space between adjacent cuts
        self.X_SHEET_SIZE = 325 # full sheet size is 420 but a full sample with buffer wont fit
        self.Y_SHEET_SIZE = 300 # set by provided material
        self.glob_ply_list = [] #This is a 2D list with each sample number
        self.sheet_list = []

        # Sample contains a list of instances of the sample class
        # Amount contains the number of samples that need to be printed
        self.samp_dict = {
            "Sample"   :[],
            "Amount"   :[],
            "Plys"     :[],
            "Layers"   :[[],[],[],[],[],[],[],[]]
        }

    """
        Read the CSV file to create samples
    """
    def read_make_samples(self):
        with open("pattern_param_clean.csv", mode="r") as file:
            row_count = sum(1 for line in file)-1 # Removes header line
        
        # Goes through each row and fills the sample from the csv
        for row in range(row_count):
            samp_temp = Sample(row)
            numb_of_samp = samp_temp.fill_sample(row)
            self.samp_dict["Sample"].append(samp_temp)
            self.samp_dict["Amount"].append(int(numb_of_samp))
            self.samp_dict["Plys"].append([])

        return (self.samp_dict["Sample"],row_count)

    """
        with the list of samples creates a pattern of plys
        based on the amount asked for only for one sample though
    """
    def create_ply_list(self, sample_number=-1):
        count = 0
        amount = self.samp_dict["Amount"][sample_number]

        for sample in self.samp_dict["Sample"]:
            amount = self.samp_dict["Amount"][count]
            temp_list = []

            for ply in sample.ply_list:
                for j in range(int(amount)):
                    temp_list.append(ply)
            
            self.samp_dict["Plys"][count] = temp_list
            # self.glob_ply_list.append(temp_list)
            count+=1
    """
        Creates a ply list split by layer
    """
    def ply_list_by_layer(self):
        amount = self.samp_dict["Amount"][-1]
        ply_list_temp = []

        ply_dict = {}
        for sample in self.samp_dict["Sample"]:
            for i in range(len(sample.ply_list)):
                ply = sample.ply_list[i]
                for j in range(amount):
                    self.samp_dict["Layers"][i].append(ply)



    """
        Generate global ply position from the list
        TODO the txt file doesn't match with the generated file
    """
    def sheet_text_guide(self, ply_name_list, key_info):
        sheet_name = key_info["sheet name"]
        sheet_number = key_info["sheet number"]
        samp_amount = key_info["sample copies"]
        samp_width = key_info["sample width"]
        samp_length = key_info["sample length"]
        number_long_side = key_info["samp in x and y"][1]
        sheet_ply_cnt = math.prod(key_info["samp in x and y"])
        name_list = []
        page_cnt = 0

        # Places all of the names in a list that matches up with how the text file
        # should be written
        for i in range(len(ply_name_list)):
            name = ply_name_list[i]
            name = f"{i}: {name}"
            
            if ((i%sheet_ply_cnt)>(number_long_side-1)):
                index_val = int((i % (number_long_side)) + (number_long_side*page_cnt))
                name_list[index_val].append(name)
            elif ((i%sheet_ply_cnt) == 0) and i != 0:
                page_cnt +=1
                name_list.append([name])
            else:
                name_list.append([name])

        with open(f"sheet_txt_files\{sheet_name}.txt",mode='w') as f:
            string = f"sheet number{sheet_number} number of samples{samp_amount} Sample size {samp_width} x {samp_length}\n"
            f.write(string)
            slice_start = sheet_number*number_long_side
            slice_end = sheet_number*number_long_side + number_long_side
            list_slice = name_list[slice_start:slice_end]
            for name in list_slice:
                first_val = name[0]
                try:
                    second_val = name[1]
                    second_val += "\n"
                except Exception as e:
                    second_val = "\n"
                f.write(f"{first_val}       {second_val}")

    """
        Generates a list of start positions for each sheet
        the sample is entered and for each ply is placed in the appropriate area.
    """
    def start_pos_gen(self, sample_number=-1):
        inc_val = 0
        samp_sheet_pos_list = [] # list of where corner will be placed
        ply_name_list = []
        num_plys = len(self.samp_dict["Plys"][sample_number])
        sample = self.samp_dict["Sample"][sample_number]
        samp_width = sample.samp_size[0]
        samp_length = sample.samp_size[1]
        samp_name = sample.samp_name
        samp_amount = self.samp_dict["Amount"][sample_number]
        samp_in_x = math.floor(self.X_SHEET_SIZE/(samp_length+(self.BUFFER*2)))
        samp_in_y = math.floor((self.Y_SHEET_SIZE-(self.BUFFER*2))/(self.CUT_WIDTH+samp_width))
        samp_in_sheet = samp_in_x * samp_in_y
        sheet_cnt = np.ceil(num_plys/samp_in_sheet)

        for sheet_number in range(int(np.ceil(sheet_cnt))):
            sheet_list = [] #list of all the start positions for one sheet
            for x_samp in range(samp_in_x):
                x_pos = self.BUFFER + (x_samp*samp_length) + (x_samp*(2*self.BUFFER))
                for y_samp in range(samp_in_y):
                    y_pos = self.BUFFER + (y_samp*samp_width) + (y_samp*self.CUT_WIDTH)
                    
                    if inc_val < num_plys:
                        ply = self.samp_dict["Plys"][sample_number][inc_val]
                        pos = [x_pos, y_pos]
                        sheet_list.append((x_pos, y_pos))
                        line_entry = f"Ply: {ply.ply_name} pos: {pos}"
                        ply_name_list.append(line_entry)
                        inc_val += 1
                        

            sheet_name = samp_name + f"sheet{sheet_number}"
            sheet_name = sheet_name.replace(".","_",3)

            key_info = {
                "sheet name"        :sheet_name,
                "sheet number"      :sheet_number,
                "sample copies"     :samp_amount,
                "sample width"      :samp_width,
                "sample length"     :samp_length,
                "samp in x and y"   :(samp_in_x, samp_in_y)
            }

            self.sheet_text_guide(ply_name_list, key_info)
            
            samp_sheet_pos_list.append([sheet_list,sheet_name,sheet_number])

        return samp_sheet_pos_list

    """
        Start Position generated for each ply of a given layer
        This is hard coded
    """
    def start_pos_new(self):
        samp_sheet_pos_list = [] # list of where corner will be placed
        ply_name_list = []
        sample = self.samp_dict["Sample"][-1]
        samp_width = sample.samp_size[0]
        samp_length = sample.samp_size[1]
        num_plys = 8
        samp_in_x = 2
        samp_in_y = 8
        samp_in_sheet = samp_in_x * samp_in_y
        

        for layer_number in range(8):
                sheet_list = [] #list of all the start positions for one sheet
                for x_samp in range(samp_in_x):
                    x_pos = self.BUFFER + (x_samp*samp_length) + (x_samp*(2*self.BUFFER))
                    for y_samp in range(samp_in_y):
                        y_pos = self.BUFFER + (y_samp*samp_width) + (y_samp*self.CUT_WIDTH)
                        
                        for ply in self.samp_dict["Layers"][layer_number]: 
                            pos = [x_pos, y_pos]
                            
                            line_entry = f"Ply: {ply.ply_name} pos: {pos}"
                            ply_name_list.append(line_entry)
                            sheet_list.append((x_pos, y_pos))

                no_dup_list = [list(pos) for pos in set(tuple(element) for element in sheet_list)]
                sorted_sheet_list = (sorted(no_dup_list,key=lambda x : (x[1])))

                key_info = {
                    "sheet name"        :f"Sheet_{layer_number}",
                    "sheet number"      :layer_number,
                    "sample copies"     :4,
                    "sample width"      :samp_width,
                    "sample length"     :samp_length,
                    "samp in x and y"   :(samp_in_x, samp_in_y)
                }

                self.sheet_text_guide(ply_name_list, key_info)
                
                # samp_sheet_pos_list.append([sheet_list,f"Sheet_{layer_number}",layer_number])
                samp_sheet_pos_list.append([sorted_sheet_list,f"Sheet_{layer_number}",layer_number])

        return samp_sheet_pos_list