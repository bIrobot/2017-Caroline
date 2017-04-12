#!/usr/bin/env python3
"""
    This is the most lit robot code for the most lit robot
"""

import wpilib
from networktables import NetworkTables
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from robotpy_ext.common_drivers.navx import AHRS
from hal.functions import isSimulation
isSimulation = wpilib.RobotBase.isSimulation()
if isSimulation:
    pass
else:
    from cscore import CameraServer, UsbCamera
    import cscore

class MyRobot(wpilib.IterativeRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        is used for initialization code.
        """
        self.ahrs = AHRS.create_spi(update_rate_hz=100)
        
        # joystick 1 on the driver station
        self.stick = wpilib.XboxController(0)
        
        if isSimulation:
            pass
        else:
            cs = CameraServer.getInstance()
            cs.enableLogging()
            self.camera1 = cscore.UsbCamera("USB Camera 0", 0)
            self.camera2 = cscore.UsbCamera("USB Camera 1", 1)
            self.camera1.setResolution(320, 240)
            self.camera2.setResolution(320, 240)
            self.camera1.setFPS(20)
            self.camera2.setFPS(20)
            cs.addCamera(self.camera1)
            cs.addCamera(self.camera2)
            self.server = cs.addServer(name="serve_USBCamera")
            self.server.setSource(self.camera2)
        
        # Channels for the wheels
        frontLeftChannel    = 0
        rearLeftChannel     = 1
        frontRightChannel   = 2
        rearRightChannel    = 3
        
        # object that handles basic drive operations
        self.robot_drive = wpilib.RobotDrive(frontLeftChannel, rearLeftChannel,
                                         frontRightChannel, rearRightChannel)
        self.robot_drive.setExpiration(0.25)
        
        # invert motors
        self.robot_drive.setInvertedMotor(0, True)
        self.robot_drive.setInvertedMotor(2, True)

        # initialize motors other than drive
        self.loader = wpilib.Spark(4)
        self.shooter = wpilib.Spark(5)
        self.intake = wpilib.Spark(6)
        self.winch = wpilib.Spark(7)
        self.agitator = wpilib.Spark(8)
        
        # objects that get passed to the autonomous modes
        self.components = {
            'ahrs': self.ahrs,
            'robot_drive': self.robot_drive,
            'loader': self.loader,
            'shooter': self.shooter,
            'agitator': self.agitator,
            'addActuator': wpilib.LiveWindow.addActuator
        }
        self.automodes = AutonomousModeSelector('autonomous', self.components)
        
        # live editable motor speed values used by the bang bang controller during autonomous
        sd = NetworkTables.getTable("SmartDashboard")
        sd.putNumber('slowSpeed', 0.07) # set default values
        sd.putNumber('fastSpeed', 0.2)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        
    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        self.automodes.run()
        
    def teleopInit(self):
        wpilib.IterativeRobot.teleopInit(self)
        
        # reset the navx
        self.ahrs.reset()
        
        # initialize variables used by teleopPeriodic for various toggles
        self.cameraToggle = 0
        self.driveToggle = 1
        self.FODtoggle = 1 # don't start in FOD drive
        
        # initialize variables used by teleopPeriodic for timing of motors
        self.beforeButton = 0
        self.afterButton = 0
        
    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        try:
            if self.stick.getRawButton(6) is True: # right bumber
                if self.FODtoggle is 0:
                    self.FODtoggle = 1
                else:
                    self.FODtoggle = 0
#                     self.ahrs.reset()
                self.stick.rightRumble = int(1 * 65535)
                self.stick.leftRumble = int(1 * 65535)
                wpilib.Timer.delay(0.19)
                self.stick.rightRumble = int(0 * 65535)
                self.stick.leftRumble = int(0 * 65535)
            if self.FODtoggle is 0:
                self.gyroAngle = self.ahrs.getAngle()
                if self.stick.getRawButton(4) is True: # Y button
                    if self.cameraToggle is 0:
                        self.cameraToggle = 1
                    else:
                        self.cameraToggle = 0
                    wpilib.Timer.delay(0.2)
            else:
                self.gyroAngle = 0
                if self.stick.getRawButton(4) is True: # Y button
                    if self.cameraToggle is 0:
                        self.cameraToggle = 1
                        self.driveToggle = -1
                    else:
                        self.cameraToggle = 0
                        self.driveToggle = 1
                    wpilib.Timer.delay(0.2)
            if isSimulation:
                pass
            else:
                if self.cameraToggle is 0:
                    self.server.setSource(self.camera1)
                else:
                    self.server.setSource(self.camera2)
        except:
            if not self.isFmsAttached():
                raise
        try:
            xAxis = self.stick.getRawAxis(0) # Get joystick value
            xAxis = self.normalize(xAxis, 0.1) # Set deadzone
            xAxis = self.joystickAdjust(xAxis, 0.5) # Adjust sensitivity
            xAxis = xAxis * self.driveToggle
            
            yAxis = self.stick.getRawAxis(1)
            yAxis = self.normalize(yAxis, 0.1)
            yAxis = self.joystickAdjust(yAxis, 0.5)
            yAxis = yAxis * self.driveToggle
            
            rotation = self.stick.getRawAxis(4) # x axis right joystick
            rotation = self.normalize(rotation, 0.1)
            rotation = self.joystickAdjust(rotation, 0.5)
            
            leftTrigger = self.stick.getRawAxis(2)
            leftTrigger = self.normalize(leftTrigger, 0.05)
            
            rightTrigger = self.stick.getRawAxis(3)
            rightTrigger = self.normalize(rightTrigger, 0.05)

            # send motor values to drive function
            self.robot_drive.mecanumDrive_Cartesian(xAxis, yAxis, rotation, self.gyroAngle + 180)
#             wpilib.Timer.delay(0.005)
        except:
            if not self.isFmsAttached():
                raise
        try:
            if self.stick.getRawButton(5) is True: #left bumper
                self.winch.set(-1)
            else:
                self.winch.set(0)
                
            if leftTrigger > 0:
                if self.stick.getRawButton(1): # A button
                    self.intake.set(1)
                else:
                    self.intake.set(0.65)
            else:
                self.intake.set(0)
                
            if rightTrigger > 0:
                if self.stick.getRawButton(1): # A button
                    self.shooter.set(1)
                else:
                    self.shooter.set(0.62)
                if self.afterButton > 20:
                    self.agitator.set(-1)
                if self.afterButton > 50:
                    self.loader.set(1)
                self.beforeButton = 0
                self.afterButton += 1
            else:
                self.shooter.set(0)
                if self.beforeButton < 10:
                    self.agitator.set(1)
                else:
                    self.agitator.set(0)
                self.loader.set(0)
                self.afterButton = 0
                self.beforeButton += 1

        except:
            if not self.isFmsAttached():
                raise

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()
        
    def disabledInit(self):
        wpilib.IterativeRobot.disabledInit(self)
        
    def normalize(self, input, deadzone):
        """Input should be between -1 and 1, deadzone should be between 0 and 1."""
        if input > 0:
            if (input - deadzone) < 0:
                return 0
            else:
                return ((input - deadzone)/(1 - deadzone))
        elif input < 0:
            if (input + deadzone) > 0:
                return 0
            else:
                return ((input + deadzone)/(1 - deadzone))
        else:
            return 0
    
    def joystickAdjust(self, input, constant):
        """Input should be between -1 and 1, constant should be between 0 and 1."""
        adjustedValues = constant * (input**3) + (1 - constant) * input
        return adjustedValues
    
if __name__ == "__main__":
    wpilib.run(MyRobot)
