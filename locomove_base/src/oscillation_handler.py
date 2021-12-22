#!/usr/bin/env python2

import rospy
from geometry_msgs.msg import Twist
from rospy.topics import Publisher

class oscillation_handler:
    def __init__(self):
        rospy.init_node('cmd_vel_manipulator', anonymous=False)

        self.theta_velocity_buffer = []
        self.oscillation_flag = False
        self.oscillation_mode = 8
        self.oscillation_last_element = 1
        self.manipulator_twist = Twist()

        self.cmd_sub = rospy.Subscriber("/cmd_vel", Twist, self.cmd_callback)
        self.cmd_pub = rospy.Publisher("/handler_vel", Twist, queue_size=0)

        self.rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            if(self.oscillation_flag == True):
                print("titresim var")
                self.manipulator_twist.angular.z = self.oscillation_last_element*1.5
                for i in range(0,20):
                    self.cmd_pub.publish(self.manipulator_twist)
                    print("publishliyorum")
            else:
                print("publishlemiyorum")

        self.rate.sleep()

    def double_equal(self, a, b, epsilon=0.001):
        if(a != 0 and b != 0):
            return abs(a-b) < epsilon
        else:
            return False
        
    def cmd_callback(self, data):
        if(len(self.theta_velocity_buffer) < 8):
            self.theta_velocity_buffer.append(data.angular.z)
        else:
            self.theta_velocity_buffer.pop(0)
            self.theta_velocity_buffer.append(data.angular.z)
    
            a = self.theta_velocity_buffer[3]
            b = self.theta_velocity_buffer[4]

            if((self.theta_velocity_buffer[0] == self.theta_velocity_buffer[1]) and (self.theta_velocity_buffer[1] == self.theta_velocity_buffer[2])
                and (self.theta_velocity_buffer[2] == self.theta_velocity_buffer[3]) and (self.theta_velocity_buffer[4] == self.theta_velocity_buffer[5]) 
                and (self.theta_velocity_buffer[5] == self.theta_velocity_buffer[6]) and (self.theta_velocity_buffer[6] == self.theta_velocity_buffer[7])
                and self.double_equal(a,(-1)*b)):
                rospy.logwarn("Titriyoz haa 8")
                self.oscillation_flag = True
                self.oscillation_mode = 8
                self.oscillation_last_element = self.theta_velocity_buffer[7]

            elif((self.theta_velocity_buffer[1] == self.theta_velocity_buffer[2]) and (self.theta_velocity_buffer[2] == self.theta_velocity_buffer[3])
                and (self.theta_velocity_buffer[4] == self.theta_velocity_buffer[5]) and (self.theta_velocity_buffer[5] == self.theta_velocity_buffer[6])
                and self.double_equal(a,(-1)*b)):
                rospy.logwarn("Titriyoz haa 6")
                self.oscillation_flag = True
                self.oscillation_mode = 6

            else:
                self.oscillation_flag = False


if __name__ == '__main__':
    try:
        oscillation_handler()
    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")
