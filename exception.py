
class Error(Exception):
  "Base class for other exceptions"
  pass

class InvalidModuleException(Error):
  pass

class InvalidFleetException(Error):
  "Raised if input value is too high"
  pass
