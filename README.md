# traefik-helper

This is a helper container for traefik. It can add, remove and update services.

## NOTICE

PLEASE PLEASE PLEASE MAKE SURE YOU HAVE A BACKUP OF YOUR CONFIG FILE BEFORE USING THIS CONTAINER. I AM NOT RESPONSIBLE FOR ANY DATA LOSS.

## Usage

### Add command alias

```bash
alias traefik-helper='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /home/traefik/data/config.yml:/app/config.yml -e CONTAINER_NAME=traefik fascinated/traefik-helper:latest python src/manage.py'
```

### Add service

```bash
traefik-helper add [name] [domain] [service url]
```

### Remove service

```bash
traefik-helper remove [name]
```

### List services

```bash
traefik-helper list
```

## Windows Alias

```bash
function Traefik-Helper {
    $argsAsString = $args -join ' '

    $sshCommand = "ssh root@ip -i C:\Users\you\.ssh\your_ssh_key docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /home/traefik/data/config.yml:/app/config.yml -e CONTAINER_NAME=traefik fascinated/traefik-helper:latest python src/manage.py $argsAsString"

    Invoke-Expression $sshCommand
}

# Set the alias
Set-Alias -Name "traefik" -Value "Traefik-Helper"
```
