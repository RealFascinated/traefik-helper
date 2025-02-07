from command.impl.addCommand import AddCommand
from command.impl.listCommand import ListCommand
from command.impl.removeCommand import RemoveCommand
from command.impl.restartCommand import RestartCommand
from command.impl.logsCommand import LogsCommand
from command.impl.addSubPathCommand import AddSubPathCommand
from command.impl.addCatchAllCommand import AddCatchAllCommand

class CommandManager:

  commands = []

  def __init__(self):
    self.addCommand(AddCommand())
    self.addCommand(RemoveCommand())
    self.addCommand(ListCommand())
    self.addCommand(RestartCommand()) 
    self.addCommand(LogsCommand())
    self.addCommand(AddSubPathCommand())
    self.addCommand(AddCatchAllCommand())
    pass


  def addCommand(self, command):
    self.commands.append(command)
    pass

  def getCommand(self, name):
    for command in self.commands:
      if command.name == name:
        return command
    return None
  
  def commandExists(self, name):
    return self.getCommand(name) != None
    