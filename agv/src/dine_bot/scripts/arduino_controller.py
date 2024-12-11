#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial

class ArduinoSerialHandler:
    def __init__(self):
        # ROS 노드 초기화
        rospy.init_node('arduino_serial_handler', anonymous=True)

        self.pub = rospy.Publisher('return', String, queue_size=10)

        # 시리얼 통신 초기화
        self.serial_port = rospy.get_param('~serial_port', '/dev/ttyUSB0')  # 파라미터로 포트 설정 가능
        self.baud_rate = rospy.get_param('~baud_rate', 9600)               # 파라미터로 보드레이트 설정 가능

        try:
            self.serial = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            rospy.loginfo(f"Serial connection established on {self.serial_port}")
        except serial.SerialException as e:
            rospy.logerr(f"Failed to connect to serial port: {e}")
            self.serial = None

    def read_serial_data(self):
        """시리얼 데이터를 읽고 'return' 메시지 처리"""
        if self.serial and self.serial.in_waiting > 0:
            try:
                data = self.serial.readline().decode('utf-8').strip()
                rospy.loginfo(f"Received serial data: {data}")
                if data == "return":
                    # 'C' 메시지를 move_to_location 토픽에 퍼블리시
                    self.pub.publish(String("return"))
                    rospy.loginfo("Published 'return'")
                else:
                    rospy.logwarn(f"Unknown serial data: {data}")
            except Exception as e:
                rospy.logerr(f"Error reading serial data: {e}")

    def spin(self):
        """ROS 루프에서 주기적으로 read_serial_data 호출"""
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

