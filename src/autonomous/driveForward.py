from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
from robotpy_ext.common_drivers.navx import AHRS
        
class DriveForward(StatefulAutonomous):
    MODE_NAME = 'Drive Forward'
    DEFAULT = True
    
    # The following PID Controller coefficients will need to be tuned */
    # to match the dynamics of your drive system.  Note that the      */
    # SmartDashboard in Test mode has support for helping you tune    */
    # controllers by displaying a form where you can enter new P, I,  */
    # and D constants and test the mechanism.                         */
     
    # Often, you will find it useful to have different parameters in
    # simulation than what you use on the real robot
     
    # These PID parameters are used on a real robot
    kP = 0.03 #needs to be smaller
    kI = 0.00 #need to set something
    kD = 0.00 #don't know if we should use it
    kF = 0.00
    
    kToleranceDegrees = 2.0
    
    def initialize(self):
        
        # Communicate w/navX MXP via the MXP SPI Bus.
        self.ahrs = AHRS.create_spi()
         
        turnController = self.PIDController(self.kP, self.kI, self.kD, self.kF, self.ahrs, output=self)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(self.kToleranceDegrees)
        turnController.setContinuous(True)
         
        self.turnController = turnController
        
        # Add the PID Controller to the Test-mode dashboard, allowing manual  */
        # tuning of the Turn Controller's P, I and D coefficients.            */
        # Typically, only the P value needs to be modified.                   */
        self.addActuator("DriveSystem", "RotateController", turnController)
        
        self.ahrs.reset()
        self.turnController.disable()

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0) #Stop robot

    @timed_state(duration=4.3, next_state='stop')
    def drive_forward(self):
        self.turnController.setSetpoint(0.0)
        self.turnController.enable()
        rotation = self.rotateToAngleRate
        gyroAngle = self.ahrs.getAngle()
        self.robot_drive.mecanumDrive_Cartesian(0, 0.25, rotation*-1, gyroAngle) #Drive forwards and straight (hopefully)
#         print("NavX Gyro", self.ahrs.getYaw(), self.ahrs.getAngle())

    @state()
    def stop(self):
        self.robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0) #Stop robot
        
    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        self.rotateToAngleRate = output