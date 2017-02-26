#!/usr/bin/env python3
"""
    This is the most lit robot code for the most lit robot
"""

import wpilib
from networktables import NetworkTables
from robotpy_ext.autonomous.selector import AutonomousModeSelector
# from robotpy_ext.common_drivers import navx

class MyRobot(wpilib.IterativeRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        is used for initialization code.
        """
        # joystick 1 on the driver station
        self.stick = wpilib.XboxController(0)
        self.rbToggle = 0
        
        # start camera server
        wpilib.CameraServer.launch('vision.py:main')
        
        # networktable stuff
        self.cameraTable = NetworkTables.getTable("Camera")
        
        # Channels for the wheels
        frontLeftChannel    = 0
        rearLeftChannel     = 1
        frontRightChannel   = 2
        rearRightChannel    = 3
        
        # object that handles basic drive operations
        self.robot_drive = wpilib.RobotDrive(frontLeftChannel, rearLeftChannel,
                                         frontRightChannel, rearRightChannel)
        self.robot_drive.setInvertedMotor(0, True)
        self.robot_drive.setInvertedMotor(1, True)
#         self.robot_drive.setExpiration(0.1)

        # initialize motors other than drive
        self.loader = wpilib.Spark(4)
        self.shooter = wpilib.Spark(5)
        self.intake = wpilib.Spark(6)
        self.winch = wpilib.Spark(7)
        self.agitator = wpilib.Spark(8)
        
        self.components = {
            'robot_drive': self.robot_drive,
        }
        self.automodes = AutonomousModeSelector('autonomous', self.components)
        

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        self.automodes.run()
        
    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        try:
            xAxis = self.stick.getRawAxis(0) #Get joystick value
            xAxis = self.normalize(xAxis, 0.1) #Set deadzone
            xAxis = self.joystickAdjust(xAxis, 0.5) #Adjust sensitivity
            
            yAxis = self.stick.getRawAxis(1)
            yAxis = self.normalize(yAxis, 0.1)
            yAxis = self.joystickAdjust(yAxis, 0.5)
            
            rotation = self.stick.getRawAxis(4)
            rotation = self.normalize(rotation, 0.1)
            rotation = self.joystickAdjust(rotation, 0.5)
            
            leftTrigger = self.stick.getRawAxis(2)
            leftTrigger = self.normalize(leftTrigger, 0.05)
            
            rightTrigger = self.stick.getRawAxis(3)
            rightTrigger = self.normalize(rightTrigger, 0.05)
            
            gyroAngle = 0
            self.robot_drive.mecanumDrive_Cartesian(xAxis, yAxis, rotation, gyroAngle)
 
            if self.stick.getBumper("left") is True:
                self.winch.set(1)
            else:
                self.winch.set(0)
                
            if leftTrigger > 0:
                self.intake.set(0.65)
            else:
                self.intake.set(0)
                
            if rightTrigger > 0:
                self.shooter.set(0.70387)
                self.agitator.set(1)
                self.loader.set(1)
            else:
                self.shooter.set(0)
                self.agitator.set(0)
                self.loader.set(0)

            if self.stick.getYButton() is True:
                self.stick.rightRumble = int(1 * 65535)
                self.stick.leftRumble = int(1 * 65535)
            else:
                self.stick.rightRumble = int(0 * 65535)
                self.stick.leftRumble = int(0 * 65535)
                
            if self.stick.getBumper("right") is True:
                if self.rbToggle is 0:
                    self.rbToggle = 1
                else:
                    self.rbToggle = 0
                self.cameraTable.putNumber("switched", 1)
            else:
                self.cameraTable.putNumber("switched", 0)
            self.cameraTable.putNumber("whatCamera", self.rbToggle)
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
