# !/usr/bin/env python3
# 
#  Uses the CameraServer class to automatically capture video from two USB
#  webcams and send it to the FRC dashboard without doing any vision
#  processing. 
# 
#  Warning: If you're using this with a python-based robot, do not run this
#  in the same program as your robot code!

from networktables import NetworkTables
from cscore import CameraServer, UsbCamera
import cscore
import time
 
def main():
    cameraTable = NetworkTables.getTable("Camera")
     
    cs = CameraServer.getInstance()
    cs.enableLogging()
    camera1 = cscore.UsbCamera("USB Camera 0", 0)
    camera2 = cscore.UsbCamera("USB Camera 1", 1)
    camera1.setResolution(640, 480)
    camera2.setResolution(640, 480)
#     camera1.setFPS(10)
#     camera2.setFPS(10)
    cs.addCamera(camera1)
    cs.addCamera(camera2)
    server = cs.addServer(name="serve_USBCamera")
#     #if this ^ doesn't work, switch with next lines and uncomment
#     camera1.setVideoMode(cscore.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
#     camera2.setVideoMode(cscore.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
#     server = cs.MjpegServer("serve_USBCamera", 1181) #1181
#     
#     cs.waitForever()
    server.setSource(camera1)

    while True:
        whatCamera = cameraTable.getNumber("whatCamera", 0)
        switched = cameraTable.getNumber("switched", 0)

        if whatCamera is 0:
#             cs.removeCamera(camera2)
#             cs.addCamera(camera1)
            server.setSource(camera1)
        else:
#             cs.removeCamera(camera1)
#            cs.addCamera(camera2)
            server.setSource(camera2)
        while switched is 0:
            switched = cameraTable.getNumber("switched", 0)
            time.sleep(0.001)
#         if whatCamera is 0:
#             cs.removeCamera(camera1)
#         else:
#             cs.removeCamera(camera2)
        time.sleep(0.5)
 
if __name__ == '__main__':
     
    # To see messages from networktables, you must setup logging
    import logging
    logging.basicConfig(level=logging.DEBUG)
     
    # You should uncomment these to connect to the RoboRIO
    #networktables.initialize(server='10.60.98.2')
     
    main()
