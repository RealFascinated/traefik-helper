from colorama import Fore
from command.command import Command
from traefik.traefikConfig import TraefikConfig

class ListCommand(Command):
  def __init__(self):
    super().__init__("list", "List all services", "list")

  def execute(self, traefikConfig: TraefikConfig, args):
    print("Listing all services:")

    domains = traefikConfig.getAll()

    # Print domains
    for name, domain in domains.items():
      print(f" - {Fore.CYAN}[{name}] {Fore.GREEN}http://{domain['domain']} {Fore.RESET}-> {Fore.YELLOW}{domain['serviceHost']}{Fore.RESET}")  

    print("")
    print("Total: %s" % len(domains))