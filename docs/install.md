# Installation

This installation guide will lead you through the whole process of installation and starting up your personal Braubar.

## Raspberry Pi 

A common and small distribution is the raspbian image. Download it and copy it to your sd card. For the copy enshure that the device is not mounted. You need to be root.

```bash
dd bs=4M if=/tmp/2016-03-18-raspbian-jessie-lie.img of=/dev/mmcblk0 && sync
```

`sync`enshures that all data will be written to the sd card. 
You can find the appropriate image on <https://www.raspberrypi.org/downloads/>

After you finished with sync, mount your sd card under `/mnt` 

Open `/mnt/boot/config.txt` and add the following lines at the end

```
# rotate display
lcd_rotate=2
```

For IP settings modify `/mnt/etc/dhcpdc.conf` to configure your network settings.

```
interface eth0
static ip_address=192.168.3.100
static routers=192.168.3.1
static domain_server=8.8.8.8
```

Adjust IP settings to your needs. Now unmount your sd card and get your Pi running. Afterwards you need to get access to the Pi, my favorite is ssh.

Open `raspi-conf` and select entry `Expand Filesystem` to expand the image to the full size of your sd card and reboot. Othervise there is not enough space left. 

### Debian and Packages
The following software will be installed:

- supervisor
- python3
- pip
- iceweasel
- xinit
- matchbox

Debian 8:
After boot run a update and then install the required software

```bash
apt-get update && apt-get install supervisor python3 python3-pip iceweasel xinit matchbox
```

### X Window System 

create `.xinitrc` file in `home` folder

```
matchbox-window-manager &
exec /usr/bin/iceweasel http://localhost:5000
```

To start iceweasel in fullscreen mode it is neccesary to start it one, enter fullscreen mode and exit. Then it it will be saved in your profile. Another option is to create your own profile, but I won't handle that here.

### Auto Login

Edit file at `/etc/systemd/system/getty.target.wants/getty@tty1.service` and change `ExecStart=` line in section `[Service]` to this

```
ExecStart=-/sbin/agetty -a pi %I $TERM
```

To get X with iceweasel started automatically add the following snippet to the end of `~/.bash_login`

```
[[ -z $DISPLAY && $(tty) == /dev/tty1 ]] && exec startx
```

Since we have no window manager which runs in systemd it is neccesary to set `multi-user.target` as default

```
systemctl set-default multi-user.target
```

But be careful, now you can't login to anything other than the iceweasel application. Except you do a remote login. 

### Braubar installation

Download braubar-pi to you Pi 

```bash
wget https://github.com/braubar/braubar-pi/archive/master.zip
```

and unzip it e.g. to your home folder 

```bash
unzip master.zip && rm master.zip && cd braubar-pi-master
```

to install the needed python requirements run as root

```bash
pip3 install -r requirements.txt
```

### Install and configure dnsmasq

If there is a DHCP Server already running then please change IP settings and ignore this section.

First install dnsmasq on your system. 

```bash
apt-get install dnsmasq
```

There is a preconfigured file for dnsmasq for Braubar. `$BRAUBAR_HOME/install/dnsmasq.conf`

```bash 
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bak
ln -s /home/pi/braubar-pi-master/install/dnsmasq.conf /etc/dnsmasq.conf
```




### Config Braubar start with Supervisor

Adjust paths to your configuration!

Create link to config in /etc/supervisor/conf.d/braubar.conf

```bash
ln -s $BRAUBAR_HOME/install/braubar.conf /etc/supervisor/conf.d/braubar.conf
```

```ini
[program:braubar]
command=/home/pi/braubar-pi-master/bin/braubar
directory=/home/pi/braubar-pi-master/bin
loglevel=warning
process_name=%(program_name)s
autostart=true
autorestart=unexpected
startsecs=10
startretries=3
stopasgroup=true
redirect_stderr=false
stdout_logfile=/home/pi/braubar-pi-master/log/braubar.log
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
stderr_logfile=/home/pi/braubar-pi-master/log/braubar.err
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB
stderr_events_enabled=false
serverurl=AUTO
```

reread and restart supervisr and show status
`supervisorctl reread && supervisorctl reload && supervisorctl status`

control log in `/var/log/supervisor/supervisor.log`


## Arduino 
In Braubar the Arduino acts as a temperature sensor. 

### Geting started

It is required to have an running Arduino environment. Then you can either upload the program to your Arduino within Arduino Studio or with the shipped Makefile, which is recommended. 
Before running Make you shoud have a look at the Makefile to ensuhre your Serial Port is mapped to the right device. 
To upload the compiled program to your Arduino run:

```
make clean && make && make upload
```

After running successfully it will request an IP from your DHCP server and start sending broadcast packages all over your local network. To avoid broadcasting, please enter the desired IP for `IPAddress server` in `braubar_temp.ino` file.
Also it is possible to change the port from 50505 to  your wish. 

### Functionality

It sends a package every second with the current temperature value, the id of the sensor and a start and end sequence consistion of `0xF0FF` and a end sequence with the same sync bits. 


