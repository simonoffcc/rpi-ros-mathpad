#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import time
import RPi.GPIO as GPIO

# Настройка матричной клавиатуры
KEYPAD = [
    ['1', '2', '3', '+'],
    ['4', '5', '6', '-'],
    ['7', '8', '9', '*'],
    ['C', '0', '=', '/']
]

ROWS = [6, 13, 19, 26]
COLS = [5, 21, 20, 16]

GPIO.setmode(GPIO.BCM)

for row_pin in ROWS:
    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for col_pin in COLS:
    GPIO.setup(col_pin, GPIO.OUT)
    GPIO.output(col_pin, GPIO.HIGH)

def get_key():
    key = None
    for col_num, col_pin in enumerate(COLS):
        GPIO.output(col_pin, GPIO.LOW)
        for row_num, row_pin in enumerate(ROWS):
            if GPIO.input(row_pin) == GPIO.LOW:
                key = KEYPAD[row_num][col_num]
                while GPIO.input(row_pin) == GPIO.LOW:
                    time.sleep(0.05)
        GPIO.output(col_pin, GPIO.HIGH)
    return key

def keypad_node():
    rospy.init_node('keypad_input', anonymous=True)
    pub = rospy.Publisher('/calculator/input', String, queue_size=10)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        key = get_key()
        if key:
            pub.publish(key)
            rospy.loginfo(f"Key pressed: {key}")
            time.sleep(0.2)
        rate.sleep()

if __name__ == '__main__':
    try:
        keypad_node()
    except rospy.ROSInterruptException:
        GPIO.cleanup()

