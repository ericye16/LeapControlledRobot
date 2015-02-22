import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../../lib/x64' if sys.maxsize > 2**32 else '../../lib/x86'
lib_dir = '../../lib'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, lib_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from math import degrees
import serial
from time import sleep

def serial_init():
    port = serial.Serial(0)
    print "Connecting to " + port.name
    return port 

def serial_deinit(port):
    if port:
        port.close()

def send_to_arm(arm, angle_wrist, angle_rot_wrist, hand_fistedness, 
    angle_hand_yaw, angle_arm, angle_arm_yaw):
    arm.write("\x02")
    arm.write(int(angle_wrist))
    # etc
    arm.write("\x03")

def update(controller, arm):
    frame = controller.frame()
    hands = frame.hands
    if hands.is_empty:
        print "No hands"
        return

    hand = frame.hands.rightmost
    if not hand.is_valid:
        print "Invalid hand" # should never print
        return

    # wrist angle
    angle_wrist = degrees(hand.direction.pitch)

    # wrist rotation angle
    angle_rot_wrist = degrees(hand.direction.roll)

    # how fisted the hand is
    hand_fistedness = hand.grab_strength

    # hand yaw
    angle_hand_yaw = degrees(hand.direction.yaw)

    # arm angle
    arm = hand.arm
    if arm.is_valid:
        angle_arm = degrees(arm.direction.pitch)
        angle_arm_yaw = degrees(arm.direction.yaw)
    else:
        angle_arm = 0
        angle_arm_yaw = 0

    def print_arm_status():
        print "Wrist: %d, Rot: %d, Fist: %d%%, Arm: %d" % (angle_wrist, angle_rot_wrist, hand_fistedness * 100, angle_arm)

    print_arm_status()

    # send_to_arm(...)

def main():
    # Create a sample controller
    controller = Leap.Controller()

    # Connect to arduino controlling the arm
    arm = None # serial_init()

    # Keep this process running until interrupted
    print "Press ctrl+c to quit..."
    try:
        while True:
            update(controller, arm)
            sleep(0.03)
    except KeyboardInterrupt:
        pass
    finally:
        # Close the serial connection when done
        serial_deinit(arm)



if __name__ == "__main__":
    main()
