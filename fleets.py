from exception import *
#contains class Fleet: that allows to construct a fleet based on a text input file
from ships import *

class Fleet:
  def __init__(self, fleetFile):
    file = open(fleetFile, 'r')
    #print(file.read().splitlines())
    lst = file.read().splitlines()
    ## Make the fleet
    self.ships = []

    '''Initial stats'''
    self.init_totalHull = 0
    self.init_totalArmor = 0
    self.init_totalShield = 0
    self.init_command_points = 0
    self.init_DPS = 0
    self.init_num_ships = 0

    ''' Current Stats'''
    self.totalHull = 0
    self.totalArmor = 0
    self.totalShield = 0
    self.command_points = 0
    self.DPS = 0
    self.num_ships = 0

    self.cost = 0

    count = 0
    for i in lst:
      
      if i[:1] == 'B':
        self.ships.append(Battleship(i[2:]))
        self.cost += 8
        self.init_totalHull += self.ships[-1].hull
        self.init_totalArmor += self.ships[-1].armor
        self.init_totalShield += self.ships[-1].shield
        self.init_command_points = self.cost
        self.init_DPS += self.ships[-1].get_dps()
        self.init_num_ships += 1

      elif i[:1] == 'C':
        self.ships.append(Cruiser(i[2:]))
        self.cost += 4
        self.init_totalHull += self.ships[-1].hull
        self.init_totalArmor += self.ships[-1].armor
        self.init_totalShield += self.ships[-1].shield
        self.init_command_points = self.cost
        self.init_DPS += self.ships[-1].get_dps()
        self.init_num_ships += 1
      elif i[:1] == 'D':
        self.ships.append(Destroyer(i[2:]))
        self.cost += 2
        self.init_totalHull += self.ships[-1].hull
        self.init_totalArmor += self.ships[-1].armor
        self.init_totalShield += self.ships[-1].shield
        self.init_command_points = self.cost
        self.init_DPS += self.ships[-1].get_dps()
        self.init_num_ships += 1
      elif i[:1] == 'F':
        self.ships.append(Fighter(i[2:]))
        self.cost += 1
        self.init_totalHull += self.ships[-1].hull
        self.init_totalArmor += self.ships[-1].armor
        self.init_totalShield += self.ships[-1].shield
        self.init_command_points = self.cost
        self.init_DPS += self.ships[-1].get_dps()
        self.init_num_ships += 1
      elif i[:1] == " " :
        pass

      else:
        if count>0:
          raise InvalidFleetException("Tried to create an invalid ship type")
      
      count += 1
      
        
        
      if self.cost > 100:
        raise InvalidFleetException("Your fleet is too expensive! Get rid of some ship(s)!")
    ''' Update stats from above'''
    self.update_stats()
            

    file.close()
  




  def __str__(self):
    self.update_stats()
    return ("Starfleet   Ships: " + str(self.num_ships) + "/" + str(len(self.ships))  + "   Command Points: " + str(self.command_points)+ "/" + str(self.init_command_points) + "   DPS: " + str(self.DPS) + "  ( " + str(float(self.DPS/self.init_DPS)*100) + "% Damage Output)   " + "Hull: " + str(self.totalHull) + "/" +  str(self.init_totalHull) + "   Shield: " + str(self.totalShield) + "/" +  str(self.init_totalShield) + "   Armor: " + str(self.totalArmor) + "/" +  str(self.init_totalArmor))

  def update_stats(self):
    self.totalHull = 0
    self.totalArmor = 0
    self.totalShield = 0
    self.command_points = 0
    self.DPS = 0
    self.num_ships = 0
    for i in self.ships:
      if(i.hull!=0):
        self.num_ships += 1
        self.command_points += i.get_cost()
        self.DPS += i.get_dps()
        self.totalShield += i.shield
        self.totalArmor += i.armor
        self.totalHull += i.hull

           


                

  def list_ships(self):
    for i in self.ships:
      print(str(i))