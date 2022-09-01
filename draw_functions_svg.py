import os
import csv
import cairo

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
    dictList = []
# Opens the file
    with open(fileName, 'r') as data:
        for line in csv.DictReader(data):
            dictList.append(line)

    return dictList[-1]

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
    Draws one sample on the SVG file
"""
def draw_svg_samp(context, startX, startY,):
    # TODO Somewhere somethign to get the sample sizes and scale the drawing placement accordingly but for now it is fine
    samp_list = get_samp_size()
    sample_padding = 5 #mm
    # size = get_samp_size()
    size = scale_sample(init_offset)
    
    pos1 = get_square_pos(init_offset, size)
    
    context.rectangle()