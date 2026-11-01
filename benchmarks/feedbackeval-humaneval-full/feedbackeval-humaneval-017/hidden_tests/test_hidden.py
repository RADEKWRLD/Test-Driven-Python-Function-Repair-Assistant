import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[''],
 ['o o o o'],
 ['.| .| .| .|'],
 ['o| o| .| .| o o o o'],
 ['o| .| o| .| o o| o o|'],
 ['o o| o| o|'],
 ['.| .| o| o| .|'],
 ['o| o| o| .| o| .|'],
 ['.| .| o| o| o| o| .| .| o| o| o| o| o| o| o o o o'],
 ['.| .| o| o| .| .| o| o|'],
 ['o| .| .| .| o| o|'],
 ['o| o| o| o| .| .| .| .|'],
 ['.| o| .| o| o| .| o| .|'],
 ['o o| o| o| o| o| o| o|'],
 ['.| .| o| o| o| o| o| .| o| o| o| o| o| o o o o o o o| o|'],
 ['.| .| o| o|'],
 [''],
 ['o| o| o| o| o| o| o|'],
 ['o| o| o| o| .| .| .|'],
 ['o o| o| o| o| o'],
 ['o| o|'],
 ['.| .| o|'],
 ['o| .| .| .| o| o| .| .| o| o|'],
 ['o| o| o| o| o| .| .| .| .| o| .| o| .|'],
 ['o o| o| o| o|'],
 ['o| o| o| o| o| o'],
 ['o| o| o| .|'],
 ['o| o| o|'],
 ['o o| o| o| o'],
 ['o| o| o| o|'],
 ['o| .| .| o| o|'],
 ['o| o| o| o| o| o|'],
 ['o|'],
 ['o o| o| .| .| o| o| o| o| o| .| o| o| o| o| o| o o o o o o o| o| o| o| o'],
 ['o| o'],
 ['o| .| .| o| o| .| .| o| o|'],
 ['.| .| o| o| o| o o o'],
 ['o| o| o| o'],
 ['o o| o'],
 ['o| .| .| .| o|'],
 ['o o| o| .| .| o| o| o| o| o| .| o o o o o o o o| o| o| o| o'],
 ['o'],
 ['o o'],
 ['o o| o| .| o| o| o| o| o| o o o o o o o| o| o| o| o'],
 ['.| .| o| o| o'],
 ['o o| o| o'],
 ['o| .| .| o| o| .| .| o|'],
 ['o| .|'],
 ['o| .| .| o| o| .| o|'],
 ['.| .| o| o| o| o| .| .| o| o| o| o| o| o| o o o| .| .| .| o| o| o'],
 ['.| .| o| o| o o o'],
 ['o o| o| .| o| o| o| o| o| o| o| o| o| o'],
 ['o| o o| o| o| o| o|'],
 ['.| .| o| o| o| o| o| .| o| o| o| o| o| o o o| o|'],
 ['o o| o| o o| o'],
 ['o| .| o| .|'],
 ['o| o o| o|'],
 ['o| .| .| o|'],
 ['o| o| o| o| .| o| .|'],
 ['.| .| o'],
 ['o| o| o| o| o| o| o| .| .| .| .|'],
 ['o| o o| o| .| .| o| o| o| o| o| .| o| o| o| o| o| o o o o o o o| o| o| o| o|'],
 ['o| o| o'],
 ['o| .| o| o| o| o|'],
 ['o| o| o| o o| o| o| o| o| o| o| .| o| .| o| o|'],
 ['.| .| o| o| o| o'],
 ['o| o| .|'],
 ['o o| o| .| .| o| o| o| o| o| .| o| o| o| o| o| o| o| o'],
 ['o o| o| o o'],
 ['o| o| o| o| o| o| o| .| .| .| .| o| o|'],
 ['o| .| .| .| o| o| o o| o'],
 ['o| .| .| .| .| o| o|'],
 ['.| .| o| o| .| .| o| o o| o| .| .| o| o| o| o| o| .| o| o| o| o| o| o o o o o o o| o| o| o| o| '
  '.| o| o|'],
 ['o o| o| .| .| o| o| o| o| o| o| o| o| o| o'],
 ['o o| .|'],
 ['o o o'],
 ['o o|'],
 ['.| .| o| o| o| o| .| .| o| o| o| o| o| o| o o o| .| .| .| o| o|'],
 ['o o| o| .| o o| o| o'],
 ['o| o o|'],
 ['.| .| o| o'],
 ['o| o| o| o| .| o|'],
 ['o o| o| o o o'],
 ['o o o o'],
 ['o| .| .| o| o| .| o'],
 ['.| .| o| o| o| o| .| .| o| o| o| o o o'],
 ['o| o| o| o| o| o| o| o| o| .| .| .|'],
 ['o o| o| .| o| o| o| o| o| o| o| o'],
 ['o| o .| o| .|'],
 ['o| o| o| o| .| .| .| .| o| .| o| .|'],
 ['o .|'],
 ['.| .| o o'],
 ['o| o| o| .| o| .| o| .|'],
 ['o| o .|'],
 ['.| .| o| o| o| o| .| .| o| o| o| o| o| o| o o| .| .| .| o| o|'],
 ['o| .| .| o| o| o|'],
 ['.| .| o| o| o| o| .| .| o| o| o| o| o o| o o o| .| .| .| o| o|'],
 ['.| o'],
 ['.| .| o .|'],
 ['.| .| o| o| o|'],
 ['o| .| .| .| .| o| .| o| .|'],
 ['o| o| .| o|'],
 ['o| .| .| o| o| o| o| o| .|'],
 ['o| o| o| o| o| .| .| .| .| o| o|'],
 ['o| o| o| o| o o| o| o| o| o| o| o| .| o| .| o| o| o| o| o| o|'],
 ['o o o o| o o| o| o| .| .|'],
 ['o| .| o| .| .| o| .| .| o| .| o| .| o| .| o| .| .| o|'],
 ['o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| .| .| .| '
  '.|'],
 ['.| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .|'],
 ['o o o| o o| o| o|'],
 ['o| o| o| o| o| o| o| o|'],
 ['.| .| .| .| o o o o o o o o| o o o o o o o| o| o| .| .|'],
 ['.| .| .| .| .| .| .| .| o o o o o o o o| o o o o o o o| o| o| .| .| o o o o o o o o| o o o o o '
  'o o| o| o| .| .|'],
 ['o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o| o| o| o| o| '
  'o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| .| .| .| .| .| .| .| .| .| .| .| .| .| '
  '.| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| o o o o o o o o| o o o o o '
  'o o| o| o| .| .| o o o o o o o o| o o o o o o o| o| o| .| .|'],
 ['.| o o| o o o| .| o o| o o o| .| o o| o o o| .| o o| o o o| o o o| o'],
 ['o o| o| o| o| o|'],
 ['o| o| o| o| .| .| .| .| o o o o o o o o| o o o o o o o| o| o| .| .| o|'],
 ['.|'],
 ['o o| o o| o o| o o| o o| o o| o o| o o| o o| .| .| .| .|'],
 ['.| .| .| .| o o o o o o o| o| o o o o o o o| o| o| .| .|'],
 ['o| .| o| .| .| o| .| .| o .| o| .| o| .| .| o|'],
 ['o| o| o| o| o| o| o| o'],
 ['o| o| o o| o| o'],
 ['o| o| o| o| .| .| .| .| o o o o o o o o| o o o o o o o| o| o| .| o|'],
 ['o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o| o| o| o| o| '
  'o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| .| .| .| .| .| .| .| .| .| .| .| .| .| '
  '.| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| o o o o o o o o| o o o o o '
  'o o| o| o| .| .| o o o o o o o o| o o o o o o o| o| o| .| .| o'],
 ['o o o o o o| o| o| .| .|'],
 ['o o o| o| .| .|'],
 ['o o| o| o| o o| o o| o o| o o| o o| o o| o o| .| .| .| .|'],
 ['.| .|'],
 ['o o| o o| o o| o o| o o| o o| o o| o| .|'],
 ['o| o o| o o| o| o|'],
 ['o o o| o| o|'],
 ['.| o o| o o o| .| o o| o o o| .| o o| o o o| .| o o| o o o| o o o o| o o| o| o| .| .| o| o'],
 ['o| o| o o| o| .| .| .| .| o o o o o o o o| o o o o o o o| o| o| .| .|'],
 ['o o| o o| o o| o| o| .| .|'],
 ['o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o| o| o| o| o| '
  'o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| .| .| .| .| .| .| .| .| .| .| .| .| .| '
  '.| .| .| .| .| o'],
 ['o| o| o o o o o o o o o| o o o o o o o| o| o| .| .|'],
 ['o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o| o| o| o| o| '
  'o| o| o| o| o| o| o| .| .| .| .| .| .| .| .| .| .| .| .| .| o'],
 ['o| .| o| .| .| o| .| .| o| .| o| .| o| .| o| .| .| o'],
 ['.| .| .| .| o o o o o o o o o| o| o| .| .|'],
 ['o o| o o| o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o| o| '
  'o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| .| .| .| .| .| .| .| .| .| .| '
  '.| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| o o o o o o o o| '
  'o o o o o o o| o| o| .| .| o o o o o o o o| o o o o o o o| o| o| .| .| o o| o| o| .| .|'],
 ['.| .| .| .| .| .| .| .| o o o o o o o o| o o o o o o o| o| o o o o| o| o| .| .|'],
 ['o o| o o| o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o| o| '
  'o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| .| .| .| .| .| .| .| .| .| .| '
  '.| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| o o o o o o o o| o o o '
  'o o o o| o| o| .| .| o o o o o o o o| o o o o o o o| o| o| .| .| o o| o| o| .| .|'],
 ['o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o| .| o'],
 ['o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o o| o| o| o o| o '
  'o| o o| o o| o o| o o| o o| .| .| .| .| o o o| o| o| .| .| o o o o o o o o| o o o o o o o| o| '
  'o| .| .| o'],
 ['o| o| o| o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o o| o| '
  'o| o o| o o| o o| o o| o o| o o| o o| .| .| .| .| o o o| o| o| .| .| o o o o o o o o| o o o o o '
  'o o| o| o| .| .| o| o o o o o o o| o| o| .| .| o|'],
 ['o o o| o o| o|'],
 ['o o| o| o o| o| o| .| .|'],
 ['o| o o| o o| o|'],
 ['o o| o o| o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o| o| '
  'o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| .| .| .| .| .| .| .| .| .| .| '
  '.| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| o o o o o o o o '
  'o| o o| o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o| o| '
  'o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| .| .| .| .| .| .| .| .| .| .| '
  '.| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| o o o o o o o o| o o o '
  'o o o o| o| o| .| .| o o o o o o o o| o o o o o o o| o| o| .| .| o o| o| o| .| .| o o o o| o| '
  'o| .| .| o o o o o o o o| o o o o o o o| o| o| .| .| o o| o| o| .| .|'],
 ['.| .| .| .| o o o o| o o o o| o o o o o o o| o| o| .| .|'],
 ['o o o| o o| o'],
 ['o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o| o| o| o| o| '
  'o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| .| .| .| .| .| .| .| .| .| .| .| .| .| '
  '.| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| o o o o o o o o| o o o o o '
  'o o| o| o| .| .| o o o o o o o o| o o o o o o| o| o| o| .| .| o'],
 ['o o| o o| o| o o o o o| o o o o o| o o o o o| o o o o o| o o o| .| .| .| .| .| .| .| .| .| .| '
  '.| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| o o o o o o o o| o o o o o o o| o| '
  'o| .| .| o o o o o o o o| o o o o o o o| o| o| .| .| o o| o| o| .| .|'],
 ['o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o| o| o| o| o| '
  'o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| .| .| .| .| .| .| .| .| .| .| .| .| .| '
  'o'],
 ['o o o| o|'],
 ['o o| .| .|'],
 ['o o| o| o| o o| o o| o o| o o| o o| o o| .| .| .| .|'],
 ['o o| o| o| o o| o o| o o| o o| o o| o o| o o| .| .|'],
 ['o| o| o o o o o o o o o| o o o o o o| o| o|'],
 ['o o| o o| o o| o o| o| o o| o o| o o| o o| o o| o o| o o| o o| .| .| .| .|'],
 ['o| o o| .| .| o|'],
 ['o o| o o| o| o o o o o| o o o o o| o o o o o| o o o o o| o o o| .| .| .| .| .| .| .| .| .| .| '
  '.| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| o o o o o o o o| o o o o o o o| o| '
  'o| .| .| o o o o o o o o| o o o o o o o| o| o| o o| o| o| o| o o| o| o| .| .|'],
 ['o| o| o o o o o o o o o| o o o| o o| o| o| o| o|'],
 ['o| o| o| o| o o| .| .| .| o o o o o o o o| o o o o o o o| o| o| .| o|'],
 ['o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o o o o o| o| o| o| o| o| '
  'o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| .| .| .| .| .| .| .| .| .| .| .| .| .| '
  '.| .| .| .| .| .| .| o o| o o o o o o o| o| o| .| .|'],
 ['o o o o o|'],
 ['o o o o o o o o'],
 ['o o o| o| o .| .| .| .| o o| o .| o| o| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| o o o o '
  'o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o| o| o| o| o o o o o o o o '
  'o o o o o o o o o o o o o o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| o| '
  'o| o|'],
 ['o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o '
  'o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o '
  'o o o o o o o o o o'],
 ['o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o| o| .| .| .| '
  '.|'],
 ['o o o| o o|'],
 ['.| o o| o o o| .| o o| o o o| o o o| o'],
 ['o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o| o| .| .| .| .|'],
 ['o o o| o'],
 ['o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o .| .| .| .| .| .| .| .| o o '
  'o o o o o o| o o o o o o o| o| o| .| .| o o o o o o o o| o o o o o o o| o| o| .| .| o| o o| o| '
  'o| .| .| .| .|'],
 ['.| .| .| .| o o o o o o o o| o o o o o o o| o| o .|'],
 ['o o o| o o'],
 ['o o| o o| o| o|'],
 ['.| o| o| o| .| .|'],
 ['.| o o| o o o| .| o o| o o o| .| o o| o o o| .| o o| o o o| o o o| o o o o o o o o| o o o o o o '
  'o| o| o .|'],
 ['.| o o| o o o| .| o o| o o o| .| o o| o o o| .| o o| o o o| o o o| o o o o o o o| o o o o o o '
  'o| o| o .|'],
 ['o o| o o| o| o'],
 ['o o o| .| o o| o o o| .| o o| o o o| .| o o| o o o| .| o o| o o o| o o o| o o o o o o o| o o o '
  'o o o o| o| o .|'],
 ['.| o o| o o o| .| o o| o o o| .| o o| o o o| .| o o'],
 ['.| .| .| .| o o o o o o o o| o o o o o| o o| o| o .|'],
 ['.| o o| o o o| .| o o| o o o| .| o o| o o o| .| o o| o| o o| o o o| o o o o o o o o| o o o o o '
  'o o| o| o .|'],
 ['o o| o o| o o| o o| o o| o o| o o| o| o o| o o| o o| o o| o o| .| .| .| .|'],
 ['.| .| .| .| o o o o o o o o| o o o o o| o o| .|'],
 ['o o| o o| o|'],
 ['o o| o o| o o| o o| o o| o o| o| o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o| o| .| .| .| '
  '.|'],
 ['o o o| o .| .| .| .| o o o o o o o o| o o o o o o o| o| o'],
 ['.| o o| o o o| .| o o| o o o| .| o o o| .| o o| o o o| o o o| o o o o o o o| o o o o o o o| o| '
  'o .|'],
 ['o o| o o| o'],
 ['.| .| .| .| o o o o o o o| .| .|'],
 ['.| .| .| .| .| .| .| .| o o o o o o o o| o o o o o o o| o| o| .| .| o o o o o o| o o o o o o o| '
  'o| o| .| .|'],
 ['.| o| o| o .|'],
 ['.| .| .| .| o o o o o o o o| o o o| o .|'],
 ['o o o o| o|'],
 ['.| o o| o o o| .| o o| o o o| .| o o| o o o| .| o o| o o o| o o o| o o o o o o o| o o o o o o o '
  'o| o .|'],
 ['o o| o o| o o| o o| o o| o o| o| o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o|'],
 ['.| .| .| .| .| o o| o o o| .| o o| o o o| .| o o| o o o| .| o o| o o o| o o o| o o o o o o o| o '
  'o o o o o o| o| o .| .| .|'],
 ['o o| o o| o o| o o| o o| o o| o| o| o o o| o .| .| .| .| o o o o o o o o| o o o o o o o| o| o '
  'o| o| .| .| .| .|'],
 ['.| o o| o o o| .| o o| o o o| .| o o| o o o| .| o o| o o o| o o o| o o o o o o o o| o o o o o '
  'o| o| o .|'],
 ['o o| o|'],
 ['.| o o| o o o| .| o o| o o o| .| o o o o o o| o| o .|'],
 ['o o| o o| o o| o o| o o| o o| o| o| o o| o o| o o| o o| o o| o|'],
 ['o o o| .| o o| o o o| .| o o| o o o| .| o o| o o o|'],
 ['.| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .|'],
 ['.| .| .| .| o o| o o o o o o| o o o o o| o o| .|'],
 ['.| .| .| .| .| .| .| .| o o o o o o o o| o o o o o o o| o| o| .| .| o o o o o o| o o o o o o o| '
  'o| o| .| o o o| o'],
 ['.| .| .| .| o o o o o o o o| o o o o o .|'],
 ['o o| o o| o o| o o| o o| o o o| o o| o o| o o| o o| o o| o|'],
 ['o| o o'],
 ['.| .| .| .| o o o o o o o| o o o o o o o| o| o| .| .|'],
 ['o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o .| .| .| .| .| .| .| .| o o '
  'o o o o o o| o o o o o o o| o| o| .| .| o o o o o o o o| o o o o o o o| o'],
 ['.| .| .| .| .| .| .| .| o| o o o o o o o| o o o o o o o| o| o| .| .| o o o o o o| o o o o o o '
  'o| o| o| .| .|'],
 ['o o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| o o| .| '
  '.| .| .|'],
 ['.| o o| o o o| .| o o| o o o o| o .|'],
 ['.| .| .| .| .| .| .| .| .| .| .| .| .| .| .| .|']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-pO-JCg1=a)l*BvS%5x6hPu_C}K7;1|EqRUmK7mtIgJa^&L);wSnpAzSXy?ev-'
    b'(?c_hI9`M3Z3%YXgL^UvS@{Et8W{lEV{t<*pN`0Lzr_qv1EF!mgw-'
    b'kNL$w=?(N%T{a0_(rvOE%@^7aps=N8tK*>{`}uR|NgIk{57<3h98S1r!hTQ4$X4gp%?d@>PjWHl}lYEB`+neb&T)DUT&FQ-'
    b'ph>I!d#Ybcka^84r^GM)#i<1aMycEyREfgG1`bH-rUBVKJwwpKbL8%#k}_jomG|Mz1xXpmXys|-'
    b'>qxx9!6`i?$csFyV)44g~F4i7Jn{NE}u%dl|0kP>7-'
    b'#?vw7NghIMP5d(2iwTcc=!c7m1CYrku!>Feh*^_G0*Xxwqt9BgJj(08b9r7_|P+eeElnz!OMil0_yEOmOTbLDqY+x;v8GfQ6m)O$'
    b'#md#rVMTzQ2|)Q-*WVUN}0=F)lY<;_|hyUw4>jI{&7AwBo3IcDB1kWRm3sc+I1LdrYs8Z3`6#y&Uq?WdEs8qRn_T-'
    b'u6@+mAf%B3Wgf-VYb%>zO^Kl0E8HkssTzP<kYfUVAKi*PqK+k2PhMFz;Pf%v!iT$B}y4(;|hJVzIqe+;Qa0I_j>y-'
    b'AIf|^7C_<OeMB{=QfME%^aKnSUlJ7w2-'
    b'z}%e9TVci5NMw_S6u<J2_!tvi0PS<8B&AWkW}ZZ8yCE~l?`Zz9a6?vZjKT%DA)Ln>HhG^*cut~XO_)*d{CT@y{!D~Sj`_`N-{-'
    b'8y49W%>1W_9|99%|UgKb~`10&({p=ToM)T8sktn1cPw#PxsW$I*sC8Gu{$t0v<HZ-ukSqc_9n!=Q1Z-wH-'
    b'qrzC)?Iq&CK+Sl6|h&a9;e>tlFpJR-pW7}6p4s}Z~PE{Y(OVO76HZSz}RXUN`&3kcF~CQ!ahCrqg*z{RU~Dw>q}Ui;@V|0KMj-'
    b'3Aa-_|q2%l1N9iS?;hnXu(X~-+Lw*4pdk?)pH^DI~zS$-'
    b'twaiEYCIxTwJy7eP)?~<{CWsB=&Sks>H}w?lxA43SY_{v?+DGb<=yEzz40|Mh~-'
    b'iId=}Qsl~}kM$aVn)Nam77U2f7@|bo>#PRdSrcl{46{|fb_YhsNiks9nAyh2abE}05j&Pz<2I!VHPs+!(=by{m7WPWs%Zl8F{yx@'
    b'M^SW-Lo7RbObUL=pSX&-F)jLza8Cau0D3Ui*mx3yUHq+HKo-Mj;rE>#?8G@xa0R{SKojFI^R>N8w_z&rxl-'
    b'}6bEjxpi`E=Gco43f1+aW(d7nnLB0&2$&0RqQ(PCgHk<hbC6w~8;2Ms29ci9ySCwM4q;YTKk|a80*OV>Y9t8u?O*f}r8r@&00Q%Y'
    b'|0T&1M9N-134r^6bY~DaX9?-5LRgyY5&3Iwep3!gVWm*S9ry>;PJ#3V}B-bAiZx*wVU3pO=MHYL1|c$S(#k$R>@!!-'
    b'WyH{ahx}hhFjkT4N4s&J(CbfGbtM!f;yWkh&3Qp&E#eJ-'
    b'B=FW&JNRP$DUYd&y6Mu$=CpS$Q&+H8#<A>Jpx^<>9~)Kn`dz7j+f@{<o(FWfA+F?am40ZcFrOudSECWhbGWI}(IOU&FP;eg%FI0J'
    b'5Gve+fU4)kKF(Cp^1%<JV&YgUDe)6OeZLbx@|+SQ3y2gza$^3L5qcaiW&a5eG+p^OExkq*8n(gLkyqW_>w9+kEm;NMxhUo(JWA($'
    b'|_}MQ9!N5gJhI+>~yhV&J;QPt!RbNy;{1Ke!BD*#_58E%9Z|dqF0&NumQ6sw49+F}itX{y!794Po2}TtpgcSxc>zyHq^T#GCN5%2'
    b'}-wSp-m~xpRqr(kiWN>I6V-'
    b'h=n+JUaQWY5DHMkjFbR<G5w7VdG5Y<0szi|!jW6?rks_FIpery$Q6{=KxsHo+Mw1B2~}3zK1c_#=FIR1v3?%A@zINlxiyBeM13?F'
    b'y@)!gRM|WLz=eG$@*%xX1MMJ$b|;|+Wax8&wQa6TAEji0MvXKzf9cr_A_F8r>&_ys{`x)*1Z_}VuM_1Fso<S1w}nj<&B*g0^BP!W'
    b'r*D{ZAj0wuPB|-MZ-+bRm=TUc^^C+@tsowHh%@m_dO{~!fHYW_sCKD~ltS;o|G00$Q9}j!8ff4cCo$bc{2)k%fGuq5i~{CD-'
    b'~=#59FapEvX+X>Z-{Rh!35xt<~eXxjXl8)t4~D3JRzeyp?D~c%&mOXvovi%T7Yu*tzvILF;MOo_?iHWRCVZ<(Q3ri+JWa%2dHj3-'
    b'C)8Bt|LcLK_R_8RdTuT-'
    b'#%y`WKTXmArZg^!j5MEhy?FY`sAN#qN@B5MN569o!XnJb`;BLQv|g5l2ALSzn$psSgq47FjP3eX9?6T&Bb>d=4#@m?`gnmX_p}|Y'
    b'xJI#1^58UAQh-;unAp23_)=T4+Lf<KDdOMf2Ba%5iU8jM2%LDJON^>o^c^e38D((Vk7EAL^#rpFe4^i;sZv1tC*G0ku*2A8-'
    b'k1l|8REz2Yev#TL>@A*%=v@7pV$B8AUzNnLn37nE`P;209Zd+S{NR@F29OJ2G-'
    b'*aHy(3=~b2`x!ycXN*}HDD@+cF%Z_$L^|vz<eAGcDRD_*Ns{->q;zf}1pffPmGP-'
    b's2E7cx8)&zo4(|DDV&^3gC0uhi!ln2_elYjJZpm<ug0^6+wjmNg7Aj^9h#3>)627@rP$X_&rOPnHRc{nV{c4#G_8amDMp;0La+Ih'
    b'F~vSwLARM5}?$|VJbc!uf&D1n1WqT`Z7l82%3kbo>5lf+Lue(<#(P{!$ZtKeEqYhe*7B!Lf}2$j(>ixe%o8Xa$lY`Orb2kOp{UHs'
    b'}M$!Y8vxBz^eC9x*)p<+l5RS6(&ls$-'
    b'_P{eL^^O+2i!O`Wdn|Ak12FQ{xk^~{{9As6zCA9c(T8GS2caWIzkN_FQH&@hu=e<k<6VbOQA1uLv?`dyG+i%-'
    b'22DTciq`9{DK<z^=Gfeb4^_UTv^~K^8P~xm)E43H@)gZ-*@EbAVUT)gL48uzRt1j(~Ad!*4#m-'
    b'+y2hQ%ObO0J0FrA1u{2eliS`nbkN>5-'
    b'G4cUzoyBniKKJYXJ{GI31H*p|4M<x+iP24}RI?}(O2~q8^5f+;0V~5EZHH{h;FRlwtyg;$A?5Hj74D%QTo)8hKN}Cs?QlknAR(K+'
    b'747pawS}-'
    b'bJWFPLQw&3TE&849Xxf~Fp86JYv){)Pz&>{cbMnfZEru6MaKHzYXhIGWsQ;2|?AnZB$5u(dB00eU**&)tq)FN>~e2$VSY6=<@wo?'
    b'}xq~FiZgK}tTlnVM8jzQ`*TC+P9M4{mgdhZA$B+W`T=wAX~W9d!5=<lKmUZGX&AJlwfaT&{W@g{}lE2IlpJ>cK2XrzMl3X4omL}G'
    b'WCXnkH23F0&owiREC>N`lbGOwYyLEwu7gD0lu7%(~HjA~!}Hr$Zv*k4aw6i+#*hgN|H7zkZ(NoLHc)19HgpLwHJCL#==0RdWtVW~'
    b'a9`Gqa{l;RO;<tgu&3x*q-'
    b'*4#p61b7@hNmj0PEsp+D*C*69?yThx(odjp23i5e1OrY2_}6TOXMqloxc8zATpFGqg$kzO^GYA$v+|)IK-'
    b'M)kDHe$;ZHr6psBE;*KBx%X6YP!2)-@mu{5-;oS|ZB#g{>YvPvANQZX&0N$`hTJEPanc<2ux0r<-'
    b'I+d4eNY#FNd96nlXJUs*v;<jX`bCX}HJZ^O<zg|82H^zFcrsLkm*3Ih=81JuW7yuu{oxWUB*UwQ>qG##TJr>ZH*E5HK@vkSTbR;W'
    b'M|l#<ge!SkstS*AeKLG55mqD^SeD$f{@>d<8tA;P>RYWU(YcsD5~iXl+-'
    b'pDu<HP*fE;Q{{!IXVEImcoP7!2c!ph<SKCmVwYkv$M<p4?K995R-!cXwDXJt@a09-'
    b'LxMVB+QY`PRgo0UPju>n6Z3Xd+Q!0to}mGK#21?j-'
    b'vaB=a5#@8HB5Xj&twt}k63_{kva(yCWj{7@R6^YXb(UeZ6k0b{X`*Px_SP@hjUGd)OO4(QAUkA=CSj`)AM>SlTj*gvP8ut$U!4BR'
    b'31XE(XI&58cwWeNTblPbB&e&*`|9W>z_%Soesg3f@T6<SXmB?m;m15tW(aU@FAdiF^sFCX|Nu2g34peU!JPCy9|=>s|Xvy2Pk=@_'
    b'Q$2oqnsy-FP#lZ;C+B;V&FyozkjxDf})B3CAxs;1pld3<V(9eS`HJ>k$6-'
    b'>V+pz|5kkfMLgGXqy|BeHSuVO0|8lOV8(j;w?C1k&GNd;KYs2R_O5yfQ-AHG{zC7pp=T5I3%}3)PIV~EN2L<iYrO}YXh-'
    b'6KUp^Y;y(tzcH+axrNB?E~e{g{C&C+ysx2<D^l6Loaa%DbYM5iyH0#<(<zDd3oAIb0V*1m=7*Q38kvi>*=G-~@VWKt(v^9$}-'
    b'CkdU+jk+TcC$X+}S5a8h=-'
    b'(~8}$nX$A0$4X7ic$5MAkb<C0&g%w3fJnYl4+RnHK|Lk(h%M+`hk#5Q;IR`L7^ZbF&KS`*Aa@+P&gwbRvl0!_X!v`OaoMmIGy|L@'
    b'XB3B1Ob5-'
    b'7#_ii8dTe%(y$ujzoXUhV^|bNg~70MQCf`#(gVFAwg5L_{$zWWd?Ec+Nt0pe2@wx|@Xio~I?_eNXoHJ>@dS&%<SX>wNT{o>psw;n'
    b'Ne0dAIzVw^1OWk9!b^h;v9Dub2s8W(v%k#{68uJSXUGR_Eqrm<97;pp79bgCwPn1?I>GJ<FqTVh;2RMB&5JWSs>&@@Jg>l(JBbn}'
    b'D8u6?T;jzmBXvct{ZM(hm$hmJfAdSetc0)^JRGEnC%Evz1f-'
    b'g#0r;tu_Qclpgf)amk#!B1M1x&qYWfmR<5M7%mb|TmOb6bQzCzlxIBi@OJZ7CVtvFC!$TPIAreFNdOTL=9upAOzx<<vbNcz*`h$2'
    b';9x|$<UDY_z%+AysH9f>*MX<n09T~f<klhwo(fbl+21=IzoeIeyUEPC6(0y44MQYQof0}b}gZ!)Twpc$HlFc=Ym>Mm4HaGFLE7z9'
    b'UHYbtMmE0!EwqL#EY`?f1OywiH1Y7xI1+ryV4j?47T*i<l17gt<?&;+v{R@MvtPFp;9?w9V4<n92amvDA!u&?eWdz1jG8^`F5%&#'
    b'ZA_7{$*96*EoS4{7sI!y^aXcqw44?1bMPVNyiQsNy!UQpP$j$vGFP(DZuD!Pk5=6jhCI(=Q+9WwQsO6Kpg^LTVwzM3PV;RvinoZj'
    b'Oah#mBRQ%~UKn<=bLT_(T|ksBf(SH??Knv&d6*bA7Bjj{o!;j)X|r#LhC9{UFri=Y8fq$R@nBG{zHKEpJ(L6%<n`H^5!B4=g8+8w'
    b'MKCKjIlMjhB|bXb4`a6+&tIETcNGAWn?2OK7%6r+HFKh&k0oHBZw60py~fHg_VfS*7<Jjj$y@jFMJlW-7c@EGZsg-Qv7vM5JHBKI'
    b'Rv-'
    b'=ffi5Uy!jFzS|fkN88s!q6O}Y;}}!&XOe5+{X2pY;Ue!Ke`(j79^5JB?IXVD&vDl6Ivg{azOq{np3gpAN(0o>r@!ha9EnP{F=m^='
    b'3JEm4B9PlQ3`^F{GisFdIGfy-'
    b'C|*7(UBQw%xciqz8}FvfJ655ju7yDjxP(cv|Xcx;|)Ozx$ixAni;hHMN0_(L3|eX)(yx6eFVojw+60EYE1Kg1bZ9^sH_<umiX~lT'
    b'dJ2R4ywoDKrs28UPD1Rap)9afySgMD4V@CjabM@`X3{$jWaaMxt=Kk@-'
    b'CrV!NM2)aPgE8&j5{I`E0N%WwbkzFm!I7s7NrPWOTo#uJo{ZL35Lg4{x-'
    b'i20mNElp<2MW{cYL#^%!;eb+;9H|vGsP(?^c(wsC$N7GW3Z%;w;8P_M^v>T{|q+w<R{bM)-'
    b'c&NC2AOK86%Xf|BWY=gN6hXMZ=tnE!DPf<!4^;}?BOTCkSZ{>*smY0~<3u24T-2H1u`lE-Wj($Pf*epFO`wQMI&i0>deH)K8^9+@'
    b'ptu{Fi0-X{Mh%8NLMMTP_J){9i5g73PrdKiNGn>pO8XZ4Si^Tq@wGq^xGDnAW;AaE#6Fci&`wnDlx~SD1-'
    b'O^5*bqbrp72&p7C_MyFj$*<8wLJ`PeH>Pzgarg2NOFqnP(YtcB_z6zyJkE70{~aODLL(*5ph%*H{=$q1~ewZ-'
    b'8g*U3r=P0Hj!;N?GiTwv8B>q#5;yu&*QRkhusts0IW?H^63}_5<(?^$OZJwNofJ<O#HT!#OLlqyy>WsVXTQ;3HxR;7!_jjI+H!f&'
    b'Kt-'
    b'v7hHWhOM#$1vRM3P{{boz_TH~NELF6nl1?PAsIF>(=WkfI*FhF9tW1fQ{fg6eY0Z<&<7pkU3Zr2<w4uRU>N@b1^ul1IT#)t#leT_'
    b'#(&|V7EdL459ErJjy5Hdp~<-'
    b'w_rODdu1AZD5LNlchm_kvJM;0a9j$(oHh>ElgfwvUT}&h@RQjc`WK}xRX;Lcfn^C|b@nIq)o+gm;*ooBeWVcSF&|n#TX(tvBKHAW'
    b'p@N$}k#UdhKNcX6nYYi##wgP2?IU>Cy8&f)@(=->&RdX-egK(z+>y}eAP55?MwJgmHicpyF@~3nsolHj;5nILRQMa{YsL=PBbRw('
    b'h!SEe`kV@<PBxC6wi`Rkps~w#{+Q*`=$s{&$Am$;BgZ1>|fDb*7=y>s_o^>$IwlHtx^s1%#U)!-x<Ryi@D8FO02~-4<Lv%-'
    b'26L$&mtzz1Tb`2d0L3M_LqJbcBDkw$RdX&dC1$2>i1?jBa;^V<`(g^L_SekZG9k^5Mz%Doq%~OV^%sO&IwoDUs%{jVUYZF00VmcX'
    b'+aRIMq*i`?bK?hxeMuH&%1|FR>?~If)G;%s#S>AQ-+6RsogbteSh4n!?QWRiB?>(~_(+L^qPnG<Sxj@k2lB6va=zgcms&Kw-'
    b'Y50<Ye?UQ-T+Q8+d(|?q8xcDdG#-#Hd$w$I>pey7UvvY(fM?_(%I%wNT_hR-jCUB%N`kQ%2>`A1tSB4BIdusZpyMVw#3MyI5rgS|'
    b'4klR@j&!O3*1)tcu^852><(lb1ts|iuK?1ngEx>fkgiA7UiX_R?Ewxd3}=Ig1miTlIa~)_UGcMvr>cWqm<@&L1cykW)4_Cl?IjrP'
    b'A)<;-'
    b'*?H|UFn44PCsMQ<25{gEmd<0fWe3s<B7CstavyCbzCA@aFS?BNKp_S%C)w|`8a|H)L;)KTCp^QQfUvUxS%HU`eVrWmKs4fe!E>%&'
    b'As8?PXrXWLAWD#*>Dm;~fKpp%G}9UdJ+6&48ss|~*R(wxG@Usbq3t?(wsi1sc<P&JeAo`_QcxKt4OK364XXkczsJ8qrzwX<hORSe'
    b'K(_V+Fo0x6o}Qoq%&vnkh(B_{&l+7Q;(-Xh`3=wA@cD@GL%A+(h9dz-Y6zjKU76wJGHOSSTS#UZF3BBnj|zDcuBmo#?HbVrBoi%-'
    b'QKdWS{EPQqun8I;ngGM`wm3feopL{<rTvZ%^BRa@Ih(Xj()=e4jDOZX=FmYlqO1|EL~u%JpjW%*>xPNt@^9VHw9j^Ra+F0u)8Uk0'
    b'I!vA=-0(5&+%%0FU};oY0gn3S33<lx4Z$};1GBF)UFeL6{j*&#I@(jBp>~$h7@!$fnzBB#a=o^@tZ}+8h)!5cN7xW$uuor-lbZhX'
    b'Bz%elOScEI(r?sSHC=IlQR)WA{DxTjujv_PWVtE&WrM0{?kT(HICMA?=y=q>HXFIvhU^ZV3bplbp8-'
    b'=GVW~}RZD{R6Ec|Z78Umaa1`@A6JB${P9Uy7T4Ml>-@*Cd}gYF}_D!jXJ$S3Q$npQMa1=J`bhdIA^S&Fx6LWE{UfpC-'
    b'G^EWz2MC;?#r;c`DJprfs@OHw;FYu^v31Eus7Nkzn?3>@-'
    b'GspCM;EHg=J=i9~ix62!TjH}cDG;ALb_XW#f1c1Q2}f|XnF5&tk^RdQk)wvO;E+qLuH6Wf2$nDlT}#ox4x~$F8u9|$OQR=r$&%q('
    b'-{2)9nvua%{<$F8eTE`JWRYD&0|S6M3z=TRX(X)y^BUMeDD~5RMKt2LL7iA#a6`JW8)OUCyV#0Qdr&oD`*k`B`a#fR^mR0)epQTz'
    b'M>+d5ve&K<Xe_&d-T~$-t%Nv7Q&`u$k^oYZO$RE?m4xqb2-Y282H>rLyh_qs749pS#~+2tsSu$+95JX-QNvepx2hrk*k2VFGbE2m'
    b'gl7*+XO{$*Q&MrD1$3MXfr{yFFd(&w|7tC0I*`X#HyBj`wF8Qjp=*1?b#iY&Hck67)F-9~1|-'
    b'ee!QsIo7epSyHQ&BwpcklKx)C)F#Z{05paS88j#5|=-hq5NwF$ZQ=imlfL0e8T0^fud)fQ<#B0Dv%n0_6-'
    b'iYV3z+Mx4e7&5NR((;Xz4HRN{+MyGg?`5!-)9~pLHF`AjxfS&=A7BD1Bs@c`^foukSy#hRVn=Z?NUkr$Q_Q1-'
    b'eb{Jv1lL{QA3nxfuwH;rtUI-1^dS<?wjoN;TvvtOzk_;-nx@eEh62D$#1>q&bvh+a5e5z(*+>(Zm|dqMhmHiI`>D3{t0-'
    b'oH7HNEH23v<ELc3I+&$o`ofri@u*O87O?rM>C0{ls7Y$Pgv8w47SEVLNK1h(qzk_vD%fX@$gUGF2+3(6m?r;KPGDg&6t7Uyp&KvJ'
    b'n3Ru2SFsN5Tk{R}fMCR9Ll!`8$M1VOKBB2Mo+qN~)8H3v*F7fldg$Auv6c?PVq%+SDhAr&Ix7~+J3a5idj5WVXF#2B@GN|aAkR6X'
    b't%8LcQ#gOP7*a)M9kpg5n-z~&8Y>$n`|AE{qy_+QV^vIadm?XhrgG`1!_q<p~HT`g$pPynC50INBe{IF@xzt^`Rscj-'
    b')OAhxwqfSGTQWZ!nK%4eQHIdrk#CB2RQ~~Bd`^Ln{`?p(0&`=+g6-xz?55ioVAJksd{?-&6Yy>ar2^fMHR*ZE}5_O<NUV@oaX<b-'
    b'0O)50u#b6x_BgL*`jShta7ciJV0>vZjTu>X@oYg7oZ|*m9Idq!HtO*~lw4I|WL?qM)WJm3yxNUaYZYPtBUt-Pt8R$b9LtS039JGb'
    b'%(xeAdy1-yVrLNwjn{_4_)I@#qhmJ%_*3v)U8I!Fe=~bK6xla_s4)Q)20u>;#c%bnXsntAeK7D@SP}BHBM}6MdKpLazv`!6}-'
    b'i8j-Xg2cuA>tr$AD4n_AU`#%lb}JH=9FxR(>`0ayG}_rSOcF`>P5-Z#?J<v)LrI>C{v8U5Gfx;W$A2^Rs0cY{7%@#j0Q4PT|h-'
    b'ua7w(8U5=2T6D?SFJ*N?KKT)SN*9d_&!N7mx!&}uQ9eTjS9lb4bRI6Q^7@GIrqWKYygGQ?uvczh1@_nslIJsBf07F+sYl9&X<r#J'
    b'2781VFFgkHVOEj!Qfe|#C*SL@7*;DJ?AKvIBA>|(rW>|a9TR2DBU0jUk-CQVBp*-X%w2g<>FhVsyhqb>EndUkzW2>7^FCiQ$d-'
    b'9>%her8Oj~naIb=Yc4i);IWplssf^ziS#=CcbX7pPOva0b$~;td}~i1!|VHGw_@Gn}jxib?G=HSSvZn-{OzG~OR1g&=OV%hEB^-'
    b'GETABbBL>To;UD-JoepcJxXJ&2RnN9t9k-'
    b'=0KOaFLz+1c!snno9>vcXS)RwZ7fD77_SaZxsKFmm+S2*gtrFedhz5y*8&@Ygrr@X+IAh2MiNT&Ey;9NnzV5?df=&Wt>3`zgp3G9'
    b'9dPG~O_UWBHh}I#$uwn1L1SR(4RHv9CT+|>!a4)|Z7gNYv*_Fk<A=MnM1;L8qxJ|iI4?R^YyehRd3AKaq^flGqJC%g9j7&YNiFpW'
    b'9Z^NM`>-fFfiiLa8n|?wMoqN#p%}HL`pmDUe<Lyk0|2~9w~mZB#ilKfwRJ$V5cPv-$9;k^-'
    b'Mne1fjDm6$kJ@zM)uU{>bQV*OqGsgi20j6AWV~LYi7ZKz%2fSw0C&9%Vjr!)82V8%Q>2YJntyz9T2<$k(%1gB=*|52y!$P0@6`_e'
    b'-1vNpo~ke?<}O|#28KCf@Kf|FB$<Dcwq+3Yobmnfx9?D=^cVXpf}g0h|l@9D-'
    b'a*rS^_3e;vwn<r>MQXIMGdOAuTm43m9)514?=Wqr{-'
    b'?n6c#$zVkOI20T8BT4%>1kX)(YrsJ81AX31o5pn!<wgM?u*Upg+(qmh{gTbC@T$)}3!?I8=WM_i4XkeaFJTtTriN4n^NC#3!$U6T'
    b'|6g5`-'
    b'oG&7=j?h%h=O1kcKtLdRDc~75yL4LxAdYq;lk3Pd{sL;Z?`hyg!q$(@1kZ+0La}zgC0NxPXA7<(`Ff9RiV5*|1c>lzw=@u>Z?hI^'
    b'7BjlGftKD6(R)Xz8K_#X)94+qm^P#X#A8Qr{!ORR&>VRC`@QP{A7bhRa1lgG<2fY(JQp6G=-(@=g4$)#yXos0yP(-'
    b's9^W*HoJH9_{v8_yshzQcadz#-'
    b'FUTrTN+*K4gP&DI`_ZVsN1z_d^ZOQ{P70NcnASOcWKh;w1>i9%XYz0frHqIza^BpER#sVSuNHavCY(&;NugO?$ZCrn3kbTQY5OG%'
    b'NFroJPI^^KXEmSgBONH}1^NGGif*g+%qz1_L&bSar;ri*4R#@5!PWLAfvuPMOnMBs!GAQ8^<9Q<>4d&(%4<LvN+@anN{8a03;K&l'
    b'2F;IW)8QPt3mk&m@CU!A$dJHDyl1v$SF@?D4tU-rc#h;|?GeK_Xr*a}ElDHmRRTOvs_ommD+fo0K_s$UuL?CFNhI3~or-'
    b';>pXemqR?`8yterG;9$5hu5zO{!KSQT%iWF?kgC2s)bcE7Z*N*)FymS_jekDK{1MN)V*=a9u|2u4t3n=vVj(U4iC%?Vu^mx|Lq|8'
    b'3_ZjKohdh<!KsHrG=$FIWG^xbz(v=ZE`L!mco=M&sH(igzq0D^Ut1NoFh<Zv%7`J7wTyJ~oh?|^5bVX&hG$=t?s(DZnT+Cb_^$V@'
    b'}}*2{Wv;>Qy?q*g<qn9zfW%y;hBwE1}p5_cBa+DW7VZI%b(7&>wvVQIq40rf?59>}n{4#KqGQyobEXYR<iCUP|CRb6f8^JLyeEzg'
    b'^TTRTC-'
    b'8Kjco%MVwO)9BwWtBzgh9TBh3p;$qRriJvn??Nx7mi2a3>|p@dI{rYvVQD3o+vvZq@9pP^Cp;bjrL8xhC^fw?s=%Pqqv^dI?|PGt'
    b'o2FT}X5C|8$`xY&&;JKBqnV@'
)))

def _is_floats(value):
    if isinstance(value, float):
        return True
    return (
        isinstance(value, (list, tuple))
        and bool(value)
        and all(isinstance(item, float) for item in value)
    )


def _framed(payload):
    return len(payload).to_bytes(8, 'big') + payload


def _stable_output_bytes(value):
    if value is None:
        return b'n'
    if isinstance(value, bool):
        return b'b1' if value else b'b0'
    if isinstance(value, int):
        size = max(1, (abs(value).bit_length() + 7) // 8)
        magnitude = abs(value).to_bytes(size, 'big')
        return (b'i-' if value < 0 else b'i+') + _framed(magnitude)
    if isinstance(value, float):
        return b'f' + value.hex().encode('ascii')
    if isinstance(value, str):
        return b's' + _framed(value.encode('utf-8'))
    if isinstance(value, dict):
        items = [(_stable_output_bytes(key), _stable_output_bytes(item)) for key, item in value.items()]
        items.sort(key=lambda item: item[0])
        return b'd' + b''.join(_framed(key) + _framed(item) for key, item in items)
    if isinstance(value, list):
        return b'l' + b''.join(_framed(_stable_output_bytes(item)) for item in value)
    if isinstance(value, tuple):
        return b't' + b''.join(_framed(_stable_output_bytes(item)) for item in value)
    raise TypeError(f'unsupported output type: {type(value).__name__}')


def _output_sha256(value):
    return hashlib.sha256(_stable_output_bytes(value)).hexdigest()


def test_humaneval_plus_suite():
    candidate = parse_music  # noqa: F405
    for index, arguments in enumerate(INPUTS):
        output = candidate(*copy.deepcopy(arguments))
        comparison, expected = EXPECTED[index]
        if comparison == "sha256":
            if _output_sha256(output) == expected:
                continue
            raise AssertionError(f"HumanEval+ case {index} failed")
        try:
            exact_match = bool(output == expected)
        except (TypeError, ValueError):
            exact_match = False
        effective_atol = ATOL
        if effective_atol == 0 and _is_floats(expected):
            effective_atol = 1e-6
        if exact_match:
            continue
        if effective_atol != 0:
            if type(output) is not type(expected):
                raise AssertionError(f"HumanEval+ case {index} returned the wrong type")
            if isinstance(expected, (list, tuple)) and len(output) != len(expected):
                raise AssertionError(f"HumanEval+ case {index} returned the wrong length")
            if np.allclose(output, expected, rtol=1e-7, atol=effective_atol):
                continue
        raise AssertionError(f"HumanEval+ case {index} failed")
