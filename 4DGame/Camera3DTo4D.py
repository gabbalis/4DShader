import World
import Camera3DTo4D
import Camera3D
import pygame
import numpy

class Camera3DTo4D:
 """A 3D screen that displays a 4D world"""

 # Static Variables.
 _DEFAULT_FOV = 0.5

 def __init__(self, resolution=(500, 500, 500)):
   self._resolution=resolution
   self._pixelcube =numpy.empty( self._resolution, dtype=(object)) 
   self._fov=self._DEFAULT_FOV
   # An ND *flat* camera is for an (N+1)D world.
   self._dimensions = len(resolution) + 1

 def Asserts():
   """Returns true if all asserts are true."""
   return (
     True
     # The cube should be a cube. Not a rectangle.
     and len(set(self._pixelcube.shape)) == 1
     and isinstance(self._4D_world, World4D.World4D)
     )

 def getPixels(self):
   return self._pixelcube

 def getNumDimensions(self):
   return self._dimensions

 def update(self, world, input):
   # RayTracing
   assert world.getNumDimensions()==self.getNumDimensions()
   camera_loc = world.getObjectCenter(self)
   camera_rot = world.getObjectRotation(self)
   fov_vec_component = numpy.dot((0.0, 0.0, 0.0, self._fov), camera_rot)
   # should be a main variable actually.
   # but only if we use raytracing.
   # also, this can be done by Shaders I think.
   for index, _ in numpy.ndenumerate(self._pixelcube):
     normalized_index = numpy.divide((index-numpy.divide(self._resolution, 2.0)), self._resolution)
     w, x, y = normalized_index

     base_vector = numpy.dot((w, x, y, 0.0), camera_rot)
     dir_vector = base_vector + fov_vec_component
     source_loc = base_vector + camera_loc
     arw, arx, ary = index
     self._pixelcube[arw, arx, ary] = world.shade(method='RAYCASTING',
                                                  args=(source_loc, dir_vector))