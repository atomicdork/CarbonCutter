from re import I
import cairo
import sample_functions as sf


"""
    Draws the SVG file for the cutting feild Layer by layer
"""
def draw_cf_layer():
    CF = sf.CuttingField()
    CF.read_make_samples()
    CF.ply_list_by_layer()
    # sheet_list = CF.start_pos_gen(sample_number) # [sheet_list,sheet_name,sheet_number]
    sheet_list = CF.start_pos_new()

    for sheet in sheet_list:
        sheet_name = sheet[1]

        with cairo.SVGSurface(f"sheet_svg_files\{sheet_name}.svg", CF.X_SHEET_SIZE, CF.Y_SHEET_SIZE) as surface:
            context = cairo.Context(surface)
            surface.set_document_unit(7)
            context.set_source_rgba(0, 0, 0, 1)
            context.set_line_width(0.5)
            context.set_line_cap(cairo.LINE_CAP_ROUND)
            for i in range(8):
                context.move_to(i+10,10)
                context.line_to(i+10,12.5)
                context.move_to(CF.X_SHEET_SIZE-i-10,10)
                context.line_to(CF.X_SHEET_SIZE-i-10,12.5)

            inc_val = 0
            for i in sheet[0]:
                try:
                    ply = CF.samp_dict["Layers"][sheet[2]][inc_val]
                except Exception as e:
                    print(e)
                    print(sheet[2], end=" ")
                    print(len(CF.samp_dict["Layers"][sheet[2]]), end= " ")
                    print(inc_val)
                ply.draw_ply_line(context,i)
                ply.draw_ply_outline(context,i)
                inc_val += 1
        
            
            
        print("Drawing sheet done")

"""
    Draws the SVG file for the cutting feild
"""
def draw_cf(sample_number=-1):
    inc_val = 0
    CF = sf.CuttingField()
    CF.read_make_samples()
    CF.create_ply_list(sample_number)
    sheet_list = CF.start_pos_gen(sample_number) # [sheet_list,sheet_name,sheet_number]
    # sheet_list = CF.start_pos_new()

    for sheet in sheet_list:
        sheet_name = sheet[1]

        with cairo.SVGSurface(f"sheet_svg_files\{sheet_name}.svg", CF.X_SHEET_SIZE, CF.Y_SHEET_SIZE) as surface:
            context = cairo.Context(surface)
            surface.set_document_unit(7)
            context.set_source_rgba(0, 0, 0, 1)
            context.set_line_width(0.5)
            context.set_line_cap(cairo.LINE_CAP_ROUND)
            for i in range(4):
                context.move_to(i+10,10)
                context.line_to(i+10,12.5)


            for i in sheet[0]:
                ply = CF.samp_dict["Plys"][sample_number][inc_val]
                ply.draw_ply_line(context,i)
                ply.draw_ply_outline(context,i)
                inc_val += 1
        
            
            
        print("Drawing sheet done")

def make_gcode(sample_number=-1):
    inc_val = 0
    CF = sf.CuttingField()
    CF.read_make_samples()
    CF.create_ply_list(sample_number)
    sheet_list = CF.start_pos_gen(sample_number) # [sheet_list,sheet_name,sheet_number]
    gcode_string_list = []

    pen_dwn = f"G90 G0 Z-2.000\n"
    pen_up = f"G90 G0 Z2.000\n"
    gcode_string_list.append(pen_up)
    for i in range(4):
        gcode_string_list.append(f"G1 X{i} Y10 F1000\n{pen_dwn}{pen_up}")
    for i in range(4):
        gcode_string_list.append(f"G1 X{i+10} Y10 F1000\n{pen_dwn}{pen_up}")


    for sheet in sheet_list:
        sheet_name = sheet[1]
        with open(f"sheet_gcode\{sheet_name}.gcode", "w") as f:
            f.writelines(gcode_string_list)
            

            for i in sheet[0]:
                

                ply = CF.samp_dict["Plys"][sample_number][inc_val]
                # gcode_vals = ply.ply_gcode_write(f,i)
                ply.ply_gcode_write(f,i)
                # gcode_string_list.append(gcode_vals)
                inc_val += 1

            # Remove duplicates
            # fin_gcode = list(dict.fromkeys(gcode_string_list))
            # f.writelines(fin_gcode)

"""
    GCode per each ply layer
"""
def gcode_ply_layer():
    inc_val = 0
    CF = sf.CuttingField()
    CF.read_make_samples()
    CF.ply_list_by_layer()
    sheet_list = CF.start_pos_new()
    gcode_string_list = []

    pen_dwn = f"G90 G0 Z-2.000\n"
    pen_up = f"G90 G0 Z2.000\n"
    gcode_string_list.append(pen_up)
    for i in range(8):
        gcode_string_list.append(f"G1 X{i} Y10 F1000\n{pen_dwn}{pen_up}")
    for i in range(8):
        gcode_string_list.append(f"G1 X{CF.X_SHEET_SIZE-i-10} Y10 F1000\n{pen_dwn}{pen_up}")


    for sheet in sheet_list:
        sheet_name = sheet[1]
        with open(f"sheet_gcode\{sheet_name}.gcode", "w") as f:
            f.writelines(gcode_string_list)
            
            inc_val = 0
            for i in sheet[0]:
                ply = CF.samp_dict["Layers"][sheet[2]][inc_val]
                # gcode_vals = ply.ply_gcode_write(f,i)
                ply.ply_gcode_write(f,i)
                # gcode_string_list.append(gcode_vals)
                inc_val += 1


draw_cf_layer()
gcode_ply_layer()
# for i in range(4):
#     draw_cf(i)
#     make_gcode(i)