from colorama import Fore
from command.command import Command
from traefik.traefikConfig import TraefikConfig
from utils.dockerUtils import restartTraefik

class RemoveCommand(Command):
  def __init__(self):
    super().__init__("remove-sub-path", "Remove sub path from a domain", "remove-sub-path <name> <path>")

  def execute(self, traefikConfig: TraefikConfig, args):
    if len(args) < 0:
      self.printUsage()
      return
    
    name = args[0]

    if not traefikConfig.hasRouter(name):
      print(f"Router \"{name}\" does not exist")
      return
    
    print(f"Removing \"{name}\"")
    
    traefikConfig.removeRouter(name)

    traefikConfig.save()

    restartTraefik()