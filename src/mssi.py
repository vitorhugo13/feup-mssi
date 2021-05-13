import os
import sys
from sumolib import checkBinary
import traci



def run():

    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print(step)

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
