# 2D_Drawing_to_CO2_Model
CLONE THE TOOL:####################################################################

$ git clone https://github.com/malsaeedi/2D_Drawing_to_CO2_CELL_DEVS_Model.git

TOOL DESCRIPTION:##################################################################

Is a tool to quickly draw a 2d floorplan and convert it to a 2d/3d JSON scenario model.

TOOL FUNCTIONALITIES:##############################################################

	1. Add a new cell type.
	2. UI to draw a 2d floorplan using the configured cell types colors.
	3. Preview the 2d drawing as 3d.
	4. Save and re-open the 2d drawing.
	5. Create a 2d/3d scenario for the CO2 model.

TOOL CONFIGURATIONS:###############################################################

The tool uses an input config json which consists of the following parts:

1. dimentions: configure the dimentions of the grid (less than 2 for 2d model)
  "dimentions" :{
            "width" : 20,
            "length" : 15,
            "height" : 12
       },
2. neighbourhood : configure the shape of neigbourhood cells 
	"neighbourhood" : "moore",
3. range
    "range" : 1,
4. wall_only
    "walls_only" : false,
5. colours : configure the type of cells using colours.
To define a new cell, you should first select a new colour and add the following JSON part under colours:

	"<colour_name>": {
		"name" : "<cell_name>",
		"parent_cell" : "<parent_cell_colour>",
		"alpha" : <transperancy>,
		"bottom" : <bottom>,
		"top" : <top>,
		"concentration" : <co2_concentration>,
		"type" : <cell_type>,
		"counter" : <counter>
    },

TOOL PREREQUESIT LIBRARIES:#############################################

1. python3
to check the installed python version
$ python3 --version
to install python3
$ sudo apt-get install python3
2. tkinter
$ sudo apt-get install python-tk
3. matplotlib
$ pip3 install matplotlib
4. numpy
$ pip3 install numpy

TO CREATE 2D/3D SCENARIO MODEL:############################################

1. Run the tool by entering the main app folder, opening a bash prompt and using the command python3 Convert.py followed by the path to the config json, e.g python3 Convert.py config/config.json 
2. The app UI will be initiated and the user can draw a 2d floorplan and preview in 3d and/or create the 2d/3d scenario model.
3. If press the save button, the floorplan will be saved into the saveGrid folder for later use.
4. If press the create model button, a 2d/3d scenario model will be generated and populated to the outputScenario folder to be used by a CADMIUM CO2-based model.

TO USE THE CREATED 2D/3D JSON SCENARIO:#################################

1. Copy the output JSON scenario to the config folder in the targeted Cell-DEVS-CO2_spread_computer_lab/<the model you want to run>  folder and execute this command:
2. If the output JSON scenario contains a new type of cell, add also the respected code to the co2 model in co2_lab_cell.hpp
	Example: Adding the DUCT cell (DUCT=-800) which already in the created JSON scenario
	update the following code in the model:

	enum CELL_TYPE {AIR=-100, CO2_SOURCE=-200, IMPERMEABLE_STRUCTURE=-300, DOOR=-400, WINDOW=-500, VENTILATION=-600, WORKSTATION=-700, DUCT=-800};

	then add the required code under co2 local_computation function:

	co2 local_computation() const override {
			.
			.
			.
            case DUCT:
            .
            .
            .
                break;
			.
			.
			.
		}

3. Compile using make/cmake:
			a) open the bash prompt in the Cell-DEVS-CO2_spread_computer_lab/<the model you want to run> folder and execute this command:
			$ cmake ./
			$ make
			or
			$ make all clean
			c) this will create the executable co2_lab in the bin folder
4. Once compiled all changes that are not in the hpp or cpp files do not require recompilation
5. Create a folder in the same directory as the executable, name it results
6. Run the simulation by entering the bin folder, opening a bash prompt and using the command ./co2_lab followed by the path to the json and an optional number of timesteps, e.g ./co2_lab ../config/test.json 
																						or ./co2_lab ../config/test.json 500
7. Use the simulation results (output_messages.txt) under the results folder and the style JSON file under the visualization folder to visualize the results using the following link: https://staubibr.github.io/arslab-prd/app-simple/index.html
8. If the newly created JSON scenario contains a new type of cell, make sure that you also add the visualization style to the JSON style file. 