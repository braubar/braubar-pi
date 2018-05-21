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

## Database Design (DRAFT)

```
TABLES:
- brew_meta
- brew_log

BREW_META:
- id: INT
- sud_nr: INT
- start_time: DATETIME
- end_time: DATETIME

BREW_LOG:
- timestamp: DATETIME
- brew_id: INT (BREW_META.id)
- sensor_id: INT
- current_temp: FLOAT
- target_temp: FLOAT
- change: FLOAT
- timer_passed: INT
- timer_set: INT
- state: TEXT

```


