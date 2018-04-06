# from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import cv2
from eyespy.EyeTribe.peyetribe import EyeTribe
import os
import random
from eyespy.Visualize.Task.states import *
import eyespy.Visualize.Task.utils as utils


def main(opt):
  # Instantiate tracker
  # tracker = EyeTribe()
  # tracker.connect()
  # n = tracker.next()
  # tracker.pushmode()

  # initialize `task_state` for all tasks
  task_state = TaskState(opt.actions, opt.data_path, opt.tasks)
  job, state = 1, None

  while True:

    # Initialising `state` for current task / video
    if job == 1:
      image_dir = os.path.join(opt.data_path, task_state.tasks[task_state.task_idx])
      # TODO: Prepare a csv file and list to avoid loading in every loop
      frame_paths, _, path_to_frame = utils.findpaths(image_dir)
      color = utils.COLORS[random.choice(list(utils.COLORS.keys()))]
      state = State(opt.data_path, str(task_state.tasks[task_state.task_idx]),
                               image_dir, frame_paths, path_to_frame, color)

    # print info for terminal GUI
    utils.print_info(task_state, state)

    # load image and embed info
    image_path = state.frame_paths[state.image_idx]
    image = utils.imread(image_path, resize=2)
    utils.image_info(image, task_state, state)

    done = False
    count = 0
    while not done:
      count += 1
      # state.gaze.append(utils.getXY)
      print('{}: {}'.format(count, state.gaze))
      state.gaze.append((random.randint(0, 100), random.randint(0, 100)))
      key = cv2.waitKey(200)
      if key != -1 or count > 100:
        done = True
        if key != -1:
          # record user input and implement action
          job = utils.read_key(key, task_state, state)
          state.gaze = []

    # quit condition
    if job == -1:
      break


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_path', type=str, default='./eyespy/Data/Tasks/', help='Path to the folder with images by task (optional)')
  parser.add_argument('--tasks', nargs='+', type=int, default=['Shapes'], help='Tasks to start performing (optional)')
  parser.add_argument('--actions', type=str, nargs='+', help='List of actions (optional)',
                      default=['act1',
                               'act2',
                               'act3',
                               'act4',
                               'act5',
                               'act6',
                               'act7',
                               'act8',
                               'act9'])

  args = parser.parse_args()

  main(args)
