from PIL import ImageTk, Image
import numpy as np
import math
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))
from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper
from test_gripper import Gripper

class PositionHandler: 
     def __init__(self, robot: URControl, ):
          self.robot = robot
          self.gripper = RobotiqGripper()
          self.init = self.init()
     
     def init(self):
          self.gripper.connect("192.168.0.2", 63352)
     
     def move_to_position(self, position: list[float]):
          self.robot.move_joint_list(position, 0.25, 0.5, 0.02)

     
               
RED_POSITION1 = [1.7446362972259521, -1.4385647040656586, 2.3446999231921595, -0.7653154295733948, 1.5420920848846436, 3.153193950653076]
RED_POSITION2 = [1.730034589767456, -1.0733220440200348, 2.283058468495504, -1.201580212717392, 1.542656660079956, 3.153193950653076]
GREEN_POSITION1 = [1.7312546968460083, -1.5535075229457398, 2.10514480272402, -0.543575720196106, 1.5416635274887085, 3.156507968902588]
#GREEN_POSITION2 = [0.8765246868133545, -1.9948517284789027, 2.2924073378192347, -0.24166639268908696, 0.8740379810333252, 3.1760315895080566]
#GREEN_POSITION3 = [0.9921266436576843, -1.5882045231261195, 2.5257766882525843, -0.9407172960093995, 1.0111021995544434, 3.141201972961426]
GREEN_POSITION2 = [1.174616813659668, -2.16580929378652, 2.3327489534961146, -0.15603549898181157, 1.1721503734588623, 3.1608855724334717]
GREEN_POSITION3 = [1.1731359958648682, -1.8137570820250453, 2.6901567617999476, -0.8645797532847901, 1.1737935543060303, 3.1583807468414307]

gripper = Gripper()
gripper.connect()

def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    positionHandler = PositionHandler(robot)
    positionHandler.move_to_position(RED_POSITION1)
    positionHandler.move_to_position(RED_POSITION2)
    gripper.close_grip()
    positionHandler.move_to_position(GREEN_POSITION1)
    positionHandler.move_to_position(GREEN_POSITION2)
    positionHandler.move_to_position(GREEN_POSITION3)
    gripper.open_grip()
    positionHandler.move_to_position(GREEN_POSITION2)
    

    #gripper.move(0,125,125)
#     joint_state = 
#     robot.move_joint_list(joint_state, 0.25, 0.5, 0.02)
#     joint_state = degreestorad([-5.61,-83.95,112.70,-119.79,-90.07,-5.48])
    
#     gripper.move(0,125,125)
#     joint_state = RED_POSITION2
#     robot.move_joint_list(joint_state, 0.25, 0.5, 0.02)
#     joint_state = degreestorad([-5.61,-83.95,112.70,-119.79,-90.07,-5.48])
    
def degreestorad(list):
     for i in range(6):
          list[i]=list[i]*(math.pi/180)
     return(list)    
 

if __name__=="__main__":
     main()
