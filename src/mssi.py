import os
import sys
from sumolib import checkBinary
import traci



def run():

    step = 0


    res_private = traci.simulation.findRoute('start_private', 'end_private', 'routeByDistance')
    traci.route.add('trip_private', res_private.edges)
    res_public = traci.simulation.findRoute('start_public', 'end_public', 'routeByDistance')
    traci.route.add('trip_public', res_public.edges)
    traci.vehicle.add('new_veh1', 'trip_private')
    traci.vehicle.add('new_veh2', 'trip_public')

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print(step)
        print(f'Carros a correr {traci.simulation.getMinExpectedNumber()}')
        accels = map(lambda x: traci.vehicle.getAcceleration(x) ,traci.vehicle.getIDList())
        accels = list(accels)
        types = map(lambda x: traci.vehicle.getTypeID(x) ,traci.vehicle.getIDList())
        types = list(types)
        print(f'{accels}')
        print(f'{types}')
        step += 1

    traci.close()


def main():
    print('pila???')
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        print('oh mano nao sejas burro')
        return

    if len(sys.argv) < 2:
        print('need a config oh mano')
        return

    binary = checkBinary('sumo-gui')



    traci.start([binary, '-c', sys.argv[1], '--tripinfo-output', 'tripinfo.xml'])
    run()



if __name__ == '__main__':
    main()
