from command.command import Command
from traefik.traefikConfig import TraefikConfig
from utils.dockerUtils import restartTraefik

class AddCommand(Command):
  def __init__(self):
    super().__init__("add", "Add a domain", "add <name> <domain> <service host>")

  def execute(self, traefikConfig:TraefikConfig, args):
    if len(args) < 3:
      self.printUsage()
      return
    
    name = args[0]
    domain = args[1]
    serviceHost = args[2]

    if traefikConfig.hasRouter(name):
      print(f"Router \"{name}\" already exists")
      return
    
    # Validate if the service host is a valid URL
    if not serviceHost.startswith("http://") and not serviceHost.startswith("https://"):
      print(f"Service host \"{serviceHost}\" is not a valid URL")
      return

    print(f"Adding \"{domain}\" -> \"{serviceHost}\"")
  
    traefikConfig.addRouter(name, domain, serviceHost)
    traefikConfig.addService(name, serviceHost)

    traefikConfig.save()

    restartTraefik()

    print(f"Access your service at http://{domain}")