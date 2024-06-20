from tqdm import tqdm
import time
from pynput import keyboard
import termios
import os
import math

done_time = None

def on_release(key):
  print('\b', end='')
  global done_time
  done_time = time.time()

def delay_func(t, start_t):
  global done_time
  scale = 200
  if done_time is not None: # done
    return 1 / (scale * (t - done_time + 0.01))

  # not done
  return math.exp(t - start_time) / scale


if __name__ == '__main__':
  os.system('stty -echo')
  listener = keyboard.Listener(on_release=on_release)
  listener.start()


  class ProgressBar:
    bricks = [' ','▏','▎','▍','▌','▋','▊','▉','█']
    @staticmethod
    def printbricks(ratio, end):
      num_full_bricks = ratio * os.get_terminal_size()[0]
      print(ProgressBar.bricks[-1]*int(num_full_bricks) + ProgressBar.bricks[int((num_full_bricks - int(num_full_bricks)) * len(ProgressBar.bricks))], end=end)
    def __init__(self):
      pass
    def update(self, ratio):
      ProgressBar.printbricks(ratio, end='\r')
    def __enter__(self):
      return self
    def __exit__(self, *vargs):
      ProgressBar.printbricks(1.0, end='\n')


  start_time = time.time()
  with ProgressBar() as pb:
    for i in range(800):
      pb.update(i/800)
      sleep_time = delay_func(time.time(), start_time)
      not_done = done_time is None
      for _ in range(int(sleep_time * 1000)):
        if not_done and done_time is not None:
          break
        time.sleep(0.001)

      time.sleep(sleep_time % 1)

  os.system('stty echo')
  print('done')

