#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import threading
import time

class OptimizedCameraPublisher:
    def __init__(self):
        # ROS ³ëµå ÃÊ±âÈ­
        rospy.init_node('optimized_camera_publisher', anonymous=True)

        # ÀÌ¹ÌÁö ÆÛºí¸®¼Å »ý¼º
        self.image_publisher = rospy.Publisher('myagv/camera/image_raw', Image, queue_size=1)

        # OpenCV-ROS ºê¸´Áö »ý¼º
        self.bridge = CvBridge()

        # Ä«¸Þ¶ó ÃÊ±âÈ­
        self.cam = cv2.VideoCapture(0)
        if not self.cam.isOpened():
            rospy.logerr("Failed to open camera!")
            raise RuntimeError("Camera not accessible!")

        # Ä«¸Þ¶ó ¼³Á¤ (ÇØ»óµµ ¹× FPS)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
        self.cam.set(cv2.CAP_PROP_FPS, 10)

        # Ä«¸Þ¶ó¿¡¼­ ÇÁ·¹ÀÓÀ» ÀÐ±â À§ÇÑ ½º·¹µå ½ÃÀÛ
        self.running = True
        self.frame = None
        self.lock = threading.Lock()
        self.capture_thread = threading.Thread(target=self.capture_frames)
        self.capture_thread.start()

        # ·çÇÁ ÁÖ±â ¼³Á¤
        self.rate = rospy.Rate(10)  # Ä«¸Þ¶ó FPS¿Í µ¿ÀÏÇÏ°Ô ¼³Á¤

    def capture_frames(self):
        """Ä«¸Þ¶ó ÇÁ·¹ÀÓÀ» Áö¼ÓÀûÀ¸·Î ÀÐ¾î¿À´Â ½º·¹µå"""
        while self.running:
            ret, frame = self.cam.read()
            if ret:
                with self.lock:
                    self.frame = frame
            else:
                rospy.logerr("Failed to capture image!")
                self.frame = None
            time.sleep(0.01)  # ¾à°£ÀÇ Áö¿¬À» Ãß°¡ÇÏ¿© CPU ºÎÇÏ °¨¼Ò

    def publish_camera_image(self):
        """Ä¸Ã³µÈ ÇÁ·¹ÀÓÀ» ÆÛºí¸®½ÃÇÏ´Â ÇÔ¼ö"""
        while not rospy.is_shutdown():
            with self.lock:
                if self.frame is not None:
                    try:
                        img_msg = self.bridge.cv2_to_imgmsg(self.frame, encoding='bgr8')
                        img_msg.header.frame_id = "camera_frame"  # ÇÁ·¹ÀÓ ID Ãß°¡
                        self.image_publisher.publish(img_msg)
                    except Exception as e:
                        rospy.logerr(f"Failed to publish image: {e}")

            # ·çÇÁ ÁÖ±â Á¶Àý
            self.rate.sleep()

    def shutdown(self):
        # ³ëµå Á¾·á ½Ã Ä«¸Þ¶ó ÀÚ¿ø ÇØÁ¦
        self.running = False
        self.capture_thread.join()
        self.cam.release()
        rospy.loginfo("Shutting down camera publisher...")

if __name__ == '__main__':
    camera_publisher = None
    try:
        camera_publisher = OptimizedCameraPublisher()
        camera_publisher.publish_camera_image()
    except rospy.ROSInterruptException:
        rospy.loginfo("ROS Interrupt received.")
    finally:
        if camera_publisher:
            camera_publisher.shutdown()

