import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3],
 [[[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1],
 [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], 4],
 [[[6, 4, 13, 10], [5, 7, 12, 1], [3, 16, 11, 15], [8, 14, 9, 2]], 7],
 [[[8, 14, 9, 2], [6, 4, 13, 15], [5, 7, 1, 12], [3, 10, 11, 16]], 5],
 [[[11, 8, 7, 2], [5, 16, 14, 4], [9, 3, 15, 6], [12, 13, 10, 1]], 9],
 [[[12, 13, 10, 1], [9, 3, 15, 6], [5, 16, 14, 4], [11, 8, 7, 2]], 12],
 [[[2, 7, 4], [3, 1, 5], [6, 8, 9]], 8],
 [[[6, 1, 5], [3, 8, 9], [2, 7, 4]], 8],
 [[[1, 2], [3, 4]], 10],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 9],
 [[[9, 8, 7], [6, 5, 4], [3, 2, 1]], 3],
 [[[2, 3, 4], [5, 6, 7], [8, 9, 1]], 5],
 [[[5, 4, 7], [2, 1, 8], [3, 6, 9]], 4],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 5],
 [[[1, 5, 3], [4, 2, 6], [7, 8, 9]], 4],
 [[[1, 4, 7], [2, 5, 8], [3, 6, 9]], 6],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 15],
 [[[1, 5, 3], [4, 2, 6], [7, 8, 9]], 2],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3],
 [[[2, 3, 4], [5, 6, 7], [8, 9, 1]], 13],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 6],
 [[[2, 3, 4], [5, 6, 7], [8, 9, 1]], 4],
 [[[1, 4, 7], [2, 5, 8], [3, 6, 9]], 5],
 [[[1, 4, 7], [2, 5, 8], [3, 6, 9]], 7],
 [[[2, 3, 4], [5, 6, 7], [8, 9, 1]], 18],
 [[[1, 4, 7], [2, 5, 8], [3, 6, 9]], 9],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 10],
 [[[1, 5, 3], [4, 2, 6], [7, 8, 9]], 3],
 [[[5, 4, 7], [2, 1, 8], [3, 6, 9]], 12],
 [[[2, 3, 4], [5, 6, 7], [8, 9, 1]], 1],
 [[[1, 4, 7], [2, 5, 8], [3, 6, 9]], 20],
 [[[1, 4, 7], [2, 5, 8], [3, 6, 9]], 19],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 20],
 [[[2, 3, 4], [5, 6, 7], [8, 9, 1]], 17],
 [[[1, 4, 7], [2, 5, 8], [3, 6, 9]], 17],
 [[[2, 3, 4], [5, 6, 7], [8, 9, 1]], 3],
 [[[2, 3, 4], [5, 6, 7], [8, 9, 1]], 6],
 [[[1, 4, 7], [2, 5, 8], [3, 6, 9]], 13],
 [[[1, 4, 7], [2, 5, 8], [3, 6, 9]], 14],
 [[[2, 3, 4], [5, 6, 7], [8, 9, 1]], 2],
 [[[1, 4, 7], [2, 5, 8], [3, 6, 9]], 21],
 [[[2, 3, 4], [5, 6, 7], [8, 9, 1]], 12],
 [[[5, 4, 7], [2, 1, 8], [3, 6, 9]], 1],
 [[[2, 3, 4], [5, 6, 7], [8, 9, 1]], 15],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 16],
 [[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]], 16],
 [[[2, 7, 4], [3, 1, 5], [6, 8, 9]], 1],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 5],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  10],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  20],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 10],
 [[[1, 2], [3, 4]], 2],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  1],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  9],
 [[[1, 2], [3, 4]], 3],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 8],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  11],
 [[[1, 2], [3, 4]], 24],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 11],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 6],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 4],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 10],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 9],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 15],
 [[[1, 2], [3, 4]], 18],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 14],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 5],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  23],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  6],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  8],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  9],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 15],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 18],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 9],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  4],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 21],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 17],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  25],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  16],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  7],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 19],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 3],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 21],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  5],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 9],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 14],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  7],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 11],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  2],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  22],
 [[[1, 2], [3, 4]], 25],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 7],
 [[[1, 2], [3, 4]], 17],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  12],
 [[[2, 7, 4], [3, 1, 5], [6, 8, 9]], 20],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  17],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 2],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  13],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 16],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 24],
 [[[1, 2], [3, 4]], 19],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 13],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 13],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  24],
 [[[2, 7, 4], [3, 1, 5], [6, 8, 9]], 9],
 [[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]], 22],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 12],
 [[[1, 2], [3, 4]], 16],
 [[[2, 7, 4], [3, 1, 5], [6, 8, 9]], 19],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 10],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 4],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 3],
 [[[1, 2], [3, 4]], 22],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  22],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 24],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 23],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 23],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 22],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 19],
 [[[1, 2], [3, 4]], 5],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  10],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 12],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 1],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  8],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 25],
 [[[2, 7, 4], [3, 1, 5], [6, 8, 9]], 18],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  23],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 11],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 2],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 12],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 7],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 11],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 18],
 [[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]], 8],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 18],
 [[[1, 2], [3, 4]], 21],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 21],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 24],
 [[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]], 2],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  2],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 12],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 8],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  21],
 [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 16],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  19],
 [[[1, 2], [3, 4]], 1],
 [[[1, 2], [3, 4]], 4],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  16],
 [[[1, 2], [3, 4]], 7],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 4],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 19],
 [[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]], 17],
 [[[1, 2], [3, 4]], 6],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  18],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 6],
 [[[1, 2], [3, 4]], 10],
 [[[1, 2], [3, 4]], 23],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 14],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 18],
 [[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]], 9],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 7],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 23],
 [[[1, 2], [3, 4]], 8],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 17],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 22],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 20],
 [[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]], 15],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  14],
 [[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]], 14],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 8],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 1],
 [[[1, 2], [3, 4]], 11],
 [[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]], 3],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 1],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 2],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 6],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 15],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 22],
 [[[1, 2], [3, 4]], 12],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  14],
 [[[1, 2], [3, 4]], 9],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  21],
 [[[1, 2], [3, 4]], 20],
 [[[10, 7, 14, 1], [15, 9, 8, 5], [12, 6, 2, 16], [13, 11, 3, 4]], 20],
 [[[2, 7, 4], [3, 1, 5], [6, 8, 9]], 11],
 [[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]], 4],
 [[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]], 11],
 [[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]], 13],
 [[[2, 7, 4], [3, 1, 5], [6, 8, 9]], 23],
 [[[2, 7, 4], [3, 1, 5], [6, 8, 9]], 4],
 [[[1, 6, 13, 14], [9, 8, 7, 16], [12, 10, 2, 11], [5, 4, 3, 15]], 25],
 [[[1, 3, 5, 7], [9, 11, 13, 15], [2, 4, 6, 8], [10, 12, 14, 16]], 20],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  20],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  1],
 [[[2, 7, 4], [3, 1, 5], [6, 8, 9]], 14],
 [[[10, 5, 20, 14, 16],
   [7, 11, 12, 17, 9],
   [13, 19, 1, 15, 8],
   [3, 18, 4, 6, 2],
   [22, 21, 23, 24, 25]],
  3],
 [[[1, 2, 3, 4, 5],
   [6, 7, 8, 9, 10],
   [11, 12, 13, 14, 15],
   [16, 17, 18, 19, 20],
   [21, 22, 23, 24, 25]],
  17]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-q~YJCZF)4TiyhwO|oaK9vR$vk{C`K4N?}fQ2>YWxsrCy3S<*WlYdx%=F__WlF#PM^?>0|Mc&_^*?-'
    b'l{r$&Ze*5!3ex0edAHV&Q=Qe5AtzOTiwJ9=B(Y4L)wVYeBb<UXP<F<T@k2#n0QMzX14}bjY$FG0<?U%HRXxhD8JKB5?YiFAHl~T-'
    b'X*JPuu(OpmN+NA9(sn;`nOVU)oFEdx|b(E#8)!e4foZ4-'
    b'p+<Q+e+lP3bWe#cSvVL8bZLM^5CNFCH`!d}{jNg`#?ih17yG8a|bEQ6Kwl2AxIghXvA6i;p(-'
    b'JF@b8AoQ`!ab|8Ev#XTWPnhc}A*L`DmUk)spwkGxt<QoGYDTSx?S8b+2dE{H&%=J9+fHy_e!Hd)~})ShJQQvP-'
    b'|)kBnLBRI5{ZN^=w{xYpU{`!ZWQznl4-vS-=W`Iz>3G?^b~Pj*^AX-}1&z0N+}yxR1_B5R)Cml-'
    b')*9%}2Jc|}gHEj4a_*<x?4_q*0ORjhYCz~Gi!j%As3t*WDZUq*q#*;FC5td%DBU1**h&3k)ptI(s;wu<UvbvA8lv1PH;+Mb46lIv'
    b'b~E@PKmPpxtRUEfxP1~!|8_JYHj$2du6?U|1kJ$GvL@-'
    b'F<E+@0?#y`=1I9iMVW=11MQ@Ljdiu{oRPTZg2P&Pro4EC4|6crNqOOuYoZmu9L}UA>6OSod}<xv7HT(s!kERLkpXpowaB_g%;7H|'
    b'gE;oSE)<F0<1pzPS`z&SKVj$*G(6!3a=ds$ZrzmJe7)zHKevKwhU*YIUE>wDHv-'
    b'{&igW%^azZW)yI6)k&@OE`GhdXBOs`o1{|<Q&CvXQ{vXNUa+7P#>%d@*ciQCpm^Cl2s0P$y;a+}i?q2ewH_H50;H!l=Sr;7N~QvL'
    b'B}>fRyd4DgblGV3Y1UbAZP!|I?<zvecgmxtcX7k)8Czw6R?1pZQ?eQ?ch9w1i#n}j;$pB5v~;}haVwpHQ|!)nOI)}^%E@Ceb2@UG'
    b'w_K$MP`1snyBeb_^{Ssa`ta^ar~%_O_R@FZcN&#Qqr+G|Ycq+BRoT{pKzf7I(rPtLMmtNCE>Z9<lPj)P{GqKi+me*Z8LDuBpCk)m'
    b'QB5F$d)o3cTeIF$UTx$wb4*(^%crOFF5kRFqFqpnQ8FuZnA|E{JrC=48+9v!qEyLj1Ya;Gb(lL`(d&{e^SKOa+9tj9>Dvz1x_uuz'
    b'y_eayo^HsVbT$;YPURvpH^!#XkwZV<rSuFFLVJ8_+y&|NK4OZlLY88FnLn1Y$5A>DdZ&SKh?hUd5%|XnaMv`Q78<CeOdyZGD(mWT'
    b'F{T;bWG#}GZ9c7~OIu7Ec&<L)T}}0n(|uY?TnGOEa~m}(3IL1a3b?jyu9BQ?SWo*@+)y9jG7ouh!&P)nSWdA?$qWp`Oq+fu&7tj+'
    b'mN!_jHjITa!_>APAJs49^WX;05#rB%*flq2FU&4wI{7S}n2qT`C$SaX6SGq~qdrp;(Y78+=YFHlYN?*K;o<{qbipUhXSkV(<tT1~'
    b'rIQ=CWa?xoW5tJlaxoYX2%@E)8(Jt(@v^io9m#OIj9u090lN&-'
    b'a$f@lfR>@Cvk=Gc%dCX5g7k$u^4ktLOkQ(k#7`<?^#th_smjla!e04cb=o<LW~KeW&!PK`bQOb6Pjx6`Py?azc(W32&SmP{qIRU7'
    b'uwu4TMH6dH{h6ukg>RvwfeuRR%$AlF7@+5lvSet2!Zuntn6|47FYG}D>nXz?@0X@9vZy-'
    b'*Q&MWR_dIcam`3#0TMMHIgNkl=ZxrZSQ{ygmGNkhEXzoq9lzykm%nVHUmSMNAwVQUu{1hYus0VM(02YQ5-'
    b'zrleO?hfl8AVs^DNla6hro}OZL%DvU<1?7oeHu{?FuS!tKQa76FgDg&rBJE)LZllwL^)|&P(f_p1-IS1za2DDg$A-'
    b'T#P+uW@6=%TIj>OwMjZK$#`q_-'
    b'04`pX;7q680>+x8({*igQ#;qbq6L6<bTH&)S~t8%ZLZY*U<qJr3N>F#=@7jN;$YItfspU<_L>Ouuw<8@e8^Zkb9T55F@OC=s<bN6'
    b'I2puARRGcWg^yyJAY!7J=E{o#VEE2BTOe{TA%2lH@?C<&R7%)r1ZXo`SuC_-E^|wVL2&S!7u>d6rTv&S@-'
    b'{QW_T&xSp`lSwZ%($2p!Z!YjI~xlw|-zpk)K4K$-~NYC?+`7mUu_5B%0429imu4bXYO$<j`oS<W&lnGjbJW5~8khG2(}eGSJ-'
    b'>M@%4tR~ZHz^-EzmO*yMRA@R(aTN8!f5-v;69ch>D)HLExVxkxq@st5{b0v-'
    b'@Nc5C><&uyS`j<ImHUJ~>t!%TnW#b`u9n_ZF#Le~J|(VqP!#SwMnr45L6R3>b8%w364^?%3|;dbDuTzskzR~hJ1pseAAFx>QNeJ)'
    b'*9Gy*B<YUISXc)l5yOx@k%!c8_R)Z-'
    b'7|mc#KZcfcQ8Lwo$tc`l!z;mvA+Jc~fYuAEY*=LWz>l$miyIiwBVF~+sQ^=ym`h+Ew7>DFd7Vz-fg!;mgn?zj*GrjobG-P(VB-'
    b'V0WqVcw_6wp8+FLmD+IkErgi1tUKDi$mHqz6q2ltNqKf$tWzr|EMRv>0Nv^pOsuP;b~whyb!89CqxJl9rcgC>BNfZPGWXii-'
    b')8InIF3i{_#JPa_nP&ZP7u#g}wTU9F&*pTvB66#HF_B~ktof{@PJ!YQ`u-'
    b'TP@>QEB?zAn<YV`8ZYLjhCS#)iRNjap^wi4q(teyZ>Eh_4a9J>-;{L3s?4lfR&5M434v2VO*1Gp-JU!k;?R0SjZuQRnkyhMU`F;s'
    b'aG7gS$G`4h&pkGxT<&Vz|AGvAIY_!mZ%>!o`ol06wcB{*%TGc7oIr%|}hhMh=-'
    b'~#P`7E3??aoY=~aQHfIwMMqY<`KjK>@FR<OYxH{N_a;)NlNd)Y@*9jw0ZrsZz8P9QYu(Ti$4PtqcuP%B?T*C7S>xqKQf&m~OlS>P'
    b'@OF<NvTL`HzRuqlfY_4?hr2XZSws+1bUNUVb<E_zdp%nC!wXu{*QlERXhfdnR+E89R8jg}VXEHKTfceN+nr9e{A;AqbYJ{(8SSey'
    b'Kc6$k^?x8vo?(gKzF98Z}u!YB|%mQ@$$ekf1ga!USA$r;(Q&i+dc8cU~5~6}vt1uIC5m&YX^`l`)W_ve>dmq^l1|npsD$$k9I1I@'
    b'^0De~JE>5zL3ZTxMlPZi5;R{QbKE|Y{l@4Rcc#@Vg&IGb!g;cjSP^tmiM5Tcuflu(o+-'
    b'bE9q0qaJ_=1_^4w^Or0Z!S0;~dANsBy=F29g?mCu$5NXQv>3$D(jAeMl5~JqA0`4n`SNgxbP%INa6g{jCslgc#y<g`F$OgnAL>F9'
    b'xnZ?1u-'
    b'&Tp8KrI+VpC2132RJl_VIMr&?xUdLL@qm!%!Ph+6?uX~;eUu=cojy2oL#13alLxQN|Kx_asjIkoLwWH`tC(t7`3vOmWKk$PW$)yN'
    b'j3yoiJZ`{b{Rh-*KaS?4O4^wIwkA%Ps=x_u=8iDe2vOgdirUUQEh(k&nJv>YRE)DI%g~idoTymFgdN^f<#UyHCD42<NEo8-'
    b'}hpBML1}?$ghCXjRw*=bo9~C!CAZ8jeI*&Jt6<JWp!8kr8t_M;_=6l8Mu^r8rG1E*gBz?mn3%(=Bhuve26L4phXkG=GAD!A!fr+0'
    b'$u1`buGCv{D9|kq2TtE-E!D45D-'
    b'7f;S5;7_X9^#<>?x_Hou^a_o`5+ivDrBElJ0h0|5M+0ZDg8IxFzLI){ebFrd?r7rA45wY!!9=5EOP{<hpz*=GuRz%h5_kGL^(X<l'
    b'EW2x^_G-OXyxZ2_<-Pcfwm-'
    b'1nozQY>u9n3n~6m|902ARIfRfH0nkc3hP=`mA7e7&_)Ipcq~R@#qXw8xLJvzSVcv*5h>|douJJqx>Mv~330(c<GYUQdGg-th?A0c'
    b'$gaVTsNm+0~lQ?n~0v<@o@n{H1^0@%8Kps!S!%g(ak+V1hh14tBlwnGvI(yCyNb15QT#O9_WQIH0<m8$7&3*TX3=CDUGYCs@OoCk'
    b'{_6+pT8VS==SRoR{Dia?lI6E(7w2echxA$`jNm5eQVpwRo<SGhFcS8<{rF-'
    b'3o7hG9Mb)6U`1*b!7LO2YODe^f6iYEXoW)}F7$x_?loe492#UlY!4ESuk;Ua=KP7yLVVd=8sz}|J~FY(PwPZD1`F?mVDOQj{14`V'
    b'FJc8C*ZUuc7Kg>9sLq(iq{^w#&}4owK=Xx8pNY`*)nOybPIxo_n@*w~9GnNe#1K+vS_kUQ=2uTWIzYs#z*Kgj%N({~$g9aEB#Ykb'
    b'^^nM(MsIK-'
    b'#fAe_R*u|5NYAt7tfcfyotRGEQ44{gz%NxU&wA~MppQEc3f*l=r@W@2!u5Glg(J47uU;D+dlL2%^woL=u%Adc2xK^hf`HsX0sgz*'
    b'u!hG^xHD}2F*xIadC*Ld($jUGPAz);4K1HDd$2Sou8trO23C}=!<@C-'
    b'eK2f7K#pdZj2bq0bMrl042o4wNpY<eB(bYjt_66^%QCCi`SDUGA5iOsl!u(U~>@mvfJUH&fnz4Vytr6)qauSYrfRU@{0Ko!2nKfp'
    b'9Zq7Cn^FCL9^BPt5#pj4zpgcnyw2Btn<-'
    b'*sCrMOLz@K!@YvB$Q#;p2$ncJ^C6RqYX#N4^^8qm1eUOE6DNbhoO3iBGe|1!DMM1j#LIWrVfu19vTO>)`UtHbAVp5m^R?XQBxVU*'
    b'3ZF<hbM|m(|e!?<CpRJ1EPy#393JD%AlB8?>lIoOqOn#jvn*=*;Jk#<B(!A>~B_l8V1c7rb&`OmM7K|&MKi8<`A9%Bh86nI6q(GA'
    b'>~dm*+mJ@)K)=GBfA{Lp<d})p;N6I5AGWms4!E5(Ex^l^9O$QOB-'
    b'e!Lmf|Xs9u>S0&DHun@UQ;J0UulH@OUshK|uA+4+8sRux~E(It(ORkA5XChq#pa|9tW-'
    b'W&W6cBCLKr;Aa*k<#q+zsH9!o!`84()Q9BMbXG!m<m!YnG~HO;bGU}xtPajBWfcj0xU}FI}`FCY(v77yqG>N9eih)dSfhbog<9ai'
    b'ivWhg_48gjsf3Prb9;-Pced3Cc_zF<K1-k(pw!YVyofX!<uJpiyRfTWk`q_;ufb1lr$XgPL@YBP8cs72-E*LB7+DdIdd-'
    b'Ltf=n=dWq;<VvrCPwx^NJry`6tzc7#8sxl)%e2fWsCpW>>U%&$yuG|SD^&EhF3nWK!CV~^72Yi-sM-'
    b'}QoJAlp4R}S9seiDzA!stbaBSB#V5ql<r%~G;nv;nxVQR~2Kq61PMXc(={x5@AF?ZcO9^U@I+$h{C2L$*8M2+&X$ZrJkIdt<o29L'
    b'GWYB<O)<2bADqnS{X4gm0e%IpM=AKm)w6N%)7R4qhT0tlPFSsPURhkO$U|%j1bKt65(@TzKc*Bm@w%jjK%Y(5_sxifOlac@ZheL<'
    b'W_w2QSS>A*N$FH(qq_Gvm2I{b>cpTA1vCcA(A^vg;m)o(EwIGuYx33VQ(*N^e-LPGb-'
    b'1e$eQbU*mbnQGhr|m4<RRv}RdQcwe{1lPv;?efikP$_xWZwKl9O1E)dqNX#eQp_>f${jb%Ppgv`_pl9PIsPEV384jimXv70*yd$K'
    b'A9`*b3n^L*0Oxno!gM+BBt-'
    b'N43f)9JADv)e0tM`U5c$`tuABGzkrZ`>vyf(NJoO#S(8MtB4=^MF@cnN1xZ+0~5UM!{T6~TX_Hk2VOO!_FpOI84+p$mul`qaa=nJ'
    b')sLA;;%pKl&sw3ej-S#t2Bk@Sq9m@#wPcr&9&OqEQ-'
    b';ff)jZ3+<cnI>jaaFpla@1V@e+|IE4g+m2M@abOqspPi}^WBFo3wHOlwAH)+3?6}dMOy>Z!5-'
    b'?}xqn5zIXv`HV(B6GB^QG5#Ub@UnFHOJoj>$W|`1kdH5G0{f=}!3f+G>=4Vv(HtjClKHF||7$*jYTh&^YfnVc7*Ch!@O$zKqszNC'
    b'cj=aEJJ*0eRCapf1eY!V*vPE-ZN1ToMp%+DAsCk`VsKLP83xeIMT!6+>OH3w-'
    b'eA&amU(N}YZX;5ZdzA9;DatdVL~u>DyLB&G)!%H`NDx|B%XLBK7%yM#x=N1i$JiiflDMqX#I$g_TM1@Fdr%(W8xFvb-'
    b'#aN^AcVrIXWGRjQ^y#~h$2Dt+VyKNfRCqAPZ=x2VJ(%(riZ@njqO+)G=<%_k6j>#BgvKEI+B`sXnE_{26vkZ3AxdGH(T{d-'
    b'H?>^>w$<V$;6fZsXcu9O;^2L}jl!!~Cc8~*DXV6_|ynBE+(2x!=$u6tm+D0Hw8Oo-'
    b'&W2C#j`<M$8S982OnxMEkZ!#=n9ig+}_bAf7gC0~!e?=$MM*~aPPDg>xyIlOzqvMy}OMfAHoWK4D#$nol'
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
    candidate = minPath  # noqa: F405
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
