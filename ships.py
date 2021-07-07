from exception import *
from weapons import *
class Ships:
  def __init__(self, cost, num_weapons, num_defenses, multistat, evasion, dmg_multiplier, accuracy, modules):
    self.multistat = multistat
    self.shield = multistat
    self.armor = multistat
    self.hull = multistat
    self.point_defense = 0
    self.cost = cost
    self.num_weapons = num_weapons
    self.num_defenses = num_defenses
    self.evasion = evasion
    self.dmg_multiplier = dmg_multiplier
    self.accuracy = accuracy
    self.modules = modules
    self.target = None

    self.weapons = []
    self.defenses = []
    if len(modules) > (self.num_weapons + self.num_defenses):
      raise InvalidModuleException("This ship is overencumbered! There are too many modules!")
    else:
      pass
      
    w = modules[:num_weapons]
    d = modules[num_weapons:]
    for i in w:
      if i == "L":
        self.weapons.append(Laser(self))
      elif i == "R":
        self.weapons.append(Railgun(self))
      elif i == "T":
        self.weapons.append(Torpedo(self))
      else:
        raise InvalidModuleException("Your Ship has an unknown piece of Alien weaponry on one of its modules!")
        pass
    num_ion_thrusters = 0
    for i in d:
      if i == "S":
        self.shield += (.5 * self.multistat)
      elif i == "A":
        self.armor += (.5 * self.multistat)
      elif i == "E":
        num_ion_thrusters += 1
        if num_ion_thrusters != 1 or 0:
          raise InvalidModuleException("Your ship has more than one ion thruster!")
        else:
          self.evasion = self.evasion*2
      elif i == "P":
        self.point_defense += .3333333333333333333333333
      else:
        raise InvalidModuleException("Your ship has an unknown piece of Alien defenses on one of its modules!")
        pass
    self.init_shield = self.shield
    self.init_hull = self.hull
    self.init_armor= self.armor

  def get_multistat(self):
    return(self.multistat)

  def get_cost(self):
    return(self.cost)

  def get_weapon_slots(self):
    return(self.weapon_slots)
    
  def get_defense_slots(self):
    return(self.defense_slots)
    
  def get_evasion(self):
    return(self.evasion)
    
  def get_dmg_multiplier(self):
    return(self.dmg_multiplier)
    
  def accuracy(self):
    return(self.accuray)
    
  def get_dps(self):
    cdr = 0
    for i in self.weapons:
      cdr += (i.base_dmg/i.cooldown) * self.dmg_multiplier
    return cdr
        

    
class Fighter(Ships):
  cost = 1
  weapon_slots = 1
  defense_slots = 0
  multistat = 100
  evasion = 0.9 #90 %
  dmg_multiplier = 1 #100 %
  accuracy = 1 #100 %
  def __init__(self, string):
    super().__init__(1, 1, 2, 100, .9, 1, 1, string)
    self.priority = 0

  def __str__(self):
    s = "Fighter "
    s+=" Modules: " + self.modules + " Defenses: ["
    s+= 'H: ' + str(self.hull) + ' S: ' +  str(self.shield) + ' A: ' + str(self.armor) + " PD:" + str(self.point_defense) + ' E: ' + str(self.evasion)
    s+= '] Weapons: ['
    for i in self.weapons:
      if isinstance(i,Railgun):
        s+='R@' + str(self.dmg_multiplier*10) + ', '
      if isinstance(i,Laser):
        s+='L@' + str(self.dmg_multiplier*10) + ', '
      if isinstance(i,Torpedo):
        s+='T@' + str(self.dmg_multiplier*(15/2)) + ', '
    s+= ']'
    return s
                




class Destroyer(Ships):
  cost = 2  
  weapon_slots = 2
  defense_slots = 1
  multistat = 300
  evasion = 0.35 #35 %
  dmg_multiplier = 1 #100 %
  accuracy = 1 #100 %
  def __init__(self, string):
    super().__init__(2, 2, 1, 300, 0.35, 1, 1, string)
    self.priority = 1
  
  def __str__(self):
    s = "Destroyer "
    s+=" Modules: " + self.modules + " Defenses: ["
    s+= 'H: ' + str(self.hull) + ' S: ' + str(self.shield) + ' A: ' + str(self.armor) + " PD: " + str(self.point_defense) + ' E: ' + str(self.evasion)
    s+= '] Weapons: ['
    for i in self.weapons:
      if isinstance(i,Railgun):
        s+='R@' + str(self.dmg_multiplier*10) + ', '
      if isinstance(i,Laser):
        s+='L@' + str(self.dmg_multiplier*10) + ', '
      if isinstance(i,Torpedo):
        s+='T@' + str(self.dmg_multiplier*(15/2)) + ', '
    s+= ']'
    return s



class Cruiser(Ships):
  cost = 4
  weapon_slots = 3
  defense_slots = 2
  multistat = 600
  evasion = 0.2 #20 %
  dmg_multiplier = 1.2 #120 %
  accuracy = 0.9 #90 %
  def __init__(self, string):
    super().__init__(4, 3, 2, 600, 0.2, 1.2, 0.9, string)
    self.priority = 2
  
  def __str__(self):
    s = "Cruiser "
    s+=" Modules: " + self.modules + " Defenses: ["
    s+= 'H: ' + str(self.hull) + ' S: ' + str(self.shield) + ' A: ' + str(self.armor) + " PD: " + str(self.point_defense) + ' E: ' + str(self.evasion)
    s+= '] Weapons: ['
    for i in self.weapons:
      if isinstance(i,Railgun):
        s+='R@' + str(self.dmg_multiplier*10) + ', '
      if isinstance(i,Laser):
        s+='L@' + str(self.dmg_multiplier*10) + ', '
      if isinstance(i,Torpedo):
        s+='T@' + str(self.dmg_multiplier*(15/2)) + ', '
    s+= ']'
    return s



class Battleship(Ships):
  cost = 8
  num_weapons = 4
  num_defenses = 3
  multistat = 1000
  evasion = 0.1 #10 %
  dmg_multiplier = 1.5 #150 %
  accuracy = .8 #80 %
  def __init__(self, string):
    super().__init__(8, 4, 3, 1000, .1, 1.5, .8, string)
    self.priority = 3
  
  def __str__(self):
    s = "Battleship "
    s+=" Modules: " + self.modules + " Defenses: ["
    s+= 'H: ' + str(self.hull) + ' S: ' + str(self.shield) + ' A: ' + str(self.armor) + " PD: " + str(self.point_defense) + ' E: ' + str(self.evasion)
    s+= '] Weapons: ['
    for i in self.weapons:
      if isinstance(i,Railgun):
        s+='R@' + str(self.dmg_multiplier*10) + ', '
      if isinstance(i,Laser):
        s+='L@' + str(self.dmg_multiplier*10) + ', '
      if isinstance(i,Torpedo):
        s+='T@' + str(self.dmg_multiplier*(15/2)) + ', '
    s+= ']'
    return s


