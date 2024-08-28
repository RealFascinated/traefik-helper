from command.command import Command
from traefik.traefikConfig import TraefikConfig
from utils.dockerUtils import restartTraefik

class AddSubPathCommand(Command):
  def __init__(self):
    super().__init__("add-path", "Add sub path to a domain (eg: bob.com/joe)", "add-path <name> <domain> <path> <service host>")

  def execute(self, traefikConfig: TraefikConfig, args):
    if len(args) < 3:
      self.printUsage()
      return
    
    domain = args[1]
    name = args[0] + "-sub-path-" + domain
    path = args[2]
    serviceHost = args[3]

    # Fix the path
    if path.startswith("/") == False:
      path = "/" + path

    if traefikConfig.hasPathRewrite(name):
      print(f"Router \"{name}\" already exists")
      return
    
    if traefikConfig.hasRouter(name) == False:
      print(f"Router \"{name}\" does not exist")
      return
    
    # Validate if the service host is a valid URL
    if not serviceHost.startswith("http://") and not serviceHost.startswith("https://"):
      print(f"Service host \"{serviceHost}\" is not a valid URL")
      return

    print(f"Adding \"{domain}\" -> \"{serviceHost}\"")
  
    traefikConfig.addSubPathRouter(name, domain, path, serviceHost)
    traefikConfig.save()

    print(f"Access your service at http://{domain}")