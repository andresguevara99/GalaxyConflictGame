from fleets import Fleet
from simulation import Simulation

f = Fleet("fleets/fleet_1.txt")

attacker = Fleet("fleets/fleet_1.txt")
defender = Fleet("fleets/fleet_2.txt")

Simulation(attacker, defender, True)
