#!/usr/bin/env python
import serial, sys, os, time

for i in range(5):
    port='/dev/ttyACM%d' % i
    if os.path.exists(port):
        break
baud = 115200

ser = serial.Serial(port, baud, timeout=2)

ser.read(20000)

t = t0 = time.time()
interval = 0.1
i = -1
while 1:
    i += 1
    while time.time() < t+interval:
        time.sleep(0.010)
    t += interval
    t_real = time.time()
    ser.write('M105\n')
    line = ser.readline()
    #print line.strip()
    actual = float(line.split()[1][2:])
    target = float(line.split()[2][1:])
    power  = float(line.split()[-1][2:])
    print '%.3f' % (t - t0), actual, target, power
    if i*interval == 30:
        ser.write('M104 S50\n')
        ser.readline()
    if i*interval == 60:
        ser.write('M104 S220\n')
        ser.readline()
    if i*interval == 60*7:
        ser.write('M106\n')
        ser.readline()
    if i*interval == 60*12:
        ser.write('M104 S200\n')
        ser.readline()
    if i*interval == 60*20:
        ser.write('M104 S0\n')
        ser.readline()
    if i*interval == 60*40:
        break
    sys.stdout.flush()
