from command.command import Command
from traefik.traefikConfig import TraefikConfig
from utils.dockerUtils import getTraefikLogs

class LogsCommand(Command):
  def __init__(self):
    super().__init__("logs", "Get traefik logs", "logs")

  def execute(self, traefikConfig: TraefikConfig, args):
    getTraefikLogs()