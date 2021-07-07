class Weapons:
  def __init__(self, base_dmg, cooldown, dmg_toHull, dmg_toArmor, dmg_toShields):
    self.base_dmg = base_dmg
    self.cooldown = cooldown
    self.dmg_toHull = dmg_toHull
    self.dmg_toArmor = dmg_toArmor
    self.dmg_toShields = dmg_toShields

class Railgun(Weapons):
  def __init__(self, ship):
    self.ship = ship
    self.base_dmg = 10
    self.cooldown = 1
    self.dmg_toHull = 1.0
    self.dmg_toArmor = 0.5
    self.dmg_toShields = 1.5
    self.cooldown_left = 0
  
  def get_damage(self):
    return 

class Laser(Weapons):
  def __init__(self, ship):
    self.ship = ship
    self.base_dmg = 60
    self.cooldown = 6
    self.dmg_toHull = 1.0
    self.dmg_toArmor = 1.5
    self.dmg_toShields = 0.5
    self.cooldown_left = 0
  
class Torpedo(Weapons): #Add Specials
  def __init__(self, ship):
    self.ship = ship
    self.base_dmg = 150
    self.cooldown = 20
    self.dmg_toHull = 1.0
    self.dmg_toArmor = 1.0
    self.dmg_toShields = 0
    self.cooldown_left = 0
    
    
    