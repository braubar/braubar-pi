# Braubar

Hey there, this is Braubar!

![Braubar Control Screenshot](https://raw.githubusercontent.com/braubar/braubar-pi/master/docs/img/Braubar_Screenshot.png "Braubar control screenshot")

Inspired by the current trend of Craft Beer, Braubar aims to make microbrewed beer accessible to everyone. The basic idea of Braubar is to partially automate the process of brewing - with affordable and widely available hardware. Aiming for easy adjustability, Braubar relies on open-source and economically efficient technology to recreate - or even enhance - the current microbrewing process.

## One Wire Sensor 

To enable One-Wire Temperature sensor add 
```
dtoverlay=w1-gpio
```

to  `/boot/config`. Then wire the sensor to GPIO4 (pin 7)

For more information and install manuals see: <http://braubar.github.io>

