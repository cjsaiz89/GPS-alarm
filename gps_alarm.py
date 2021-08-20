# USER EDIT -----------------------------------------------------
# Select serial port configuration
select_port = 'COM5'
select_baud = 4800
# Select lon to trigger the alarm with longitude or lat with latitude
select_direction = 'lon' # or 'lat'
# Select the targets lat OR lon coordinate in dd.ddd
p1 = 79.899
p2 = 79.826
p3 = 79.733
p4 = 79.651
p5 = 79.560
p6 = 79.442
p7 = 79.337
p8 = 79.249
ptest = 79.7
# Select the radius in dd.ddd around the targets to trigger the alarm
r = 0.01


# CODE - DON NOT CHANGE -----------------------------------------------------

from tkinter import *
from tkinter import ttk
import serial
import time
import winsound


class gpstime:
    def __init__(self, hh, mm, ss):
        self.hh = hh
        self.mm = mm
        self.ss = ss

class gpsdate:
    def __init__(self, d, m, y):
        self.d = d
        self.m = m
        self.y = y

def deg(x):
    lx = len(str(int(float(x))))
    xdeg = str(int(float(x)))
    if ( lx == 3):
        return xdeg[0:1]
    elif ( lx == 4):
        return xdeg[0:2]
    elif ( lx == 5):
        return xdeg[0:3]

def min(x):
    lx = len(str(int(float(x))))
    xmin = str(float(x))
    if (lx == 3):
        return xmin[1:]
    elif (lx == 4):
        return xmin[2:]
    elif (lx == 5):
        return xmin[3:]    


root = Tk()
root.title('GPS alarm')

usb_port = StringVar()
baud_rate = IntVar()
usb_port.set('COM5')
baud_rate.set(4800)

ttk.Label(root, text = 'Serial Port:').grid(row = 0, column = 0)
ttk.Label(root, textvariable=  usb_port).grid(row = 0, column = 1)

try:
    usb_port = StringVar()
    baud_rate = IntVar()
    usb_port.set('COM5')
    baud_rate.set(4800)
    myport = serial.Serial(port = usb_port.get(), baudrate= baud_rate.get(), bytesize=8,timeout=2, stopbits=serial.STOPBITS_ONE)
    t0 = time.time()


    # while( (time.time() - t0) < dt):
    while True:
        if(myport.in_waiting > 0):
            line = myport.readline()
            dline = line.decode('Ascii')
            print(dline)
            if '$GPRMC' in dline or '$INRMC' in dline:
                print('condition true')
                lline = dline.split(',')
                utc_date = lline[9]
                utc_time = lline[1]
                utc_date = gpsdate(utc_date[0:2], utc_date[2:4], utc_date[4:6])
                utc_time = gpstime(utc_time[0:2], utc_time[2:4], utc_time[4:6])
                lat = lline[3]
                lat_deg = int(deg(lat))
                lat_min = float(min(lat))
                ns = lline[4]
                lon = lline[5]
                lon_deg = int(deg(lon))
                lon_min = float(min(lon))
                ew = lline[6]
                v = lline[7]
                hdg = lline[8]
                # txt = "Date: {}/{}/{} , Time: {}:{}:{} , LAT: {}° {}' {} , LONG: {}° {}' {} , Speed: {} kt , Heading: {} °"
                txt = "LAT: {}° {}' {} , LONG: {}° {}' {} , Speed: {} kt , Heading: {} °"
                # print(txt.format( utc_date.m, utc_date.d, utc_date.y, utc_time.hh, utc_time.mm, utc_time.ss , lat_deg, lat_min, ns, lon_deg, lon_min, ew, v, hdg ))
                print(txt.format( lat_deg, lat_min, ns, lon_deg, lon_min, ew, v, hdg ))

                lat_dec = lat_deg + lat_min/60
                lon_dec = lon_deg + lon_min/60
                print(lat_dec, lon_dec)
                
                if select_direction == 'lon':
                    ln = lon_dec
                elif select_direction == 'lat':
                    ln = lat_dec
                else:
                        print("ERROR WRONG WORD, CHOOSE 'lat' or 'lon'")

                if( (abs(ln-p8) <= r) or (abs(ln-p7) <= r) or (abs(ln-p6) <= r) or (abs(ln-p5) <= r) or (abs(ln-p4) <= r) or (abs(ln-p3) <= r) or (abs(ln-p2) <= r) or (abs(ln-p1) <= r) or (abs(ln-ptest) <= r)):
                    print('You got to the target location!')
                    duration = 5000  # milliseconds
                    freq = 1000  # Hz
                    winsound.Beep(freq, duration)
                    time.sleep(3)
                    
        
    myport.close()
except:
    print('no gps')
    pass

root.mainloop()



# http://aprs.gids.nl/nmea/
# $GPRMC,120141,A,2627.5038,N,07634.4757,W,0.5,107.5,130321,9.1,W*75

# eg2. $GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68


#            225446       Time of fix 22:54:46 UTC
#            A            Navigation receiver warning A = OK, V = warning
#            4916.45,N    Latitude 49 deg. 16.45 min North
#            12311.12,W   Longitude 123 deg. 11.12 min West
#            000.5        Speed over ground, Knots
#            054.7        Course Made Good, True
#            191194       Date of fix  19 November 1994
#            020.3,E      Magnetic variation 20.3 deg East
#            *68          mandatory checksum