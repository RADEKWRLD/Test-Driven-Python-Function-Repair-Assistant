import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[['**', '*', '+'], [2, 3, 4, 5]],
 [['+', '*', '-'], [2, 3, 4, 5]],
 [['//', '*'], [7, 3, 4]],
 [['+', '-', '*', '//'], [5, 2, 3, 4, 7]],
 [['**', '-', '//'], [9, 2, 5, 3]],
 [['*', '-', '*', '//'], [3, 6, 2, 4, 2]],
 [['-', '//', '+', '*'], [10, 2, 4, 3, 6]],
 [['+', '-', '*', '**'], [2, 3, 4, 5, 2]],
 [['*', '+', '-'], [1, 2, 3, 4]],
 [['-', '+', '*', '**'], [5, 4, 3, 2, 1]],
 [['*', '//', '-'], [10, 5, 3, 2]],
 [['**', '+', '-'], [3, 2, 1, 4]],
 [['*', '+', '//'], [2, 5, 3, 8]],
 [['-', '+', '*', '**'], [5, 3, 3, 2, 1]],
 [['*', '-', '*'], [10, 5, 3, 2]],
 [['-', '//', '-'], [10, 5, 3, 2]],
 [['*', '*', '-'], [10, 5, 3, 2]],
 [['-', '+', '*', '**'], [5, 3, 3, 2, 2]],
 [['*', '*', '-'], [9, 10, 3, 2]],
 [['*', '-', '*', '//'], [2, 6, 2, 4, 2]],
 [['+', '-', '*', '*'], [2, 3, 4, 5, 2]],
 [['*', '+', '//'], [2, 3, 8, 5]],
 [['-', '//', '+', '*'], [9, 2, 4, 3, 6]],
 [['*', '+', '//'], [2, 5, 4, 8]],
 [['*', '-', '**'], [10, 5, 3, 2]],
 [['-', '+', '*', '**'], [5, 3, 2, 2, 2]],
 [['-', '//', '+'], [10, 2, 4, 3]],
 [['*', '//', '//'], [2, 5, 8, 5]],
 [['-', '//', '-'], [10, 2, 3, 2]],
 [['*', '//'], [2, 5, 5]],
 [['-', '+', '**', '**'], [5, 3, 3, 2, 2]],
 [['**', '**', '//'], [9, 2, 5, 3]],
 [['*', '-', '*', '//'], [2, 6, 2, 3, 2]],
 [['*', '//', '+'], [2, 5, 8, 5]],
 [['-', '+', '*', '**'], [5, 4, 3, 2, 2]],
 [['//', '//', '+'], [2, 4, 3, 4]],
 [['+', '//', '//'], [2, 5, 4, 8]],
 [['**', '//', '//'], [2, 5, 4, 8]],
 [['**', '+', '//'], [2, 5, 4, 8]],
 [['*', '//', '//'], [2, 3, 8, 5]],
 [['-', '//', '+', '*', '*'], [10, 2, 4, 2, 6, 2]],
 [['*', '-', '*', '*'], [10, 5, 3, 2, 5]],
 [['**', '+', '-'], [3, 2, 0, 4]],
 [['-', '+', '*', '**'], [5, 5, 3, 2, 2]],
 [['-', '//', '+', '*', '*'], [10, 2, 4, 2, 5, 2]],
 [['**', '**', '//'], [9, 2, 5, 4]],
 [['-', '-', '+', '*', '*'], [10, 2, 4, 2, 5, 2]],
 [['*', '*', '-'], [10, 4, 3, 2]],
 [['-', '+', '*', '**'], [8, 4, 2, 2, 2]],
 [['+', '//', '*', '**'], [2, 3, 4, 5, 2]],
 [['//', '+', '//'], [2, 4, 3, 4]],
 [['-', '+', '-', '**'], [5, 4, 3, 2, 1]],
 [['-', '+', '**', '**'], [5, 5, 3, 2, 2]],
 [['-', '+', '**'], [5, 3, 3, 2]],
 [['+', '-', '*', '**'], [8, 3, 4, 5, 2]],
 [['+', '//', '*', '**'], [2, 3, 3, 5, 2]],
 [['-', '+', '-', '**', '**'], [5, 4, 3, 2, 1, 5]],
 [['-', '//', '+', '*', '*'], [10, 2, 4, 3, 5, 2]],
 [['-', '+', '*', '**', '*'], [5, 3, 2, 2, 2, 2]],
 [['**', '**', '//'], [9, 2, 6, 4]],
 [['//', '+', '//'], [1, 4, 3, 4]],
 [['+', '-', '*', '**', '+'], [2, 2, 3, 4, 5, 2]],
 [['*', '*', '-'], [10, 5, 10, 2]],
 [['-', '//', '-'], [2, 3, 6, 2]],
 [['-', '+', '**', '**'], [5, 3, 3, 2, 1]],
 [['+', '+', '//'], [6, 4, 3, 8]],
 [['//', '+', '//'], [8, 4, 3, 4]],
 [['**', '//'], [9, 5, 4]],
 [['**', '+', '-'], [4, 2, 0, 4]],
 [['*', '-', '**'], [10, 5, 2, 6]],
 [['-', '+', '**'], [10, 3, 3, 2]],
 [['**', '+', '//'], [8, 5, 4, 8]],
 [['**', '+', '-'], [2, 2, 2, 4]],
 [['*', '**', '//', '-'], [10, 5, 3, 3, 2]],
 [['-', '//', '+', '//', '*', '*'], [10, 2, 4, 3, 5, 2, 4]],
 [['**', '+', '-'], [0, 2, 1, 4]],
 [['-', '//', '-'], [1, 5, 3, 2]],
 [['//', '-'], [1, 5, 3]],
 [['-', '-', '//'], [1, 5, 3, 2]],
 [['//', '+', '*', '**'], [5, 3, 3, 2, 2]],
 [['**', '+', '-'], [2, 8, 2, 4]],
 [['*', '//', '+'], [2, 5, 8, 6]],
 [['-', '+', '**'], [5, 3, 2, 3]],
 [['*', '-'], [10, 5, 2]],
 [['-', '+', '*', '**', '*'], [5, 3, 2, 2, 2, 4]],
 [['**', '+', '-'], [3, 2, 0, 5]],
 [['*', '*'], [9, 10, 3]],
 [['//', '+'], [4, 3, 4]],
 [['-', '+', '*', '**'], [8, 4, 2, 1, 2]],
 [['*', '-', '*', '*', '-'], [10, 5, 3, 2, 5, 3]],
 [['*', '//'], [2, 3, 8]],
 [['**', '//', '//'], [5, 4, 8, 4]],
 [['+', '-', '*', '//'], [3, 2, 3, 4, 7]],
 [['*', '-', '-', '*'], [10, 5, 3, 2, 5]],
 [['-', '+', '-', '**', '**', '+'], [5, 4, 3, 2, 1, 5, 2]],
 [['*', '*', '-', '*'], [10, 10, 5, 10, 2]],
 [['//', '+', '//', '//'], [8, 4, 3, 4, 4]],
 [['-', '+', '**', '**'], [5, 3, 10, 2, 1]],
 [['**', '+', '-'], [3, 1, 1, 4]],
 [['**', '+', '-', '+'], [2, 2, 2, 4, 2]],
 [['*', '+', '-'], [10, 4, 3, 2]],
 [['*', '+', '//'], [2, 3, 8, 3]],
 [['+', '-', '*', '*'], [2, 3, 4, 5, 10]],
 [['+', '-', '*', '//'], [10, 5, 2, 3, 9]],
 [['*', '**', '-', '//'], [5, 2, 7, 10, 3]],
 [['**', '-', '//', '+', '*'], [2, 3, 4, 5, 6, 7]],
 [['//', '-', '*', '**', '+'], [10, 3, 5, 2, 7, 1]],
 [['*', '*', '-', '**', '//', '+'], [2, 4, 5, 2, 10, 3, 8]],
 [['//', '**', '-', '+'], [7, 5, 3, 9, 2]],
 [['*', '+', '//', '-', '**'], [9, 3, 8, 2, 10, 7]],
 [['**', '//', '-', '*', '+'], [3, 4, 5, 6, 7, 8]],
 [['+', '-', '//', '*', '**'], [10, 5, 2, 4, 3, 8]],
 [['-', '//', '*', '**', '+'], [7, 8, 3, 10, 2, 4]],
 [['-', '//', '*', '**', '+'], [7, 8, 3, 8, 2, 4]],
 [['//', '-', '*', '**', '+'], [10, 3, 6, 2, 7, 2]],
 [['//', '**', '-', '+'], [7, 5, 3, 9, 9]],
 [['//', '-', '*', '**', '+'], [10, 2, 6, 2, 7, 2]],
 [['//', '-', '*', '**', '+'], [10, 6, 2, 7, 2, 6]],
 [['//', '-', '**', '+'], [10, 6, 2, 7, 2]],
 [['//', '-', '**', '+'], [10, 6, 2, 6, 2]],
 [['*', '+', '//', '-', '**'], [9, 3, 8, 2, 10, 2]],
 [['**', '//', '-', '*', '+'], [3, 4, 3, 6, 7, 8]],
 [['-', '//', '*', '**', '+'], [9, 8, 3, 8, 2, 4]],
 [['+', '-', '//', '*', '**'], [10, 5, 1, 4, 3, 8]],
 [['//', '-', '*', '**'], [10, 3, 2, 7, 2]],
 [['//', '**', '-', '+'], [4, 5, 3, 9, 9]],
 [['*', '+', '//', '-', '**'], [9, 3, 8, 2, 10, 6]],
 [['//', '-', '*', '//'], [10, 3, 2, 7, 2]],
 [['*', '+', '//', '-', '**'], [2, 3, 8, 2, 10, 2]],
 [['//', '**', '-', '+'], [7, 5, 9, 3, 9]],
 [['-', '//', '+', '**', '+'], [7, 8, 3, 8, 2, 4]],
 [['+', '-', '//', '*', '**'], [10, 5, 1, 4, 6, 8]],
 [['**', '-', '//', '+', '*'], [2, 3, 2, 5, 6, 7]],
 [['+', '-', '//', '*', '**'], [10, 5, 2, 4, 3, 7]],
 [['*', '+', '//', '-', '**', '*'], [9, 3, 8, 2, 10, 6, 9]],
 [['//', '**', '-', '+', '+'], [7, 5, 4, 9, 3, 9]],
 [['//', '-', '*', '**', '+'], [10, 6, 2, 2, 6, 10]],
 [['**', '-', '//', '+', '*'], [2, 3, 2, 5, 6, 6]],
 [['*', '+', '//', '-', '**'], [9, 3, 8, 1, 10, 6]],
 [['//', '-', '*', '**', '+'], [10, 2, 6, 2, 5, 2]],
 [['//', '**', '-', '+'], [2, 5, 9, 3, 9]],
 [['-', '//', '+', '**', '-'], [7, 8, 3, 8, 2, 4]],
 [['-', '**', '*', '**', '+'], [9, 8, 3, 8, 2, 4]],
 [['+', '-', '*', '**', '-'], [10, 5, 1, 4, 3, 8]],
 [['-', '//', '*', '**', '+'], [7, 8, 8, 10, 2, 4]],
 [['//', '-', '**', '//'], [10, 3, 2, 7, 2]],
 [['+', '-', '//', '*', '**'], [3, 5, 1, 4, 6, 8]],
 [['-', '//', '*', '**', '**'], [7, 8, 3, 8, 2, 4]],
 [['**', '//', '-', '**', '+'], [3, 4, 3, 6, 7, 8]],
 [['*', '+', '//', '-', '**'], [9, 3, 8, 6, 10, 7]],
 [['**', '-', '//', '*', '*'], [2, 3, 8, 5, 6, 6]],
 [['**', '-', '+'], [7, 9, 3, 9]],
 [['**', '**', '-', '+', '+'], [7, 5, 4, 9, 3, 9]],
 [['**', '-', '//', '+', '*'], [2, 3, 5, 5, 6, 8]],
 [['-', '*', '+'], [5, 9, 3, 9]],
 [['**', '-', '//', '+', '**'], [2, 3, 4, 5, 6, 7]],
 [['**', '-', '//', '+', '*'], [2, 3, 1, 5, 6, 6]],
 [['-', '//', '*', '**', '+'], [8, 8, 10, 1, 2, 4]],
 [['//', '**', '-', '+'], [10, 7, 3, 9, 9]],
 [['**', '-', '//', '+', '*'], [2, 3, 1, 9, 6, 6]],
 [['*', '-', '**', '//'], [10, 3, 2, 7, 2]],
 [['**', '-', '+'], [7, 4, 3, 9]],
 [['//', '-', '*', '**', '+'], [10, 5, 6, 2, 7, 2]],
 [['//', '**', '-', '+', '+'], [7, 5, 4, 9, 3, 3]],
 [['//', '-', '+', '//'], [10, 3, 2, 7, 2]],
 [['-', '//', '*', '**', '+'], [8, 7, 10, 1, 2, 4]],
 [['+', '-', '//', '-', '**'], [3, 5, 1, 4, 6, 8]],
 [['//', '**', '-', '+'], [7, 4, 9, 3, 9]],
 [['-', '+', '*', '**', '+'], [7, 8, 3, 8, 2, 4]],
 [['+', '-', '//', '-', '**'], [3, 5, 1, 4, 6, 2]],
 [['**', '-', '*', '//', '+', '*'], [2, 3, 1, 5, 6, 6, 6]],
 [['//', '**', '-', '+', '+'], [7, 5, 4, 10, 3, 9]],
 [['-', '-', '*', '**', '+'], [7, 8, 8, 10, 2, 4]],
 [['**', '-', '//', '+', '**'], [2, 9, 4, 5, 6, 7]],
 [['+', '-', '//', '-', '**'], [3, 5, 1, 4, 6, 5]],
 [['**', '-', '+'], [7, 2, 9, 3]],
 [['**', '-', '+'], [7, 9, 10, 9]],
 [['**', '//', '-', '*', '+'], [3, 4, 2, 6, 7, 8]],
 [['**', '-', '//', '+', '*'], [2, 3, 3, 5, 6, 5]],
 [['+', '-', '//', '*'], [10, 2, 4, 3, 8]],
 [['//', '-', '**', '**', '+'], [10, 6, 2, 7, 2, 6]],
 [['-', '//', '*', '**', '+'], [7, 8, 8, 9, 2, 4]],
 [['-', '-', '*', '**', '+'], [10, 6, 2, 2, 6, 10]],
 [['**', '-', '+'], [7, 2, 3, 3]],
 [['**', '-', '+'], [7, 2, 3, 9]],
 [['-', '//', '*', '**', '+'], [7, 9, 8, 10, 2, 4]],
 [['-', '//', '*', '**', '+'], [7, 8, 3, 7, 8, 4]],
 [['+', '-', '//', '-', '**'], [3, 1, 1, 4, 6, 8]],
 [['+', '-', '//', '-', '**'], [6, 3, 1, 4, 6, 8]],
 [['*', '**', '-', '//'], [5, 2, 7, 10, 1]],
 [['*', '**', '-', '*'], [3, 2, 7, 10, 3]],
 [['-', '//', '*', '*', '+'], [7, 8, 3, 8, 2, 4]],
 [['*', '**', '-', '//'], [3, 2, 7, 10, 3]],
 [['*', '+', '//', '-', '**', '-'], [9, 3, 8, 2, 10, 6, 10]],
 [['**', '-', '//', '+', '*'], [2, 3, 4, 4, 6, 7]],
 [['-', '//', '*', '**', '+', '+'], [7, 8, 8, 9, 2, 4, 2]],
 [['-', '//', '*', '**', '+'], [7, 8, 2, 7, 8, 4]],
 [['//', '-', '*', '**', '+'], [10, 6, 6, 7, 2, 6]],
 [['//', '+', '*', '//'], [10, 3, 2, 7, 2]],
 [['*', '*', '-', '**', '//', '+'], [2, 4, 5, 2, 10, 3, 10]],
 [['**', '-', '//', '+', '*'], [2, 3, 4, 5, 6, 1]],
 [['+', '-', '*', '+', '*'], [2, 3, 1, 5, 6, 6]],
 [['-', '//', '+', '**', '+'], [7, 4, 8, 3, 2, 4]],
 [['//', '**', '-', '+'], [7, 5, 9, 3, 7]],
 [['**', '-', '**', '//'], [10, 3, 2, 7, 2]],
 [['*', '+', '//', '-', '**'], [9, 3, 7, 2, 10, 7]],
 [['**', '-', '//', '+', '*'], [9, 3, 3, 5, 6, 5]],
 [['*', '**', '-', '//', '*'], [5, 2, 7, 10, 1, 5]],
 [['//', '**', '-', '+', '+'], [4, 10, 3, 10, 9, 9]],
 [['//', '-', '*', '**', '+'], [10, 6, 2, 6, 2, 6]],
 [['*', '+', '//', '-', '*'], [9, 3, 8, 2, 10, 6]],
 [['*', '+', '//', '-', '*'], [10, 3, 8, 2, 10, 6]],
 [['//', '-', '*', '**', '+'], [10, 5, 2, 6, 2, 6]],
 [['**', '-', '+', '+'], [7, 2, 6, 3, 3]],
 [['**', '-', '*', '//', '+', '*'], [2, 3, 1, 5, 1, 6, 6]],
 [['//', '-', '*', '**', '-'], [10, 6, 2, 6, 2, 6]],
 [['*', '-', '**', '//'], [10, 3, 2, 2, 7]],
 [['+', '-', '//', '*'], [10, 2, 4, 3, 7]],
 [['**', '//', '-', '*', '+'], [4, 9, 5, 6, 7, 8]],
 [['-', '**', '//', '*', '**', '+'], [9, 8, 8, 10, 2, 4, 2]],
 [['**', '-', '+'], [7, 2, 9, 2]],
 [['*', '+', '//', '-', '**'], [9, 4, 8, 2, 10, 7]],
 [['//', '-', '**', '**', '+'], [10, 6, 6, 7, 2, 6]],
 [['-', '*', '+'], [4, 9, 3, 9]],
 [['+', '-', '*', '**'], [3, 0, 4, 6, 8]],
 [['//', '-', '**', '**', '+'], [10, 5, 2, 6, 2, 6]],
 [['//', '-', '**', '-', '**', '+'], [10, 5, 2, 6, 2, 6, 2]],
 [['**', '-', '//', '**', '*'], [2, 3, 3, 5, 6, 5]],
 [['+', '-', '*', '**', '-', '*'], [10, 5, 1, 4, 3, 8, 1]],
 [['**', '-', '//', '+', '*'], [2, 3, 2, 1, 6, 6]],
 [['*', '+', '**', '-', '**'], [9, 3, 8, 1, 10, 6]],
 [['-', '-', '*', '**', '+'], [7, 8, 8, 10, 2, 3]],
 [['+', '-', '//', '*', '**'], [10, 5, 1, 4, 6, 4]],
 [['+', '-', '//', '*'], [10, 2, 4, 3, 6]],
 [['+', '-', '//', '**', '**'], [10, 5, 1, 4, 6, 4]],
 [['//', '**', '-', '+'], [7, 4, 8, 3, 9]],
 [['+', '-', '//', '-', '**'], [6, 3, 6, 4, 6, 8]],
 [['**', '-', '*', '//', '+', '*'], [9, 8, 1, 5, 1, 6, 6]],
 [['-', '//', '*', '**', '+'], [7, 9, 8, 5, 2, 4]],
 [['//', '-', '*', '**', '+'], [10, 6, 2, 6, 6, 6]],
 [['**', '-', '//', '+', '*'], [9, 3, 4, 5, 6, 5]],
 [['**', '-', '//', '+', '*', '//'], [4, 9, 3, 3, 5, 6, 5]],
 [['-', '*', '//', '+', '*', '+'], [2, 3, 1, 5, 1, 6, 6]],
 [['//', '-', '**', '**', '+'], [10, 5, 2, 6, 5, 6]],
 [['//', '-', '*', '*', '+'], [10, 5, 6, 2, 7, 2]],
 [['**', '-', '//', '-', '+', '*'], [9, 3, 4, 5, 6, 5, 6]],
 [['//', '**', '-', '+'], [7, 5, 2, 9, 2]],
 [['*', '+', '//', '-', '**'], [9, 4, 9, 2, 10, 7]],
 [['//', '*', '**', '+', '**'], [7, 8, 3, 10, 2, 4]],
 [['-', '-', '*', '**', '+'], [8, 8, 8, 10, 2, 3]],
 [['+', '-', '*', '**', '*', '-'], [10, 5, 1, 4, 3, 8, 3]],
 [['**', '-', '+', '+'], [7, 5, 9, 3, 9]],
 [['**', '-', '//', '**', '//'], [2, 3, 3, 5, 6, 5]],
 [['**', '-', '*', '+'], [4, 3, 6, 7, 8]],
 [['+', '//', '*', '**'], [10, 5, 3, 4, 3]],
 [['**', '-', '//', '+', '*'], [2, 3, 4, 4, 7, 7]],
 [['*', '+', '//', '-', '*'], [9, 10, 8, 2, 10, 6]],
 [['//', '-', '**', '//'], [10, 3, 2, 7, 3]],
 [['**', '//', '*', '**', '+'], [7, 9, 8, 10, 2, 4]],
 [['**', '-', '//', '**', '//'], [2, 2, 3, 5, 6, 5]],
 [['-', '//', '+', '**', '-'], [7, 8, 3, 8, 3, 4]],
 [['-', '**', '*', '**', '*'], [9, 8, 3, 8, 2, 4]],
 [['+', '-', '//', '-', '**'], [6, 3, 0, 4, 6, 8]],
 [['-', '//', '*', '//', '+'], [7, 8, 3, 8, 2, 4]],
 [['//', '**', '-', '+'], [2, 5, 10, 3, 9]],
 [['**', '-', '*', '+'], [4, 3, 6, 7, 5]],
 [['*', '+', '//', '-', '*'], [9, 10, 10, 2, 10, 6]],
 [['*', '*', '-', '**', '//', '+', '//'], [9, 2, 4, 5, 2, 10, 3, 10]],
 [['//', '-', '*', '**', '+', '+'], [10, 6, 9, 2, 2, 6, 10]],
 [['*', '+', '//', '-', '*', '//'], [9, 10, 10, 2, 10, 2, 9]],
 [['//', '-', '*', '+', '+'], [10, 5, 6, 2, 7, 2]],
 [['**', '-', '//', '+', '*'], [2, 3, 1, 1, 5, 6]],
 [['-', '//', '*', '**', '+'], [7, 8, 8, 10, 2, 0]],
 [['**', '-', '//', '+', '**'], [2, 3, 4, 5, 0, 7]],
 [['-', '//', '+', '**', '-'], [7, 8, 3, 9, 2, 4]],
 [['**', '**', '-', '+', '+'], [7, 3, 4, 9, 3, 9]],
 [['**', '-', '//', '*', '*'], [2, 3, 8, 4, 6, 6]],
 [['//', '-', '**', '+'], [10, 6, 2, 2, 6]],
 [['-', '//', '+', '**', '*'], [7, 8, 3, 8, 2, 4]],
 [['-', '//', '*', '**', '+'], [7, 8, 3, 8, 7, 4]],
 [['+'], [5, 10]],
 [['+', '*', '-'], [0, 0, 0, 0]],
 [['//', '-', '*', '**', '+', '**'], [10, 3, 5, 2, 7, 1, 3]],
 [['//', '-', '*', '**', '+'], [10, 3, 7, 5, 7, 1]],
 [['//', '-', '*', '**', '+', '**'], [10, 3, 5, 2, 4, 1, 3]],
 [['+', '-', '*', '//'], [1, 5, 2, 3, 9]],
 [['*', '-', '**', '//', '+', '//'], [2, 4, 5, 2, 10, 3, 8]],
 [['//', '-', '*', '*', '+'], [10, 3, 5, 2, 7, 1]],
 [['**', '*', '*', '-', '//', '+'], [2, 4, 5, 2, 10, 3, 8]],
 [['//', '-', '*', '*'], [10, 3, 5, 2, 1]],
 [['//', '-', '*', '**', '+', '**'], [10, 4, 5, 2, 4, 1, 7]],
 [['//', '**', '-', '+'], [7, 5, 4, 9, 2]],
 [['//', '**', '-', '+'], [7, 4, 4, 9, 2]],
 [['**', '*', '*', '-', '//', '//'], [2, 4, 5, 2, 10, 3, 8]],
 [['*', '**', '-', '//'], [5, 1, 7, 10, 2]],
 [['+', '-', '//', '*', '**'], [10, 5, 1, 4, 3, 7]],
 [['//', '**', '-', '+'], [1, 5, 4, 9, 2]],
 [['//', '-', '*', '*'], [8, 3, 5, 8, 1]],
 [['*', '**', '+'], [2, 7, 10, 3]],
 [['*', '*', '-', '**', '//', '+'], [2, 4, 5, 2, 10, 7, 8]],
 [['*', '**', '-', '*', '//'], [11, 5, 2, 7, 10, 3]],
 [['*', '**', '-', '*', '//', '//'], [11, 5, 2, 6, 7, 10, 3]],
 [['//', '-', '*', '**', '+', '+'], [10, 3, 7, 5, 7, 9, 1]],
 [['+', '-', '*', '//'], [1, 5, 3, 3, 9]],
 [['+', '-', '//', '*', '**'], [3, 5, 1, 4, 3, 7]],
 [['+', '-', '//', '*', '**'], [10, 5, 4, 3, 8, 4]],
 [['//', '**', '-', '-'], [1, 5, 4, 9, 2]],
 [['*', '**', '-', '*', '//'], [11, 5, 2, 6, 7, 10]],
 [['//', '+', '**', '+'], [7, 5, 4, 9, 2]],
 [['+', '-', '//', '*', '**', '-'], [10, 5, 4, 3, 4, 3, 8]],
 [['//', '-', '*', '**', '+'], [10, 3, 5, 7, 1, 1]],
 [['*', '**', '-', '//'], [2, 1, 7, 10, 2]],
 [['//', '+', '-', '+'], [7, 4, 4, 9, 2]],
 [['//', '-', '**', '*', '*'], [10, 3, 5, 2, 1, 1]],
 [['+', '-', '//', '*', '**'], [3, 4, 1, 4, 3, 7]],
 [['+', '-', '//', '*', '**'], [10, 5, 2, 3, 11, 8]],
 [['+', '-', '//', '*', '**'], [7, 5, 1, 4, 3, 7]],
 [['*', '**', '//', '//'], [2, 1, 7, 10, 11]],
 [['*', '-', '**', '//', '+', '//'], [2, 4, 5, 2, 10, 7, 8]],
 [['//', '-', '*', '*', '*'], [8, 6, 3, 5, 8, 1]],
 [['+', '-', '//', '*', '**'], [8, 5, 1, 4, 3, 7]],
 [['-', '//', '//', '**', '+'], [7, 8, 3, 10, 2, 4]],
 [['*', '**', '-', '**', '//', '//'], [11, 5, 2, 6, 7, 10, 3]],
 [['//', '-', '**', '*', '*'], [10, 3, 1, 5, 2, 1]],
 [['+', '-', '*', '//'], [7, 5, 3, 3, 9]],
 [['//', '**', '-', '-'], [1, 8, 4, 9, 2]],
 [['//', '-', '*', '*', '*'], [8, 10, 3, 5, 8, 1]],
 [['//', '**', '-', '-'], [7, 4, 4, 9, 2]],
 [['//', '-', '*', '**', '+', '**'], [10, 3, 5, 2, 6, 1, 3]],
 [['//', '-', '*', '**', '+', '**'], [10, 3, 5, 2, 4, 1, 5]],
 [['**', '*', '*', '-', '//', '-'], [2, 4, 5, 2, 10, 3, 8]],
 [['//', '-', '**', '*', '*', '**'], [10, 9, 3, 5, 2, 1, 1]],
 [['**', '*', '*', '-', '//', '//'], [2, 4, 2, 10, 3, 8, 4]],
 [['//', '**', '-', '-'], [7, 4, 7, 9, 2]],
 [['*', '**', '-', '**', '//', '//', '-'], [11, 5, 2, 6, 7, 10, 3, 10]],
 [['+', '-', '*', '//'], [1, 5, 2, 3, 3]],
 [['+', '-', '//', '*', '**'], [7, 5, 1, 4, 2, 7]],
 [['//', '-', '*', '*', '*', '//'], [8, 4, 6, 3, 5, 8, 1]],
 [['//', '-', '*', '//', '+', '**'], [10, 3, 5, 2, 7, 1, 3]],
 [['//', '*', '*', '**', '+', '**'], [10, 3, 5, 2, 4, 1, 3]],
 [['+', '-', '**', '*', '//'], [10, 5, 2, 3, 9, 10]],
 [['//', '-', '*', '*', '*', '//'], [8, 4, 10, 3, 5, 8, 1]],
 [['//', '**', '-', '+'], [7, 4, 3, 9, 2]],
 [['//', '-', '*', '**', '//', '**'], [10, 3, 5, 2, 7, 1, 3]],
 [['//', '+', '**', '+', '//'], [7, 5, 4, 9, 2, 9]],
 [['//', '*', '*', '**', '+', '*'], [10, 3, 5, 2, 4, 1, 3]],
 [['+', '-', '*', '+'], [1, 5, 2, 3, 9]],
 [['//', '-', '*', '**', '+', '**'], [10, 4, 5, 2, 4, 1, 8]],
 [['*', '**', '-', '*'], [5, 1, 7, 10, 2]],
 [['+', '-', '*', '//', '-'], [10, 11, 2, 3, 9, 3]],
 [['*', '-', '**', '//', '//'], [11, 5, 2, 6, 7, 3]],
 [['-', '//', '*', '+'], [7, 8, 3, 10, 4]],
 [['*', '**', '-', '//'], [5, 1, 7, 10, 3]],
 [['//', '+', '-', '+'], [7, 5, 4, 9, 2]],
 [['*', '**', '-', '**', '+', '//', '-'], [11, 5, 2, 6, 7, 10, 3, 10]],
 [['**', '**', '-', '*'], [4, 1, 7, 10, 2]],
 [['**', '//', '-', '*', '*', '+'], [10, 3, 5, 2, 7, 1, 7]],
 [['//', '-', '*', '*', '*', '//'], [8, 10, 3, 5, 8, 1, 1]],
 [['+', '-', '//', '**', '**'], [3, 5, 1, 4, 3, 7]],
 [['*', '**', '-', '**', '+', '//', '-'], [11, 5, 2, 4, 7, 10, 3, 10]],
 [['*', '*', '-', '**', '//', '+'], [2, 4, 5, 8, 2, 10, 7]],
 [['*', '*', '-', '**', '//', '+', '+'], [2, 4, 5, 5, 8, 2, 10, 7]],
 [['*', '*', '*', '**', '+', '**'], [10, 3, 5, 2, 4, 1, 3]],
 [['+', '-', '//', '*', '**'], [10, 4, 1, 4, 3, 7]],
 [['*', '**', '-', '**', '//', '-'], [11, 5, 2, 4, 7, 3, 10]],
 [['//', '**', '*', '**', '+', '**'], [10, 4, 5, 2, 4, 1, 8]],
 [['+', '-', '//', '*', '**'], [10, 5, 2, 4, 4, 8]],
 [['**', '*', '-', '*', '+'], [3, 4, 5, 6, 7, 8]],
 [['+', '-', '*', '//', '-'], [10, 11, 2, 3, 3, 3]],
 [['*', '**', '-', '//'], [2, 4, 7, 10, 2]],
 [['+', '-', '*', '//'], [7, 5, 3, 3, 3]],
 [['+', '-', '//', '*', '**'], [9, 4, 1, 4, 3, 7]],
 [['//', '-', '*', '**'], [8, 3, 5, 8, 1]],
 [['+', '-', '//', '*', '**'], [7, 5, 2, 4, 3, 7]],
 [['-', '*', '//', '//'], [7, 5, 3, 3, 9]],
 [['*', '*', '-', '//', '*', '*'], [2, 4, 5, 2, 10, 3, 8]],
 [['//', '-', '*', '**', '+', '**'], [11, 3, 5, 2, 4, 1, 3]],
 [['//', '-', '*', '**', '+'], [9, 3, 5, 7, 1, 1]],
 [['+', '-', '*', '+'], [1, 5, 2, 4, 9]],
 [['//', '-', '**', '*', '*', '**'], [10, 9, 3, 10, 2, 1, 1]],
 [['+', '-', '**', '*', '**'], [10, 5, 1, 4, 3, 8]],
 [['*', '**', '-', '**', '//', '//', '-'], [11, 5, 2, 6, 7, 10, 10, 10]],
 [['*', '*', '-', '**', '//', '+'], [2, 4, 5, 8, 3, 10, 7]],
 [['*', '//', '-', '*', '*', '+'], [10, 3, 5, 2, 7, 1, 7]],
 [['//', '*', '*', '**', '+', '**'], [4, 3, 5, 2, 4, 1, 3]],
 [['//', '-', '*', '**', '+', '+'], [10, 3, 7, 5, 5, 9, 1]],
 [['*', '**', '-', '//'], [5, 6, 7, 10, 3]],
 [['+', '-', '//', '-', '**'], [8, 5, 1, 4, 3, 7]],
 [['//', '-', '*', '**', '+'], [10, 3, 5, 7, 6, 1]],
 [['//', '**', '-', '+'], [1, 5, 4, 6, 2]],
 [['*', '-', '**', '//'], [5, 2, 6, 7, 3]],
 [['+', '-', '//', '*', '**'], [10, 4, 8, 4, 3, 7]],
 [['**', '*', '*', '-', '//', '//'], [2, 4, 5, 2, 10, 3, 9]],
 [['+', '-', '*', '//', '-', '-'], [10, 11, 2, 2, 3, 3, 3]],
 [['**', '-', '//', '+', '*'], [3, 3, 4, 5, 6, 7]],
 [['+', '-', '//', '*', '**'], [4, 4, 1, 4, 3, 7]],
 [['**', '*', '*', '-', '//', '-'], [2, 2, 5, 2, 10, 3, 8]],
 [['//', '**', '-', '-'], [7, 5, 4, 9, 2]],
 [['//', '-', '**', '**', '+'], [10, 3, 5, 2, 7, 1]],
 [['-', '//', '*', '+'], [6, 8, 3, 10, 4]],
 [['//', '**', '-', '-', '//'], [7, 4, 4, 9, 2, 9]],
 [['*', '**', '*', '-', '**', '//', '//', '-'], [11, 5, 2, 6, 7, 10, 3, 8, 10]],
 [['//', '**', '-', '+'], [1, 5, 11, 6, 2]],
 [['//', '**', '*', '*'], [10, 3, 5, 2, 1]],
 [['//', '-', '*', '**', '+', '**'], [8, 3, 5, 2, 7, 1, 3]],
 [['//', '-', '*', '*'], [10, 1, 5, 2, 1]],
 [['//', '-', '*', '//', '+', '**'], [10, 3, 5, 1, 7, 1, 3]],
 [['//', '**', '*', '*'], [10, 3, 5, 6, 1]],
 [['+', '-', '//', '*', '**'], [7, 5, 5, 4, 3, 7]],
 [['**', '*', '*', '//', '//', '//'], [8, 4, 5, 2, 10, 4, 3]],
 [['*', '**', '-', '**', '//', '**', '-'], [11, 5, 2, 6, 7, 10, 3, 10]],
 [['//', '**', '*', '**', '+', '**'], [10, 4, 1, 2, 4, 1, 8]],
 [['//', '**', '*', '**', '+', '**'], [11, 4, 1, 2, 4, 1, 8]],
 [['*', '-', '*', '+', '*'], [3, 4, 6, 6, 1, 8]],
 [['+', '-', '*', '*'], [1, 5, 2, 3, 3]],
 [['+', '-', '//', '**', '**'], [1, 4, 3, 7, 5, 5]],
 [['-', '//', '//', '**', '+'], [7, 9, 3, 10, 2, 4]],
 [['+', '-', '//', '*', '-'], [10, 5, 4, 3, 8, 4]],
 [['+', '-', '**', '+'], [1, 5, 2, 4, 9]],
 [['//', '-', '*', '//', '+', '**'], [10, 3, 5, 1, 5, 1, 3]],
 [['*', '**', '-', '//'], [8, 1, 7, 10, 2]],
 [['+', '-', '//', '*', '-'], [10, 5, 4, 3, 9, 4]],
 [['**', '-', '//', '+', '*'], [1, 3, 4, 5, 6, 7]],
 [['+', '-', '//', '*', '**'], [10, 5, 11, 4, 4, 8]],
 [['//', '*', '*', '**', '+', '**', '+'], [10, 3, 5, 2, 4, 1, 3, 5]],
 [['*', '**', '-', '//'], [5, 1, 7, 10, 1]],
 [['//', '-', '**', '-', '*', '*', '**'], [10, 9, 3, 5, 2, 1, 1, 10]],
 [['*', '**', '-', '*', '//'], [11, 5, 2, 6, 7, 11]],
 [['*', '*', '*', '**', '+', '**'], [11, 3, 5, 2, 4, 1, 3]],
 [['//', '-', '**', '**', '*', '**'], [10, 9, 3, 5, 2, 1, 1]],
 [['//', '-', '*', '**', '+'], [10, 3, 5, 6, 6, 1]],
 [['//', '-', '*', '**', '*'], [9, 3, 5, 7, 1, 1]],
 [['**', '-', '//', '+', '*'], [2, 4, 4, 5, 6, 7]],
 [['*', '**', '//'], [1, 7, 10, 2]],
 [['//', '-', '*', '**', '+', '**'], [10, 5, 2, 4, 1, 5, 3]],
 [['//', '+', '-', '*'], [7, 5, 4, 9, 2]],
 [['-', '*', '//', '//'], [6, 5, 3, 3, 9]],
 [['//', '-', '**', '*', '-', '**'], [10, 9, 3, 5, 2, 1, 1]],
 [['*', '**', '-', '**', '+', '//', '-'], [11, 5, 6, 6, 7, 10, 3, 10]],
 [['*', '**', '-', '//'], [5, 1, 7, 10, 7]],
 [['*', '-', '*', '+', '-'], [3, 4, 6, 6, 1, 8]],
 [['**', '**', '-', '//'], [5, 1, 7, 10, 3]],
 [['//', '-', '*', '**', '+', '**'], [5, 3, 5, 2, 6, 1, 3]],
 [['//', '*', '*', '**', '+', '**'], [4, 3, 5, 3, 4, 1, 3]],
 [['-', '*', '-', '*', '+'], [3, 4, 5, 6, 7, 8]],
 [['+', '-', '*', '//'], [10, 5, 3, 3, 9]],
 [['-', '//', '+'], [8, 3, 10, 4]],
 [['*', '**', '//', '*'], [2, 1, 7, 10, 11]],
 [['//', '-', '*', '**', '+'], [10, 3, 5, 6, 6, 3]],
 [['+', '-', '+', '-'], [1, 5, 2, 4, 9]],
 [['//', '-', '**', '*', '*', '**'], [10, 9, 3, 2, 1, 1, 10]],
 [['//', '-', '**', '*', '*', '*'], [10, 3, 5, 2, 1, 1, 5]]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-qaKJCbF+v7IGD8jCCifW#x=-HFJ+Gw91!ge+M!dFQKd9scJu2LOW%GT2>RwGTFsxgLoG>i_<?|NPtk`7fXU{I7rfkH7!-|NXa-'
    b'O8v**|05LJ^Bjw_PP@5W8)c6%);{a{s%f^9*Wim~gw}$!m0Rs=7K=SK`^W$L$KU?z-'
    b'~S`$nAYey+#2RBHE*8AH;vx+yrbV$X6&c#kjKes<z&~r%+u@L`-'
    b'Z<Bvrgw{`xzzVsA1%NLSHpTXJB!MIqtPob{(~+<B{(V9%7rh#d7j@G%Msg_@v__Y#*)f<SW~4Vb8eu)_%-'
    b';+x4cnN}Dk@pSf0VtL+s3dQ8nX@_Ysr$89;JQA0@A`enxIS!=I!XV`J_!@Rw>n^JBgSiND*``2TvjNSOYV&x>ibH~CvT~F3`jkeD'
    b'@ZKQE~jx7bg5O2C8PBYKD=J9<@xIJZNr0v!Y%ad%JvCP{HvyJMj?|XXS3+bfO&T6aFSn>$B@$kPMlfv*DdT%$B+Xe$Y(+;b<n%&f'
    b'6s59@JVment*yWBLO7ABy^(@VA!4EIOQV$-qJsj59viHDz5HLFzEuk%+vxnM3WS-'
    b'{<jBQ41q5Sn2CVQ^qsf=3l>a!l3H{VoZxP^r+o1ZQOCjVwDv#|S?K4vYaO>6z_6hDfauv^);hf!8%y@K}{nU;Hs&ufPqIen6Ex5N'
    b'?eT=@o@EbCg042=D4GK6Lfa7@p$<Xdm9R#;-zWX0BJxoOT8wMfZh%Qe&$Qmr-'
    b'h*85oF?Mh`{$pDVr19_i#d0TU=G*hg0N9jfwuI)W~H1cTHkYcwqcB+d-c)Q?r+2Pw}%EgCPg^aKFFzW!=$TQw*tE}crWA?#6Itg-'
    b'CaPV{Iw<~qC@5Rg5?S2win$rd?M;{*JCF8@+dCa~C_<KpMlZMq@sxhDI_O~lld4D@Glv3|v{HI(Hy>}-'
    b'c^0+>HjLr(o*6;qz+U65#sjGtqKHeq+;Q^)WS$YGL!Z_t@vQAU(A(O8)HiLg)tyo90-KxiRYGT3GuJ(2`#&G!Tp!}%LB=md2B-'
    b'B`%?mYp>i)W5$@t#(0b;h=Pve{a@W&ZV;m^~MQ+89X(NHU=|PP`$pGEhx2i*eXGXRZLTMkgK&IOZeM3iomN0d{;=$(|Tx2{8|?zR'
    b'lHYfFEjQhRHi{kMv5T?Xh#Lxi)XHmGswR^o=8U+``S$R)XhGo^#y>jrOnrAcKIi`6B){uM;of4Nsknboh>D86QC6kCrp=Fu?;yjS'
    b'!4PKqhTd>!$@6?z)iz#g3hGOG%sguWyCPBW8FMH^jy|sW=4A=YtJ?`<XMfQwiP%Zmr!TQCp*@?7$)bkZ;}~Yh`iYF8CuUkW$q<%`'
    b'y`|a5nD%d|O3Pg%JB-'
    b'B15nBUe@=(Pvm#rWfDZ?#vH@joT_?x=wLvY#z3?zX+sZl7@V}1)o{H66Sd??=3UR|<Gs@*73UZIS~Fr}r`Z9J%e&Nc0IqG7sPn3j'
    b's;ly{eEu4#rnFXZ6nQzzkZFHChPRK|v`8xl#Y)RI(Rg8}Zp1V^W_>`Q<bUkdV7=8F(r@n!8h)qPShYbO^1*Rko>^+pUziJLRJkec'
    b'TexvAO}%?Q@bqjzBb?E{3x0T2f}k=VgLKnMtSOS-ZMj&Ncp^rMp+ix^<m?==1K{I8*?%6x2pw!X)jPaK-1XLYcMoAC!oORHYt_-'
    b')a0vJIh~r?;lb|>``ZxUG1R^ez{sCYgMj$uHFOtRg-Y%*@)L7>oqqk};-'
    b'L?_z4!G35zoS_I=;ApC<YHZ81Vcy3giX440HJUtC<Y{Lhb3cT^&v*G#>lb#c8VXR=A&eIG@6dCOaWmz9MF<NIYg}!BP7BY;MfW!H'
    b'GUQc#h><E6IkgtLC^K4DE77_hqKBUXtCkucrQUSFALOHzu-bIspo=$VU)Q;dr?S@g8Bjl>)QJQ6RnO}lA&C9`&i<xySM00NI@`*7'
    b'lXh;L@2B<47^RX3~O&?(xWM^qyk0}8D|(ma;Gl%ulEA$h<b4C4&_dFH(rbB2XFwIf(%DHx1YRTXAKCFJQwH@ubr&K4-}+y-'
    b'IX}XEJ72yNK*D5Z)Yf}$^3rF7dCSvg+jlw88vhS2ht3{x`>Z~MZJ?DwCNaU@`_nzwL3}x+nFBAq;3;HuQ-'
    b'dI?q168nIq6mtiW4-arBNFG}500=f!j1fzUJpW&9xBdBcdQ0<eLCT-Sp2LOk)XNVzl;*?0ziL_P#toq-'
    b'R696<>iulx3;9woygUHl5Rmh7ApONuiO4bq$pmYMiOh{Kr!K#k&yasmASyx)zsMEU-'
    b'y3cSH$Y}UMOpdD`t%OE@i+{A>qBlD0n`||%V1`qFXVlT-Qf}5Eb%-~o1HP!(&i!vsxwoCA`o*RKqQUZ(%-'
    b'0)*#^U`^)bTG1Uw+@j5Irp0kEFK9)QXMGL@u3Gkn>8UoNizh(H2kS*R%9If+U$UE?knAecvx>&s*IHL<|_yff)+OsYE2RN&Wvv_$'
    b'?bS}tJ`cafd;)I=;Fm;BXri|@I#5^+gNH8WbKtV8wh*st?wrNa2BQ!>rpE*DYTpT`bK@UgTf2nDMqozO_uR-'
    b'Aso~<AX+A?aw0Mo?O-#&UQw^dyMGe-BNS>ah{5@GG&Ka~lrZsJnV}k3Ht(_+?W6xg8v~C^o&eMhfnQjG3>rXgaw2c7N1ZJfj5yes'
    b'PXcL3pAfp0o+HW(P(kM7!*HGj=s&x_E)}ZfUs>13b-'
    b'zb(1MD7Fm_S#3OtqCM?}umJ$wFx?8e;)E7~D2+$c)fnxdYw~rTNw~JaTsid$1bV=5;13=rDI_7-tp)eOwBE^L-'
    b'dwW3o{JZQP8VZfh;_-`-'
    b'k}M+W*hqcf7F@cO$H&;%Mgvx<k)JhdY@b~L}E3@|7Gv4C7}hw;q3ADhIBXfmvis^!%JL#punJ<>$x0O~GhVpAQr0Y7QnIGW<P!m@'
    b'6ByWo$uavqJwB}G|0o{hUjLXn$OfsP4036Oz!(AO&ZB(zvl(Ez<VK`4^tp2tNg9y2qZa@H|Y;AuT(LXK6<$pO6!u9ClFl{%bkEXw'
    b'f#w9abl2V0Ng=Ft>Cs)@eZbmI{>v*0Ps{&C8q9acS#><#mS_#TiXf~_#2=zbD~hi_~i$|!taDksvt@tANfW8J_ANq-'
    b'&2Va3oCggLmnnX`guADWN|Mzs_`nEtgM*hvO~!6f2qZp|Pv<6~+&ARjAN;~BRSQBZW!{#mUDL>4!yy#8m33xnw>enRZ*3D<t0bi+'
    b'9;-h$kH-v$ERa#Dt2`fiKKF+$0{apQ)`Jt#2*#b9wwyjT4ol8X0j_7R_zC1WL8MeJfBSvM3a@;CkVr}j-'
    b'*YBgz(F*}}9QJPZB7yuS)-'
    b'rHD)qR20&lV1|6us{Nleo8b=CWbW7f^1_!u?BOb!vkaHGkL&Z+VDsyA%VQ1aS<Ae0rKJBxdF}Rf!s4o#t4uQ{8^?VImFU)c5yX^i'
    b'?qimqT8`VGbNZ1PH(?55V6E(<#|1#4-qJg`Vul&)7-'
    b'?^Z50eFNhTL_B0{n(Y}^gr&dP7&=1xb!<C;RiK8zmgWDcU0784#Gut)U!!0fW{6#~COGMr3Ek@)}P!+8P5nmxwkan~04uZ$VY)D8'
    b'NJoe<rF&re|Wr_`NJ4{j0h@q=_yFt&?;K`D6MEX(vuGU4`GK~duNhKgS*W+C?giUkxjnQKCAy@jndWxq`2%#2jpxE0JMMg@%nPRl'
    b'fx#H4Hl6e*sVL*9D&imC>OFZs^85|I-'
    b'Zk<Ch?e0+zr+hOI1+y$%*Wh)_*lKvP>2o>eala1eYML>!<RCbv=DeDd+sQyRjHNTgE@3RNq=m=Y9!H(~gdQH3px%SmJSQWwyx;}^'
    b'D?jyWJUk`?aBSSXyl^9tItqv&<uVPq&Y2XFhued<&=0w<$TNtv=>|hNxR6DhSxg$h3ZxwmXcso%5VL7qq#mTDhHZ^x)nVn^I7!sF'
    b'(2o%!>oM~*m&aq<eh5>7kT?r}R#?YvqfFWi+zRjseEeEg2w-9|bLPLrS270#IDTX-!ew-nqSqz2VQ2}16m=cdwWU>+h`OBKT)I!U'
    b'^zszSfY&oBbyiL3k&_JkOKB8BQP}b(U!G`>U6PP)!pW4DVfi284IdF+MGyp*c=@RKIE|vy97^rZtolp?ZkJ%fdsG`8{TX{`JZk0f'
    b'iYApk}Bd4A3K_XQw0Xzv^k+EPSnky<KbB0g{?y2oR-9V4x<_-'
    b'Bi8cjAB09wvC<2lcgzHKBmb{A2JevHfzzLg1u!C3rrZ$R4~S3zj~*;vBy``tVYjLwi}USjof7BOG=Vs{pNCBhdAn*affIi4G(hp4'
    b's31oNgj1nN!*fMFyi;Jd3FP*3nxLX4mqGm90`JNWxH(U#cG19Ko4s)}>p$E4jcDxG(?0L~Ra30=h7kkZ7UHiTO9I1r$DNyQm!JJF'
    b'OC&CwrwP2}l1XaVfMYzuBfJJoR7MkLmO>SiKvmIb)3aiM<DWn?N@o<Otjf-'
    b'~b~rU>%Idha|FGZZsnR|rL<FbaY{0rjYx#w>O)56HL+0e8>8KswRH4E9=?WUJdk9*iI1g{UGC(TW=qYse`ktEm*lL~ePF0LQ-'
    b'F^?1aZkE{nHoe4`*D$|bXzvNMY7H3d_Hu1~}elmM;4E|h#AzNzcyrmfOyORin!$UYQ%-K*YT}jhb%K_ZcVXQYgmsy^UqneR-'
    b'4tUto{^>{ScQojasS+^ML^eW5W|avhA=l9sM5~0W>av?jN255Ageq7F&yIcn(w)tO;(;xR-9?0wD;--'
    b'OB>fXcFu0});Bb{I0i7f((R?XCe0?7yvT5yJ`62!ZAIPNac)@FsBA^C3f0ws}Q-w-'
    b'oE$Heh9@h9PO2rLy@Y7;ga0EZUP7DXj+SGl)Qah+iI8@|bBAp<!PPDE~wuIkSj-gudw2D~ZwQE<usHn#}Z6gtZU*titHT2|V6YH`'
    b'UzJcW@pyRJ3kJBYAOO(L8Y9>Qp@<s9iRRq}*9r$W;c4`yaC5H&B5;pm6`BzOMXMtj7YXbx)mJA}p-'
    b'Mav!6_>>iv&Nnl{2Y<EwGGvNacni%d<&wFwksaVq(?7>0oP_Z#`~(mO?dfg2=vs^PaW~ci_Jt<cI_OZxY{LLF&C0teSV`D4OF8xI'
    b'W{1Dh9k9eWx1K8Ac84-s2-1$gt~{TEbp#{AYAp$<7dmzPhd5~u+R+y^7cq>9n9*EjUgUQ>q-'
    b'*aBFvbpItX{;{}xW{ZDs#iq4!DL3^ine3nZ?)_NcYhB_9?T=3-'
    b'XyTM4DxU;&irUUK~B0;8&z=k&PudQ}*sMl^Iy_}@O527r#RJ;jF51=LZ!0Uy=yQ+;+wBdc#q8=!AN^p#9{)Nr+7zfV6A-'
    b'vE20TgU~pue#ds%BL^vb*xf?VB<z5;ysb7stRJTzNyK?WbI90s#TR9xW9$dZ0dvMMN-yl!r#0bHc0z3&I?}RtB^up%L=8N+z3C9N'
    b'X5-YnbCxyPwM%>Y3~ZCqUU%BhL2Aq3K1W<@R0l~^omALnTDi-8ju6UQ~*$aZ<V^op7z30fg0nWTvo-'
    b'*7No8A<?jA<11*g0K^m7H)R2K6v;4`84d<i3q|Tf?yw?6%;X!HLvnC<l>~X)JnwoPItD9<#aS^C6Z)_0f2gC?Jl_Gn-'
    b'>ROUe!8j1^7t`s#`pv77{2Q6n*MJWBe3q9rf;-'
    b'`2EUxx<6C7eOK%{NfIzGiZ9;faDa2g?K>AO<Z&WS0tNrv~3Sr~w3N`7TPM&*LY8kMjBZP?tQ3Pe)EoC9g?ce;Y;bb^Hy4^`p0Pz_'
    b'`hgF=}A^KiH4u}9w*U(2k++(<W5F>w&hZ-vPtdA*rE(sr2Ti|Mh35CPr5oxNk2DlI7phqgjdroiJ?#}p94ka+NSib)LoKob`=oK('
    b'tazKOKP5{iks<8Vt7RDfq-t0<2IVMdGEWxt~t+Ajv!E^Mw{zMIu4b2IEP9CpO`IicBGPM>auA!CDVu9$!ozIaozT6W_-'
    b'RXs`wGE)ccP#q6C#pL6FXFa&_i1sq9`5t^>gGQwCuiwvDA6Ch=QGGw}Z$#IuNyRi*Qozo@FowFQu-_JoxJw{r)MuQ3dw1w`@?k@S'
    b'1#3d=2+I$Q068@6R3-gX;SDA*+%hx{(K>7dqyP595&OWr9LnC)!0x@YH94+LD1-'
    b'$8+#xO7>ea`xGL=USjQ*MO?@EDMOb(IM4)3cfPm3ywB2d+$b%}*|^vXR3^&`R30zu^_5b`rZkCI`lJ1wTzJ|#I|-'
    b'1ykYi;6)!V!IcBkn9FWfnQ+BiGfeu93s14*aBBDvxqYFhGA373g=YW3RQVW=nCe;3c+JtACkOd!S2jV7~b;xQt6c9$k~Z64gp(BP'
    b'J)G5yYQJ0A%;M20>;$+fan4LQdL-ktn2YX1O~{o89XyFs1x@?E>G5*DeTjE8wEG>29hGS^C(CvFbzTmrGHBF(E%0$SVd-'
    b'4+*LDWb#ku+bI{IK$CG7sFJvSLCT%s>xwWRo`@pB{-'
    b'xNP;Q+~u#D|Ji&FtH8gN&FvGMd#gQcDSjk>Q)LXem=b}>MCvJAaJ~?)#N8=uNdjGiSX(CwVckU`0R`Pj>twZ0Ic7YFSF=qpi9hL='
    b'}x)Dub*Odbub8Vf;&<x1&$plq+T45F(Rl{iQD*Ibk44%GD`CTX-HNO`3GB_@7A`6L#+9jz8S`|y1_-'
    b'lpiS(hnl_N?_*7mHhawTjthV3A(yNL|YM;J&KA5;5u;B2vuiEl!&`Av7eWB(G3luH^wHMOBHlS&^#P4GW#(6LaSf<JXt)zX8rsV~'
    b'&Hp>(Sv!Y67XrRCzu)*e?KBkB~{gs`0|AB{r2y@$30IEGQcz$P0Q{H^ReMnuDoTM>ybF8gUK8G>CaYG8>P);{9Xd^`)JLiR#TC|9'
    b'>XU+L@1x-qCi_{)5sSg7$1Jm#I7DN}sOGqKVH!@$_Kn5N5O(d-'
    b'W_v11?mF=N(a5}vLEfNw%J@cr7@>5%?Gp|cD6w5iG?He8wZXkL{u!yzs3h`XHkJa;Au-inZu+Dzfq(?pbueyQCVg(V4s!j}>bK=;'
    b'qs!{@Bb+e+Z91}&lsN;A7<r}^u*r3(l-'
    b'W{_q+rWe6ZM3uB)M{Wlb~JgXlz@2Vc{G=t#lHcLsE3WZ9^nTR7c0Mk1;FBCy^3~L_fE)y8Q}#?TTpc$^d&-'
    b'x+i6+#XJDCy|CdI+&3h0h_>y~wIb04V8C)^2UnPQx0Y%wQVwlC$DPmKX8Gdeo(_iw%tEmf*1@MUU!>deEV<kQnk={w2dDXCoslit'
    b'DAlSK1$fwFjmA751A;trA7foDNgAPicP(&W&e;${*$+m&VC<HVrx+G!2yTmWL^Op>~2tur*lXOI@g#o#M;{eRnjt)5*_;73IKtV-'
    b'4^mStd4b#@fI``L9gbpCpS|+_O3k;0_x7wIP+il`fn?HEFRC#9ytF<);^Z`Zq;`tUtAC=@Eh2Nt+nB{o)dX?haG3ixpo7h-'
    b'D@z(J<d>79^((tl-=}<1Olu)bcJ08F0*H@cvZ+!T_*JvJ9+E65`N+duQ7j-=_Xz?$@%=?l9>WN@P2xmml#-'
    b'T%bW0h{h^RLC}5l}Gh#cK^!{7+~M%woy-'
    b'*ZI%31!RsX{ZWqiN8<equc!kCQW9bHR&50`2lUUPu#<QJ;JC%EDJj}D?dE|w>&z`wr;tcnth1{R$E7?zW<EZbG|25#9o9G&kwEx}'
    b'9Le=%2v4)7I$F;iflaiW-Z5HDM~i;PX;@mEvaW$BsvLs2d>6hFTD&@cVujG{StN(?A%1iSt}dOX0y_3@>sSq-SW1!^3)Kd^!Ap|j'
    b'c+c@UQ{MinQ{nu8rL+pqCXf(0xLbeQs`7|6ADymvR9Xc!K}=QMmn#bg$$*LhVK!eOMX({Zgh8qZJ3tJq;xtK?qkV@j!GIEnAeh~7'
    b'WY_|=v9d6g0j2}`gFrYSaH|B=Dv~zfkbK}`rG+0~B=JZ>CNK>W8wLibg0qkQo#o&IPv)D!8XiILkS%MeiBtt&99jZxe%6BsnCnxP'
    b'+^mGsMr|tm%mip)&v>9E`ClL{OI>>hSXvShm)898IbRVtXaSZ+@dH{WnA!y}otPDz^%<KL$QS|=8}Y8ITwoLRcYxMEwUrS26Pu;&'
    b'%|srl!3MLwTAxH)lj<8j87w%1M-1Tnu?3t=t;t&-'
    b'9&evI6^ODLeG(O)dT#j)zKmPf=TMpIlm{wBNn9Ky2|_@i+im|u+uVm))T!H4RSt=uH4h}$37`puUIY}fav>NQs72$03H9xS_I_K1'
    b'eAIvQYMblL=}|SV^RrWBwIMq{jL%#d><GxuCN?+{7ii@efmRqzw=D$b3~2wEM38!sRr#|i(kDQU7@XSw;fI(mR<Ws4=OrAtO73_I'
    b'okCDsn*Z>I4}kG@>FPq|Rg!9Igohz~i6>H(%vd@vB{9LPFJ*iN+OT}T>a_}UDPe?w=zQ_sfDfUighw9DiczRK>cNa7ZJLoJs-'
    b';I#g)f9(fAP!<zUC9)wNVj6qt%R#+PH{hG3y8kavM-I9U!~~r*mLxa2g5o_;dwg6K_7T=0NRbHPF%+r-*7|vXoor9*_~770(SoY-'
    b't+?1j}u$w~$^8D>2GK`-Px}OWx$daS1;cv`;o-'
    b'CQ+~+z%f+JJ5PxV&}Nmj{}jPl{ee5g4XN>s$&Eq#AhoGmkTry<iOM6wKy)P?Ma_J&BVl%5Z|gUYGJI&#bk+`9N6#|Rr6n8=F97aq'
    b'{1H<G&G8LQofb`9pkai7tjp^QTg!Mxoazb$GO<mVXE42m<Q1w`SV9Yt#R2Nn9feInOxWn)S4{n_gL%{(^5{H6^NIkjT@u^?%2f&!'
    b'mr3xrj(tji+8`n<JE}>Gy$wZ*6(NV$uW6dlysXPzNLVrk*#PYm%41r$sLCVbPgtmc?$cEv&79Q2Y5_lR>0__?<}v&vkgyzf@U;#Q'
    b's_pWj;#+j}+wY;!k7UT<MXIDOMg-w{)2{0~H`1xvY#*XdvLfr-TLQRI<CDpf{IAkDu5<VVI4Fngg`<1$^!UigqhjWx(L8z#8jjp6'
    b'<gp8w+J=aaPO<`nUe(dm0U_OnQ<i`!cg(TQ@%9Q^)W;VByz0GvGdE=Hkhl&oWA!kdpTLSrSVC3a50Vt4cQQd3D#8QNfHgKGGKSz!'
    b'-xhLHb@ZldVJ2EWxV9$F(VZ3A#Fpaq)Xza5@S>B<7&pu3>t?j?Xil5VDKo>|W0?ce$2SZEu(;Inou1YSM4k>+!6Jy$y(_M?tH0-'
    b'~Z%PUnWHdwprd{R51b<KUmcaBfHn2B2De6WE5A`fN%m)qV5b9T6<9o<#LH!6iX^<zg2y);-'
    b'wEy{GQ7mCmdv`N14Mx??4NI4G_^)6W6ZR+(F(2}nX`w@MNBNO5M?Ly!00=;-'
    b'uH4!^*SJJ3Q#u8^S>9ImUmYfNh?t0jdNUFpNLNt<PRB}L_!BV}qCwgD(;arj6#$F62f_CFyW@rTB(y@s4x(KMd9^hFxkH!h&4Xwh'
    b'EL{rnGpw2peRZtuVN~dy-'
    b'<2QJ0jP>%D;=!~RB2Og=}0&pg@_wSG+AApcEZz65<WzLjGXOd{R?ZRGB@GZbQFFKIcK#;E_Wi@IyyC7Ri?DJ-'
    b'N6tdMw{MH*2J8>Ejw!gSRf4QMw&APN&CJ{o8f`iV(F$-'
    b'er9YceG!<*YC(eQx}{%g{(IfIP#A7jYX?t3gOgHYs<5=xwISoKLsvzcojRAM2SAUv6lF{Pb71b(WtVTT_}{BB_?5otTSeijg3_J)'
    b';G)KEqwCJg7)-'
    b'YZB8c&qs%+*v8Qt;<j>L<6tL^Qz7LTscDWNTGSmR99EEG!`B!lh}nv!aOj;fl0QJiTy^(c2+Z9}#CYI}US?xTyc-he1L?n1gNV1W'
    b'oNEC>%ea6aJ7^C^E`Ybe0k<(tb|FwfRG?mU0J*N;Y{!(6DcX8S6Kn`V4x@@W>LER?Hbt!L<T2cA^d3^FQkG^_}rh56We6xH$9X{N'
    b'dF&Nm>4ajnrOs7U6{p*k{{&S=-z2Sfv06K+!{`+s{d+VU<so)qR*9XwdoIf#{D9-XH}AYek7F694=>Yf6bz<u-'
    b'sPWUTKE>XD&B$Py1V4dk8<Izdg&zYoC`t(wTC&x;~CF_u$f=nl5?tQyb+QgaX>ijrw3g7D9nUV`Byiuvb-'
    b'q5FZ#izbf)U4XnL!(n5+t$Bjvwc}AdyWEIBZ#y1bB4|iqBDrcdbRfu5ojni?6b}XA*2~Gh%EYyZ%Z9p{q*4X<)w~;VM#cF?m$-'
    b'roSIK<O6uMc5Nnq*RKY&rG)`@<-xZ3FwBI^WXB2N8O<lp>SXMQ;!b!z5T7+*UDRr#+6rCNugqK&wE3Z5syE{BJs(6z-'
    b'%g;fxGmEVI^{9HPEwyDrlxQ+uRGWehf=pd53*oo?eW}*(8mvl0y(Mi0NRo8MoKD4Yq|aq%9$0te>pn@_x1U59%v}5J-JyL#)2-'
    b'MwBNSLxU9US20yIWlr&xfVIAYdO*^2P*eOpmAWfA4KKEAI1k)7W+>JF=f`h~wzMUjDx3xt4%KtYmV5z7)+OwW>*n2-lX?m~?=-'
    b'd<V=3I*m~t-y0jB$W?Krlg%(-QlC6Z&dM4*Zvn2y@BnRFbCwuuT^EsKkBAS5=OOC2A0(8-'
    b'F5llLYe9)gsv*qKo@9^+C=3XB#O#@^X-w5S67;)SzWES_|e=%4dL+bAmCPa{`r6q6m-;Ns{L9&%(|-'
    b'dXZa{UVM0i#`aV)@X1OuamDM<`=+n`Amc>*#Kv$|GbvV?L6@SNJil3j_I^3n(AqcFc_GDe#D6XiwmGR*3VM}$o-'
    b'=$S8Rc%z{`wXrv*|);v5&Df<X4c`9av-ZoVjWq7Lw+qO1OSZ};c@YPmOr-'
    b'WWcM(gz1Y9f>Z`kfOih<p7k2EGKq#0+E$m^a%b3JReuCF~@%a^kA;^&>1k-Ku#NWqE$V&|_OZRhQl(lcXB-|IyP-fM^udK51*dmq'
    b'H2`K)EaXjPCrG<~$F)nL=A~t3tiJ%asiXl0ES|@Y(R-'
    b'Go)Y})qds6(u*>1w+n$nB5sy?#}&gT8F&2K6q<k9N_~<If2rW&!g}crTT`=H#7amP*ie*lw(RPyV)#0^OWof(jxWRheo&I!IxsRW'
    b'$+Y3?^`3H6T-x>sE}oSdmx?S~=$YmZu(>#7D)<M-'
    b'uYYuX%WLWAGy*^r$HHXl^2|NqKns66+oSJr%4GG2D)Bf&h22PJ?c%GFK4qV4X<ztG<!nX?4>T=0b=YFc)Aov$#Ogq~DYvi4Xj!KG'
    b'IQj831Pfaqi=$-c%a-b2&>(I*1H;BT}#0O^Vw3qU#bCX3{?JP+<0e46RaJOI>C~)#Uc};+jX>>W}UOFX?lcQ1;JB-lDXHI`0v3z)'
    b'ibN9m4aj3jh3^%Id1p@;w7L<bUoW1JyhY1J-'
    b'p|hfmwU1n8O7X{<KQp#zbhRm|!pLPr#08g!lecWL3$u6N|`OSe54AzKx)LwPmR=g1g#wFMn@Bye@6#Ur@fEAP1Xud73y?HF$ipte'
    b'KjjbKVY*u=?;rlU&;PUaN}>U?z&1N640Mr<{Pg|`cyiiNIYUOIk397FZ7>7spgCh6#Ay0&;7op%M(4EqMKW*vD%FOT1qtpE-0Z-'
    b'Aq0HSC5g2TPIAq_l2ZibJZgs$~vBzB-C`Qd8^U-M@CzN1JZ16a|*9X?G;*JP1pJuyBtm#G~25LfZfms$l3cgnX`+-'
    b'9P_OZXA!hI(SFv2A{;asAjb@0jO+UXHhp4rM9{#+UpW=LBF_+h^WN7e$&v~`VEoSbv_^T>_dlMc4!job*UJwng=F}C~ELOtY<*%4'
    b'LW^03Qqj~8azQt54wis=<4sSGi=0;AN_KMQk%XY34C=|3s{}j{*=QY8#K%B=GRBIEO%WTv2<25Gjb+G$*bRHK^CCrm^DpG4kI63h'
    b'8VWmCOaw)MCiYUt4FE%sIvd4)ba0iN$RU#fx$y{a2fz7M)IdZtf0~52^a{8No_3g+(jhnCP;&%rwXZX#-'
    b'A$WS{dgK%oG%e?sS}8zsF089KcIqG^7(sAgNouOi;wgs71~&8{u)!KD0E!OtKGYf_TssMZO#Krt|28Es4@mTWYaX%kxn8U-'
    b'{?N81r9l$9VIYM^%BL?p$3(4$uPtV3_Wi<*zIb?@lo2Ru02;C@o>Aiv8+tYCh(1kALOPqdk~Mh2BS^?bRK2ZyxigME2+ck^`r%jK'
    b'A!7lpJ(dqU)>_)TB~oCup|mrmWDI?52)iZH{AQ!3z6bhY~*DqiY`Uzp7+w54D`Z=+wvlspZX}dvOl9%oC5AJ<uGds9mzW{pA63lW'
    b'U-6tpGpaz<1+dqi%^g2y9>oJIg3L^j(p0XcXkokT?Yh#-HEXnALlt6TMsQrQt|{Bwmt7=g$>lICp5-'
    b'PttjFT|)w{fu*{dd;SV`QheY*QOO1C#|RML1Jb|iK#Mvfw=NTvcn1IbRHUP}xWY!?{BH1Mcu_aRwutLXYN^xS*++Gh2r67`!u&LC'
    b'w$BZ_dsn#mBTz}8@smln=p4C!eiIb@tzU0}d$AKi2oM1~d{8YN_1eublvQ_VCKOXc`~B|QVvY;W1|b^}IemYA%iYwy5h@HdloA33'
    b'1HKVHm9&w7B0Z&5c)8!LD#(XTZ0MQ>28&qjs6_PhY@cfqu3Ab|;N38$T1SRAY(GD-'
    b'!PNPC3<!%5+Ec&3Lq|@GOhOvqni4UCIS<Iosp=py9JBU0jmrC_m_z@agMkw#9t;&lK%v8t)~d>{`?-'
    b'kw^a;rYp}u~7OJAXDdnb^@P&{vDZ?AiMbxCS#N5KFip!IMY<mH+=w{hm@8b4j+bI`*bnPLg=psj-'
    b'%K(vH62)`rvrEcx@X_sq~5<2Hwbu!3xsVDXZCTLn*{-'
    b'D}L@Wq;Kg(9PRd|m&mZlFh4j7s2r%u3bCND{(;%1$UL4hGcN^*d7WVL>+iVmFfxrKqdw*5BMT@OFER9d>J#Q3gPP6v(>xM!z0;!z'
    b'$(8)7vGCy=2@6T0Xdz@7H06O92H=E0PEw?~ddm5I6itsOfHXyFe*#cXX-?=+NPxj#q~nia-'
    b'86(EnE5K=GWVTQ0Q;0CyrFmaf8q)(%l^s8&3DBqbmXUGf9@@MUsAw;Jc)P1BEriHaeh#9`re8WpvWbm=t8s;amQG{sRw+15`;x(z'
    b'Nl$vWmC0Q2sDZjCGYEx_tBK+SIjFKCs?A+fPKLgweX6diFX2?ZA>`WMu&#j-1>&j0-X#JLGU'
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
    candidate = do_algebra  # noqa: F405
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
