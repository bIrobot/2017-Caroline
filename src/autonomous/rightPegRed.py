from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
from components import navxStuff
from networktables import NetworkTables

class RightPegRed(StatefulAutonomous):
    MODE_NAME = 'Right Peg Red'
    DEFAULT = False
    
    def initialize(self):
        self.navx = navxStuff.Navx(self.ahrs)
        self.sd = NetworkTables.getTable("SmartDashboard")

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0) #Stop robot
        self.navx.reset()

    @timed_state(duration=2.0, next_state='turn_left')
    def drive_forward(self):
        self.robot_drive.mecanumDrive_Cartesian(0, 0.25, self.navx.drive(self.sd.getNumber("slowSpeed"), self.sd.getNumber("fastSpeed"), 0), 0) #Drive forward and straight

    @timed_state(duration=2.93, next_state='stop')
    def turn_left(self):
        self.robot_drive.mecanumDrive_Cartesian(0, 0.25, self.navx.drive(self.sd.getNumber("slowSpeed"), self.sd.getNumber("fastSpeed"), -60), 0) #Drive forward at 45 degrees left

    @state()
    def stop(self):
        self.robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0) #Stop robot
        