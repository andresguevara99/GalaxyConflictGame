import random

def target_ship(target_fleet, ship=False, own_fleet=False):

  # add all ships that have not yet been destroyed to the target_list
  possible_targets = []
  for ship in target_fleet.ships:
    if ship.hull > 0:
      possible_targets.append(ship)

  if len(possible_targets) == 0: return False

  # select a random ship as target
  return random.choice(possible_targets)
