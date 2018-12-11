import World
import Camera3DTo4D
import Camera3D
import pygame
import numpy

class Camera3D:
 """A 2D screen that displays a 3D world"""

 # Static Variables.
 _DEFAULT_FOV = 0.5

 def __init__(self, resolution=(1000, 1000)):
    self._resolution=resolution
    self._pixelgrid =numpy.empty(self._resolution, dtype=(object))
    self._fov=self._DEFAULT_FOV
    self._dimensions = len(resolution) + 1

 def getPixels(self):
   return self._pixelgrid

 def getNumDimensions(self):
   return self._dimensions

 def update(self, world, input):
   # RayTracing
   assert world.getNumDimensions()==self.getNumDimensions()
   camera_loc = world.getObjectCenter(self)
   camera_rot = world.getObjectRotation(self)
   fov_vec_component = numpy.dot((0.0, 0.0, self._fov), camera_rot)
   # should be a main variable actually.
   # but only if we use raytracing.
   # also, this can be done by Shaders I think.
   for index, _ in numpy.ndenumerate(self._pixelgrid):
     normalized_index = numpy.divide((index-numpy.divide(self._resolution, 2.0)), self._resolution)
     x, y = normalized_index

     base_vector = numpy.dot((x, y, 0.0), camera_rot)
     dir_vector = base_vector + fov_vec_component
     source_loc = base_vector + camera_loc
     arw, arx = index
     self._pixelgrid[arw, arx] = world.shade(method='RAYCASTING',
                                             args=(source_loc, dir_vector))