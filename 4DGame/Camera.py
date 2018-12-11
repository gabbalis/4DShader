import World
import pygame
import numpy

class Camera:
 """A 3D screen that displays a 4D world"""

 # Static Variables.
 _DEFAULT_FOV = 0.5

 def __init__(self, resolution=(500, 500, 500)):
   self._resolution=resolution
   self._pixelarray =numpy.empty( self._resolution, dtype=(object)) 
   self._fov=self._DEFAULT_FOV
   # An ND *flat* camera is for an (N+1)D world.
   self._dimensions = len(resolution) + 1

 def getPixels(self):
   return self._pixelarray

 def getNumDimensions(self):
   return self._dimensions

 def update(self, world, input):
   # RayTracing
   assert world.getNumDimensions()==self.getNumDimensions()
   camera_loc = world.getObjectCenter(self)
   camera_rot = world.getObjectRotation(self)
   fov_vec_component = numpy.dot([0.0 for _ in range(self.getNumDimensions()-1)]+[self._fov], camera_rot)
   # should be a main variable actually.
   # but only if we use raytracing.
   # also, this can be done by Shaders I think.
   for index, _ in numpy.ndenumerate(self._pixelarray):
     normalized_index = numpy.divide((index-numpy.divide(self._resolution, 2.0)), self._resolution)
     base_vector = numpy.dot(numpy.append(normalized_index, 0.0), camera_rot)
     dir_vector = base_vector + fov_vec_component
     source_loc = base_vector + camera_loc
     self._pixelarray[index] = world.shade(method='RAYCASTING',
                                          args=(source_loc, dir_vector))