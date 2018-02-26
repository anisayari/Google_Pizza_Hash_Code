import pandas as pd
import numpy as np



def read_input_file(filename):
    print("reading file: "+filename+"...")
    dict_map = {'T':1, 'M':0}
    with open(filename, 'r') as f:
        line = f.readline()
        height, width, min_ings, max_cells = [int(n) for n in line.split()]
        pizza = np.zeros([height, width])
        for row in range(height):
            pizza[row] = (map(dict_map.get, [str(n) for n in f.readline().strip()]))
    return pizza, min_ings, max_cells

class Pizza():
    def __init__(self, pizza, width, height):
        self.pizza = pizza
        self.width = width
        self.height = height

def pizzaolo():
    filename = 'files/input/small.in'
    print(read_input_file(filename))


if __name__ == '__main__':
    pizzaolo()
