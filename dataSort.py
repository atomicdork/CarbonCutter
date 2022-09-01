import csv
import pandas as pd
import matplotlib.pyplot as plt

def sort_data_files():
    # open both files
    with open('data/test 1_1.csv','r') as mainFile, open('data/test1.csv','w') as firstfile, open('data/test2.csv', 'w') as secondfile, open('data/test3.csv', 'w') as thirdfile:
        
        lines = mainFile.readlines()
        type(lines)

        for idx in range(0, len(lines)):

            # if between 12 and 23701 copy to test1
            if idx >= 11 and idx <= 23700 and idx != 12:
                firstfile.write(lines[idx])
            # if between 23702 and 39999 to test2
            elif idx >= 23701 and idx <= 39998 and idx != 23702:
                secondfile.write(lines[idx])
            # if between 40000 and 56045 to test3
            elif idx >= 39999 and idx <= 56045 and idx != 40000:
                thirdfile.write(lines[idx])

def plot_force():

    test1 = 'data/test1.csv'
    test2 = 'data/test2.csv'
    test3 = 'data/test3.csv'
    
    t1 = pd.read_csv(test1)
    t2 = pd.read_csv(test2)
    t3 = pd.read_csv(test3)

    # plt.plot(t1['Time'],t1['Force'])
    plt.plot(t2['Displacement'], t2['Force'])
    plt.plot(t3['Displacement'], t3['Force'])

    plt.show()

plot_force()
# sort_data_files()