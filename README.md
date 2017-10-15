# SnapBOOST
This is a BOOST extension for [Snap!](http://snap.berkeley.edu/)

It is based on Connor Hudson (AKA technoboy10) [snap-server](https://github.com/technoboy10/snap-server).

I just converted it to python3 and added the BOOST methods from own library, [pyb00st](https://github.com/JorgePe/pyb00st).

It still needs some cleaning and improvements but it already works on my Ubuntu laptop and my Raspbery Pi Zero W.

The idea is to use a Raspberry Pi with BLE (like the Raspberry Pi 3 or the Raspberry Pi Zero W, but any
model with a USB BT 4.x BLE dongle will work) as a gateway between a browser (on Windows, OSX, Linux
Android, iOS...) and a LEGO BOOST Move Hub.

Altough it uses my own python library, it can be easily adapted for any other python library, like [pylgbst](https://github.com/undera/pylgbst)

For now, this extension only controls the motors by time and only read the internal tilt sensor
and the Color/Dist sensor, will add the rest of the commands later.


# Requirements

- python 3.x
- pyb00st


## Installation:

Create a working directory on the Raspberry Pi, like 'snap-boost'.

Save the Snap! extension script ('snap-boost.py') inside this directory and give it execution permissions.

Save the XML with the block definitions ('snap-boost-blocks-v#.xml') to the computer/tablet/phone
from where you will use a browser to run Snap!

Create a subdirectory named 'pyb00st'.

Download my [pyb00st library](https://github.com/JorgePe/pyb00st/archive/master.zip)
Only 3 files are realy needed, they are inside 'pyb00st-master/pyb00st/':

- movehub.my
- constants.py
- \_\_init\_\_.py

Put those 3 files in the 'pyb00st' subdirectory of your working directory. 


## Usage:

The extension assumes a Color/Distance sensor connected to port C, you can change to port D
by changing the variable 'colordist_port':

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

On your browser, start the [Snap!](http://snap.berkeley.edu/snapsource/snap.html) runtime and use the menu option
'Import...' and specify the XML file you saved before.

You will now have blocks for motors (under 'Motion' category) and sensors (under 'Sensing' category).


# Available blocks

The XML file includes definitions of 2 Motion blocks and 3 Sensing blocks:

![](https://github.com/JorgePe/SnapBOOST/blob/master/images/move1motor.png)

![](https://github.com/JorgePe/SnapBOOST/blob/master/images/move2motors.png)

![](https://github.com/JorgePe/SnapBOOST/blob/master/images/read_color.png)

![](https://github.com/JorgePe/SnapBOOST/blob/master/images/read_distance.png)

![](https://github.com/JorgePe/SnapBOOST/blob/master/images/read_tilt.png)

For each block you need to specify the IP Address of your Raspberry Pi to use it (you could define a
variable and use it with every block). If you change the port (8001 by default) on the python code you
should also specify it.

`move1motor` requires a motor (`a`, `b`, `c` or `d`), a `time` value (between 0 and 999 milliseconds)
and a `speed` value (between -100% and 100%)

`move2motors` is simillar but doesn't require a motor (as it works only with A+B motors) and requires
two `speed` values (one for motor A and the other for motor B)

`read color` returns one of these colors: 'BLACK', 'BLUE', 'GREEN', 'YELLOW', 'RED', 'WHITE'.

`read distance` returns a number between 0 and 10.

`read tilt` returns of these values: 'TILT_HORIZ', 'TILT_UP', 'TILT_DOWN', 'TILT_RIGHT', 'TILT_LEFT', 'TILT_INVERT'.


# First Example

This example makes the two internal Interactive Motors turn for 0.25 seconds at full speed whenever the
distance sensor detects something at less than '6' whatever-units-LEGO-uses.

![](https://github.com/JorgePe/SnapBOOST/blob/master/images/example01.png)

On my Vernie, that makes it runaway for a bit.


# Second Example

When this example is used with Vernie it explores the world, moving forward until it founds an obstacle, then it turns right and keeps doing that, designing a path on the screen:

![](https://github.com/JorgePe/SnapBOOST/blob/master/images/example02.png)
