import sys
import subprocess
import yaml
import os

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

  print("Traefik restarted!")

def addDomain(name, domain, serviceHost):
  # Check if name already exists
  if name in routers:
    print("Name \"%s\" already exists" % name)
    exit()

  print("Adding domain \"%s\" -> \"%s\"" % (domain, serviceHost))
  print("Website Url: http://%s" % domain)

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
    print("Name \"%s\" does not exist" % name)
    exit()

  print("Removing domain \"%s\"" % name)

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
    print(" - [%s] http://%s -> %s" % (name, domain["domain"], domain["serviceHost"]))  

  print("")
  print("Total: %s" % len(domains))

def updateDomain(name, serviceHost):
  # Check if name exists
  if name not in routers:
    print("Name \"%s\" does not exist" % name)
    exit()

  print("Updating domain \"%s\" -> \"%s\"" % (name, serviceHost))

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