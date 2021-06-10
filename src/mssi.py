import os
import sys
from sumolib import checkBinary
import traci
import random
import time

from person import Person


def objective(t, p, c):
    return 2*t + p/2 + c/3

def public_objective(waiting, travel, emission, ticketprice):
    t = 2*waiting + travel
    p = emission
    c = ticketprice
    return objective(t, p, c)

def private_objective(travel, emission, costs):
    t = travel
    p = emission
    c = costs
    return objective(t, p, c)


class MssiVehicle:

    def __init__(self, name, start_time):
        self.name = name
        self.start_time = start_time
        self.end_time = None
        self.emissions = 0
        self.fuel_consumption = 0

    def set_end_time(self, end_time):
        self.end_time = end_time

    def update_emissions(self, emissions):
        self.emissions += emissions

    def update_fuel_consumption(self, fuel_consumption):
        self.fuel_consumption += fuel_consumption

    def reset(self):
        self.emissions = 0
        self.fuel_consumption = 0

    def __repr__(self):
        return str(self)

    @property
    def travel_time(self):
        return self.end_time - self.start_time

    @property
    def finished(self):
        return self.end_time != None

    def __str__(self):
        return f'Name:{self.name} Emission:{self.emissions} Start:{self.start_time} End:{self.end_time}'




step = 0
def run():

    global step
    vehicles = dict()
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep(step=float(step))

        departed = traci.simulation.getDepartedIDList()
        current_time = traci.simulation.getTime()

        for vehicle in departed:
            vehicles[vehicle] = MssiVehicle(vehicle, current_time)

        arrived = traci.simulation.getArrivedIDList()
        for vehicle in arrived:
            vehicles[vehicle].set_end_time(current_time)

        for _, mssi_vehicle in vehicles.items():
            if mssi_vehicle.finished:
                continue
            mssi_vehicle.update_emissions(traci.vehicle.getCO2Emission(mssi_vehicle.name))
            mssi_vehicle.update_fuel_consumption(traci.vehicle.getFuelConsumption(mssi_vehicle.name))

        step += 1

    return vehicles



def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

BUS_CAPACITY = 30
FUEL_COST = 1.5/1000
def distribute(people):

    car = []
    bus = []


    for person in people:

        action = person.choose_action()

        if action == 0:
            car.append(person)
        else:
            bus.append(person)


    buses = [x for x in chunks(bus, BUS_CAPACITY)]

    return (car, buses)



def spit_out(fp, day, person, mssi_vehicle, utility):
    typ = 'car' if mssi_vehicle.name.startswith('car') else 'bus'
    fp.write(f'{day},{mssi_vehicle.name},{person.name},{typ},{mssi_vehicle.emissions},{mssi_vehicle.fuel_consumption},{mssi_vehicle.travel_time},{utility}\n')
    return


def simulation(file_name):



    fp = open(file_name, 'w')
    fp.write('day,vehicle_name,name,type,emissions,fuel_consumption,travel_time,utility\n')
    res_private = traci.simulation.findRoute('start_private', 'end_private', 'car')
    traci.route.add('trip_private', res_private.edges)
    
    res_public = traci.simulation.findRoute('start_public', 'end_public', 'bus')
    traci.route.add('trip_public', res_public.edges)

    people = [Person(f'person_{i}') for i in range(100)]

    for day in range(365):

        cars, buses = distribute(people)
        for index, person in enumerate(cars):
            name = f'car_{index}'
            traci.vehicle.add(name, 'trip_private', typeID='car')
            person.set_vehicle(name)

        for index, lst_person in enumerate(buses):
            name = f'bus_{index}'
            traci.vehicle.add(name, 'trip_public', typeID='bus')
            for person in lst_person:
                person.set_vehicle(name)

        print(f'\ndia {day}\n')
        print(f'spawnados bus:{len(buses)} car:{len(cars)}')
        vehicle_data = run()

        for person in people:

            mssi_vehicle = vehicle_data[person.vehicle]
            utility = 0
            if person.vehicle.startswith('car'):
                utility = private_objective(mssi_vehicle.travel_time, mssi_vehicle.emissions, FUEL_COST * mssi_vehicle.fuel_consumption)
            else:
                utility = public_objective(max(0, random.gauss(5, 2)*60), mssi_vehicle.travel_time, mssi_vehicle.emissions, 2)
            person.update_values(utility)
            spit_out(fp, day, person, mssi_vehicle, utility)


        for car in cars:
            car

    traci.close()
    fp.close()




def main():
     if 'SUMO_HOME' in os.environ:
         tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
         sys.path.append(tools)
     else:
         print('oh mano nao sejas burro')
         return


     # TODO: Not the best solution
     if len(sys.argv) != 3:
         print('need a config oh mano')
         return

     binary = checkBinary('sumo')


     traci.start([binary, '-c', sys.argv[1], '--tripinfo-output', 'tripinfo.xml'])


     simulation(sys.argv[2])


    
if __name__ == '__main__':
    main()
