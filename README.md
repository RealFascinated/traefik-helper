# traefik-helper

This is a helper container for traefik. It can add, remove and update services.

## NOTICE

PLEASE PLEASE PLEASE MAKE SURE YOU HAVE A BACKUP OF YOUR CONFIG FILE BEFORE USING THIS CONTAINER. I AM NOT RESPONSIBLE FOR ANY DATA LOSS. </br>
This helper also assumes that you have SSL certificates setup for your services.

## Usage

### Add command alias

```bash
alias traefik-helper='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /home/traefik/data/config.yml:/app/config.yml -e CONTAINER_NAME=traefik fascinated/traefik-helper:latest python src/manage.py'
```

### List commands

```bash
traefik-helper
```

## Windows Alias

Create the directory `~/Documents/WindowsPowerShell` and create a file called `Microsoft.PowerShell_profile.ps1` in that directory. Add the following code to the file.

```bash
function Traefik-Helper {
    $argsAsString = $args -join ' '

    $sshCommand = "ssh root@ip -i C:\Users\you\.ssh\your_ssh_key docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /home/traefik/data/config.yml:/app/config.yml -e CONTAINER_NAME=traefik fascinated/traefik-helper:latest python src/manage.py $argsAsString"

    Invoke-Expression $sshCommand
}

# Set the alias
Set-Alias -Name "traefik" -Value "Traefik-Helper"
```

This will allow you to run the `traefik` command in PowerShell.
