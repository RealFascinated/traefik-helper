# traefik-helper

This is a helper container for traefik. It can add, remove and update services.

## Usage

DO NOT CHANGE: `/home/config.yml`

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /home/traefik/data/config.tml:/home/config.yml fascinateed/traefik-helper:latest
```
