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
commands = ["add", "remove", "list"]
command = len(sys.argv) > 1 and sys.argv[1]

if command not in commands:
  print("")
  print("Usage: manage.py [command]")
  print("")
  print("Commands:")
  print("  - add [name] [domain] [service host]")
  print("  - remove [name]")
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

  # domain -> service host
  domains = {}

  # Get domains (Host and HostRegexp)
  for name, router in routers.items():
    if "rule" in router:
      rule = router["rule"]

      # Host
      if rule.startswith("Host"):
        domain = rule.split("`")[1]
        domains[domain] = services[name]["loadBalancer"]["servers"][0]["url"]

      # HostRegexp
      if rule.startswith("HostRegexp"):
        domain = rule.split("`")[1]
        domains[domain] = services[name]["loadBalancer"]["servers"][0]["url"]

  # Print domains
  for domain, serviceHost in domains.items():
    print(" - %s -> %s" % (domain, serviceHost))

match command:
  case "add":
    name = sys.argv[2]
    domain = sys.argv[3]
    serviceHost = sys.argv[4]
    addDomain(name, domain, serviceHost)

  case "remove":
    name = sys.argv[2]
    removeDomain(name)
  case "list":
    listDomains()