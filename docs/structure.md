# Projekt Structure

Generally Braubar is divided into three parts: 

- **braubar-pi**: Controling and displaying information on a Raspberry Pi 
- **braubar-temp**: Temperature sensor that sends temperature values via UDP on Port 50505 
- **EG-PM2-LAN**: Power-strip to switch the magnet valve or your stove on and off. 

## braubar-pi

braubar-pi is mainly written in python and aims to be used in python >3.4. It consits of three different modules with different roles: 

- Brewdaemon
- Socketserver
- Flask-Webserver

### Brewdaemon 
The Brewdaemon manages the whole application, keeps track of the different states, computes a PID output, switches the power-switch and writes everything in a SQLite database.


### Socketserver
Starts a socket-server on port 50505 and listens for packages from **braubar-temp**-project. After receiving a package the values will be written in a temporary log file, which will be read every two seconds by **Brewdaemon**. 

### Flask-Webserver

Overview of the current state, shows a temperature-plot with three graphs: 

- real temperature curve
- desired temperature curve 
- PID output scaled to a output from 0-100.

Also it is possible to go to the next state.

## braubar-temp

As mentioned before, braubar-temp is a ethernet temperature sensor. The attached sensor is a *ds18b20* sensor for temperature measurement. 

In the current setting the sensor yields a value every 750ms. Therefore it sends at maximum every second a new value, only if the temperature changed. 

The ethernet package looks like the following listing. The start- and end-sync bytes help to ensure that we got a correct package. In the future the end sync should be changed to a CRC to check the payload.

```
+------------------+------------+-----------+---------+----------------+
| start-sync-bytes | temp value | sensor id | heating | end sync bytes |
+------------------+------------+-----------+---------+----------------+
```

Braubar-temp requieres a DHCP-server to obtain a IP-address. 

## EG-PM2-LAN

An easy to use power-switch that can be controlled with HTTP calls. 
The responsible script for controlling the power-switch is `braubar-pi/braubar/service/powerstrip.py`

