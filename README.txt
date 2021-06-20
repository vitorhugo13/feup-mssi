PREREQUISITIES

- Install SUMO
- Install Python3

--------------------------------------------------
HOW TO RUN

- In the /src folder execute the following command:
`python3 mssi.py network_file output_file`

	where:
		- network file: file that contains the network needed to run the simulation. At this moment it is possible to import a network of 5,10 or 20 km. To do this, just introduce the 			directory of the network you want to open (ex: replace network_file by ../networks/5km-network/5km.sumo.cfg)
		- output file: csv file where the data collected during the simulation will be saved (ex: output.csv)

- There are two ways to run the simulation, with or without graphical interface. By default the simulation will run without GUI in order to allow faster analysis, however, if you want to see graphically how the simulation goes, just change binary = checkBinary('sumo') to binary = checkBinary('sumo-gui') 

--------------------------------------------------
HOW TO VARY INPUT VARIABLES

At the moment it is only possible to vary the input variables of the system directly in the source code.
To test the various scenarios presented, the following values must be changed: 

- Road's length: change between the various sumo.cfg files as mentioned above.
- Fuel's price:  FUEL_COST = 1.5/10 -> to vary the fuel price, just change the numerator of the FUEL_COST fraction 
- Ticket price:  to vary the ticket price, just change the last argument in the call to public_objective function-> public_objective(max(0, random.gauss(mean_wait_time, sigma)*60), mssi_vehicle.travel_time, mssi_vehicle.emissions, 2) 
- Waiting time:  to vary the average time that a commuter waits for the bus, just modify the value of mean_wait_time (in minutes) -> mean_wait_time=5
- CO2 Emissions: to vary the weight of CO2 emissions in the calculation of utility, just change the value by which the variable p is multiplied (by default 1/2) -> return 2*t + p/2 + c/3

--------------------------------------------------
We also sent with the code the csv files used to build the plots that are in our paper. They can be found in the folder /results.
