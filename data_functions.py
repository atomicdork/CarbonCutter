import os
import csv
import cairo
from PIL import Image, ImageDraw

"""
    Saves the data that was entered to csv
"""
def save_to_CSV(header_labels, data):

    if not os.path.isfile('pattern_param.csv'):
        with open('pattern_param.csv', 'w', newline='') as f:
           param_writer = csv.DictWriter(f, fieldnames=header_labels)
           param_writer.writeheader()

# writes the data to the file
    with open('pattern_param.csv', mode='a', newline='') as param_file:
        param_writer = csv.DictWriter(param_file, fieldnames=header_labels)
        param_writer.writerow(data)

"""
Opens up a csv file and gets the contents
Puts it into a dictionary and returns it
"""
def get_csv_param(fileName):
# Opens the file
    with open(fileName, 'r') as data:

        #MAKE SURE SAMPLE IS ALWAYS AT THE BOTTOM OF THE CSV FILE (LAST ROW)
        reader = csv.DictReader(data)
        dict_out = [dict(d) for d in reader]
        for i in range(len(dict_out)):
            for key in dict_out[i]:
                try:
                    dict_out[i][key] = float(dict_out[i][key])
                except Exception as e:
                    # print(e)
                    pass
    return dict_out


"""
    Splits the sample size text
"""
def get_samp_size():
    list_param = get_csv_param("pattern_param.csv")
    sample_size_txt = list_param["Sample Size"]
    adj_str = sample_size_txt.replace('m', '')

    samp_list = []
    for i in adj_str.split():
        if i.isdigit():
            samp_list.append(int(i))

    # Outputs the sample size as a list of [x, y]
    return samp_list

"""
    Fill in the data components from csv
"""
def fill_components():

    list_param = get_csv_param("pattern_param.csv")
    print(list_param)
    for i in range(len(list_param)):

        for key in list_param[i]:
            try:
                if list_param[i][key] in (None,"",''," "):
                    if key =="Dx Value":
                            list_param[i][key] =list_param[i]["Layers"] * list_param[i]["Height"]  
                    if key =="Dy Value":
                        list_param[i][key] = list_param[i]["ID Distance"] * (list_param[i]["Layers"]-1)
                    if key == "Height":
                        list_param[i][key] = list_param[i]["Dx Value"] * list_param[i]["Layers"] 
                    if key == "ID Distance":
                        list_param[i][key] = list_param[i]["Dy Value"] /(list_param[i]["Layers"]-1)
            except Exception as e:
                print(e)
                print("Incomplete data, please correct")

    keys = list_param[0].keys()
    with open("pattern_param_clean.csv","w") as file:
        csvwriter = csv.DictWriter(file,keys)
        csvwriter.writeheader()
        csvwriter.writerows(list_param)


"""
    Solves for ID and fils the values in for the csv file 
"""
def clean_csv():
    full_file_list = []
    list_param = get_csv_param("pattern_param.csv")
    print(list_param)
    for i in range(len(list_param)):
        all_param = {}

        for key in list_param[i]:
            all_param[key] = list_param[i][key]

        all_param["ID"] = round(list_param[i]["Dy Value"] /(list_param[i]["Layers"]-1),2)
        full_file_list.append(all_param)

    keys = full_file_list[-1].keys()

    if not os.path.isfile('pattern_param_clean.csv'):
        with open("pattern_param_clean.csv",mode="w", newline='') as file:
            csvwriter = csv.DictWriter(file,keys)
            csvwriter.writeheader()
            csvwriter.writerows(full_file_list)
    else:
        # writes the data to the file
        with open('pattern_param_clean.csv', mode='a', newline='') as file:
            csvwriter = csv.DictWriter(file,keys)
            csvwriter.writerow(full_file_list[-1])

# """
#     Finds the scale factor
# """
# def scale_size(samp_size, pad_val=(20,20), samp_space=20):
#     img_size = (600, 400)

#     # Finds the amount the x and y sizes
#     x_len = img_size[0]-(2*pad_val[0])
#     y_len = img_size[1]-(2*pad_val[1])

#     # gives the scale of the image when the border is taken into account
#     # adj_img_size = (img_size[0]-(2*padx),img_size[1]-(2*pady)-(samp_space/2))
#     adj_img_size = (x_len, y_len)

#     x_scale_factor = adj_img_size[0]/samp_size[0]
#     y_scale_factor = adj_img_size[1]/samp_size[1]

#     return (x_scale_factor, y_scale_factor)

# """
#     Changes the sample size according to the factor
# """
# def scale_sample(pad_val):
#     size = []

#     sample_size = get_samp_size()
#     scale_amount = scale_size(sample_size, pad_val)

#     # Multiples the scale factor by the sample size
#     for i in range(len(sample_size)):
#         temp = sample_size[i]*scale_amount[i]
#         size.append(temp)
    
#     return size

# """
#     Create a list of tuples to control the displayed square size
# """
# def get_square_pos(start_pos, size):
#     pos_list = []

#     x_adj_list = [start_pos[0]] * 5
#     y_adj_list = [start_pos[1]] * 5

#     x_adj_list[1] += size[0]
#     x_adj_list[2] += size[0]

#     y_adj_list[2] += size[1]
#     y_adj_list[3] += size[1]

#     for i in range(5):
#         pos_list.append((x_adj_list[i], y_adj_list[i]))
    
#     return pos_list

# """
#     Draws one sample on the SVG file
# """
# def draw_svg_samp(context, startX, startY,):
#     # TODO Somewhere somethign to get the sample sizes and scale the drawing placement accordingly but for now it is fine
    
#     sample_pad = 5 #mm
#     # size = get_samp_size()
#     size = scale_sample(init_offset)
    
#     pos1 = get_square_pos(init_offset, size)
    
#     context.rectangle()

# """
#     Draws the image of two of the layers of the sample
# """
# def draw_samples(img):
#     init_offset = (30,30)
#     sample_pad = 20
#     # size = get_samp_size()
#     size = scale_sample(init_offset)

#     # adj_y_start = init_offset[1]+sample_pad+size[1]
#     # snd_start = (init_offset[0],adj_y_start)

#     draw = ImageDraw.Draw(img)
#     pos1 = get_square_pos(init_offset, size)
#     # pos2 = get_square_pos(snd_start, size)
#     draw.line(pos1, fill='black')
#     # draw.line(pos2, fill='black')

#     img.save('test.png')

# def draw_diagram():
#     im = Image.new('RGBA', (600,400), 'white')
    
#     draw = ImageDraw.Draw(im)
#     draw.line([(0, 0), (199, 0), (199, 199), (0, 199), (0, 0)], fill='black')
#     draw.rectangle((20, 30, 60, 60), outline= 'black')
#     draw.rectangle((40, 60, 150, 70), fill='red')
#     # draw.ellipse((120, 30, 160, 60), fill='red')
#     # draw.polygon(((57, 87), (79, 62), (94, 85), (120, 90), (103, 113)),fill='brown')
#     # for i in range(100, 200, 10):
#     #     draw.line([(i, 0), (200, i - 100)], fill='green')
#     im.show()
#     im.save('drawing.png')

# im = Image.new('RGBA', (600,400), 'white')

# draw_samples(im)

# im.show()

# draw_diagram()