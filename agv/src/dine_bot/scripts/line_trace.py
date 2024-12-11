#!/usr/bin/env python3
import rospy
from pymycobot.myagv import MyAgv
from std_msgs.msg import String

class LineTraceNode:
    def __init__(self):
        # AGV 객체 생성
        self.agv = MyAgv('/dev/ttyAMA2', 115200)
        
        # ROS 노드 초기화
        rospy.init_node('line_trace_node', anonymous=True)
        
        # 토픽 구독 설정
        rospy.Subscriber('/line_trace', String, self.line_trace_callback)
        rospy.loginfo("AGV control node started. Listening to /line_trace topic.")

    def agv_move(self, direction, speed=5, timeout=0.5):
        """AGV 이동 명령 함수"""
        if direction == 'left':
            self.agv.counterclockwise_rotation(int(speed), timeout=float(timeout))
        elif direction == 'right':
            self.agv.clockwise_rotation(int(speed), timeout=float(timeout))
        elif direction == 'go':
            self.agv.go_ahead(int(speed), timeout=float(timeout))
        elif direction == 'stop':
            self.agv.stop()

    def line_trace_callback(self, msg):
        """콜백 함수: 명령을 처리"""
        try:
            # 방향 명령 처리 (right, left, go, stop)
            direction = msg.data.strip()
            if direction in ['right', 'left', 'go', 'stop']:
                self.agv_move(direction)
                rospy.loginfo(f"Executed command: {direction}")
            else:
                rospy.logwarn(f"Unknown command: {direction}")
        except Exception as e:
            rospy.logerr(f"Failed to execute command: {e}")

    def run(self):
        """ROS 노드 실행"""
        rospy.spin()

if __name__ == '__main__':
    try:
        node = LineTraceNode()
        node.run()
    except rospy.ROSInterruptException:
        pass
