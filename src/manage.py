import sys
import subprocess
import yaml
import os
from colorama import Fore

# Variables
configFile = "./config.yml"
containerName = "traefik"

# Are we running in a Docker container?
if os.environ.get("CONFIG_FILE"):
  configFile = os.environ.get("CONFIG_FILE")
if os.environ.get("CONTAINER_NAME"):
  containerName = os.environ.get("CONTAINER_NAME")

# DO NOT TOUCH
commands = ["add", "remove", "list", "update"]
command = len(sys.argv) > 1 and sys.argv[1]

if command not in commands:
  print("")
  print("Usage: manage.py [command]")
  print("")
  print("Commands:")
  print("  - add [name] [domain] [service host]")
  print("  - remove [name]")
  print("  - update [name] [new service host]")
  print("  - list")
  exit()

with open(configFile, "r") as config:
  configYml = yaml.safe_load(config)

http = configYml["http"]
routers = http["routers"]
services = http["services"]

def restartTraefik():
  print("Restarting Traefik, please wait this can take a while...")
  
  # Restart Traefik in the base directory
  subprocess.run(["docker", "restart", "traefik"])

  print(f"{Fore.GREEN}Done!{Fore.RESET}")

def addDomain(name, domain, serviceHost):
  # Check if name already exists
  if name in routers:
    print(f"Name \"{Fore.RED}{name}{Fore.RESET}\" already exists")
    exit()

  print(f"Adding domain \"{Fore.BLUE}{name}{Fore.RESET}\" -> \"{Fore.YELLOW}{serviceHost}{Fore.RESET}\"")
  print(f"Domain: {Fore.GREEN}http://{domain}{Fore.RESET}")

  # Add router
  routers[name] = {
    "entryPoints": ["https"],
    "rule": "Host(`%s`)" % domain,
    "middlewares": ["default-headers", "https-redirectscheme"],
    "tls": {},
    "service": name
  }

  # Add service
  services[name] = {
    "loadBalancer": {
      "servers": [
        {
          "url": serviceHost
        }
      ]
    }
  }

  # Write to file
  with open(configFile, "w") as config:
    yaml.dump(configYml, config)
  
  # Restart Traefik
  restartTraefik()

def removeDomain(name):
  # Check if name exists
  if name not in routers:
    print(f"Name \"{Fore.RED}{name}{Fore.RESET}\" does not exist")
    exit()

  print(f"Removing domain \"{Fore.BLUE}{name}{Fore.RESET}\"")

  # Remove router
  del routers[name]

  # Remove service
  del services[name]

  # Write to file
  with open(configFile, "w") as config:
    yaml.dump(configYml, config)
  
  # Restart Traefik
  restartTraefik()

def listDomains():
  print("Listing domains:")

  # name and domain -> service host
  domains = {}

  # Loop through routers
  for name, router in routers.items():
    # Get domain
    domain = router["rule"].split("`")[1]
    
    # Get service host
    serviceHost = services[name]["loadBalancer"]["servers"][0]["url"]

    # Add to domains
    domains[name] = {
      "domain": domain,
      "serviceHost": serviceHost
    }

  # Print domains
  for name, domain in domains.items():
    print(f" - {Fore.BLUE}[{name}] {Fore.GREEN}http://{domain['domain']} {Fore.RESET}-> {Fore.YELLOW}{domain['serviceHost']}{Fore.RESET}")  

  print("")
  print("Total: %s" % len(domains))

def updateDomain(name, serviceHost):
  # Check if name exists
  if name not in routers:
    print("Name \"%s\" does not exist" % name)
    exit()

  print(f"Updating domain \"{Fore.BLUE}{name}{Fore.RESET}\" -> \"{Fore.YELLOW}{serviceHost}{Fore.RESET}\"")

  # Update service
  services[name] = {
    "loadBalancer": {
      "servers": [
        {
          "url": serviceHost
        }
      ]
    }
  }

  # Write to file
  with open(configFile, "w") as config:
    yaml.dump(configYml, config)
  
  # Restart Traefik
  restartTraefik()

match command:
  case "add":
    name = sys.argv[2]
    domain = sys.argv[3]
    serviceHost = sys.argv[4]
    addDomain(name, domain, serviceHost)
  case "remove":
    name = sys.argv[2]
    removeDomain(name)
  case "update":
    name = sys.argv[2]
    serviceHost = sys.argv[3]
    updateDomain(name, serviceHost)
  case "list":
    listDomains()