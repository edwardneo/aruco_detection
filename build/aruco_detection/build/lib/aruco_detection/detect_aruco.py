import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ArUcoTracker(Node):
    def __init__(self):
        super().__init__('aruco_tracker')
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.subscription = self.create_subscription(
            Image,
            '/vimba_front_left_center/image',
            self.image_callback,
            qos_profile)
        self.bridge = CvBridge()
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250) # May need to change depending on marker
        self.parameters = cv2.aruco.DetectorParameters_create()

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        corners, ids, rejected = cv2.aruco.detectMarkers(cv_image, self.aruco_dict, parameters=self.parameters)

        if len(corners) > 0:
            cv2.aruco.drawDetectedMarkers(cv_image, corners, ids)
            print(f"{len(corners)} marker(s) detected!")
            

        cv2.imshow('ArUco Tracker', cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    aruco_tracker = ArUcoTracker()
    rclpy.spin(aruco_tracker)
    cv2.destroyAllWindows()
    aruco_tracker.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
