from robotpy_ext.common_drivers.navx import AHRS
from networktables import NetworkTables

class Navx():
    BANGBANG_TOLERANCE = 7.0
    
    def __init__(self, ahrs):
        # Communicate w/navX MXP via the MXP SPI Bus.
        self.ahrs = ahrs
        
    def reset(self):
        # Reset navX position data to zero
        self.ahrs.reset()
        
    def drive(self, slowSpeed, fastSpeed, setAngle):
        gyroAngle = self.ahrs.getAngle()
        rotation = self.bangBang(slowSpeed, fastSpeed, setAngle, gyroAngle)
        return rotation
        
    def bangBang(self, slowSpeed, fastSpeed, setAngle, gyroAngle):
        if gyroAngle == setAngle:
            rotation = 0
        if (gyroAngle - setAngle) < self.BANGBANG_TOLERANCE and (setAngle - gyroAngle) < self.BANGBANG_TOLERANCE:
            if gyroAngle > setAngle:
                rotation = slowSpeed * -1
            else:
                rotation = slowSpeed
        else:
            if gyroAngle > setAngle:
                rotation = fastSpeed * -1
            else:
                rotation = fastSpeed
        return rotation