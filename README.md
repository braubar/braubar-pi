# Braubar

Hey there, this is Braubar!

## Requirements

- python3
- pip
- flask (via pip) -> http://flask.pocoo.org/docs/0.10/quickstart/
- git

## Config
To use braubar correctly link dnsmasq.conf and interfaces in config folder to appropiate folders on target system.
Raspberry Pi with Debian example:

dnsmasq.conf: `/etc/dnsmasq.conf`
interfaces: `/etc/network/interfaces`

after enable dnsmasq as a daemon to provide IPs for all connected devices in the network.