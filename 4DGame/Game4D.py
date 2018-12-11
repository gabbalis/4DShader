import World3D
import World4D
import Camera3DTo4D
import Camera3D
import CubeScreen
import pygame
import numpy
import time

class Game4D:
 _3D_world = None
 _3D_camera = None
 _4D_world = None
 _4D_camera = None
 _screen = None
 MAX_FPS = 60.0
 # can make a circular queue to measure actual FPS
 BACKGROUND_COLOR = (256, 256, 256, 0)
 CUBESCREEN_SIZE = 5
 _resolution = None

 def __init__(self):
   self._resolution = (200, 200)
   self._3D_world = World3D.World3D()
   self._3D_camera = Camera3D.Camera3D(self._resolution)
   self._3D_world.addCamera(self._3D_camera, (0.0, 0.0, 0.0))

   self._4D_world = World4D.World4D()
   self._4D_camera = Camera3DTo4D.Camera3DTo4D(self.CUBESCREEN_SIZE)
   self._4D_world.addCamera(self._4D_camera, (0.0, 0.0, 0.0, 0.0))

   # Now place a screen displaying the 4D camera in the 3D world
   cube_screen = CubeScreen.CubeScreen(cam=self._4D_camera)
   self._3D_world.addObject(cube_screen, (0.0, 0.0, 1.0))
   
   # And now: For our screen :3
   self._screen = pygame.display.set_mode(self._resolution)

 def playGame(self):
  now = time.time()
  while True:

    lastframe = now
    inputs = {}
    #while now - (1.0/self.MAX_FPS) < lastframe:
    # inputs.update(self.getInputs())
    # now = time.time()
    inputs.update(self.getInputs())
    if '<Event(12-Quit {})>' in repr(inputs):
        exit(0)
    print(inputs)
    self.update(inputs)
    self.render()

 def getInputs(self):
  inputs = pygame.event.get()
  input_dict = {'inputs': inputs}
  return input_dict

 def update(self, inputs):
  self._4D_world.update(inputs)
  self._3D_world.update(inputs)

 def render(self):
  cam_array = self._3D_world.getCameraView(0)
  int_arr = cam_array.flatten()
  int_arr2 = numpy.array([(a, b, c) for a,b,c in int_arr])

  new_arr = numpy.reshape(int_arr2, self._resolution+(3,))
  print (new_arr.shape)
  pygame.pixelcopy.array_to_surface(self._screen, new_arr)


def main():
    game = Game4D()
    game.playGame()


if __name__ == "__main__":
    main()