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
    
    router = args[0]
    domain = args[1]
    path = args[2]
    # Fix the path
    if path.startswith("/") == False:
      path = "/" + path
    serviceHost = args[3]
    subPathName = domain + path

    if traefikConfig.hasPathRewrite(subPathName):
      print(f"Sub path for \"{domain}{path}\" already exists")
      return
    
    if traefikConfig.hasRouter(router) == False:
      print(f"Router \"{router}\" does not exist")
      return
    
    # Validate if the service host is a valid URL
    if not serviceHost.startswith("http://") and not serviceHost.startswith("https://"):
      print(f"Service host \"{serviceHost}\" is not a valid URL")
      return

    print(f"Adding \"{domain}\" -> \"{serviceHost}\"")
  
    traefikConfig.addSubPathRouter(subPathName, domain, path, serviceHost)
    traefikConfig.save()

    print(f"Access your service at http://{domain}{path}")