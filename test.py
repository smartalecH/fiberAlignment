"""Thorlabs DCx series cameras
Drivers for Windows and Linux can be downloaded from Thorlabs__.
__ http://www.thorlabs.de/software_pages/viewsoftwarepage.cfm?code=DCx
Python implementation of ueye interface: https://github.com/bernardokyotoku/pydcu
"""

from __future__ import print_function
import sys
import ctypes
from ctypes import byref, c_double, c_int
import numpy as np
from .camera import Camera
from .exceptions import ThorlabsDCxError

class CamInfo(ctypes.Structure):
    _fields_ = [
        ("SerNo", ctypes.c_char*12),
        ("ID", ctypes.c_char*20),
        ("Version", ctypes.c_char*10),
        ("Date", ctypes.c_char*12),
        ("Select", ctypes.c_byte),
        ("Type", ctypes.c_byte),
        ("Reserved", ctypes.c_char)
    ]

class ThorlabsDCx(Camera):
    """Class for Thorlabs DCx series cameras."""

    # Setup and shutdown
    # -------------------------------------------------------------------------

    # TODO: Change to use a logger!
    def _chk(self, msg):
        """Check for errors from the C library."""
        if msg:
            if msg == 127:
                print("Out of memory, probably because of a memory leak!!!")
            if msg == 125:
                print(
                    "125: IS_INVALID_PARAMETER: One of the submitted " + \
                    "parameters is outside the valid range or is not " + \
                    "supported for this sensor or is not available in this mode.")
            print("msg:", msg)

    def _initialize(self, **kwargs):
        """Initialize the camera."""
        # Load the library.
        if 'win' in sys.platform:
            try:
                self.clib = ctypes.cdll.uc480_64
            except:
                self.clib = ctypes.cdll.uc480
        else:
            self.clib = ctypes.cdll.LoadLibrary('libueye_api.so')

        # Initialize the camera. The filehandle being 0 initially
        # means that the first available camera will be used. This is
        # not really the right way of doing things if there are
        # multiple cameras installed, but it's good enough for a lot
        # of cases.
        number_of_cameras = ctypes.c_int(0)
        self._chk(self.clib.is_GetNumberOfCameras(byref(number_of_cameras)))
        if number_of_cameras.value < 1:
            raise ThorlabsDCxError("No camera detected!")
        self.filehandle = ctypes.c_int(0)
        self._chk(self.clib.is_InitCamera(
            ctypes.pointer(self.filehandle)))

        # Resolution of camera. (height, width)
        self.shape = (1024, 1280)

        # Allocate memory. Declare variables for storing memory ID and
        # memory start location:
        self.pid = ctypes.c_int()
        self.ppcImgMem = ctypes.c_char_p()

        # Allocate the right amount of memory:
        bitdepth = 8 # Camera is 8 bit.
        self._chk(self.clib.is_AllocImageMem(
            self.filehandle, self.shape[1], self.shape[0],
            bitdepth, byref(self.ppcImgMem),  byref(self.pid)))

        # Tell the driver to use the newly allocated memory:
        self._chk(self.clib.is_SetImageMem(self.filehandle, self.ppcImgMem , self.pid))

        # Enable autoclosing. This allows for safely closing the
        # camera if it is disconnected.
        self._chk(self.clib.is_EnableAutoExit(self.filehandle, 1))

    def get_camera_properties(self):
        filename = 'thorlabs_dcx.json'
        self.logger.warning("Warning: Warnings do not work!")
        self.props.load(filename)

    def close(self):
        """Close the camera safely."""
        self._chk(self.clib.is_ExitCamera(self.filehandle))

    # Image acquisition
    # -------------------------------------------------------------------------

    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""

    def _acquire_image_data(self):
        """Code for getting image data from the camera should be
        placed here.
        """
        # Allocate memory for image:
        img_size = self.shape[0]*self.shape[1]/self.bins**2
        c_array = ctypes.c_char*img_size
        c_img = c_array()

        # Take one picture: wait time is waittime * 10 ms:
        waittime = c_int(20)
        self._chk(self.clib.is_FreezeVideo(self.filehandle, waittime))

        # Copy image data from the driver allocated memory to the
        # memory that we allocated.
        self._chk(self.clib.is_CopyImageMem(self.filehandle, self.ppcImgMem, self.pid, c_img))

        # Pythonize and return
        img_array = np.frombuffer(c_img, dtype=ctypes.c_ubyte)
        img_array.shape = np.array(self.shape)
        return img_array

    # Triggering
    # -------------------------------------------------------------------------

    def get_trigger_mode(self):
        """Query the current trigger mode."""

    def set_trigger_mode(self, mode):
        """Setup trigger mode."""

    def trigger(self):
        """Send a software trigger to take an image immediately."""

    def start(self):
        """Do nothing for this camera."""
        pass

    def stop(self):
        """Do nothing for this camera."""
        pass

    # Gain and exposure time
    # -------------------------------------------------------------------------

    def _update_exposure_time(self, t):
        """Set the exposure time."""
        IS_EXPOSURE_CMD_SET_EXPOSURE = 12
        nCommand =  IS_EXPOSURE_CMD_SET_EXPOSURE
        Param = c_double(t)
        SizeOfParam = 8
        self._chk(self.clib.is_Exposure(self.filehandle, nCommand, byref(Param), SizeOfParam))

    def get_gain(self):
        """Query the current gain settings."""

    def set_gain(self, gain, **kwargs):
        """Set the camera gain."""

if __name__ == "__main__":
    with ThorlabsDCx() as cam:
        pass
    """This was in the class. It shouldn't have been!
    def test(self):
        print("Testing camera:")
        os_version = self.clib.is_GetOsVersion()
        print("OS version:",os_version)
        if os_version == 12:
            print("Windows 7")
        number_of_cameras = ctypes.c_int(0)
        mypoint = ctypes.pointer(number_of_cameras)
        self.clib.is_GetNumberOfCameras(mypoint)
        print("Number of cameras:",number_of_cameras.value)
        if number_of_cameras >= 1:
            return_value = ctypes.c_int()
            caminfo = CamInfo()
            return_value = self.clib.is_GetCameraInfo(self.filehandle, ctypes.pointer(caminfo))
            if return_value == 0:
                print("SerNo: ",caminfo.SerNo)
                print("ID: ",caminfo.ID)
                print("Version: ",caminfo.Version)
                print("Date: ",caminfo.Date)
                print("Select: ",caminfo.Select)
                print("Type: ",caminfo.Type)
                print("Reserved: ", caminfo.Reserved)
            else:
                print("No camera detected!")
                print("returned:",return_value)
            # Allocate image storage
            img_size = self.shape[0]*self.shape[1]/self.bins**2
            c_array = ctypes.c_char*img_size
            c_img = c_array()
            print(self.shape)
            pid = ctypes.c_int()
            mem = ctypes.c_char_p
            ppcImgMem = mem()
            self._chk(self.clib.is_AllocImageMem(self.filehandle, 1280, 1024, 8, byref(ppcImgMem),  byref(pid)))

            print("Inquiring about memory:")
            print(pid)
            width = c_int()
            height = c_int()
            bitdepth = c_int()
            self._chk(self.clib.is_InquireImageMem(self.filehandle, ppcImgMem, pid, byref(width), byref(height), byref(bitdepth), None))
            print("width:",width)
            print("height:",height)
            print("depth:",bitdepth)
            print("SetImageMem")
            self._chk(self.clib.is_SetImageMem(self.filehandle, ppcImgMem , pid))
#            print("Set display mode")
#            self._chk(self.clib.is_SetDisplayMode(self.filehandle,  1))
            #pMem = ctypes.pointer(ctypes.c_void_p())
            #self._chk(self.clib.is_FreezeVideo(self.filehandle, 0))
#            self._chk(self.clib.is_CaptureVideo(self.filehandle, 0))
#            print("is live?")
#            self._chk(self.clib.is_CaptureVideo(self.filehandle, 0x8000))
#            time.sleep(0.2)
            self._chk(self.clib.is_FreezeVideo(self.filehandle, c_int(20)))
            self._chk(self.clib.is_CopyImageMem(self.filehandle, ppcImgMem, pid, c_img))

            # Pythonize and return.
            img_array = np.frombuffer(c_img, dtype=ctypes.c_ubyte, count=1280*1024)
            img_array.shape = np.array(self.shape)#/self.bins
            return img_array"""
