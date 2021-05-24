import os
import sys
from sumolib import checkBinary
import traci

NUM_CARS = 200
NUM_BUSES = 30

def create_vehicles(num_cars, num_buses):

    cars = []
    buses = []
    for i in range(num_cars):
        cars.append('car'+ str(i))

    for i in range(num_buses):
        buses.append('bus'+ str(i))

    return cars, buses

def run():

    step = 0

    
    cars, buses = create_vehicles(200, 30)

    for car in cars:
        traci.vehicle.add(car, 'trip_private', typeID='car')

    for bus in buses:
        traci.vehicle.add(bus, 'trip_public', typeID='bus')

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep(step=step)
        step += 1020



def simulation():

    res_private = traci.simulation.findRoute('start_private', 'end_private', 'car')
    traci.route.add('trip_private', res_private.edges)
    
    res_public = traci.simulation.findRoute('start_public', 'end_public', 'bus')
    traci.route.add('trip_public', res_public.edges)

    for day in range(365):
        print(f'\ndia {day}\n')
        run()
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


    if sys.argv[2:]:
        num_cars = sys.argv[2]

    if sys.argv[3:]:
        num_buses = sys.argv[3]

    traci.start([binary, '-c', sys.argv[1], '--tripinfo-output', 'tripinfo.xml'])
    simulation()



if __name__ == '__main__':
    main()
