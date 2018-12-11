import World3D
import World4D
import Camera3DTo4D
import Camera3D
import pygame
import numpy

class Camera3DTo4D:
 """A 3D screen that displays a 4D world"""
 _pixelcube = None
 _4D_world = None
 _fov = None
 _resolution = None
 # Static Variables.
 _DEFAULT_FOV = 0.5


 def Asserts():
   """Returns true if all asserts are true."""
   return (
     True
     # The cube should be a cube. Not a rectangle.
     and len(set(self._pixelcube.shape)) == 1
     and isinstance(self._4D_world, World4D.World4D)
     )

 def __init__(self, resolution=500):
   self._resolution=(resolution, resolution, resolution)
   self._pixelcube =numpy.empty( self._resolution, dtype=(object)) 
   self._fov=self._DEFAULT_FOV

 def setWorld(self, world):
     self._4D_world = world

 def getPixels(self):
   return self._pixelcube


 def update(self, input):
   # RayTracing
   camera_loc = self._4D_world.getObjectCenter(self)
   camera_rot = self._4D_world.getObjectRotation(self)
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
     self._pixelcube[arw, arx, ary] = self._4D_world.shade(method='RAYCASTING',
                                                           args=(source_loc, dir_vector))

     