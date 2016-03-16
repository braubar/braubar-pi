.. BrauBar documentation master file, created by
   sphinx-quickstart on Mon Jan  4 00:15:37 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BrauBar's documentation!
===================================

Contents:

.. toctree::
   :maxdepth: 2

   raspberry
   Brauen
   install


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



Features
--------

 - controls temperature with a network-enabled Arduino. 
 - is awesome
 - helps to simplify your brewing process

We like to brew! 

Installation
============

Note: BrewBar needs a bunch of hardware to run porperly.
Here is the list of my hardware:

 - Arduino Uno with Ethernet Shield 2 + PoE Module
 - Raspberry Pi 2 with 7" Touch Display
 - Temperature sensor ds18b20
 - PoE enabled Switch
 - ethernet wires
 - LAN enabled power-switch EG-PM2-LAN

Requirements
------------

As easy as it can be: 
Clone these two Repositories at GitHub 

 - https://github.com/ofesseler/braubar-pi.git
 - https://github.com/ofesseler/braubar-temp.git

then upload the code to your Arduino Uno with Ethernet-Shield on top and a ds18b20 sensor.


