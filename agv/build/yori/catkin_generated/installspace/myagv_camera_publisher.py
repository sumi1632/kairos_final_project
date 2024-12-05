#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class OptimizedCameraPublisher:
    def __init__(self):
        # ROS ?? ???
        rospy.init_node('optimized_camera_publisher', anonymous=True)

        # ???? ??
        self.image_publisher = rospy.Publisher('myagv/camera/image_raw', Image, queue_size=1)

        # OpenCV-ROS ??? ??
        self.bridge = CvBridge()

        # ??? ???
        self.cam = cv2.VideoCapture(0)
        if not self.cam.isOpened():
            rospy.logerr("Failed to open camera!")
            raise RuntimeError("Camera not accessible!")

        # ??? ??
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
        self.cam.set(cv2.CAP_PROP_FPS, 10)

        # ?? ?? ??
        self.rate = rospy.Rate(30)  # ?? 30???

    def publish_camera_image(self):
        while not rospy.is_shutdown():
            ret, frame = self.cam.read()
            if not ret:
                rospy.logerr("Failed to capture image!")
                continue

            # OpenCV ???? ROS ???? ??
            try:
                img_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
                self.image_publisher.publish(img_msg)
            except Exception as e:
                rospy.logerr(f"Failed to publish image: {e}")

            # ?? ??
            self.rate.sleep()

    def shutdown(self):
        # ??? ?? ??
        self.cam.release()
        rospy.loginfo("Shutting down camera publisher...")


if __name__ == '__main__':
    try:
        camera_publisher = OptimizedCameraPublisher()
        camera_publisher.publish_camera_image()
    except rospy.ROSInterruptException:
        pass

