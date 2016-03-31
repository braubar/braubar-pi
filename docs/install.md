# Installation

This installation guide will lead you through the whole process of installation and starting up your personal Braubar.

At first we begin with the installation of the Raspberry Pi and related software.

## Raspberry Pi 

A common and small distribution is the raspbian image. Download it and copy it to your sd card. For the copy enshure that the device is not mounted. You need to be root.

```
dd bs=4M if=/tmp/2016-03-18-raspbian-jessie-lie.img of=/dev/mmcblk0
```
You can find the appropriate image on <https://www.raspberrypi.org/downloads/>

### Debian and Packages


- supervisor
- python3
- pip

Debian 8For the copy enshure that the device is not mounted. You need to be rootFor the copy enshure that the device is not mounted. You need to be root:

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
then iceweasel will start everytime you start your raspberry.

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
