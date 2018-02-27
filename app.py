import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dict_map = {'T': 1, 'M': 0}


def read_input_file(filename):
    print("reading file: " + filename + "...")
    with open(filename, 'r') as f:
        line = f.readline()
        height, width, min_ings, max_cells = [int(n) for n in line.split()]
        pizza = np.zeros([height, width])
        for row in range(height):
            pizza[row] = (list(map(dict_map.get, [str(n) for n in f.readline().strip()])))
    print("reading file: " + filename + " Done :)")
    return pizza, height, width, min_ings, max_cells


def construct_output_file(Plate):
    outputfile = 'output.in'
    with open(outputfile, 'w') as f:
        f.write(str(len(Plate.slices))+"\n")
        for slice in Plate.slices:
            f.write(str(slice.row_start)+" "+str(slice.row_end)+" "+str(slice.col_start)+" "+str(slice.col_end)+"\n")
    return

def print_matrix(matrix):
    cmap = plt.cm.jet
    cmap.set_bad('white', 1.)
    plt.imshow(matrix, interpolation='nearest', cmap=cmap, extent=(0.5, 10.5, 0.5, 10.5))
    plt.colorbar()
    plt.show()

class Pizza():
    def __init__(self, pizza, width, height):
        self.pizza = pizza
        self.width = width
        self.height = height


class Plate():
    def __init__(self):
        self.slices = []

    def NumberOfSlice(self):
        return len(self.slices)

    def Serve(self):
        pass


class Slice():
    def __init__(self, row_start, col_start, row_end, col_end, slice_array):
        self.row_start = row_start
        self.col_start = col_start
        self.row_end = row_end
        self.col_end = col_end
        self.slice = slice_array
        self.cells = self.CountCells()
        self.tomatos,self.mushrooms = self.CountIngs()
        self.nan = self.CountNan()

    def CountNan(self):
        return np.isnan(self.slice).sum()

    def CountIngs(self):
        return self.slice.sum(),self.cells - self.slice.sum()

    def CountCells(self):
        #if self.col_end-self.col_start == 0:
            #width_of_slice = 1
        #else:
            #width_of_slice = self.col_end-self.col_start
        #if self.row_end-self.row_start == 0:
            #length_of_slice = 1
        #else:
            #length_of_slice  = self.row_end-self.row_start
        #return width_of_slice * length_of_slice

        width_of_slice = self.slice.shape[0]
        try:
            length_of_slice = self.slice.shape[1]
        except IndexError:
            length_of_slice = 1
        return width_of_slice * length_of_slice
        #return self.slice.shape[0]*self.slice.shape[1]



class Pizzaiolo():
    def __init__(self, Pizza, Plate, min_ings, max_cells):
        self.Pizza = Pizza
        self.Plate = Plate
        self.min_ings = min_ings
        self.max_cells = max_cells
        self.best,self.key_min = self.ThinkAboutBest()

    def Checkconstraint(self, Slice):
        tomatos = Slice.tomatos
        mushrooms = Slice.mushrooms
        cells = Slice.cells
        nan = Slice.nan
        dico_bool =  {"min_ings":False , "max_cells":False, "nan":False}
        if tomatos <= self.min_ings and mushrooms <= self.min_ings:
            dico_bool["min_ings"] = True
        if cells <= self.max_cells:
            dico_bool["max_cells"] = True
        if nan == 0:
            dico_bool["nan"] = True
        if dico_bool["min_ings"] and dico_bool["max_cells"] and dico_bool["nan"]:
            response = True
        else:
            response = False
        return response,dico_bool

    def AddSlicetoPlate(self, current_slice):
        self.Plate.slices.append(current_slice)
        pass

    def CuteSlice(self, row_start, col_start, row_end, col_end, slice_array):
        new_slice = Slice(row_start, col_start, row_end, col_end,slice_array)
        for row in range(new_slice.row_start, new_slice.row_end + 1):
            for col in range(new_slice.col_start, new_slice.col_end + 1):
                print(self.Pizza.pizza)
                self.Pizza.pizza[row, col] = np.nan
        return new_slice

    def CheckSlice(self, new_slice):
        response, dico_bool = self.Checkconstraint(new_slice)
        if response:
            self.AddSlicetoPlate(new_slice)
        else:
            del new_slice

    def MakeSlices(self):
        pizza = self.Pizza.pizza

        for i in range(1,self.max_cells+1):
            for row in range(self.Pizza.width):
                for col in range(self.Pizza.height):
                    row_start = row - i
                    col_start = col - i
                    row_end = row + i
                    col_end = col + i
                    if col_end > self.Pizza.width:
                        col_end = self.Pizza.width - 1
                    if row_end >  self.Pizza.height:
                        row_end = self.Pizza.height - 1
                    if row_start < 0:
                        row_start = 0
                    if row_end < 0:
                        row_end = 0
                    slice_array = pizza[row_start:row_end,col_start:col_end]

                    if slice_array.shape[1] == 0:
                        continue
                    slice_tmp = Slice(row_start, col_start, row_end, col_end, slice_array)
                    response, dico_bool = self.Checkconstraint(slice_tmp)
                    if not response:
                        del slice_tmp
                    else:
                        slice = self.CuteSlice(row_start, col_start, row_end, col_end, slice_array)
                        self.CheckSlice(slice)
                        self.AddSlicetoPlate(slice)

        pass

    def ThinkAboutBest(self):
        unique, counts = np.unique(self.Pizza.pizza, return_counts=True)
        dico = dict(zip(unique, counts))
        key_min = min(dico.keys(), key=(lambda k: dico[k]))
        best=int(dico[key_min]/self.min_ings)
        print("The best cut may be: "+str(best)+" depending of: "+str(key_min))
        return best,key_min


def AmazingPizza():
    filename = 'files/input/small.in'
    pizza, height, width,min_ings, max_cells = read_input_file(filename)
    pizza = Pizza(pizza,height, width)
    print_matrix(pizza.pizza)
    pizzaiolo = Pizzaiolo(pizza, Plate(),min_ings, max_cells)
    pizzaiolo.MakeSlices()
    construct_output_file(pizzaiolo.Plate)
    print_matrix(pizzaiolo.Pizza.pizza)


if __name__ == '__main__':
    AmazingPizza()
