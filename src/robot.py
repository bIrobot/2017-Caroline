#!/usr/bin/env python3
"""
    This is the most lit foundation to build robot code on
"""

import wpilib
# from robotpy_ext.common_drivers import navx
# from robotpy_ext.common_drivers import xl_max_sonar_ez
from networktables import NetworkTable
import networktables

class MyRobot(wpilib.IterativeRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        is used for initialization code.
        """
        # joystick 1 on the driver station
        self.stick = wpilib.Joystick(0)
        
        # object that handles basic drive operations
        self.robot_drive = wpilib.RobotDrive(0, 1, 2, 3)
        self.robot_drive.setInvertedMotor(0, True)
        self.robot_drive.setInvertedMotor(1, True)
        self.robot_drive.setSafetyEnabled(True)
        self.robot_drive.setExpiration(0.1)
        
        # initialize motors
        self.loader = wpilib.Spark(4)
        self.shooter = wpilib.Spark(5)
        self.winch = wpilib.Spark(6)
        
        # Initialize Gyro
        self.gyro = wpilib.ADXRS450_Gyro(0)
        
        # Initialize Accelerometer
#         self.accelerometer = wpilib.ADXL362(8, 0)
        
                
        #initialize switch
#         self.gear_switch = wpilib.DigitalInput(0)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.auto_loop_counter = 0

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        try:
            # Check if we've completed 100 loops (approximately 2 seconds)
            if self.auto_loop_counter < 100:
                self.robot_drive.mecanumDrive_Cartesian(-0.1, 0, 0, 0) # Drive forwards
                self.auto_loop_counter += 1
            else:
                self.robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0)    #Stop robot
        except:
            if not self.isFmsAttached():
                raise

    def teleopInit(self):
        wpilib.IterativeRobot.teleopInit(self)
        
        xAxis = 0
        yAxis = 0
        rotation = 0
        gyroAngle = 0

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        try:
            xAxis = self.stick.getRawAxis(1)*-0.5
            yAxis = self.stick.getRawAxis(0)*-0.5
            rotation = self.stick.getRawAxis(4)*0.25
#             gyroAngle = self.gyro.getAngle()
            self.robot_drive.mecanumDrive_Cartesian(xAxis, yAxis, rotation, gyroAngle)
            
            left_trig = self.stick.getRawAxis(2)
            right_trig = self.stick.getRawAxis(3)
            right_trig = -1 * right_trig
            self.winch.set((left_trig + right_trig) * 1)
 
            if self.stick.getRawButton(1) is True:
                self.loader.set(1)
                self.shooter.set(1)
            else:
                self.loader.set(0)
                self.shooter.set(0)

            if self.stick.getRawButton(4) is True:
                self.stick.setRumble(0, 1)
                self.stick.setRumble(1, 1)
            else:
                self.stick.setRumble(0, 0)
                self.stick.setRumble(1, 0)
        except:
            if not self.isFmsAttached():
                raise
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()
        
    def disabledInit(self):
        wpilib.IterativeRobot.disabledInit(self)
         
if __name__ == "__main__":
    wpilib.run(MyRobot)