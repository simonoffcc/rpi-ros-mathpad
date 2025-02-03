
#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

expression = ""

def keypad_callback(msg):
    global expression
    key = msg.data

    if key == 'C':
        expression = ""
    elif key == '=':
        try:
            result = str(eval(expression))
        except Exception:
            result = "Error"
        expression = ""
        rospy.loginfo(f"Calculation result: {result}")
        result_pub.publish(result)
    else:
        expression += key
    rospy.loginfo(f"Current expression: {expression}")
    result_pub.publish(expression)

def calculator_node():
    global result_pub
    rospy.init_node('calculator', anonymous=True)
    rospy.Subscriber('/calculator/input', String, keypad_callback)
    result_pub = rospy.Publisher('/calculator/result', String, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    try:
        calculator_node()
    except rospy.ROSInterruptException:
        pass
