import argparse
import csv
import matplotlib.pyplot as plt
import os.path as op
import numpy as np
import statistics

def convert_type(element):
    if element == "": 
        return None
    try:
        return int(element)
    except ValueError:
        try:
            return float(element)
        except ValueError:
            return element

def parse_file(filename, delimiter):
    assert(op.isfile(filename)), "The File Doesn't Exist"
    with open(filename,'r') as fhandle:
        my_csvreader = csv.reader(fhandle,delimiter=delimiter)
        outer_list_csv = []
        for row in my_csvreader:
            row_list_csv=[]
            for element in row:
                new_element_csv = convert_type(element)
                if new_element_csv is not None:
                    row_list_csv.append(new_element_csv)
            if len(row_list_csv) > 0:
                outer_list_csv += [row_list_csv]
    return outer_list_csv

def line_to_dict(lines, header=False):
    if header:
        column_titles = lines[0]
        lines = lines[1:]
    else:
        column_titles = []
        for idx in list(range(1, len(lines[0])+1)):
            column_titles += ["Column"+str(idx)]
    
    data_dict = {}
    for idx, column in enumerate(column_titles):
        data_dict[column] = []
        for row in lines:
            data_dict[column] += [row[idx]]
    return data_dict

def generate_points(coefs, min_val, max_val):
    xs = np.arange(min_val, max_val, (max_val-min_val)/100)
    return xs, np.polyval(coefs, xs)


def plot_data(dd, polys=[1,2,3,4],plot_option=False):
    ncols = len(dd.keys())
    fig = plt.figure(figsize=(30,30))   
    for i1, column1 in enumerate(dd.keys()):
        for i2, column2 in enumerate(dd.keys()):
            loc = i1*ncols + i2 + 1
            plt.subplot(ncols, ncols, loc)
            x = dd[column1]
            y = dd[column2]
                
            plt.scatter(x, y)
            plt.xlabel(column1)
            plt.ylabel(column2)
            plt.title("{0} x {1}".format(column1, column2))

            for poly_order in polys:
                coefs = np.polyfit(x, y, poly_order)  
                xs, new_line = generate_points(coefs, min(x), max(x))
                plt.plot(xs, new_line)
    fig.tight_layout(pad=0.4,w_pad=0.5,h_pad=1.0)
    plt.legend()
    plt.savefig("./my_pairs_plot.png")

def summarize_data(dd, summary):
    if summary in dd.keys():
        print("mean is "+str(statistics.mean(dd[summary])))
        print("max is "+str(max(dd[summary])))
        print("min is "+str(min(dd[summary])))
        print("standard deviation is "+str(statistics.pstdev(dd[summary])))
        if len(np.unique(dd[summary]))/len(dd[summary])<discrete_threshold:
            print("your column most likely contains discrete values")
        else:
            print("your column most likely contains continuous values")
    else:
        print("Not a valid column name")
        
def interpolate_data(dd,interpolate):
    column1 = interpolate[0]
    column2 = interpolate[1]
    value = float(interpolate[2])
    if column1 in dd.keys() and column2 in dd.keys() and value >= float(min(dd[column1])) and value <= float(max(dd[column1])):
        if len(np.unique(dd[column1]))/len(dd[column1])<discrete_threshold or len(np.unique(dd[column2]))/len(dd[column2])<discrete_threshold:
            print("Your values are most likely discrete. It doesn't make sense to interpolate in this case. Try another column")
        else:
            for poly_order in [1,2,3]:
                coefs = np.polyfit(dd[column1], dd[column2], poly_order) 
                print("The "+str(poly_order)+" degree corresponding value for your input is "+str(np.polyval(coefs, value)))
    else:
        print("These are not valid column name or your value does not exist in the column. Refer to summary option for more details on the column")
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",type=str,help='Please input file name')
    parser.add_argument("delimiter", type=str,help='Please indicate the delimiter in your file')
    parser.add_argument('-H', '--header', action="store_true", help="determines if a header is present")
    parser.add_argument('-p','--plot', action="store_true", help="indicate if a plot should be created")
    parser.add_argument('-s','--summary',help="provide summary per column")
    parser.add_argument('-i','--interpolate',nargs=3,help="please input names of two columns and value of the first in order")
    args = parser.parse_args()
    
             
    data = parse_file(args.filename, args.delimiter)
    data_dict = line_to_dict(data, header=args.header)
    if args.plot:
        plot_data(data_dict)
    if args.summary is not None:
        summarize_data(data_dict, args.summary)
    if args.interpolate is not None:
        interpolate_data(data_dict,args.interpolate)
            
discrete_threshold = 0.1
if __name__ == "__main__":
    main()






