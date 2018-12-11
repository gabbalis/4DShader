import World
import Camera3DTo4D
import Camera3D
import pygame
import numpy

class World:
 """A world that Contains objecs."""

 def __init__(self, dimensions=3):
     self._dimensions = dimensions
     self._id_matrix = numpy.identity(self._dimensions)
     self._cameras = {}
     self._cameras_list = []
     self._renderable_objects = {}

 def addObject(self, obj, coords):
   self._renderable_objects[obj] = coords

 def addCamera(self, cam, coords):
   assert self.getNumDimensions()==cam.getNumDimensions()
   self._cameras[cam] = coords
   self._cameras_list.append(cam)

 def update(self, input):
   for obj in self._renderable_objects:
     assert not isinstance(obj, Camera3D.Camera3D)
     assert not isinstance(obj, Camera3DTo4D.Camera3DTo4D)
     obj.update(self, input)
   for cam in self._cameras_list:
     assert self.getNumDimensions()==cam.getNumDimensions()
     cam.update(self, input)

 def getCameraView(self, cam_num):
   return self._cameras_list[cam_num].getPixels()

 def getObjectCenter(self, obj):
     if obj in self._renderable_objects:
         return self._renderable_objects[obj]
     elif obj in self._cameras:
         return self._cameras[obj]

 def getObjectRotation(self, obj):
     return self._id_matrix

 _MAX_RAY_LEN = 2.0
 def shade(self, method, args):
     if method == 'RAYCASTING':
         source_loc, dir_vector = args
         vec_len = numpy.power(sum([abs(x) for x in dir_vector]), 1.0/self._dimensions)
         base_vector = numpy.divide(dir_vector, vec_len)
         ray_size = 0.3
         ray_inc = numpy.multiply(base_vector, ray_size)
         ray_len = 0
         loc = source_loc
         while ray_len <= self._MAX_RAY_LEN:
             for obj in self._renderable_objects:
                 col = obj.colorOf(self, loc)
                 if col:
                     return col
             loc += ray_inc
             ray_len += ray_size
     return (100, 0, 0)

 def getNumDimensions(self):
     return self._dimensions