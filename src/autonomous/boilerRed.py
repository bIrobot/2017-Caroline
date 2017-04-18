from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
from components import navxStuff
from networktables import NetworkTables

class boilerRed(StatefulAutonomous):
    MODE_NAME = 'Boiler Red'
    DEFAULT = False
    
    def initialize(self):
        self.navx = navxStuff.Navx(self.ahrs)
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.counter = 0
        
    @timed_state(duration=0.5, next_state='shoot', first=True)
    def drive_wait(self):
        self.robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0) #Stop robot
        self.navx.reset()

    @timed_state(duration=8.0, next_state='turn_right')
    def shoot(self):
        self.shooter.set(0.63)
        if self.counter > 20:
            self.agitator.set(-1)
        if self.counter > 75:
            self.loader.set(1)
        self.counter += 1
        
        if self.counter < 50:
            self.robot_drive.mecanumDrive_Cartesian(-0.40, 0, 0, 0)
        else:
            self.robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0)

    @timed_state(duration=4, next_state='stop')
    def turn_right(self):
        self.shooter.set(0)
        self.agitator.set(0)
        self.loader.set(0)
        self.robot_drive.mecanumDrive_Cartesian(0, 0.35, self.navx.drive(self.sd.getNumber("slowSpeed"), self.sd.getNumber("fastSpeed"), 45), 0) #Drive forward at 45 degrees right

    @state()
    def stop(self):
        self.shooter.set(0)
        self.agitator.set(0)
        self.loader.set(0)
        self.robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0) #Stop robot
