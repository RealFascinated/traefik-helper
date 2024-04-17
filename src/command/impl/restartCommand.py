from command.command import Command
from traefik.traefikConfig import TraefikConfig
from utils.dockerUtils import restartTraefik

class RestartCommand(Command):
  def __init__(self):
    super().__init__("restart", "Restart traefik", "")

  def execute(self, traefikConfig: TraefikConfig, args):
    restartTraefik()