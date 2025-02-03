#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from RPLCD.i2c import CharLCD

# Настройка LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)

def input_callback(msg):
    lcd.clear()
    lcd.write_string(f'Input:\n{msg.data}')
    rospy.loginfo(f'Displaying input: {msg.data}')

def result_callback(msg):
    lcd.clear()
    lcd.write_string(f'Result:\n{msg.data}')
    rospy.loginfo(f'Displaying result: {msg.data}')

def lcd_display_node():
    rospy.init_node('lcd_display', anonymous=True)
    rospy.Subscriber('/calculator/input', String, input_callback)
    rospy.Subscriber('/calculator/result', String, result_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        lcd_display_node()
    except (rospy.ROSInterruptException, KeyboardInterrupt):
    	lcd.clear()
    	lcd.close(clear=True)
