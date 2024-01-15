import sys
import os

from command.commandManager import CommandManager
from traefik.traefikConfig import TraefikConfig

# Variables
configFile = "./config.yml"

# Are we running in a Docker container?
if os.environ.get("CONFIG_FILE"):
  configFile = os.environ.get("CONFIG_FILE")

traefikConfig = TraefikConfig(configFile)
if traefikConfig.isValid() == False:
  print("Invalid traefik config file, please check your config.yml file")
  exit(1)

command = len(sys.argv) > 1 and sys.argv[1]
commandManager = CommandManager()

if not commandManager.commandExists(command):
  print("Usage: manage [command]")
  print("")
  print("Commands:")
  for command in commandManager.commands:
    print(f"  - {command.usage}")
  exit()

args = sys.argv[2:]
commandManager.getCommand(command).execute(traefikConfig, args)
