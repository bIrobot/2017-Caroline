#!/usr/bin/env python3
#
# Uses the CameraServer class to automatically capture video from two USB
# webcams and send it to the FRC dashboard without doing any vision
# processing. 
#
# Warning: If you're using this with a python-based robot, do not run this
# in the same program as your robot code!
#

from cscore import CameraServer, UsbCamera
from networktables import NetworkTables
import time

def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()
    
    camera1 = cscore.UsbCamera("USB Camera 1", 0)
    camera2 = cscore.UsbCamera("USB Camera 2", 1)
    self.addCamera(camera1)
    self.addCamera(camera2)
    camera1.setResolution(640, 480)
    camera2.setResolution(640, 480)
    server = self.addServer(name="serve_" + "USB Camera")
    cameraTable = NetworkTables.getTable("Camera")
    
    while True:
        whatCamera = cameraTable.getNumber("whatCamera", 0)
        switched = cameraTable.getNumber("switched", 0)
        
        if whatCamera is 0:
            server.setSource(camera1)
        else:
            server.setSource(camera2)
        
        while switched is 0:
            switched = cameraTable.getNumber("switched", 0)
            time.sleep(0.01)

if __name__ == '__main__':
    
    # To see messages from networktables, you must setup logging
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    # You should uncomment these to connect to the RoboRIO
    #networktables.initialize(server='10.60.98.2')
    
    main()