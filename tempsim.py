#!/usr/bin/env python
from pylab import *

#data = loadtxt('coldstart.txt')
data = loadtxt('temptests.txt')

t = data[:,0]
real_measured = data[:,1]
real_target = data[:,2]
real_power = data[:,3]

sim_heater   = []
sim_measured = []
dtime = t[1]-t[0]
room_temp = 25.0
number_of_delay_elements = 5
for i, time in enumerate(t):
    if i == 0:
        # set all temperatures to the one that was really measured
        measured = heater = real_measured[i]
        delayed_measurement = number_of_delay_elements*[real_measured[i]]
    else:
        c1 = 0.00167  # heater strength
        c2 = 0.000278 # cooldown strength
        if time > 7*60: c2 *= 1.42 # fan turned on, stronger cooldown
        T_measurement = 9.8 # measurement delay (time constant, seconds)
        c3 = 1 - exp(-dtime/(T_measurement/number_of_delay_elements))
        power = real_power[i] 
        #if time > 7*60: power = 127
        heater += c1 * power # energy pumped in
        heater += c2 * (room_temp - heater) # energy lost to room
        for j in range(number_of_delay_elements):
            if j == 0:
                value = heater 
            else:
                value = delayed_measurement[j-1] 
            delayed_measurement[j] += c3 * (value - delayed_measurement[j])
        measured = delayed_measurement[-1]

    sim_heater.append(heater)
    sim_measured.append(measured)


plot(t, real_measured, label='real: measured')
plot(t, sim_measured, label='sim: measured')
plot(t, sim_heater, label='sim: heater')
#plot(t, real_target, label='real: target')
plot(t, real_power, label='real: heater power')
xlabel('seconds')

T_room = 24.9

legend()
grid()
show()
