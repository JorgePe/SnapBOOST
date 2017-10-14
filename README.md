# SnapBOOST
Snap! extension for LEGO BOOST

This Snap! extension allows us to use Snap! with the LEGO BOOST.

The idea is to use a Raspberry Pi with BLE (like the Raspberry Pi 3 or the Raspberry Pi Zero W, but any
model with a USB BT 4.x BLE dongle will work) as a gateway between a browser (on Windows, OSX, Linux
Android, iOS...) and a LEGO BOOST Move Hub.

It uses my own python library, pyb00st, but can be easily adapted for any other python library.

For now, this extension only controls the motors by time and only read the internal tilt sensor
and the Color/Dist sensor, will add the rest of the commands later.

## Installation:

Create a working directory on the Raspberry Pi, like 'snap-boost'
Dowload the 2 files on this repository and put them on your working directory.
Give execution permission to the python script (i.e. 'snap-boost.py') and copy the xml file
to the computer/tablet/phone from where you will use a browser to run Snap!

Creat a subdirectory named 'pyb00st'.
Download my [pyb00st library](https://github.com/JorgePe/pyb00st/archive/master.zip)
Only 3 files are realy needed, they are inside 'pyb00st-master/pyb00st/':

- movehub.my
- constants.py
- __init__.pt

Put those 3 files in the 'pyb00st' subdirectory of your working directory. 

## Usage:

The extension assumes a Color/Distance sensor connected to port C, you can change to port D
by change the variable 'colordist_port':

`colordist_port = PORT_C`


Start the extension:

`./snap-boost.py`

You'll get:

```
Snap! BOOST extension by JorgePe
Serving at port 8001
Go ahead and launch Snap!
<a>http://snap.berkeley.edu/snapsource/snap.html</a>
Then import the 'snap-boost-blocks-v#.xml' containing block definitions for motor and sensors.
System:  linux
```

On your browser, start [Snap!] (http://snap.berkeley.edu/snapsource/snap.html) and then import
the xml file you saved before.

You will now have blocks for motors (under 'Motion' category) and sensors (under 'Sensing' category).
