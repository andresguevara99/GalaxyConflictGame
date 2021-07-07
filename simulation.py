import curses
import random
from time import sleep
from bpriorityq import BPriorityQueue as PriorityQueue #--> you will need this for the pqueue!
from ships import Battleship, Cruiser, Destroyer, Fighter
from weapons import Torpedo, Railgun, Laser
from computers.random import target_ship

class Simulation:
  def __init__(self, attacker, defender, gui=True):

    self.round = 0
    self.speed = 0.5

    # initialize opponents
    self.attacker = attacker
    self.defender = defender

    if(gui):
      self.screen = curses.wrapper(self.gui)
      self.exit()

    else:
      # Combat without gui
      print("Starting Battle: {0} VS {1}".format(attacker.name, defender.name))

      # Combat continues for as long as both players have ships and we have not passed round 1000
      # the last condition is to prevent stalemates where no players can hit each other.
      while self.attacker.cost > 0 and self.defender.cost > 0 and self.round < 1000:
        self.combat_round()
        self.round += 1

      self.exit()

  def combat_round(self):
    '''
    Conducts a single combat round and updates both fleets with the damage they took

    Schedule all remaining ships to fire their weapons on random (for now) targets.
    After weapons have a target, ships will fire in order of their size: Fighter (0) -> Destroyer (1) -> Cruiser (2) -> Battleship (3)
    Use a bounded priority queue to add weapons to their appropriate priority queue

    After scheduling ships of the same type should fire simulataniously. Thus all Fighters will
    apply damage first. Now all Destroyer weapons will fire, as long as the ships they are mounted on are still alive. Then the same cycle repeats for Cruisers and Battleships.
    '''
    '''Attackers load weapons'''
    battleQueue = PriorityQueue()
    fighers = []
    destroyers = []
    cruisers = []
    battleships = []
    for ship in attacker:
      if(ship.hull>0):
        ship.target = target_ship(defender, ship, attacker)
      for w in ship.weapons:
        if self.round % w.cooldown == 0:
          if ship.priority == 0:
            fighters.append(w)
          if ship.priority == 1:
            destroyers.append(w)
          if ship.priority == 3:
            cruisers.append(w)
          if ship.priority == 0:
            battleship.append(w)
    battleQueue.enqueue(fighters, 0)
    battleQueue.enqueue(destroyers, 1)
    battleQueue.enqueue(cruisers, 2)
    battleQueue.enqueue(battleships, 3)
    '''Defenders load weapons'''
    for ship in defender:
      if(ship.hull>0):
        ship.target = target_ship(attacker, ship, defender)
      for w in ship.weapons:
        if w.cooldown_left > 0:
          w.cooldown_left -=1
        else:
          battleQueue.enqueue(w, ship.priority) 
          w.cooldown_left = w.cooldown
    


  def damage(self, weapon, target):
    '''
    Resolves a weapon applying damage to a specific target.

    If a hit would deduct more damage than the remaining shields the remaining damage of that specific shot is voided. E.g. A ship has 100 shields left. Your weapon made 150 damage. Instead of disabling the shields and doing 50 damage to the armor of the target it will only disable the shield. The next weapon hit will damage armor. Also make sure hull, armor and shields only go down to 0, not become negative values.
    '''

    ''' Torpedo '''
    if isinstance(weapon, Torpedo()):
      if random.random() > target.point_defense:
        if target.armor > 0:
          target.armor -= (150 * weapon.ship.dmg_multiplier)
          if target.armor < 0:
            target.armor = 0 
        else:
            target.hull -= (150 * weapon.ship.dmg_multiplier)
            if target.hull < 0:
              target.hull = 0 
    
    ''' Laser '''
    if isinstance(weapon, Laser()):
      if random.random() > target.evasion:
        if target.shield > 0:
          target.shield -= (60 * weapon.ship.dmg_multiplier * 0.5)
          if target.shield < 0 :
            target.shield = 0
        elif target.armor() > 0:
          target.armor -= (60 * weapon.ship.dmg_multiplier * 1.5)
          if target.armor < 0:
            target.armor = 0
        elif target.hull() > 0:
          target.hull -= (60 * weapon.ship.dmg_multiplier)
          if target.hull < 0:
            target.armor = 0
          

    ''' Railgun '''
    if isinstance(weapon, Railgun()):
      if random.random() > target.evasion:
        if target.shield > 0:
          target.shield -= (10 * weapon.ship.dmg_multiplier * 1.5)
          if target.shield < 0:
            target.shield = 0 
        elif target.armor > 0:
          target.armor -= (10 * weapon.ship.dmg_multiplier * 0.5)
          if target.armor < 0:
            target.armor = 0
        elif target.hull > 0:
          target.hull -= (10 * weapon.ship.dmg_multiplier)
          if target.hull < 0:
            target.hull = 0

  def info_box(self, win):
    '''
    TODO: Info area
    Here is where you want to display information such as how many ships each side has left. you are free to use the remaining space as you like but do not increase the size of the info area. The goal is to populate this limited space with as much (useful) information as possible
    '''
    win.addstr(23, 1, "this info area is waiting to be filled by you...".center(100))
    

  def gui(self, screen):

    # Clear screen
    screen.clear()
    screen.nodelay(True)

    # Ships that still have full shields is displayed in green
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # Ships that still have shields is displayed in blue
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    # Ships that still have armor are yellow
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    # Ships that still have hull are red
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    # Ships that are destroyed are invisible
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)

    pause = True
    key = -1

    screen.addstr(0, 1, "KEYS: (SPACE) to pause / resume | (Arrow Right) faster combat | (ESC) exit combat".center(100))

    # create a box with a nice border
    win = curses.newwin(27, 102, 2, 0)
    win.border()

    # Header and non-updating stuff
    win.addstr(1, 1, "{:^100}".format("COMBAT SIMULATOR"))
    win.addstr(2, 1, "{:<49}VS{:>49}".format(self.attacker.name, self.defender.name))
    win.addstr(3, 1, "{:<50}{:>50}".format("Attacker", "Defender"))
    win.addstr(4, 1, "_" * 100)
    win.addstr(19, 1, "_" * 100)

    while True:
      key = screen.getch()

      # allow to exit the simulation by pressing ESC key
      if key == 27: break

      # Combat continues for as long as both players have ships and we have not passed round 1000
      # the last condition is to prevent stalemates where no players can hit each other.
      if not pause:
        self.combat_round()
        self.round += 1

        # someone won or timeout --> pause and prevent from unpausing.
        if (self.attacker.cost == 0 or self.defender.cost == 0 or self.round > 1000):

          if self.attacker.cost > 0 and self.defender.cost == 0:
            win.addstr(3, 10, "!WINNER!", curses.color_pair(5))
            win.addstr(3, 84, "!LOOSER!", curses.color_pair(2))

          if self.defender.cost > 0 and self.attacker.cost == 0:
            win.addstr(3, 84, "!WINNER!", curses.color_pair(5))
            win.addstr(3, 10, "!LOOSER!", curses.color_pair(2))

          pause = True

      self.draw(win)
      win.refresh()

      # allow to pause / resume the simulation by pressing SPACE, also resets speed
      if key == 32:
        pause = not pause
        self.speed = 0.5

      # allows to make the combat faster with arrow right key
      if key == 261: self.speed = max(0.1, self.speed - 0.1)

      sleep(self.speed)

    self.exit()

  def draw(self, win):
    '''This will draw a beautiful combat interface onto our screen'''

    win.addstr(3, 47, "Round {0}".format(self.round).center(9))

    # Ship Display area
    a_b = 0; a_c = 0; a_d = 0; a_f = 0; d_b = 0; d_c = 0; d_d = 0; d_f = 0
    row = 6

    for ship in self.attacker.ships:
      if (isinstance(ship, Battleship)):
        win.addstr(row + a_b, 3, "[##]", self.get_color(ship))
        a_b += 1

      if (isinstance(ship, Cruiser)):
        win.addstr(row + a_c % 13, 9 + a_c // 13 * 4, "<=>", self.get_color(ship))
        a_c += 1

      if (isinstance(ship, Destroyer)):
        win.addstr(row + a_d % 13, 18 + a_d // 13 * 3, "<>", self.get_color(ship))
        a_d += 1

      if (isinstance(ship, Fighter)):
        win.addstr(row + a_f % 13, 31 + a_f // 13 * 2, ">", self.get_color(ship))
        a_f += 1

    for ship in self.defender.ships:
      if (isinstance(ship, Battleship)):
        win.addstr(row + d_b, 94, "[##]", self.get_color(ship))
        d_b += 1

      if (isinstance(ship, Cruiser)):
        win.addstr(row + d_c % 13, 85 + d_c // 13 * 4, "<=>", self.get_color(ship))
        d_c += 1

      if (isinstance(ship, Destroyer)):
        win.addstr(row + d_d % 13, 72 + d_d // 13 * 3, "<>", self.get_color(ship))
        d_d += 1

      if (isinstance(ship, Fighter)):
        win.addstr(row + d_f % 13, 55 + d_f // 13 * 2, "<", self.get_color(ship))
        d_f += 1

    self.info_box(win)


  def exit(self):
    # if a stalemate occured, set score of both players to 0
    if self.attacker.cost > 0 and self.defender.cost > 0:
      print("Simulation ended with a stalemate. Fleet stats at the end of the battle:")
    else:
      winner = self.attacker.name if self.attacker.cost > self.defender.cost else self.defender.name
      print("Simulation ended. {:} won. Fleet stats at the end of the battle:".format(winner))

    print(self.attacker)
    print(self.defender)

  def get_color(self, ship):
    if ship.hull == 0: return curses.color_pair(1)
    if ship.armor == 0: return curses.color_pair(2)
    if ship.shields == 0: return curses.color_pair(3)
    if ship.shields < ship.max_shields: return curses.color_pair(4)
    return curses.color_pair(5)



