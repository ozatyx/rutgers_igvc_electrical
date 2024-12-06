import odrive
from odrive.enums import *
import time
import hid
import controlParse
import controllerInputs # these two are pretty messy
import sys

def init():
    odrv0 = odrive.find_any()
    print(str(odrv0.vbus_voltage))

    if (odrv0.axis0.motor.config.pre_calibrated != True or odrv0.axis0.encoder.config.pre_calibrated != True):
    # calibrate
        odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        time.sleep(2)
        odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        print("not calibrated")


    print("setting defaults:")
    odrv0.config.dc_max_negative_current = -30
    odrv0.axis0.motor.config.current_lim = 30
    odrv0.axis0.motor.config.pole_pairs = 3
    odrv0.axis0.motor.config.torque_constant = 0.05
    odrv0.axis0.encoder.config.cpr = 4096
    odrv0.axis0.controller.config.input_filter_bandwidth = 2.0
    odrv0.axis0.controller.config.vel_integrator_gain = 0.16 # or something
    odrv0.axis0.controller.config.vel_gain = 0.045
    odrv0.axis0.controller.config.vel_limit = 40
    odrv0.axis0.controller.config.vel_ramp_rate = 25
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv0.axis0.controller.config.input_mode = InputMode.VEL_RAMP

    odrv0.axis1.motor.config.current_lim = 30
    odrv0.axis1.motor.config.pole_pairs = 3
    odrv0.axis1.motor.config.torque_constant = 0.05
    odrv0.axis1.encoder.config.cpr = 4096
    odrv0.axis1.controller.config.input_filter_bandwidth = 2.0
    odrv0.axis1.controller.config.vel_integrator_gain = 0.16 # or something
    odrv0.axis1.controller.config.vel_gain = 0.045
    odrv0.axis1.controller.config.vel_limit = 40
    odrv0.axis1.controller.config.vel_ramp_rate = 25
    odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv0.axis1.controller.config.input_mode = InputMode.VEL_RAMP

    return odrv0

if __name__ == "__nmain__":
    odrv0 = init()

if __name__ == "__main__":
    odrv0 = init()

    # myDeviceName = "Mayflash WiiU Pro Game Controller Adapter"
    myDeviceName = "Controller (XBOX 360 For Windows)"
    myReader = controllerInputs.ControllerReader()
    myReader.openController(myDeviceName)

    prevTime = time.time()
    prevRot = odrv0.axis0.encoder.shadow_count

    ratio = 1/251373.31 # meters per indent

    t_start_accel = 0
    v_max = 51.5

    while(True): #loop

        dt = prevTime - time.time()
        dp = prevRot - odrv0.axis0.encoder.shadow_count

        if dt == 0:
            continue

        v = dp/dt # in indents/second, 4096 indents

        # 4096 indents / 1 rotation of input shaft
        # 25.71 rotations of input shaft / 1 rotation of output shaft
        # 2 rotation of output shaft / 1 rotation of wheel

        # 10.5 inch diameter of wheel, ~33 inch circumference, 0.84m

        v_speed = v * ratio

        if v_speed != 0 :
            t_start_accel = time.time()

        if v_speed == v_max:
            t_to_accel = t_start_accel - time.time()
            print("time to accel")
            print(t_to_accel)
            sys.exit()

        # print(v_speed, end="m/s\n")
        
        output = controlParse.mapControllsTwoStick(myReader.updateInputs())
        odrv0.axis0.controller.input_vel = output['rightMotorTargetSpeed']
        odrv0.axis1.controller.input_vel = -1*output['leftMotorTargetSpeed']
        #oprint(odrv0.axis0.motor.current_control.Iq_measured)
        

    # note that maximum speed is set to 30 in controlParse.py
    # 40 speed caused motor to draw more than the max set current
