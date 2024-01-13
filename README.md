# traefik-helper

This is a helper container for traefik. It can add, remove and update services.

## Usage

DO NOT CHANGE: `/home/config.yml`

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /home/traefik/data/config.tml:/home/config.yml fascinated/traefik-helper:latest python src/manage.py
```

**Example Add**

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /home/traefik/data/config.tml:/home/config.yml fascinated/traefik-helper:latest python src/manage.py add test test.fascinated.cc http://10.0.0.10
```
