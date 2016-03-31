# Installation

## Hardware Requirements

Note: BrewBar needs a bunch of hardware to run porperly.
Here is the list of my hardware:

 - Arduino Uno with Ethernet Shield 2 + PoE Module
 - Raspberry Pi 2 with 7" Touch Display
 - Temperature sensor ds18b20
 - PoE enabled Switch
 - ethernet wires
 - LAN enabled power-switch EG-PM2-LAN

## Software Requirements

- supervisor
- python3
- pip

Debian 8:

```bash
apt-get install supervisor python3 python3-pip
```

As easy as it can be:
Clone these two Repositories

 - https://github.com/ofesseler/braubar-pi.git
 - https://github.com/ofesseler/braubar-temp.git

then upload the code of Repository `braubar-temp` to your Arduino Uno with Ethernet-Shield on top and a ds18b20 sensor.

to install the needed python requirements run `pip3 -r requirements.txt`

copy iceweasel desktop-entry to `.config/autostart` and change `Exec=iceweasel u%` to `Exec=iceweasel http://localhost:5000`
then iceweasel will start everytime you start your raspberry. 56


## Supervisord

Adjust paths to your configuration!

Create link to config in /etc/supervisor/conf.d/braubar.conf

`ln -s $BRAUBAR_HOME/config/braubar.conf /etc/supervisor/conf.d/braubar.conf`

```ini
[program:braubar]
command=./braubar
directory=/home/oli/dev/braubar-pi/bin
loglevel=warning
process_name=%(program_name)s
autostart=true
autorestart=unexpected
startsecs=10
startretries=3
redirect_stderr=false
stdout_logfile=$CWD/../log/braubar.log
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
stderr_logfile=$CWD/../log/braubar.err
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB
stderr_events_enabled=false
environment=A="1",B="2"
serverurl=AUTO
```

reread and restart supervisr and show status
`supervisorctl reread && supervisorctl reload && supervisorctl status`

control log in `/var/log/supervisor/supervisor.log`
