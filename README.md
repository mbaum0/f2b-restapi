# Fail2Ban REST API
This project is meant to act as a supplement to the [crazymax/docker-fail2ban](https://github.com/crazy-max/docker-fail2ban) container.

### How to use with docker compose
```docker
# docker-compose.yml

version: "3"
services:
  fail2ban:
    image: crazymax/fail2ban:latest
    container_name: fail2ban
    network_mode: "host"
    cap_add:
      - NET_ADMIN
      - NET_RAW
    volumes:
      - "./data:/data" # path to local configuration storage
      - socket-share:/var/run/fail2ban/ # shares fail2ban socket
    env_file:
      - "./fail2ban.env"
    restart: always

  f2b-restapi:
    image: f2b-apirest-image:v1
    container_name: f2b-restapi
    network_mode: "host"
    volumes:
      - socket-share:/var/run/fail2ban # shares fail2ban socket
    restart: unless-stopped

# setup volume for sharing fail2ban socket
volumes:
     socket-share:

```
