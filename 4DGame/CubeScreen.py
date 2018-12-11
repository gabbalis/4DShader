import World
import Camera3DTo4D
import Camera3D
import pygame
import numpy


class CubeScreen():
 """A 3D screen that displays a 4D world. Wraps a 4D camera"""

 # mode variables:
 _MODES = {
   'UD_SPLAYED':1,
   'RL_SPLAYED':2,
   'AK_SPLAYED':3,
   'TRANSPARENT_CUBE':4}
 _SPLAY_SPEED = 1.0
 _NUM_SPLAY_PIXELS = 10
 _MAX_PIXEL_TRANSPARENCY = 0.95
 # Coordinates relative to the 3D cube
 _RELATIVE_UP = (0.0, 0.0, 1.0)
 _RELATIVE_DOWN = (0.0, 0.0, -1.0)
 _RELATIVE_RIGHT = (0.0, 1.0, 0.0)
 _RELATIVE_LEFT = (0.0, -1.0, 0.0)
 _RELATIVE_ANA = (1.0, 0.0, 0.0)
 _RELATIVE_KATA = (-1.0, 0.0, 0.0)

 def __init__(self, cam=None, size=(1.0, 1.0, 1.0)):
    self._current_mode = self._MODES['TRANSPARENT_CUBE']
    self._current_splay = (0.0, 0.0, 0.0)
    self._pixel_transparency = self._MAX_PIXEL_TRANSPARENCY
    self._size = size
    self._4D_camera = cam

 def Asserts(self):
   """Returns true if all asserts are true."""
   return (
     True
     # Mode should be valid.
     and self._current_mode in self._MODES.values()
     # Maximums should remain sane.
     and self._pixel_transparency <= self._MAX_PIXEL_TRANSPARENCY
     and max(self._current_splay) <= 1.0
   )

 def setmode(self, n):
   _current_mode = n

 def update(self, world, input):
   assert self.Asserts()
   #self.makeModeUpdates()
   pass

 def colorOf(self, world, coords):
     assert world.getNumDimensions()==3
     loc = world.getObjectCenter(self)
     rot = world.getObjectRotation(self)
     rot_coords = None
     rot_coords = (coords - loc).dot(rot) # rotate the coordinate system so that coords is the same but is relative to the cube...?
     maxes = numpy.divide(self._size, 2.0)
     mins = numpy.divide(self._size, -2.0)
     for r, min, max in zip(rot_coords, mins, maxes):
         if r < min or r > max:
             return None
     # now find the distance into the cube we are and grab that color.
     # pixels = self._4D_camera.getPixels()
     # return pixels.(%downeachaxisascoordsoutofresolution)

     # or just a color for testing...
     return (0, 0, 100)


# makeModeUpdates(self, input):
# """Make some changes based on the mode"""
#   # change this to be a bit slower & steadier.
#   switch (_current_mode) {
#     case 1:
#     _current_splay = (0.0, 0.0, 1.0)
#     _pixel_transparency = 0
#     break
#     case 2:
#     _current_splay = (0.0, 1.0, 0.0)
#     _pixel_transparency = 0
#     break
#     case 3:
#     _current_splay = (1.0, 0.0, 0.0)
#     _pixel_transparency = 0
#     break
#     case 4:
#     _current_splay = (0.0, 0.0, 0.0)
#     _pixel_transparency = _MAX_PIXEL_TRANSPARENCY
#     break
#     default:
#       raise ValueError()
#   }

  