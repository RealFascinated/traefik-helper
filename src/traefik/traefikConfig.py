import yaml


class TraefikConfig:

  def __init__(self, configFile) -> None:
    self.configFile = configFile
    with open(configFile, "r") as config:
      self.configYml = yaml.safe_load(config)

  def isValid(self) -> bool:
    return "http" in self.configYml and "routers" in self.configYml["http"] and "services" in self.configYml["http"]

  def getRouter(self, name):
    return self.configYml["http"]["routers"][name]

  def getService(self, name):
    return self.configYml["http"]["services"][name]

  def addRouter(self, name, domain, serviceHost):
    # Add router
    self.configYml["http"]["routers"][name] = {
      "entryPoints": ["https"],
      "rule": "Host(`%s`)" % domain,
      "middlewares": ["default-headers", "https-redirectscheme"],
      "tls": {},
      "service": name
    }

    # Add service
    self.configYml["http"]["services"][name] = {
      "loadBalancer": {
        "servers": [
          {
            "url": serviceHost
          }
        ]
      }
    }
  
  def addSubPathRouter(self, name, domain, path, serviceHost):
    # Add trailing slashs
    if not path.endswith("/"): 
      path += "/"
    if not serviceHost.endswith("/"): 
      serviceHost += "/"

    # Add path stripper middleware
    self.configYml["http"]["middlewares"][name] = {
      "stripPrefix": {
        "prefixes": [path]
      }
    }

    # Add router
    self.configYml["http"]["routers"][name] = {
      "entryPoints": ["https"],
      "rule": "Host(`%s`) && PathPrefix(`%s`)" % (domain, path),
      "middlewares": ["default-headers", "https-redirectscheme", name],
      "tls": {},
      "service": name
    }

    # Add service
    self.configYml["http"]["services"][name] = {
      "loadBalancer": {
        "servers": [
          {
            "url": serviceHost
          }
        ]
      }
    }
  
  def removeRouter(self, name):
    # Remove router
    del self.configYml["http"]["routers"][name]

    # Remove service
    del self.configYml["http"]["services"][name]
  
  def hasRouter(self, name):
    return name in self.configYml["http"]["routers"]

  def hasPathRewrite(self, name):
    return name in self.configYml["http"]["middlewares"]

  def hasService(self, name):
    return name in self.configYml["http"]["services"]

  def getRouters(self):
    return self.configYml["http"]["routers"]
  
  def getServices(self):
    return self.configYml["http"]["services"]

  def getAll(self):
    domains = {}

    routers = self.getRouters()
    services = self.getServices()

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

    return domains
  
  def save(self):
    with open(self.configFile, "w") as config:
      yaml.dump(self.configYml, config)