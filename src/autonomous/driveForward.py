from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
        
class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Drive Forward'
    DEFAULT = True

    def initialize(self):
        pass

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0) #Stop robot

    @timed_state(duration=5, next_state='stop')
    def drive_forward(self):
        self.robot_drive.mecanumDrive_Cartesian(0, -0.5, 0, 0) #Drive forwards
        
    @state()
    def stop(self):
        self.robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0) #Stop robot