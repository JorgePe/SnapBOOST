#!/usr/bin/env python3

# #Snap! extension base by Technoboy10
# https://github.com/technoboy10/snap-server/blob/master/snap-server.py
# Adapted for python3 and LEGO BOOST by JorgePe
# October 2017
# tested on:
# - x64 laptop running Ubuntu 17.04 (kernel 4.10.0-35)

import http.server
import re
import os
import socketserver

#from . import movehub, constants
#from pyb00st import movehub, constants

from pyb00st.movehub import MoveHub
from pyb00st.constants import *

from time import sleep

MY_MOVEHUB_ADD = '00:16:53:A4:CD:7E'
MY_BTCTRLR_HCI = 'hci0'

colordist_port = PORT_C

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def send_head(self):
        path = self.path
        ospath = os.path.abspath('')

        if 'move1motor' in path:
            regex = re.compile("\/move1motor([ab])x([0-9]+)x([0-9]+)x([+-])")
            m = regex.match(path)
#            print('Regex: ', m.group(1), m.group(2), m.group(3), m.group(4))
            if m.group(4) == '-':
                dutycycle = -1 * int(m.group(3))
            elif m.group(4) == "+":
                dutycycle = int(m.group(3))
            milliseconds = int(m.group(2))
            motor = m.group(1)
#            print('Motor: ',motor)
#            print('Ms:    ',milliseconds)
#            print('DC:    ',dutycycle)
#            print('Ms/1000:',milliseconds/1000)
            if motor == "a":
                mymovehub.run_motor_for_time(MOTOR_A, milliseconds, dutycycle)
                sleep(milliseconds/1000)
            elif motor == "b":
                mymovehub.run_motor_for_time(MOTOR_B, milliseconds, dutycycle)
                sleep(milliseconds/1000)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        elif 'move2motors' in path:
            regex = re.compile("\/move2motors(([0-9]+)x([0-9]+)x([+-])x([0-9]+)x([+-]))")
            m = regex.match(path)
#            print('Regex: ', m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6))
            milliseconds = int(m.group(2))
            if m.group(4) == '-':
                dutycycle1 = -1 * int(m.group(3))
            elif m.group(4) == '+':
                dutycycle1 = int(m.group(3))
            if m.group(6) == '-':
                dutycycle2 = -1 * int(m.group(5))
            elif m.group(6) == '+':
                dutycycle2 = int(m.group(5))

#            print('Ms:    ',milliseconds)
#            print('DC1:    ', dutycycle1)
#            print('DC2:    ', dutycycle2)
#            print('Ms/1000:',milliseconds/1000)

            mymovehub.run_motors_for_time(MOTOR_AB, milliseconds, dutycycle1, dutycycle2)
            sleep(milliseconds/1000)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()


        # Warning:
        # this lefts files 'tilt', 'dist' and 'color' in the current directory
        # containing the last value read from the BOOT Move Hub

        if path=='/tilt':
            f = open(ospath + '/tilt', 'w+')
            tilt = mymovehub.last_hubtilt
            print('Tilt:',tilt)
            if tilt in TILT_BASIC_VALUES:
                f.write(TILT_BASIC_TEXT[tilt])
            else:
                f.write('?')
            f.close()
            f = open(ospath + '/tilt', 'rb')
            ctype = self.guess_type(ospath + '/tilt')
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return f

        elif path=='/dist':
            f = open(ospath + '/dist', 'w+')
            f.write(str(mymovehub.last_distance_C))
            f.close()
            f = open(ospath + '/dist', 'rb')
            ctype = self.guess_type(ospath + '/dist')
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return f

        elif path=='/color':
            f = open(ospath + '/color', 'w+')
            f.write(mymovehub.last_color_C)
            f.close()
            f = open(ospath + '/color', 'rb')
            ctype = self.guess_type(ospath + '/color')
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return f

if __name__ == "__main__":
    print('Snap! BOOST extension by JorgePe')

    PORT = 8001 

    Handler = CORSHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler, bind_and_activate=False)
    httpd.allow_reuse_address = True
    try:
        httpd.server_bind()
        httpd.server_activate()
    except:
        httpd.server_close()
        raise

    print('Serving at port', PORT)
    print('Go ahead and launch Snap!')
    print('<a>http://snap.berkeley.edu/snapsource/snap.html</a>')
    print('Then import the 'snap-boost-blocks-v#.xml' containing block definitions for motor and sensors.')

    mymovehub = MoveHub(MY_MOVEHUB_ADD, 'BlueZ', MY_BTCTRLR_HCI)

    try:
        mymovehub.start()
        mymovehub.subscribe_all()
        mymovehub.listen_hubtilt(MODE_HUBTILT_BASIC)
        mymovehub.listen_colordist_sensor(colordist_port)
        httpd.serve_forever()
    finally:
        mymovehub.stop()
