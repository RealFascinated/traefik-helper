import subprocess
import os

containerName = "traefik"
if os.environ.get("CONTAINER_NAME"):
  containerName = os.environ.get("CONTAINER_NAME")

def restartTraefik():
  # Check if we're in Windows, if so, don't restart Traefik
  if os.name == "nt":
    print("Restarting Traefik is not supported on Windows.")
    return
  print("Restarting Traefik, please wait this can take a while...")
    
  # Restart Traefik in the base directory
  subprocess.run(["docker", "restart", containerName])

  print("Done!")
