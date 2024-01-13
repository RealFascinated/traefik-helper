# traefik-helper

This is a helper container for traefik. It can add, remove and update services.

## Usage

### Add command alias

```bash
alias traefik-helper='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /home/traefik/data/config.yml:/app/config.yml -e CONTAINER_NAME=traefik fascinated/traefik-helper:latest python src/manage.py'
```

### Add service

```bash
traefik-helper add [name] [domain] [service url]
```
