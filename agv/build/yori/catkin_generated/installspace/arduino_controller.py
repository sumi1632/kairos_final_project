#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import serial

class ArduinoSerialHandler:
    def __init__(self):
        # ROS ?? ???
        rospy.init_node('arduino_controller', anonymous=True)

        # ???? ??: move_to_location ??? ???? ????
        self.pub = rospy.Publisher('move_to_location', String, queue_size=10)

        # ??? ?? ???
        self.serial_port = rospy.get_param('~serial_port', '/dev/ttyUSB0')  # ????? ?? ?? ??
        self.baud_rate = rospy.get_param('~baud_rate', 9600)               # ????? ????? ?? ??

        try:
            self.serial = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            rospy.loginfo(f"Serial connection established on {self.serial_port}")
        except serial.SerialException as e:
            rospy.logerr(f"Failed to connect to serial port: {e}")
            self.serial = None

    def read_serial_data(self):
        """??? ???? ?? 'return' ??? ??"""
        if self.serial and self.serial.in_waiting > 0:
            try:
                data = self.serial.readline().decode('utf-8').strip()
                rospy.loginfo(f"Received serial data: {data}")
                if data == "return":
                    # 'C' ???? move_to_location ??? ????
                    self.pub.publish(String("C"))
                    rospy.loginfo("Published 'C' to move_to_location")
                else:
                    rospy.logwarn(f"Unknown serial data: {data}")
            except Exception as e:
                rospy.logerr(f"Error reading serial data: {e}")

    def spin(self):
        """ROS ???? ????? read_serial_data ??"""
        rate = rospy.Rate(10)  # 10Hz
        while not rospy.is_shutdown():
            self.read_serial_data()
            rate.sleep()


if __name__ == '__main__':
    try:
        handler = ArduinoSerialHandler()
        handler.spin()
    except rospy.ROSInterruptException:
        pass
