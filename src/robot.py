#!/usr/bin/env python3
"""
    This is the most lit foundation to build robot code on
"""

import wpilib

class MyRobot(wpilib.IterativeRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        is used for initialization code.
        """
        
        # object that handles basic drive operations
        self.robot_drive = wpilib.RobotDrive(0, 1, 2, 3)
        self.robot_drive.setExpiration(0.1)
        
        self.robot_drive.setInvertedMotor(0, True)
        self.robot_drive.setInvertedMotor(1, True)
        self.robot_drive.setSafetyEnabled(True)
        
        # Initialize Gyro Board
        self.gyro = wpilib.ADXRS450_Gyro(0)
        
        # joystick 1 on the driver station
        self.stick = wpilib.Joystick(0)
        
        # initialize motors
        self.loader = wpilib.Spark(4)
        self.loader.setSafetyEnabled(True)
        self.shooter = wpilib.Spark(5)
        self.shooter.setSafetyEnabled(True)
#         self.shooter.setInverted(True)
        self.winch = wpilib.Spark(6)
        self.winch.setSafetyEnabled(True)
#         self.winch.setInverted(True)
        
        #initialize switch
#         self.flipper_switch = wpilib.DigitalInput(0)

        self.bToggle = 1

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

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        try:
            if self.stick.getRawButton(5) is True:
                self.bToggle = -1
            else:
                self.bToggle = 1
            self.robot_drive.mecanumDrive_Cartesian(self.stick.getRawAxis(1)*self.bToggle, self.stick.getRawAxis(0)*self.bToggle, self.stick.getRawAxis(4), self.gyro.getAngle())   #self.gyro.getAngle()
            wpilib.Timer.delay(0.005) # wait for a motor update time
        except:
            if not self.isFmsAttached():
                raise
        try:
            left_trig = self.stick.getRawAxis(2)
            right_trig = self.stick.getRawAxis(3)
            right_trig = -1 * right_trig
            self.winch.set((left_trig + right_trig) * 1)
        except:
            if not self.isFmsAttached():
                raise
        try:
            if self.stick.getRawButton(1) is True:
                self.loader.set(1)
                self.shooter.set(1)
            else:
                self.loader.set(0)
                self.shooter.set(0)
        except:
            if not self.isFmsAttached():
                raise
        try:
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