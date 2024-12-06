############################################################
# I'm using this file to test the limits of the motor
############################################################

import odrive
from odrive.enums import *
import time

odrv0 = odrive.find_any()
print(str(odrv0.vbus_voltage))

if (odrv0.axis0.motor.config.pre_calibrated != True): 
	# calibrate
	print("not calibrated")
	pass 
time.sleep(2)

# odrv0.axis0.motor.config.current_lim = 9.4
# odrv0.axis0.motor.config.pole_pairs = 3
# odrv0.axis0.motor.config.torque_constant = 0.05
# odrv0.axis0.encoder.config.cpr = 4096
# # odrv0.axis0.motor.config.current_lim = ?
# odrv0.axis0.controller.config.input_filter_bandwidth = 2.0
# odrv0.axis0.controller.config.vel_gain = 0.045
# odrv0.axis0.controller.config.vel_limit = 40
# odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
odrv0.axis0.controller.config.input_mode = InputMode.VEL_RAMP
odrv0.axis0.controller.config.vel_limit = 1000

curVel = 10  #turn/s
curCur = 0  #amps
while(odrv0.axis0.error == 0):
	time.sleep(4)

	odrv0.axis0.controller.input_vel = curVel
	print("commanded velocity: ", curVel)
	print("est. velocity", odrv0.axis0.encoder.vel_estimate)
	curCur = odrv0.axis0.motor.current_control.Iq_setpoint
	print("current current lmao: ", curCur)

	curVel += 5

odrv0.axis0.controller.input_vel = 60

odrv0.axis0.controller.config.vel_limit = curVel - 1
print(curVel)
# for position control
#	odrv0.axis0.controller.config.input_mode = INPUT_MODE_POS_FILTER
#	ordv0.axis0.controller.inputpos = 1

# for velocity control
#	odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
#	odrv0.axis0.controller.input_vel = 1

# note difference between control mode and input mode. to make velocity control work, make sure
# control mode is 0

