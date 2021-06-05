import os
import sys
from sumolib import checkBinary
import traci

from person import Person



class MssiVehicle:

    def __init__(self, name, start_time):
        self.name = name
        self.start_time = start_time
        self.end_time = None
        self.emissions = 0

    def set_end_time(self, end_time):
        self.end_time = end_time

    def update_emissions(self, emissions):
        self.emissions += emissions

    def __repr__(self):
        return str(self)

    @property
    def finished(self):
        return self.end_time != None

    def __str__(self):
        return f'Name:{self.name} Emission:{self.emissions} Start:{self.start_time} End:{self.end_time}'


BUS_CAPACITY = 30

def create_vehicles(num_cars, num_buses):

    cars = []
    buses = []
    for i in range(num_cars):
        cars.append('car'+ str(i))

    for i in range(num_buses):
        buses.append('bus'+ str(i))

    return cars, buses

def run(people):

    step = 0

    

    vehicles = dict()
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep(step=step)

        departed = traci.simulation.getDepartedIDList()
        current_time = traci.simulation.getCurrentTime()


        for vehicle in departed:
            vehicles[vehicle] = MssiVehicle(vehicle, current_time)

        arrived = traci.simulation.getArrivedIDList()
        for vehicle in arrived:
            vehicles[vehicle].set_end_time(current_time)

        for _, mssi_vehicle in vehicles.items():
            if mssi_vehicle.finished:
                continue
            mssi_vehicle.update_emissions(traci.vehicle.getCO2Emission(mssi_vehicle.name))



        step += 1

    
    num_bus = sum(map(lambda x: 1 if x.startswith('bus') else 0, arrived))

    print(f'number bus:{num_bus} car:{len(arrived)-num_bus}')
    print(vehicles)



def simulation():

    res_private = traci.simulation.findRoute('start_private', 'end_private', 'car')
    traci.route.add('trip_private', res_private.edges)
    
    res_public = traci.simulation.findRoute('start_public', 'end_public', 'bus')
    traci.route.add('trip_public', res_public.edges)

    people = [Person(f'person_{i}') for i in range(1000)]

    for day in range(15):


        private = 0
        public = 0
        for person in people:

            action = person.choose_action()
            if action == 0:
                traci.vehicle.add(f'car_{private}', 'trip_private', typeID='car')
                private += 1
            else:
                public += 1

                if public % BUS_CAPACITY == 0:
                    traci.vehicle.add(f'bus_{(public//30)-1}', 'trip_public', typeID='bus')

        if public % BUS_CAPACITY:
            traci.vehicle.add(f'bus_{public//30}', 'trip_public', typeID='bus')



        print(f'\ndia {day}\n')
        print(f'spawnados bus:{public//30 + (1 if public%30 else 0)} car:{private}')
        run(people)
    traci.close()


def main():
     if 'SUMO_HOME' in os.environ:
         tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
         sys.path.append(tools)
     else:
         print('oh mano nao sejas burro')
         return


     # TODO: Not the best solution
     if len(sys.argv) != 2  and len(sys.argv) != 4:
         print('need a config oh mano')
         return

     binary = checkBinary('sumo-gui')


     traci.start([binary, '-c', sys.argv[1], '--tripinfo-output', 'tripinfo.xml'])
     simulation()


    
if __name__ == '__main__':
    main()
