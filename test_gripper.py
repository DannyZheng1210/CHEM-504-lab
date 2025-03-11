
from robotiq.robotiq_gripper import RobotiqGripper

HOST = "192.168.0.2"
PORT = 30003

class Gripper:
    
    def __init__(self):
        self.host = "192.168.0.2"
        self.port= 63352
        self.gripper = RobotiqGripper()

    def connect(self):
        #tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #tcp_socket.connect((HOST, PORT))
        #gripper=RobotiqGripper()
        self.gripper.connect(self.host, self.port)
        # gripper.activate()
    
    def close_grip(self):
        self.gripper.move(255, 255, 255)
    
    def open_grip(self):
        self.gripper.move(0, 255, 255)


gripper = Gripper()
gripper.connect()
gripper.open_grip()
