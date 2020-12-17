# Draw 2D FloorPlan
# Mohammed Al-Saeedi

import sys
import json
import random
import numpy as np
import matplotlib.colors as cl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from tkinter import *
from tkinter import filedialog, ttk
from ConvertTools import ConvertTools
from GeneralTools import GeneralTools

SELECTED_COLOUR = "white"
    
class Cell():
    def __init__(self, master, x, y, size, bg_colour = "white", border_colour = "black"):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.x = x
        self.y = y
        self.size= size
        self.bg_colour = bg_colour
        self.border_colour = border_colour
        self.fill= False

    def _switch(self):
        """ Switch if the cell is filled or not. """
        self.fill= not self.fill

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = self.bg_colour
            outline = self.border_colour

            if not self.fill:
                fill = "white"
                outline = "black"

            xmin = self.x * self.size
            xmax = xmin + self.size
            ymin = self.y * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)
            
    def drawSelectedColor(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = self.bg_colour
            outline = self.border_colour

            if not self.fill:
                fill = "white"
                outline = "black"

            xmin = self.x * self.size
            xmax = xmin + self.size
            ymin = self.y * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline, width=5)
            
class ControlPalette(Canvas):
    UNFILLED = '#fff'
    def __init__(self, root, master, x, y, cellSize, p_pad = 5):
        Canvas.__init__(self, master, width = x*cellSize , height = y)  
        self.root = root
        # Generate random number
        self.randomGen = GeneralTools.RandomNumber(self.root.config["model"]["counter"]["seed"],
                                                   self.root.config["model"]["counter"]["minimum"],
                                                   self.root.config["model"]["counter"]["maximum"])
        # Load and save image buttons
        b_load = Button(self, text='open', command=self.load_grid)
        b_load.pack(side=LEFT, padx=p_pad, pady=p_pad)
        b_save = Button(self, text='save', command=self.save_grid)
        b_save.pack(side=LEFT, padx=p_pad, pady=p_pad)
        # Add a button to clear the grid
        b_clear = Button(self, text='clear', command=self.clear_grid)
        b_clear.pack(side=LEFT, padx=p_pad, pady=p_pad)
        # Add a button to preview in 3d
        b_clear = Button(self, text='view 3D', command=self.view_model)
        b_clear.pack(side=LEFT, padx=p_pad, pady=p_pad)
        # Add a button to create a 2d or 3d CO2 scenario
        b_clear = Button(self, text='create model', command=self.create_model)
        b_clear.pack(side=LEFT, padx=p_pad, pady=p_pad)
    
    def cuboid_data(self, o, size=(1,1,1)):
        X = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
            [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
            [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
            [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
            [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
            [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
        X = np.array(X).astype(float)
        for i in range(3):
            X[:,:,i] *= size[i]
        X += np.array(o)
        return X

    def plotCubeAt(self, positions,sizes=None,colors=None, **kwargs):
        if not isinstance(colors,(list,np.ndarray)): colors=["C0"]*len(positions)
        if not isinstance(sizes,(list,np.ndarray)): sizes=[(1,1,1)]*len(positions)
        g = []
        for p,s,c in zip(positions,sizes,colors):
            g.append( self.cuboid_data(p, size=s) )
        return Poly3DCollection(np.concatenate(g),  
                                facecolors=np.repeat(colors,6, axis=0), **kwargs)
        
    def view_model(self):
        """View the grid in 3d"""
        # Model dimentions
        x_coord = len(self.root.cellGrid.grid)
        y_coord = len(self.root.cellGrid.grid[0])
        z_coord = self.root.config["model"]["dimentions"]["height"]        
        # Return if 2d
        if(z_coord < 2):
            return
        # Plot the result in 3D view
        cells = self.extractCells() # Extract cells from the grid
        matrix = np.zeros((x_coord,y_coord,z_coord)) # define a 3d matrix
        colours = []
        for cell in cells:
            if(not (cell["state"]["type"] == -100)): 
                x = cell["cell_id"][0]
                y = cell["cell_id"][1]
                if (z_coord > 1): # if 3d add z cell
                    if(cell["cell_id"][2] != z_coord-1): #(condition to hide ceiling)                      
                        z = cell["cell_id"][2]
                    else:
                        continue
                else:
                    z = 0 
                matrix[x, y, z] = 1
                for key, clr in self.root.config["model"]["colours"].items():
                    if(cell["state"]["type"] == clr["type"]):
                            colours.append(cl.to_rgba(key, alpha=clr["alpha"]/100))
        # Plot the matrix as 3d
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_aspect('auto')
        
        x,y,z = np.indices((x_coord,y_coord,z_coord))
        positions = np.c_[x[matrix==1],y[matrix==1],z[matrix==1]]
        pc = self.plotCubeAt(positions, colors=colours,edgecolor="black")
        ax.add_collection3d(pc)
        
        ax.set_xlim([0,x_coord])
        ax.set_ylim([0,y_coord])
        ax.set_zlim([0,max(x_coord,y_coord)])

        plt.show()

        
    def create_model(self):
        """Convert the grid into a 2d or 3d json scenario"""
        # Generate the head of the model
        head = ConvertTools.createHead(len(self.root.cellGrid.grid), len(self.root.cellGrid.grid[0]), self.root.config["model"])
        cells = self.extractCells()
        model = ConvertTools.createStructure(head, cells)  # Combine the head and the cells        
        # Export the JSON string
        if(self.root.config["model"]["dimentions"]["height"] > 1): # Check if 2d
            GeneralTools.export("outputScenario/3d_scenario.json", ConvertTools.getString(model))
        else:
            GeneralTools.export("outputScenario/2d_scenario.json", ConvertTools.getString(model))
        
    def extractCells(self):
        """Extract cells from the 2d grid"""        
        z_coord = self.root.config["model"]["dimentions"]["height"]
        # Extract the cells
        cells = self.makeCells(self.root.cellGrid.grid, self.root.config["model"]["colours"])
        # If the model is 3D, extend the walls and add a floor and ceiling
        if (z_coord > 1):
            cells = ConvertTools.getExtendedCells(self.root.config["model"], cells)
            # Add floor & ceiling
            for cell in cells:
                if ((cell["cell_id"][2] == 0 and cell["state"]["type"] == -100) or (cell["cell_id"][2] == z_coord - 1 and cell["state"]["type"] == -100)):                    
                    cells.append(GeneralTools.makeCell([cell["cell_id"][0], cell["cell_id"][1], cell["cell_id"][2]], 0, -300, -1))  # floor & Ceiling        
                    
        return sorted(cells, key=lambda item: item["cell_id"]) # return sorted cells to render cell's colors properly
            
    # Function: makeCells
    # Purpose: turn the Canvas Grid into cells
    def makeCells (self, grid, colours):
        maxStep = len(grid) * len(grid[0])
        cells = []
        cellType = {}
        for row in grid:
            for cell in row:
                cellType = colours[cell.bg_colour]
                if not cellType:
                    cellType = colours["white"] # Empty cells considered as Air
                counter = cellType["counter"]
                if (cellType["type"] == -700):  # If the current cell is a WORKSTATION
                    counter = self.randomGen.getInt()
                cells.append(GeneralTools.makeCell(
                    [cell.y, cell.x],
                    cellType["concentration"],
                    cellType["type"],
                    counter))
        return cells
    
    def clear_grid(self):
        """Reset the grid to the background "UNFILLED" colour."""
        grid = self.root.cellGrid.grid
        for row in grid:
            for cell in row:
                cell.bg_colour = "white"
                cell.border_colour = "black"
                cell.draw()
                
    def load_grid(self):
        # Open the file and read the saved grid
        data = ""
        try:
        # Load configuration from file
            self.filename = filedialog.askopenfilename(filetypes=(
                ('JSON files', '.json'),
                ('All files', '*.*')))
            if not self.filename:
                return
            print('Loading file from', self.filename)
            with open(self.filename, "r") as f:
                data = f.read()
        except FileNotFoundError:
            print(f"ERROR: Could not load input file {self.filename}")
            sys.exit(1)

        data = json.loads(data)  # Convert JSON string into dictionary    

        drawing = []
        # Reconfigure the grid canvas 
        # Work only if the config dimentions (width, length) are equal to the saved grid
        self.root.selectedColour = 0
        self.root.cellGrid.config(width = self.root.width*self.root.cellSize, height = self.root.height*self.root.cellSize)
        # self.root.cellGrid = CellGrid(self.root, self.root.frame, self.root.width*self.root.cellSize, self.root.height*self.root.cellSize, self.root.cellSize)
        for row in range(0, self.root.height):
            line = []
            for column in range(0, self.root.width):
                cl = Cell(self.root.cellGrid, data[str(row)+'-'+str(column)][0], data[str(row)+'-'+str(column)][1], data[str(row)+'-'+str(column)][2], data[str(row)+'-'+str(column)][3], data[str(row)+'-'+str(column)][4])
                cl._switch()
                cl.draw()
                cl._switch()
                line.append(cl)
            self.root.cellGrid.grid[row] = line
        #TODO update the code to open a saved grid with different size (x,y) than config file   
         
    def save_grid(self):        
        """Load an image from a provided file."""
        drawing = {}
        grid = self.root.cellGrid.grid
        # add the size of the grid and the cell size
        drawing["dimentions"] = [self.root.width, self.root.height]
        drawing["cell_size"] = self.root.cellSize
        for row in grid:
            for cell in row:
                drawing[str(cell.y)+'-'+str(cell.x)]= [cell.x, cell.y, cell.size, cell.bg_colour, cell.border_colour]
        with open('savedGrid/saved.json', 'w') as fp:
            json.dump(drawing, fp)
    
class CellTypePalette(Canvas):
    def __init__(self, root, master, cellTypes, x, y, cellSize, p_pad = 5):
        Canvas.__init__(self, master, width = x*cellSize , height = y) 
        self.cellSize = y
        self.ncolours = []
        self.grid = []
        i = 0
        for key, item in cellTypes.items(): 
            self.ncolours.append(key)
            self.grid.append(Cell(self, i, 0, self.cellSize, key))
            i += 1
        
        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)  
    
        self.draw()

    def draw(self):
        for cell in self.grid:
            cell._switch()
            cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[column]
        for cl in self.grid: # Reset
            cl.draw()
        cell.drawSelectedColor() # Draw selected color cell
        global SELECTED_COLOUR 
        SELECTED_COLOUR = cell.bg_colour # Assign selected color
    
        
class CellGrid(Canvas):
    def __init__(self, root, master, x, y, cellSize):
        Canvas.__init__(self, master, width = cellSize * x , height = cellSize * y)        
        self.cellSize = cellSize
        self.grid = []
        for row in range(y):
            line = []
            for column in range(x):
                line.append(Cell(self, column, row, cellSize))
        
            self.grid.append(line) 
        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)  
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()
        

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell.bg_colour = SELECTED_COLOUR
        cell.border_colour = SELECTED_COLOUR
        cell._switch()
        cell.draw()
        #add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell.bg_colour = SELECTED_COLOUR
            cell.border_colour = SELECTED_COLOUR
            cell._switch()
            cell.draw()
            self.switched.append(cell)
    
class GridApp:
    def __init__(self,master, config, pad=5):
        self.config = config # model configuration
        self.width, self.height = config['model']['dimentions']['width'], config['model']['dimentions']['length'] # Grid (model) x,y dimentions
        self.cellSize = max([int(600/self.height), int(600/self.width)], key=lambda x:abs(600)) # fit the cell size to the frame size
        self.cellTypes = config['model']['colours'] # get configured cell types by colour          
        self.selectedColour = 0 # selectedColour is the index of the currently selected colour.
         # The main frame 
        self.frame = Frame(master)
        self.frame.pack()

        # Add the Control Palette    
        self.paletteControl = ControlPalette(self, self.frame, self.width, 40, self.cellSize)
        self.paletteControl.pack()
                
        # Add the Cell Types Palette    
        self.paletteCellTypes= CellTypePalette(self, self.frame, self.cellTypes, self.width, 40, self.cellSize)
        self.paletteCellTypes.pack()
        
        # Add the grid canves
        self.cellGrid = CellGrid(self, self.frame, self.width, self.height, self.cellSize)
        self.cellGrid.pack()
            

    # Function: start
    # Purpose: entry point of GridDraw object
    # Arguments:
    #     args: arguments given by the argparse module
    # Return:
    #     none
    @staticmethod
    def start (args):
        configFile = args.config

        config = ""
        try:
            # Load configuration from file
            with open(configFile, "r") as f:
                config = f.read()
        except FileNotFoundError:
            print("ERROR: Could not load configuation file")
            sys.exit(1)

        # Prepare command line arguments for later use
        debug = args.prog_msg
        imgMsg = args.img_msg
        critMsg = not args.no_crit_msg

        config = json.loads(config)  # Convert JSON string into dictionary
        
        app = Tk()
        
        frame = GridApp(app, config)

        app.mainloop()
