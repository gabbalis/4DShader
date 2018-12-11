import World3D
import World4D
import Camera3DTo4D
import Camera3D
import pygame
import numpy

class World4D:
 """Contains 4D objecs."""
 # Mostly just the camera and GUI
 # should support 4D
 _Cameras = {}
 _CamerasList = []
 _RenderableObjects = {}
 def __init__(self):
     pass

 def addObject(self, obj, coords):
   self._RenderableObjects[obj] = coords
   obj.setWorld(self)

 def addCamera(self, cam, coords):
   self._Cameras[cam] = coords
   self._CamerasList.append(cam)
   cam.setWorld(self)

 def update(self, input):
   for obj in self._RenderableObjects:
     obj.update(input)
   for cam in self._Cameras:
     cam.update(input)

 def getCameraView(self, cam_num):
   return self._CamerasList[cam_num].getPixels()

 def getObjectCenter(self, obj):
     if obj in self._RenderableObjects:
         return self._RenderableObjects[obj]
     elif obj in self._Cameras:
         return self._Cameras[obj]

 def getObjectRotation(self, obj):
     return ((1.0, 0.0, 0.0, 0.0),
             (0.0, 1.0, 0.0, 0.0),
             (0.0, 0.0, 1.0, 0.0),
             (0.0, 0.0, 0.0, 1.0))

 _MAX_RAY_LEN = 2.0
 def shade(self, method, args):
     if method == 'RAYCASTING':
         source_loc, dir_vector = args
         vec_len = numpy.power(sum([abs(x) for x in dir_vector]), 1/4.0)
         base_vector = numpy.power(dir_vector, vec_len)

         ray_size = 0.3
         ray_inc = numpy.multiply(base_vector, ray_size)
         ray_len = 0
         loc = source_loc
         while ray_len <= self._MAX_RAY_LEN:
             for obj in self._RenderableObjects:
                 col = obj.colorOf(loc)
                 if col:
                     return col
             loc += ray_inc
             ray_len += ray_size
     return (0, 100, 0)