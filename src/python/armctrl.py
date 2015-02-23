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
    port = serial.Serial("/dev/tty.usbmodem1411", 9600, serial.EIGHTBITS, serial.PARITY_EVEN, serial.STOPBITS_ONE, None, False, False, None, False, None)
    print "Connecting to " + port.name
    return port 

def serial_deinit(port):
    if port:
        port.close()

def send_to_arm(arm, angle_wrist, angle_rot_wrist, angle_hand_yaw, hand_fistedness, angle_arm, angle_arm_yaw):
    arm.write("\x02")
    # arm.write(str(int(angle_wrist) + '\n')
    # arm.write(str(angle_rot_wrist) + '\n')
    # arm.write(str(angle_hand_yaw) + '\n')
    # arm.write(str(hand_fistedness) + '\n')
    # arm.write(str(angle_arm) + '\n')
    # arm.write(str(angle_arm_yaw) + '\n')


    arm.write(str(int(angle_wrist)) + '\n')
    arm.write(str(int(angle_rot_wrist)) + '\n')
    arm.write(str(int(angle_hand_yaw)) + '\n')
    arm.write(str(int(hand_fistedness)) + '\n')
    arm.write(str(int(angle_arm)) + '\n')
    arm.write(str(int(angle_arm_yaw)) + '\n')


    # arm.write(str(angle_wrist))
    # arm.write(str(angle_rot_wrist))
    # arm.write(str(angle_hand_yaw))
    # arm.write(str(hand_fistedness))
    # arm.write(str(angle_arm))
    # arm.write(str(angle_arm_yaw))

    arm.write("\x03")
    time.sleep(0.1)

def update(controller, port):
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

    # hand yaw
    angle_hand_yaw = degrees(hand.direction.yaw)

    # how fisted the hand is
    hand_fistedness = hand.grab_strength * 100

    # arm angle
    arm = hand.arm
    if arm.is_valid:
        angle_arm = degrees(arm.direction.pitch)
        angle_arm_yaw = degrees(arm.direction.yaw)
    else:
        angle_arm = 0
        angle_arm_yaw = 0

    def print_arm_status():
        print "WriPit: %d, WriRot: %d, WriYaw: %d, Fist: %d%%, ArmPit: %d, ArmYaw: %d" % (angle_wrist, angle_rot_wrist, angle_hand_yaw, hand_fistedness, angle_arm, angle_arm_yaw)

    print_arm_status()

    send_to_arm(port, angle_wrist, angle_rot_wrist, angle_hand_yaw,hand_fistedness, angle_arm, angle_arm_yaw)


def main():
    # Create a sample controller
    controller = Leap.Controller()

    # Connect to arduino controlling the arm
    arm = serial_init()
    print("ARM: ", arm)

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
