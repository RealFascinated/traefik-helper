class Command:
  def __init__(self, name:str, description:str, usage:str):
      self.name = name
      self.description = description
      self.usage = usage

  async def execute(self, traefikConfig, args):
    pass

  def printUsage(self):
    print("Usage: %s" % self.usage)
    pass