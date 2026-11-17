import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[3, 5],
 [1101, 101],
 [0, 101],
 [3, 11],
 [100, 101],
 [30, 5],
 [31, 5],
 [5, 17],
 [10, 23],
 [20, 37],
 [50, 79],
 [100, 89],
 [200, 113],
 [7, 3],
 [12, 7],
 [50, 23],
 [101, 103],
 [20, 20],
 [37, 37],
 [200, 112],
 [19, 19],
 [3, 3],
 [200, 200],
 [79, 79],
 [17, 20],
 [100, 20],
 [100, 3],
 [6, 6],
 [23, 200],
 [78, 79],
 [6, 78],
 [5, 5],
 [6, 19],
 [5, 6],
 [7, 78],
 [113, 112],
 [3, 20],
 [6, 20],
 [7, 101],
 [101, 101],
 [7, 6],
 [5, 200],
 [17, 21],
 [21, 5],
 [10, 10],
 [20, 21],
 [20, 17],
 [17, 100],
 [19, 2],
 [99, 20],
 [17, 17],
 [7, 7],
 [79, 3],
 [6, 10],
 [99, 98],
 [78, 100],
 [79, 112],
 [112, 101],
 [112, 20],
 [19, 6],
 [8, 78],
 [79, 200],
 [112, 113],
 [10, 88],
 [112, 112],
 [12, 101],
 [8, 200],
 [80, 50],
 [113, 113],
 [20, 19],
 [50, 20],
 [12, 4],
 [202, 200],
 [19, 200],
 [98, 4],
 [19, 50],
 [113, 100],
 [8, 100],
 [200, 8],
 [17, 78],
 [37, 80],
 [88, 21],
 [202, 202],
 [10, 17],
 [19, 5],
 [19, 4],
 [36, 200],
 [101, 200],
 [112, 114],
 [88, 97],
 [17, 5],
 [200, 37],
 [100, 18],
 [88, 20],
 [20, 103],
 [6, 21],
 [7, 20],
 [19, 18],
 [21, 103],
 [80, 37],
 [21, 102],
 [36, 7],
 [100, 100],
 [20, 99],
 [36, 101],
 [80, 5],
 [36, 78],
 [234, 101],
 [50, 17],
 [4321, 1009],
 [100000, 7],
 [9876, 54321],
 [1000000, 999983],
 [999999, 100019],
 [172870, 530123],
 [1048576, 523],
 [523, 1048576],
 [233, 101],
 [172870, 9876],
 [9875, 54321],
 [172871, 523],
 [1009, 17],
 [172871, 172871],
 [999983, 999983],
 [233, 233],
 [101, 54321],
 [999984, 999984],
 [1000002, 1000000],
 [50, 9875],
 [172870, 101],
 [232, 101],
 [523, 523],
 [172871, 172870],
 [7, 999999],
 [4321, 4321],
 [54321, 17],
 [172872, 172871],
 [54321, 54321],
 [233, 530123],
 [4321, 999999],
 [235, 234],
 [1000002, 1000001],
 [233, 234],
 [172870, 172871],
 [17, 1009],
 [1000003, 1000003],
 [1000003, 17],
 [999999, 172871],
 [172870, 172870],
 [999984, 172871],
 [523, 100000],
 [100019, 172872],
 [9877, 54321],
 [16, 16],
 [7, 233],
 [18, 235],
 [1000002, 1000002],
 [101, 530123],
 [999984, 101],
 [172871, 235],
 [101, 50],
 [1000002, 18],
 [999984, 999983],
 [172869, 172869],
 [524, 523],
 [233, 172871],
 [1000000, 172871],
 [999984, 235],
 [999999, 999999],
 [101, 1000000],
 [232, 232],
 [172871, 172869],
 [9877, 9877],
 [1000000, 524],
 [1000001, 7],
 [1048576, 524],
 [51, 50],
 [530123, 530123],
 [9877, 9875],
 [522, 524],
 [7, 9877],
 [9876, 9876],
 [999984, 999999],
 [530123, 9877],
 [999984, 999985],
 [1000003, 523],
 [172869, 172871],
 [999984, 999998],
 [4321, 233],
 [9877, 9876],
 [999999, 18],
 [1000000, 1000000],
 [172871, 530123],
 [9874, 9875],
 [523, 99999],
 [1000003, 54321],
 [9, 1000001],
 [172872, 1009],
 [54323, 523],
 [235, 1009],
 [522, 999983],
 [233, 9877],
 [1000000, 999999],
 [9875, 530123],
 [9877, 54322],
 [231, 231],
 [18, 9875],
 [172869, 18],
 [1000000, 172870],
 [522, 100000],
 [524, 1009],
 [530124, 530123],
 [234, 16],
 [102, 1000000],
 [51, 1009],
 [18, 172869],
 [51, 51],
 [9875, 172871],
 [1000003, 1000002],
 [523, 524],
 [17, 172872],
 [523, 1048577],
 [522, 17],
 [99999, 99999],
 [530122, 231],
 [234, 999984],
 [8, 9877],
 [999983, 999984],
 [9, 101],
 [7, 999984],
 [232, 530122],
 [523, 172869],
 [999999, 19],
 [9875, 99999],
 [54320, 54321],
 [233, 999985],
 [522, 9876],
 [4322, 172869],
 [16, 9875],
 [17, 9877],
 [522, 9877],
 [232, 999984],
 [172870, 9875],
 [9875, 9875],
 [54322, 7],
 [172870, 172869],
 [4320, 1009],
 [1000001, 524],
 [530122, 19],
 [54322, 4321],
 [19, 17],
 [54323, 530124],
 [233, 9878],
 [54323, 232],
 [172869, 4322],
 [4320, 999984],
 [9878, 9875],
 [52, 51],
 [1000001, 1000000],
 [1048577, 1000001],
 [54322, 1000000],
 [530122, 530123],
 [8, 530122],
 [7, 1000001],
 [100019, 172871],
 [9876, 523],
 [1048576, 1009],
 [4322, 530123],
 [6, 100000],
 [172871, 18],
 [100, 101],
 [232, 522],
 [1000000, 18],
 [9877, 9878],
 [524, 51],
 [1009, 233],
 [172872, 1010],
 [6, 530123],
 [1009, 234],
 [523, 172870],
 [18, 524],
 [530123, 1009],
 [100019, 100019],
 [9875, 524],
 [1048576, 4322],
 [9874, 999983],
 [530124, 9875],
 [54320, 101],
 [172870, 1048577],
 [1048577, 54322],
 [1000001, 999984],
 [19, 9],
 [233, 100],
 [1000001, 1000001],
 [9878, 9877],
 [234, 235],
 [1048576, 100019],
 [19, 1000001],
 [9874, 9874],
 [19, 10],
 [54320, 1010],
 [1000000, 9877],
 [234, 1000001],
 [1000000, 999984],
 [232, 172872],
 [1000000, 4320],
 [19, 524],
 [172871, 1009],
 [1000002, 1000003],
 [235, 100000],
 [4320, 4320],
 [8, 232],
 [523, 999985],
 [100019, 530122],
 [19, 235],
 [1009, 1009],
 [101, 1009],
 [54321, 100],
 [236, 236],
 [1000001, 530123],
 [172871, 6],
 [4322, 1010],
 [172872, 172872],
 [9876, 18],
 [235, 236],
 [50, 523],
 [9876, 999983],
 [172873, 172872],
 [234, 233],
 [19, 100],
 [18, 18],
 [172870, 172868],
 [172873, 1009],
 [1048577, 4322],
 [19, 9875],
 [522, 522],
 [999983, 530123],
 [530123, 524],
 [999998, 999999],
 [523, 17],
 [18, 1000001],
 [172868, 235],
 [1000002, 530122],
 [172869, 232],
 [4320, 233],
 [7, 999983],
 [172869, 9875],
 [18, 523],
 [101, 999999],
 [8, 54321],
 [9875, 1048577],
 [172869, 172870],
 [9877, 233],
 [10, 999983],
 [525, 9877],
 [9878, 9874],
 [99999, 9877],
 [4321, 999985],
 [52, 172872],
 [17, 172873],
 [999984, 530122],
 [1009, 4320],
 [999985, 999983],
 [530122, 100019],
 [999998, 18],
 [172872, 530122],
 [522, 9875],
 [1000000, 54322],
 [172871, 172872],
 [1009, 235],
 [99999, 523],
 [99999, 1048576],
 [19, 4322],
 [1000000, 525],
 [4319, 4320],
 [525, 17],
 [530124, 999997],
 [522, 54322],
 [54323, 9877],
 [522, 530124],
 [9875, 530124],
 [523, 18],
 [172868, 172868],
 [54323, 231],
 [100000, 100000],
 [999984, 7],
 [172873, 19],
 [9876, 9877],
 [172871, 999983],
 [18, 19],
 [233, 236],
 [4320, 50],
 [234, 9878],
 [999985, 172871],
 [1048576, 1048576],
 [102, 54322],
 [999997, 100019],
 [4318, 4320],
 [238, 236],
 [101, 52],
 [4322, 1009],
 [999997, 18],
 [999985, 8],
 [1048577, 49],
 [19, 102],
 [4323, 999985],
 [1011, 1010],
 [999984, 18],
 [1048576, 1048575],
 [231, 530122],
 [172868, 172869],
 [4323, 4320],
 [8, 999999],
 [999998, 999998],
 [9877, 4320],
 [54322, 54322],
 [525, 525],
 [525, 524],
 [100019, 232],
 [102, 9876],
 [233, 102],
 [9877, 999998],
 [4321, 1000001],
 [9877, 999983],
 [522, 100001],
 [525, 54323],
 [16, 20],
 [10, 236],
 [4318, 19],
 [7, 232],
 [999984, 232],
 [9875, 9877],
 [100000, 236],
 [100018, 100019],
 [1000002, 54322],
 [172869, 172868],
 [100018, 172873],
 [999985, 52],
 [99, 54321],
 [9878, 17],
 [20, 18],
 [233, 172872],
 [1048577, 1048577],
 [236, 102],
 [16, 6],
 [1000002, 999984],
 [1000002, 100000],
 [999983, 172870],
 [9878, 9878],
 [232, 17],
 [1011, 1009],
 [234, 530124],
 [238, 99],
 [530122, 530122],
 [100000, 172871],
 [999997, 16],
 [999985, 172872],
 [100018, 100018],
 [530124, 530124],
 [9, 4322],
 [999997, 17],
 [231, 523],
 [16, 999997],
 [9875, 52],
 [1011, 9878],
 [172870, 100000],
 [102, 4321],
 [100019, 530123],
 [999983, 9875],
 [530123, 521],
 [18, 20],
 [1008, 1009],
 [1000002, 525],
 [530123, 530124],
 [172870, 9878],
 [100000, 6],
 [524, 524],
 [52, 1000001],
 [172873, 236],
 [10, 234],
 [236, 172874],
 [10, 1000001],
 [9875, 9876],
 [1009, 18],
 [19, 1048577],
 [999984, 1009],
 [9875, 9874],
 [18, 231],
 [172873, 1048576],
 [999983, 172871],
 [4322, 1048576],
 [99999, 9878],
 [233, 232],
 [4322, 172870],
 [19, 1000002],
 [54319, 54320],
 [7, 8],
 [999985, 999986],
 [100000, 9],
 [50, 50],
 [530121, 530122],
 [1010, 100018],
 [238, 238],
 [999984, 100001],
 [172871, 1010],
 [100000, 524],
 [1008, 18],
 [524, 18],
 [9, 530122],
 [16, 82],
 [1009, 16],
 [52, 522],
 [100001, 172871],
 [54323, 530123],
 [172873, 172873],
 [100018, 233],
 [530122, 7],
 [4321, 4319],
 [52, 17],
 [1000001, 999998],
 [100001, 100001],
 [231, 1000003],
 [100, 1011],
 [100000, 999985],
 [524, 999999],
 [54321, 172871],
 [18, 999984],
 [9, 9],
 [54322, 172873],
 [172869, 100001],
 [235, 9878],
 [237, 236],
 [999986, 9875],
 [77, 1010],
 [172871, 999999],
 [232, 4322],
 [17, 4320],
 [18, 1009],
 [172873, 172874],
 [172871, 524],
 [100001, 1048576],
 [100, 16],
 [19, 999986],
 [525, 523],
 [54318, 172873],
 [1000003, 530122],
 [1009, 9],
 [77, 172871],
 [1008, 234],
 [9, 521],
 [9874, 530124],
 [52, 1000002],
 [9875, 54319],
 [234, 54320],
 [54323, 522],
 [100, 999984],
 [9877, 530124],
 [100, 999997],
 [231, 8],
 [524, 17],
 [54320, 54322],
 [4320, 523],
 [1000000, 999986],
 [51, 1011],
 [4322, 100019],
 [18, 9874],
 [522, 521],
 [1000002, 4323],
 [54323, 54322],
 [52, 52],
 [172870, 1000004],
 [16, 1009],
 [82, 82],
 [999998, 524],
 [9874, 54321],
 [231, 54322],
 [4318, 54321],
 [100018, 999986],
 [4322, 232],
 [1000002, 172872],
 [4322, 4322],
 [999986, 1048576],
 [54318, 231],
 [234, 524],
 [54318, 4319],
 [8, 8],
 [530122, 9877],
 [521, 233],
 [172869, 54321],
 [1000004, 1000001],
 [999983, 530122],
 [54322, 54319],
 [8, 172869],
 [530121, 530121],
 [51, 54319],
 [1011, 1048576],
 [4319, 9875],
 [172870, 4323],
 [17, 530124],
 [1048576, 1048577],
 [1048578, 1048577],
 [172872, 18],
 [172873, 999997],
 [100001, 4322],
 [100018, 1008],
 [0, 1],
 [1, 1],
 [0, 2],
 [1, 2],
 [2, 2],
 [99, 2],
 [100, 2],
 [2, 1],
 [0, 100],
 [50, 1000000],
 [99999, 100000],
 [234, 523],
 [999999, 1048576],
 [530123, 234],
 [99997, 100000],
 [99997, 9877],
 [99997, 9878],
 [99997, 99997],
 [999999, 999983],
 [1048577, 172870],
 [99999, 100019],
 [234, 100],
 [101, 523],
 [99998, 99997],
 [7, 100],
 [17, 234],
 [54321, 172870],
 [999983, 99997],
 [17, 999984],
 [9876, 54322],
 [530124, 234],
 [50, 100019],
 [99997, 523],
 [17, 99997],
 [99999, 100020],
 [999982, 999982],
 [100, 7],
 [100000, 9876],
 [54322, 100],
 [16, 999984],
 [1000000, 1000001],
 [99, 7],
 [999998, 100019],
 [530124, 235],
 [234, 234],
 [9878, 1048576],
 [530124, 9878],
 [7, 234],
 [98, 99],
 [530123, 54321],
 [100, 99],
 [1000000, 234],
 [16, 523],
 [4321, 99997],
 [1048576, 530123],
 [999985, 999984],
 [172870, 999998],
 [101, 530122],
 [999982, 524],
 [999983, 524],
 [99, 101],
 [999998, 9878],
 [530123, 235],
 [1048576, 999982],
 [530123, 99997],
 [8, 7],
 [54322, 530125],
 [999982, 4321],
 [76, 100000],
 [7, 523],
 [99999, 16],
 [54322, 234],
 [999982, 999983],
 [101, 100],
 [530122, 524],
 [1048575, 46],
 [99999, 15],
 [999998, 76],
 [99, 100],
 [9876, 1010],
 [99998, 100000],
 [101, 99998],
 [999981, 4321],
 [1000000, 233],
 [9877, 1048576],
 [100020, 9878],
 [17, 1000000],
 [523, 522],
 [100, 9876],
 [54322, 99997],
 [999981, 1048577],
 [54322, 54321],
 [100000, 233],
 [4321, 999983],
 [1048575, 99],
 [98, 101],
 [530123, 99996],
 [98, 98],
 [999981, 4320],
 [523, 99997],
 [1048579, 1048577],
 [99996, 99997],
 [522, 523],
 [15, 54321],
 [98, 1048577],
 [17, 999999],
 [522, 1000000],
 [54321, 1000000],
 [999999, 100020],
 [99, 999981],
 [233, 54322],
 [530124, 99997],
 [9876, 522],
 [999998, 530122],
 [100019, 4321],
 [99996, 9877],
 [999985, 999985],
 [100020, 54322],
 [16, 9878],
 [1048576, 234],
 [235, 999998],
 [530123, 100],
 [234, 999999],
 [9876, 1048577],
 [235, 46],
 [15, 9878],
 [15, 523],
 [999999, 100018],
 [523, 99],
 [100020, 99],
 [97, 172870],
 [235, 999999],
 [101, 234],
 [8, 99],
 [1048575, 1048575],
 [530122, 99996],
 [999999, 4321],
 [100, 999981],
 [76, 76],
 [99997, 98],
 [1048576, 9876],
 [521, 1000000],
 [999999, 234],
 [530124, 530125],
 [54321, 4320],
 [1048574, 172870],
 [1048578, 1048576],
 [530124, 1048575],
 [1048576, 7],
 [1048576, 9877],
 [9879, 9878],
 [99998, 530122],
 [9876, 524],
 [524, 172870],
 [4320, 99997],
 [233, 1000000],
 [16, 1048576],
 [54322, 1048576],
 [98, 97],
 [9878, 530123],
 [523, 54321],
 [7, 172870],
 [99998, 1048576],
 [4320, 99999],
 [1011, 99997],
 [46, 235],
 [999983, 99999],
 [999998, 172870],
 [1000000, 999982],
 [100020, 50],
 [100020, 1048576],
 [101, 99997],
 [530125, 999982],
 [1048575, 100001],
 [4321, 1011],
 [9878, 521],
 [1011, 1011],
 [54322, 99998],
 [1010, 1010],
 [1048576, 522],
 [530122, 99995],
 [1000000, 100020],
 [97, 98],
 [172871, 9878],
 [101, 9878],
 [9876, 1048575],
 [9876, 530125],
 [54321, 100001],
 [999999, 530122],
 [234, 999998],
 [99997, 530125],
 [235, 99997],
 [234, 530125],
 [15, 101],
 [530122, 522],
 [1000001, 172872],
 [54322, 999984],
 [530125, 54321],
 [530122, 100],
 [88, 88],
 [99999, 999983],
 [1048577, 9878],
 [530124, 99999],
 [16, 1048577],
 [172870, 100019],
 [1048576, 99995],
 [1000001, 234],
 [17, 999985],
 [99999, 4321],
 [233, 99996],
 [1048577, 9877],
 [100021, 100021],
 [97, 9878],
 [100021, 54322],
 [100021, 99996],
 [7, 54321],
 [530122, 9878],
 [521, 17],
 [100019, 1048578],
 [1048574, 1048574],
 [235, 1000000],
 [521, 521],
 [1010, 8],
 [530122, 172871],
 [1000000, 15],
 [1048581, 1048580],
 [235, 8],
 [97, 76],
 [99998, 172872],
 [4319, 99999],
 [9878, 54321],
 [46, 1048575],
 [98, 999981],
 [98, 100018],
 [99996, 100000],
 [235, 521],
 [100020, 100020],
 [17, 1048578],
 [99998, 99998],
 [530124, 100000],
 [523, 1048575],
 [522, 999985],
 [14, 15],
 [999986, 999983],
 [99997, 97],
 [233, 523],
 [999985, 1048574],
 [99995, 99998],
 [100000, 100001],
 [1048578, 1048578],
 [99999, 1048578],
 [1048574, 100020],
 [99997, 1048576],
 [1048576, 100001],
 [4321, 99999],
 [99996, 99996],
 [17, 99998],
 [234, 530123],
 [530122, 1048576],
 [1048577, 1048576],
 [97, 99996],
 [522, 54321],
 [9879, 1048580],
 [4320, 100000],
 [999983, 100000],
 [9876, 77],
 [101, 99],
 [98, 4321],
 [98, 9876],
 [1048574, 999998],
 [235, 99999],
 [16, 9879],
 [99998, 234],
 [100018, 100000],
 [17, 99999],
 [15, 50],
 [99999, 99998],
 [530122, 530121],
 [172872, 4321],
 [100019, 100020],
 [235, 235],
 [49, 50],
 [100000, 14],
 [99996, 16],
 [999984, 100019],
 [233, 524],
 [76, 523],
 [100021, 530122],
 [99, 99997],
 [100020, 100021],
 [1048580, 99995],
 [523, 999983],
 [54321, 233],
 [1010, 101],
 [234, 232],
 [100018, 232],
 [100, 98],
 [100, 99998],
 [100020, 9879],
 [100020, 1048577],
 [76, 9878],
 [77, 9876],
 [76, 99999],
 [50, 49],
 [99996, 999999],
 [100020, 1048578],
 [1048576, 999983],
 [99999, 102],
 [4321, 530123],
 [1048577, 1048578],
 [46, 530122],
 [1048574, 100019],
 [530125, 99],
 [999999, 1000000],
 [1010, 999986],
 [235, 530123],
 [999981, 54322],
 [9879, 9880],
 [88, 89],
 [1000000, 54321],
 [999981, 999981],
 [4319, 999982],
 [76, 530125],
 [1048575, 1048576],
 [47, 47],
 [101, 102],
 [1048579, 100],
 [530122, 101],
 [100002, 100001],
 [9876, 4319],
 [1011, 521],
 [54321, 54322],
 [7, 100017],
 [4320, 9876],
 [99999, 9876],
 [97, 97],
 [99999, 1048579],
 [9880, 100000],
 [999985, 522],
 [54320, 54320],
 [234, 97],
 [76, 234],
 [89, 89],
 [7, 97],
 [99996, 172870],
 [9879, 999999],
 [1048575, 999985],
 [999984, 99999],
 [15, 1000001],
 [530122, 100021],
 [17, 523],
 [9876, 999981],
 [530122, 523],
 [999985, 98],
 [98, 530124],
 [999986, 999982],
 [46, 46],
 [1048580, 1048580],
 [16, 524],
 [101, 7],
 [530125, 47],
 [999999, 999984],
 [100, 100018],
 [1048574, 88],
 [54320, 1048578],
 [1012, 1011],
 [9878, 7],
 [14, 54321],
 [172871, 100019],
 [96, 172870],
 [4318, 1048576],
 [89, 100000],
 [530122, 999983],
 [1048575, 99997],
 [235, 530125],
 [8, 236],
 [999981, 172870],
 [89, 54322],
 [530125, 530124],
 [47, 89],
 [100002, 999998],
 [1048581, 46],
 [76, 530123],
 [1048576, 521],
 [7, 9880]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-'
    b'q{(JC^ObmR&0udao)n@goR$SrHikNHqDc0?(3_W~#pGohO5F3qT{9Zo4=0oV_E~B7r%_90Qo2|Np=J@BjC|{MY~DfBwgR{P%zVfB'
    b'wJ!Inq)8<KO?S*4|6oS4>A4M=2$hwNr`5y~5EC{;;=tkCkG(cD_@-'
    b'+qrf*=FC?;TmFy#^&kK9zyABb?JKps?xVDHp63x_88IA3p6jgP7^~JZ_hVegIq&;U<GjXIVl8~c8P6mA=f{+C&nwP-jB|&pg?sd!'
    b'OY32V>n`gm#}P`*tIgR%JwuG^n0IJrnlYc@_|K17cRy<B_wc8$F-'
    b'E!W&{vJI?L6WY=GZ%@<Eo?fbhpUQhZf>F%gLLUZ=WWIu<mrUW1nZZV%%-'
    b'_d(L#;b<TR08Q0b0dGUNLu@^1PUCJ)kURPx~|MO!$+NqMxiw|8n+<V>ix~_7!wcAxnEXTgDaO8a-'
    b'7f*RytqmU`4mK%;P<F3BFU78nwa->}T${f?YVcp~d$#*(<zyxL8FswZ?j^TY?!v;IbLXpv{<GnswwaE29D~Q<r+VzGUFYH*Vyf-x'
    b'eYAczUN+C#_89x@{b-SQU9+wGKR>30boueAgt^8%^O1QNHlmHXYEJV!T3`G`ju>H#Wu0s;-'
    b'x`m3UgyVFd|t;)V}uq<zb>|{j5}W!mUm>{Dy_X&yYsm6vC3TOzOc;e?5m%=^`3vyr+C(Tjce{u>Q#1RYkLTT4Lb4_>s1fdG^P72b'
    b'tHW0=soVvqogzBx_|739SEu3XTQV5<c@W0R;#B}G0BZ-;H~U_4Q;krj&#h-'
    b'0;M!s9>=)%pIl;|UI(8%6N`CYIJ8DzQ#nJ3eVpqIz1F?cmF~)acx+w(6Fzn<F?{<pAAJlK(@SivrW(^MJK)Ok*!hg1mkVpbf$qW{'
    b'@4MF&Sn3(h*~W-'
    b'{4lwoGr}+qPKC+v?6&e0kxVy()LuB*v#W!9@yTg@Ny=G25<_>tAErngLQOhbTuGv8q(B)1*LB7AWn=8e+?v{>G`MN&qoms<8%nAD'
    b'trm&7m#Pjd+DrJQWyC1V2_c`;~KL(0e4`OexG4P}JHOC;#HY_j<{vxbFpt|;X&$^GB08hjv8nRV+tRo-a;>|~P^A*1tW#-'
    b'#et$Xps_kl0Y-dkaJ#%=>>=`#?pJ0u9t$F?GSS69bW+xU|p`q55-'
    b'P=wZWuVaildE4AzK;yo_xnuMKH8P4Gsh1;XkQlDRj$vh!|CNse%tssk(Z_rQ=@Gn2sfPux+$V6i#&P2n4LfW{&2f|p%jRj;2{O!n'
    b'mOVCWQ?CSSUOyjG*b!Demn(D_3=HQScibU?FCnCqbBu#cxaSHrOo*<J8?cd(R@mRV=HGILzh!>+Oz|Q_P0)t*4{Thohzvs85&CXt'
    b'InGeZSR>cG&UW9>){JKc4CsnKnjxGSuN||Md6Zpusri@%#T8aOJ8qojJfi_KwFo&5bwPk@O&uk}hkt9uVY8Zm10t&P(x@awPzgl#'
    b'!pEg}r<i=Tl@FleuB~5v62VtG2|(>n(rX^@+=UGdCuo}TKs4f)Bb*%=<?rAmL`a@2jGT!NaaHB&8c>y3f0*dC69PGmIaat!UB}V|'
    b'?|PsnN6BgTh-AL5k-^s$6K~cUjy&Kc_xUQAk7&~0+NqD8=A)0fh;teKbwc4|#(!Je3x$Yv9M`~&`P>3Dr<swN7u(a~t_?<o2AN-'
    b'zw!anbJ_<1HxH24+eTk*8H?_~wJzUY!M~P!YyAG`fwgDGrebPGE-yTjPQTW!UK6)wWbuO{rcg`CWkE^%6LErOE=V&EWv`8s6_Oh{'
    b'tlaM-'
    b'j$vXGGYHnfutj)~=+_|z#7}#}&#D`wJ_0krbF_FVOUeEj#vW7isbB95sxI2M3hi{$XtF`%tiGK7kAHmk&a?OuUXg}KUyNnVhuDB!'
    b'8pq=~fywB}H>Ruf=vBH{HKVwZ{mN*Z@d0Ffn5|}^x0ns+DcBq!wzI3KF;yj_8rQPd7=HI~OHO}5L+_-'
    b'n1d88A<JW>uD7x{R@KO$`(MTU<~uRmIwzqQ1F>ni7?4gW|aR=;lYSIC77ey)8V$wT!yFqCjDV$W^{(R!50t8c=_Nf=FhR-fZrEdF'
    b'SxDgiCWs|%Hc_<G$?vIuA6&3UVJ@T4+#@HI4EjbFcO%=-'
    b'%CX1(8IXSGy37S3|tz0|puuXeXw=FLU}Wf&VGD;8chgbvQ~+l7~mvHsF){4MHmSI5prnJL2{!K#Zzi~Gn&#wC2=5HEm!z%b{)s*a'
    b'F${Mw3Zhc1LYGh&g4AHB+jzyjD+tk`9aZCw}Ks6mvD+(%j~?{E~JI`>zy@_i7jTzcH=KwJ_k68dt=brvxPvjJhC%$S381sQblWJH'
    b'Z4jM2Ugcf_z`-(i*7S|FU{%vZwc?#rY1!SaW51R}{r=t?jsIM~I$v!U&}->3P=HAlJ&i_R-&pbKSK*2G|-'
    b'eiIwqaM_Z3g8MzJ43vm09@dZ$<WRsLk(hXM7XO?bDmHezTD%TuEO0)KcFqIm($N9Y1G8k|8VHJM_4CMk{NRlz$Pi|b)~(^i+4E50'
    b'+WoG6J5~aQ^4SUF8G)#tZ(L`Wsx4eU=C{fb)5$00NXR`JE6p;p_XM00QoGh>y?{i(uWx`PUYmcK;1HoGy^*1&itEJAGeAu8Em&1{'
    b'?koY<tVhRD;JO%HMLefFU<(tb((2XPIld((wGIJqo;V!;H2jt0T)6QJH+mlALQ;USed$jtha>a4d<~+I4gDb|Ea|mdj3*|Wd560}'
    b';*VLtlk;W;2I!*_z=8?MF@>{$tdsvol<q$pzR-'
    b'(MnHX}uXIUi?#;}nwC&)b~qzwWD(A)^0ELpnwGnVi;iyY_28ODtrWmfD|2Mx>*Cq7Ts66hn87D&?=@yvuK0`<igdT=r4byY&_@qh'
    b'Dy-B-szXvcl@sO|Cp5lnaPL=uQA0SEt&Y~fiqketwfSl<Os17t9jo5=d>48%Xw-iUxOIygj84-'
    b'cqUzaY4Ycn<FOiWZ*mxBCbLX((Jn>t5@<SPF2fV|x~VmwS%{-'
    b'=2Wxbsp`$V1fK2L2KYY`vziiK^?bIOh6ddkMdm?Pz_JH7N!kw6FD*4BVZvIQOJBCBzj=#EEfD4EP$#J$^kDT*$;@86`&Kv8-'
    b'YQbf{?T3Al^Q`0$5O?egn_vRd*spofEgggZUgt0wDDBQv5Fe3Q}ww5E4TWtpU`#Pe38|I#L1=;g<Jt%q#UX$1w1670i8pe0SIPyx'
    b'N^Y+^Me;5$Uliv*D$E5op$3aC7Jqu)*?~Fo6H%aYTHMNc|J;^3?#dWEh10gm9<6(P{y&k7q$A@wGjHe+zcW##J`#D196!#P(m7c!'
    b'7;=L(5P@-'
    b'Bm>X7uM_M|4eq9pa+ig(5xLBRbeK4O56MN_~TC=N)frruGdUq#d{Lw*zldeP!DhjHML`z*!T(=)P``t#<BHYAQ$aO;dRYgQYSi9O'
    b'ut_xL>#Kl;+Ybw!;>9^mQ}CpmhC-ph#U1VOAcio=f`XF&4xEZ__2>tCG_GpRA%f|Cmwk9%x56%JBxFld!{|$Zx}1Ub73CsjSPQ_r'
    b'SI50hTw_od53+#ZXyqX#6vfMXyr(dh+HDid=WZXY&2iwabiZ)?{9bNBXy_KpNAlR?4;doq({#DLI+J7kpYO9okhJNC-'
    b'5G8ptcS;Zl3489<2tBk-'
    b'^Fqfl3_atZL~<pz%|1j2>`}Jj$I`8VEX=Tt1!%ey<<9NhM=CETDI>Yfr2#Ha@cC(G3ciqkIkHfgS>_$3!^s&mJ@G`1%wdaaI;*mr'
    b'!xy^I>8{5xkcehk@UyppM{IY@I+P_MTWLG$V|ryjdL^)E=3SB5sztJDj|+;Tz(LNJH|ZEqSY1yUL9afGcNAtqvmBdp#OL-'
    b'm1ETrwZtPB0_|HLM2nK`$-XGc@Q3xxZ99b0g5?l+yk$e_qP=CBM(oYqC6U{4TlHRc%cn(-'
    b'V+Z(eNI?+P{8I6HZHU#_y})9F8~5BOaCb21$u!{fkxs4(Aa2R-'
    b'MNLHQuFTo_vDe9r|d297|7L5fUfmk#JlUgflgN~;lxcgN^x(L)<o(m!Zk<;^>HE^hgT^WAp8fedcZ627R2e_Ja`GPDqu5=V_~}&7'
    b'Ca-s$ELysGeA~Znps)ZIO3iQwUFmU_=6{)q58K`v&R%K9>mjKbQh%S$henhf!BbufkBXco{<oF#QP!;!uZOKX(Mpb$H&g0-'
    b'AHcqQiC9y7J^XBFc9R*?wtpjr#X8b11i4nGDC;IfM4g};ojie%D#|&iJf2Y=@2Sb-+0M2_873{a`JoFb~-'
    b'P@P~5=InIORvBknIv+MA$7l!<7b3GLm5U2U_&(6F+Q6Ql^>tzM1n1Zf1E)Ygj^MnwHEQ55`9S)1o}3U1eMNZ2MIv`@e(gpmt79Cn'
    b'y<4s<z;b*iEv;8@^G_IdZ?x>p#n5U1lY7jg`YU~Mnh`!Ugt03hyl!QOF<5JSU@YXZdHW1xvd28q$1!4%c(^-'
    b'*FC(3>0GJ)rP40LMfafB-B_Jf(CrYYRWFIZ&wc?nW5ku>}C<z$gg!kpGURnP^xdOR6YCaB5;wY%WZaEr&q-z!tE4v#O;)1M-'
    b'2r_ZeDiqp~u1Qh$<e*<CCjZ4$1Y*sr?~9*I8b$HSGw68kWTWq0)C2K^B*BLop34W`eFwFi;0B!ZyHSU04<vLpTYIQ<L#wFWT{&I2'
    b'jDv6PxqEU2;#pTw4ksnC2+2*#CJvx0a7|Ij)q9_`2ch$T0h43?OSq4GvygX$S}m4heO7^`Wda35$+m^p7^7SU1NGk)ymM#_VcyR*'
    b'A&cRf3MMlkBfRc6PKQSpZ-'
    b'4T#5ubpWHph69Hx1dIB!Q$sY|{L+H8l^zg<2PPK};0;GK4`jl*A&os<uoSo(K(<Osd<(Gn@io^+y!g`jM@Ap;8LTNPjX=WcVLQ#E'
    b'FrxoC5keKOAfgZd<Lwa}w|+Ahj^>*feqc37+fiZKg>{AKqO*ut`^XE56*tfci^kj+#(}se()<Di+-v3zBw^=gCYHm-CR{|@W-'
    b'rR=7NpUS9Tt&>#Ri~2x_U*x`L!G9+%2fr=#5UqN!JPfr7IZA(;})Laq%`RNn(ZCf!hK=#H9YN4G)sAgvF=bZQ{WT{PR)_*AM#SIv'
    b'-t#UgaNfsc_<#UK#LpbN=v~11G@4Zm}luJD7Ct1(?6?an=Q`y&;t>YC?2296_s0fYgPL^U!atM}}%7)Bs;`BH#j?t+m{UqTo_pyI'
    b'&?H;SP{SFaKgVGc-#K<fp%t9$h_;%)y_J!t!C%N66@<wIf{iJdo4uFZPM60k`Xcc6=K?4w-'
    b'BpXRV@EC(#b_1nbHH+aow**P(kW207k0k)22OT7wXHd0$YL8RtrZcZmyM2a<TRu@nvP-'
    b'F>rV$v5GR;M6)b9>(Iq|Jp`VUL8_A+PgLf(YjYph~b5-9cx^{Iu;zq!{#RfBCR8tHqepcI39nZY)lg7AAWNH90P6I*$h0e-'
    b'uUEzdg9=G>bdX_bkTr0;?AAd%n3rd;K4XMHuT;zNc4$l@K<<?3Dhvy7Ba-Lcp#7`TJZ2+VPE`}`iQtukjoH^`aTWh;}~<}(#Qv7P'
    b'Y$D;mof|0Fw$h%_<6MSMa07<m&d}OM~az0`_}wSc0pOB00|5DmZYJ0e6uphpI8g%wC5bYdl)PCc$cf;$QV?+f0h{Rm{==6TKQ?hJ'
    b'j=f-ffhoGclMLjj}gq^g`s~j5nE5c2^NI%`oWtHVd44qD1?A9@i)whFn#ubc)d>e(t&Rh--!@JZFv6T-{-'
    b'kt(4qdUO#@#b)NJrZPa+U|6GTTq*nyE|%%x>WNoRy))r?wYk;6e;<bi*lhOMuQm2V>_zTJ}=xzz<<LT{RG4WY&g$8jul#C<@6AbJ'
    b'U!!T!(iyTm2-'
    b'iQAdrcppbv{XWNuj=Rj#@?xT6H|<1B)<Rsx>!JDGQj+@(cf3iR#A}bG_)P;R0=|0w$1+S7XzuGNID(I2eCM&?sqh^lK!IQX0L2zY'
    b'y*&l>!Ysot#BFZxSrDtN&KP*K&xz@xKoPct6M%ai^%p3H`W)j1EeV8C<t4A@Z4joR;gID@gi?gvJ-zHl0`$gW5!s=f-'
    b'@?`f<%T>=DDxyT5v&&4Qk(ZEJfbHRs+n~Qm^4v$6OO&0yDZ&$cWOQdeJ7lS{}30)TrA*~QJDNrfN23|5Jq4OE&&xRhxJ)##sz7u`'
    b'Mrbj)A<4K*HEEwE)VuL0uvSM8P>qmyt(qkHZ9M<E6<#eC2*JbV~B1<9u#XNCh550o(G&<cC<i16fj|8bVBQ)l7KI<g|GtXUt0U)+'
    b'-s1Sm<alvUSJL=6?`T(h&_Uo^@#Jb{D92_sct>8HNf5tWk2gn_Jhabi1g^?{p#o06t~zszwR2KB0E8RJQT<b45+EWrVc3TOOsN--'
    b'v_=Q2^Z&$qJTK=%AaPU*MN%5j=DYqP#PA}Eu$oA0WBk}>En~OWTaj#0NvvOA|8z>fasitvuV;`xIOR1*P&0{YmyWeyvQqv<69>B('
    b'M#POukFPBwnsg#frw6)+vIyeS1%r{YB#14V2JEd1;eZ_g9Mv%{3pw45K#-'
    b'}xa8$WvoaHw2zJTOF`78bKauaMS=kjNmB<oeL&zoFKLI8j`9e+c^SCSi&zl^+8@wD(T{TSz>>|t~3b68!&*!QWwd$4iTUm>JNX7}'
    b'K&(SQD!&~eFRR);d1-'
    b's#eQ_>XR$FULNO(H=?<EizPWx(oL8$o%nRm4IZ0={nS^B~U?b$*H91)GQP2l)iiqbvmNJqe}10vZbLWzjnKfR`>}*$oMdt(qzd97'
    b'2(EfDA4d(DZ%a&|{T^r0n0;mVG75R`1=zVd7jzDqxxQAmT;Xh=vE2Vw^Z9!gZd=H~8Jy^*q_Z1%~|u-'
    b'(y&31>gr37z0buYtddk?Y`h7CnVV{fqU@)yv=d4ofeNrH1$s3mJ4H>H_~n*@zHa;Ag*u~=;MQbwPq+}GtC7@lE8a*-'
    b'TJWtv7Yezn@6#{j3Y9Xh|C)qn#1a#x%sIQ;fw_DvXG#-'
    b'7s$WSlkiIbSzpUP&d{OTaQl6SiRi+6&%JRjz^%{2>=0t;g0XM@hni``D)S}@dkBi_J<PmOV#l+`#ltg@rR0jTJb;3*;A_0%AV{%P'
    b'gcztc)MkMLNy-'
    b'j+{RuGTxR2(MRyDOL9nhDPo$h8*Or&<Xprx>v3((1!{N9KI`~>+GpyV&xDv$?a$;!vw2vFWcAt3nn#V_`h+5w+NkFrJ!jW{Rf*m>'
    b'>~f$^T~KiT4*{DYe;AgWmDk_gl2f7B(|bX~~SglN5SgxO$x;M%}vbef-?BG3Z>JP(eB_3`ynbxZ)=gB5-'
    b'be9dLmVWEUa8ZhsCoabfU(e=h~c&~{unaEucntTGvN0J96eL^Or1ygBP8i^<I74s|}j>qe*%Hcsf#5~nIV4R^`(kX-sItN+RH*_}'
    b'o_&46#E&?ykm0)Dm>?iE-2a8+r@M?FHeYz(J1=>M?jtD`vxWq|FV83A@#iMzcK>-'
    b'{wdXG^)zH|e^B90mNMpXl!dE^_S+zukih4uYYQG@*waZLJ67S#Z?*>e}*^v(CH<6OSPLC}OB4nVH~GoHt`Wg<e(jenX`FO6mtz*F'
    b'OW!qU-wKTPz1YauI4e98n<i0z(t^|Uf-'
    b')5s%_Xe+B!h)hVLS!zI9MQ9G5|8W%{g6ljXk5>nIQ6_jgi`1gz)=a5TV3XU<5l@VOO<J*w5ys8emv5=S7zA-komgK8^dhSDJxxox'
    b'&d8HoCqntoFn$#4;^mKZ^z$|}o+sG&<KaB^O~9TIV9@;rE%1Xf57xd;)~f(~Aq}tRZ<HC7zynhPH34YdAKwT?9SZez%{ubol@3OI'
    b'6c!!y#drfavU>1%5h>2jjj{*ZXV#vO`IZX<MOY5n@xs{gfr8r|{0mP+9L&HLV9F~2tzfY|L3qHsn9Cf;o5YAUfS5Sl0x#LZ4Hs#c'
    b'cH_gbgz3Aj+lMru24dK02LDhx;Z)z6A6C^pedC>?iHFmW0$;0eCa~v3XJP~srEUraYlt3e`B1Q-'
    b'_Gf=115B(CA^Eh6f6<8IFnV|I9JX3+c68#l4gjBoSDu8Va~Fcv81JnIO9)-@2n3-'
    b'5cp|P5%jQw?z0r_?!~n{0j?v91l&;t^0?GM)%mJ^I4|d<-nB~R<VHd}Eno8i!M?p5W&OWV#0>^l-'
    b'4O$axuDDYBmiv9gw$Ax5JFpn%s^-NLJPS|}K|s{m@+=ubfs`O9NAr%^p>vvVil4sM6}P8~-'
    b'oUbk9&@3)Z;0aw!w(k2L(lrj+Jj4ox#BTyghUb5;OVdQh%neeuuadUd&88m2li@8K?qTZgKj=sJ2#Jg?1*<iI1GR2HUD7oYF3h?K'
    b'X2?dd4&hevV249Ew?#o&=cOtQl)t!@S#2j<beor)i=HUqx*2M>N@u%@UX?rgV+POG2Z}W;IoNwCtHp8+MI|#0D|{m<8mt(Q1b2ZV'
    b'HtH}7&QZC_dPINA{-x-'
    b'thR^pO;cq&TdTw_LhyCw1}BI_if~^ke+v``5OgESYQ&rQwst3&FHh8FXvy0Oi;gOohp|ca&O2f6<{v@??vJCUCv@Nvdk5_f;L;2?'
    b'uF02=16U`Fnb0mFtC(`fN=;DAmzuy-h1bI|Oq{xUZV^nq1-N{{;jxRwMa}a%L_{?bUTX%3AawRRr-'
    b'_(<vH=N_8?_CWSd9RAR&2}5R`iaUnot?G$;2E&_b}NK?T-'
    b'*T62aQT%=JQg0g0eQxUqViHO;1K!PE$|Jj7VfX#oNT{=LU_*M>LL6&BL(y~yU*npehm^0=;K;~wjjD_&xCErv{#jAeo*&%FkOc4S'
    b'2OoC*E)b&DbX7{TAsfIHw+7nA|nG5}f=v@UfO?*&CJXz>h@U{y*3#t4wto2v3r3I270_g8KUvn1@p?T9j&rMgDA51R=Mkez_(C2t'
    b'(Ega~b6rE9p-'
    b'n;4AbVOe>KZ3YA(65Aq3VY3bPJR<@GeH0%YVLd9Ivg_)ELOAa6sykJHIkxlK|3qi_wxze8fQDr$ZWnJ3K+WVrY$+EHT*E-'
    b'&19(3mitCydWBPi+(A3fJ2=sAb>y%n!O}GvG4`;~{YG8hYMM%i5`?u7HAH^Gkr`@}H8g+ULna=#2kMa^va(xGNa<MN-'
    b'4=_<;GV1+)S^5zIF}xxLYAQUcYCGWA{W(<15Ri2CV=C81BX;4zC^@vqD8o9aZ_V$cI^O{_=Ggk&&y^Mmb@e8h3_W#R6rj28Em?lb'
    b'KkhL-1p%trNz~OZY!$c%{=DsNHI?<T9=JO;+*>Hy)&@jxley;&<iXl9>&Pyp`YY$-jakJZ0wRt<%})67Jlyjhs4)>Q-'
    b'e%woPl=~Z{Y-XQ=vj}%-'
    b'joBRoECvNV*{Gkh9I(4MvaF!4$GE{87h?!1f~R3aD%t84Jh~WTM~O<wjFaJ`dDaFyxYH~*@|Anr2$ikgo!8!b_Dh{i5BRH=X>X$Y'
    b'?K8VLv8gOui_zq+;83~qdAD5;N<~DGlAEVfopiSu)XhiPR?23H)@{kI55vntnyrqAi#r^&7UKFQ-DcF6PFTELPl%d(9I_;{ztTbH'
    b'N%eSI!_C47kc@EeqcJ?t%WBAbM?Igv0TW0dS`kvX<Ch@7~b!lFX#?Zn0S$WnQgu|&gu2!^-y1YL@L2f0-'
    b'5Qo9$nqu55s`Z_xO;7@)CwW>GDEeJ$Rt8j{>pB=7{MD`+4%sGlp4WEEvFzr@}5ndkf}}bAaEu2m-'
    b'L|e{zmCF_B=`u;bGnZ}9A6?|a8!=G_Hb0S7L#g5J~XW9JA<U_DOO;VJS!It}X<TCN#ys-xuf0OC~wdI?s7k8JeUi^XYMoyWrByLe'
    b'{z`W^O6X!0@%uwl!@I#0KO@dBh&Pk|65aKSg>>a!H?HEnST(|5;DOSnuxJRxv|fKWH;r@=P{3?Aohll2|Pev<F`k+&10HyPP%<+c'
    b'DEVykEHI5td?-44JnFw(1co^tIop$6^hfY1C(0>n3|afPK@-XxU-Zr>ekh^l*zsPHe-wl5qGJ=C#t){Jn7+6gLKmi0aNgKPbB5sU'
    b'WcJ8=O#2QJl#<fw^5Iln?MIRe})6#%#(6v;b&^9sMM<o_y8b$pODhd6k~j8wK62jUCTcTIp%MBNk5VyA&mHXQnc)SGa>c>T@Rn-'
    b'H7XV&`!-'
    b'q#l`vz={LWdk2f2S0Yego|gwfxA(x;z^q^_sP!Y2kK4UvkE38^2&Im&9o|M0BatfDSGzoQH*Lq8On|>zm)TS|I1I3!Ud^z8T%v9`'
    b'h-'
    b'sA&pg_fROc$KI4L@5%ftAX0Qqo0&UOlO1W9Rv8w)02f?xUyiJfy)k0n!fA;6)yJFY%P9a_Z6uJ5NA{VG;v}SZ%A>8hn4fK4rr@q+'
    b'brlZF&hh5N^v0u}K&a<lJ=1oNh!ATwt;J`1?gnHgCQhU)Ml?(*Ne8CAJC>_rYR`jS|1(FwvnUP&uhR2kVr)%s%eH1I3A#*<uoveu'
    b'b~gus&KFPv%f%r>P{sMV%FUmS7cg?2eEDH4i9F0fnYaIjJX;$V8~^@mpO{4-bstKD}S<ew1H}mj0uh+-'
    b'M?UHVx}Gbu+OZ_PB_I+Jcq5k`<m5qrb)jZ9+^W)MBC#f}u~#+Ai<P1L*mb{+UIRJah55@(2B3Kk$zWd^o$RCuj6+#RcYxcnV&z5n'
    b'eK$I*GkX-'
    b'!|%X=h!XN{>9>+6@M3jwXN_R#e!6xO~+XOsTS|1jT{F`I`cx&cLP@wbPHbhadOBvweug*q?sCzes~GEV2r`^K984cC=+&k6TFJ$_'
    b'WrI7Jy5~j<LIZ*=6s{(N39#KY%c~lB)@2NC2<phX&#Zx9Sp+?ub4f=thO_LZqqU<n9zwMeq8v(+d~AfN|XG}Fy`-'
    b'}exSj<?}?Zw1<F>>J?;Vd8o5Xh){JG&^$VgS;(+63)x8aY2Vh8{VnGB@$Wvqu;OUnoj`&C#5QAl6IG+rAeXouSeB=aRktPG7dYs!'
    b'jYjki!FnEHB?^>7*ufCU;wiUL$PSfw%t@lFmqYDCfX7$*x!hF#T4?v~zbUt#ShPl`H(t)X<QSHpi*0T!rDg18l5m~uU>(e7d3k*z'
    b'fBLq}9mMOvsYeR@Yk4<ItybaQT3t#>PlnyKS`Is9KHpZM6m>m+7ST@DOZ<{4#_z7|kQ@p&>_uxdUE*lHDt@wVAol`^?3^^^&2%`e'
    b'7Q?`Kh)O~Q3#gfi`<Wi50{DHRfmct@N{O;`-T&#e_Ig=HIgq~*dMV!lOBXNEcGKnT=dXI6_-'
    b'uT6{VrF^2=Qkgn(2hE;3vjhUSKuX-Pd;VfN-Qc1RjS9B%j^>a>yf=OsS8;ic7G40;JlM4k7zgvmiXjt-'
    b'S54tsq>f@&dMrxI|bmr_iY1W0tJgTU<|*djfg;4+=TF+?YXx;k1_27fGiB|mnHke1~Ux2$K60$!{GTU+jxANj234zZv^&!o*ttHT'
    b'MMws4bgoNa#$WV?(Q3BV=F+NG@%WO2bS<H3Y({;g{QTF9kSl+fq`B~nJ0pI!Ik)vOz67Pl|63-'
    b'z)+7Dh<LGZAK!=1=51Lk{K~$UK$5Ky3+CAX#E9Yu#L6U(%SMLd(SH2n9v)?VTuu`~mgafz0p#2;9Y_lD0px<*w2%=~>l#F3A~`r_'
    b'V<TeXoCLLTUvEy^#5gzj)W!*`IXhr}K#wtya}4$_o-wRK%yC?Y50%Y3J{??v1b*|<*%$MHy!^vH3t9!QOmLcoAn`rWtE|oDzX!S*'
    b'o3jQ4!$_L;oBRsOqvh?SkupS^U6_lVN0KeSEe3PPj!}r?3s#YBRfXO>%y8Q2W$D8cf;pl=#+|T~+~EPY4Q*tV1kG-?s5Lf-'
    b'$$NoM6U@OQps9beqaG$L7^+yWYH2pq3)TqHS~Yl;LevBwM_<DW0a$j%+ATAa7`_F%A6;`5&$Hs8ucUFn04Ad0RvY0rD5^5DIUa$S'
    b'=gG{p58VMXA(XI$Z-wMX^I#eqFcJhU+Ta1nK*Sz4uaBv-UuPZ(7>5O8TIIs6iMa9RE2C#mFQgMM_syzYkTRSofmJgVTo`s%3Cx=%'
    b'$7Mk(+f`hx*1fDIkt#to-'
    b'p(P`D?&V`2Yf_Yb|uI==k296FBtBc(JiOxOT!+ZsL^O5gg0hygEbGMcD8%ZVdEZ<q6?+5PrJSu?W`$)Z{YZr0Os@bm3TSgAfNohi'
    b'?c25Z+{kivT`57&=baTKo<EE2;udVaPqn~5;9sy$2@xI{o~$1XSKG+(=iW%iV2JJX!QUn_YOT>Kp0pR4KLj`{BwYyAm%xrtAwAIV'
    b'!3xinp_J{LVgp}_q=Mv`fe!gZC@U+kuY`FwZ^HL!np8%IL&%<uT!qeULwGNmGxJz)&%bf*`BNrpJ2jB@mR|$7rT0`s5J7i(#M+Nt'
    b'C2f{Uq}(DdwW(V)X5jD0<)yZJ3|0Merzh<g%l~(I+RUpMbN%eMv&+8Db|a#0+FU&JQu}Be4rp0H%{JW*lk6S?nvxWk#+z^Y#%2;I'
    b'MoG1C=s`~p2FoYJkMc8c&tpof|?yqb2@Jk+l>iq00Yf>w%<_(AN6+rh8JU0DXB)`N(b};lJ7(XJBwTR%hv;6wjtbJ)$onrnrC|A@'
    b'YT!50jA@GM$;VFPpsyElWxoS(@o^uNp9JA@yd^tI@v<cE9>x@v7&2#J_eL4v&vkW6E&=mJvtyvAa!;|xB{BZ>a3;og|C84aAlK7;'
    b'4&{uZw(w^ZF=3<1dI~1+xCGPL>}xdCG=Cm&Eco~)P38T2|jRoky$?Oj`3Ch;!pvPi)a8STfNP?5=vmB`#=w!=t7h#4lAcQY6z@hx'
    b'50o_iPwA2@Krz2Kh@j$s}i-'
    b'fphOieJRC`~ac$uL3brljzMlsGPxhdl4O*E%pINN1D(oQqcDUNzo@y6i`ZTRG<>8rFJH>&=KQ3TS*6nDN6Dhk0;?gNZP5=1x8tc8'
    b'lO85)kUd^z>tO08<*h3mn+ML=j`-'
    b'w8Xb}0QRX68#lImr0W+F)~bF~y#a0{N+c3d*ZVKsw~+8c<wh$qfgO_CC$<AC!mXkTA@jmpWl;J9plf^+#lO`=eRte)D)TBj9_mc}'
    b'JZ`6ouiJAjmB}1vlQatqUG<n{tYFT@{=2+6Ow#F0X#$rqiRKW7<|IdVSpqHG~Ql%+#fC4_>U4-'
    b'ox?)xB~ugkF#NY1UNvPT|U<|*4etl8@(AFro@s-%q++FiBm97d^`nshPG-'
    b'S0DJl=7`z{~{Bu3+bsf1h?7x8wti={j_{w_I+W|8hbFkOmFJPUaZvD&KYP_R#D6I!2+oDN6F)gz-ENn8H;-'
    b'%N9n;GG?=sK%eVR+C?0%-'
    b'9J7Smm}=E>8#2MG_hIoMke8a4N_^uOidh(vMQOyVrZKQ_LR;rUs`OhB=|fJpVEpDiQ|8~Kluox?_&AJ;QLLokR+l&)nY^XrPWMRo'
    b'C71Wb>!E`X&PUaz|*Rj?)3cSWqd-FR-'
    b'q<Tzy$cCD3HSjv*uQn5r(ik<2(+1@~480rc>C;{^61M(j9K8;f#4ViC0Sq~na9|_)kBXUp6q>d?BcF9lsl_IyonV{th4ZnU}Gep$'
    b'~Tna|)F6Ew|o9um?JAtV+`&mR#@F~&H-j`N{a=-'
    b'e11@t5+`w`_)k?pow6rtrw=6kZ+b~WV#7yxn>tf!@IOJ=Nw|F^!q^R2{M3<@hmBc8>Q1A^R^I@(2itqbUxreoR4@o7_+uy8BAHv0'
    b'CZNvO7xHJMfLmfj&7N=rC360uy?QUO$XW8=|`-DveKfdL4IEPY&r`cVOkbx8~NbuuZ^xl9xGOhO}~u_-n-IlHGJyrsE;Uhx5v6@|'
    b'V4lD81SCbb7YVu#G_=>*1eHE5Y2<PoqFQSneX1Sn;bV&XD#+ml}8-'
    b'^X__*L|UUon~id>cFpIoJS|jW%t55<$zTomQIVTCz?hMP|nSMy*VZU1q~}AKpzXJ7~ScuEDA3^uF4CqO%yC1g`Q3+v6tn-Rm>V`<'
    b'1Jtj)*_L29S{aM3a|iENTz3RRwmdoI`T`Wk-(;=pzOK4cRNA$m-~H0Oo&66C4Y$MlV$pbm@0OTAFzhlq2Q-'
    b'{>Q{zCKnuDau4%<LPUYk+)CgW@R%jtK0$I<B>KM%ghSP4#W9GPd536r`K{;n@g!b`qhMh(4Fs;dh!cj^)jY7}C2gu9rx00X*6}D#'
    b'<Yr%fl=W6|j(?#pYhv0u}$_R4R?g#l!iI86=dmeJPAPFToy2BIdm7fA$esdFVV2ArQHyajs{SHSO){OSK$H^zbigtspIo0Fo9ezD'
    b's#Pfz}nWBqF3?h0f9`<8fubfxE5f%hFG@{if-kaEB1fI@vT3ObgvJY!*XA7r8D63;D@%*=00-n0BXLgO5E%rF(r@D>221-'
    b'73Qz8LGON9Yg9;iSO`w2NSwR`-'
    b'@X%UC2A6kFrBSELwMZTxm>4yMyZNf5S<sPib4FGR2XSZiarw!iAs=o=I2BrJC8pQvea+YeZPFsfA@y*P;$xlI;vYCV4IG#_^rWEm'
    b'=BLqFgUZYorfJ<e!y{tLRm}IX<Ic!~tXc^sf4zSDu85```;^QrR5;mY?*v5bg!+&8x1T7S~2adtwI~$x{fHi1w6}u{XdVhQJKR-'
    b'U|aM%Swjh)3d)G);>J3H;1IiG8_bRQ8aIdikhm}P?jwCwbY8~lEI$?uB|m$^+IWSBmFVPW2&vnHKYS_b%L5&-'
    b'UClPhoITCz0~6!yn%288Xb-djdH;U8#52-?HARECbYvEj!7pS5{A`&cR#0Pw(9-'
    b'ySbtH9Y#}NFH>GZ8+tsBBqGM5~h9N(5|almT(ErDK}4JUhP<><9eH2?A!CL^8JXI^rsEbJ~|PM(8op~DDP-'
    b'8k;o2JH^aBN4Z)m!_B90iJK`UJ)7wY_;sMFT+5kQ5qS-{SWOgPHMgjHf>69?=^dmp%N@(z%GE^_*^X-'
    b'n2u4{G?*4FJ%I$SExqhfG1je`(jad$BNA+^g6j}Us??`Z~s1--W(7+UZ`LW&22NW7w4bD98db9v`$?+wSrk=nAtAXywoV1r4&M`Q'
    b'v0WLHQ>)Yw%H*4RuANB-B*51Z{Jt3FEy4ej6ulf~n5gKwc5-'
    b'|EpCfD&_W&HK$(DG@~*?#!0Y{ZFLeJ*!tzf;EzJ2V2csq@44|eM~-'
    b'LqSga#u!#>K#D!#5S#=0Z^mFWdFzh!~N(wyBsZ2scjHms{eCuFBK91UMEdjM|lI?vg6au>fgqG2GErc<T9Bg)QvV!WqLsLA)+ovs'
    b'|RQb94_J$rl(7IQx$8ne-'
    b'#7dfT`?!yTQ^34f*?ZnD<9D7u|H%ouuz+h`$W(%RE7?xfwrVi(Y}#|in$>7#`0&73Y>b#aEW{T61gf`MoiIB*1y1+09Vw7CawuT;'
    b'75ALZEpQV~r}~}Ihhbv_-vuW0^>Owg+}h4(A+a3DvCSS3FYU;|OS0;)_Uza%45>Z6!Jj&-'
    b'BV@bn<~P86lz)>j2tK5D2SAj5p4bNJ77MueluRh~OwC*>-iM`yH$!bMq`!q|=f`tdKPv8-'
    b'=0(J1MbceO`#urnwz^E4V1!&aJuFT(X=FL3RUjiZCt-OU_;t4PX`l3&EmN3wJv^+-'
    b'X|_XWt1aic5O=NfS19x0MN8|pC9!D>;%0q3rjz&Fsh+qqJf?(YD|qwI+YOItP&1$d+SjVZ0PrTnA51$DuhJU%;~A3ewy|@DG4>PK'
    b'_nv70bknZlyLC(ZSv8m^&qoa7!B#$Utyab$Xv@bvdW%!hG3!wO=?O&4M;m#JRH3$}BHGZHfNfJMv!ZWX#oXtU*mCc0tr&v^Ly_Rn'
    b'PUs9T^xy#z3fkrjtZGS0il%Uw02b`VoC%lkIliELyHi3IPSYU5HWlI%78(yY4rW9|hY`SAA_xkr;Ai+mKx5skXh2e4-'
    b'*&kAs77dA&pgZ9!Gq%xh=Ap}fH%*9E}n6VVg0sm2z-_|Esk)qOcnMs-jjX%`%Oof#Pb;w)|0UJWSH=?*mjpHI=k;Sc_9x|HDZFLo'
    b'uKr4J?h!R30W)Sz=WzzVu)zzI#;tV0pJQ?LNV@yc$ug9P+ci;?}@#=$A=LeR0Vl^&a#wf4uX`2mG-'
    b'i#cn$=p*sFMHNS5Y46C@5>z`hwTb`T{%1yD3+Oa&eJw0rVgWp&KiCNf!ISL`nsMlj39zlBY{Q;qBe^_)ZBfGCD;#W3O`VAeK#vY-'
    b'l0Wfoz;m?Qh)LEdS5S?_fJWV`;4WZ6e8%|4r=2B|{2n7n6GO30dXS+jj1%nV#6;oB6%W&`Lz%(Op+p<vy=PWxQmU^w~ZMghY)vE<'
    b'9Ncnbl;;Y^<n6@fn-Ac1#fD7H3O_+-zl_uMbsHp}sr%4!W~A`IAhf5u>T4<nqu21ASOzS}-0#^dE6a>@n-`{U%-Z)%{wy5uMBR3-'
    b'ZHuu#YN#n=(9Xsl)885p9Mtz`o`6zP2q=(g26Sn8}Fw-~yg+*AlDkOlUXyCbN;PYYTd4Z-'
    b'5t!S_IYulU@lc^rc3H&5@abo+>jcI`6Y)v%mlH@liW;c)m00TwHi3uCtS4YqY1Y5*jj1ovfEy%%o?L$#Q*O-'
    b'!(qx=%;!9Trx@wGZ?i>vfuLZ{Aw=>h2Df_-wPDe_KR{I36rMrx!j}KxTU@dAA1C;3?CDE#BRwHq~@i%koii`+QHY$7}?`i6*?J-'
    b'P-M*gu)mgvll?OlPCzhmTvMz(UCg?bi%pDl(xOib&-'
    b')1QDZCV2;&9x+lkKvSIOj@6B!i3bG|Xm2(XEVbwf{a@cnI7&PVhbauu!0vcHxv2`Ioj@-r-'
    b'ez?Cc8otw4H#ct{#fQKKBs<JiFJH)TfMc`?0C*(jIHvc%y7xMDRLqZ5a;Om=n>wt^YpJx5=kLB30cRqu4=ur7uj-'
    b'm|YQHg2R(&7~9G`BIbfrQ=!b8NW$dA3HBza#eX+vVV++j)D**<G#&**#(T>D?YpJ5rg#%K$3XM|uiS*h%=3V*pBo2#@y^k|+}GME'
    b'$5sf&(CVcq{1$f>Bt|T^l^b#=`^O3Q@8<+6DWl^S$$Zih3?B77c7clu2<s@H|t%6FTe>&{w>ku<1d3AEDb2fH-DOzz=MVFb{7N5}'
    b'{74uw=sItK*PYn}CL%zz_5}cqLJ@SaJXXw6OV2M!WF=hg(Gx#jmHxJs-'
    b'{mj@cx{;9Q$F#4xO+cq~v{N+&J=3hM=mY{j2>+cwoOSsq$$KY;5L))60-b+<&!)92lFkE<7`2lC@B-'
    b'?L#pwsKB{VYWA$Hz^R@)Xk5FCYj0U^$UbFHDDj=aqM8Nhv#K)W@bL)&TxUzO0)JFGMgQ)-'
    b'U<5}2BB(Zw1`*padwk*$7wHUgG~RJQG7;BKG9QO^>)q``55+k%7X1v9ISb(&ers1*X~Sc%!f(U>_iAcVzFxvJAc2fiNOQ9HraE+X'
    b'fy5c42zdJyd!fGf;p8o?(|?8bcPmKV3^G=-0!*HSACPb0CIlB0n3>OFFYer^3MG%4)f!49e#IITkku7*i4<K&Qc}3qqc9P($H-'
    b'02<1EM&8cT&#WU?aJQ`jW{0%fsgB*f_fb<&A$Cq|}ORsU3UL7KDe$E*kA?>BlBnG0JY+x~;OST#vxM`ogZrf(q4yc^3U+!mRZqia'
    b'`vQ(BWc@nh1sXITCdtLWoxJ)+8ZI8p<&R^v%ehV#6(AGZo_hr{7f)Esz_uMPo&52hmH?RlnI$Z6v8AJB~DA*SDx6%2?yMs!|5hq@'
    b'E&yg^F9vBTcc-`Z<-'
    b'LVtJ&Zo_q7sR(%sD^{JH&sPO4$P)>jl^~*)^j*lA|XA`dNs@#K51xyR~$Asv4O#HXo5DKdUH%{%><KwGW08W`P}tPR6KMu+ym&e3'
    b'q*2W^u6qWSx&D2932(kuKy0H7tOuu@p_n09@K;Pw&>h@5JX1v+WPKKryK&_?V$HopgV8t2HTMH?aOFI96k})_>&TEFP;!dcT`(i#'
    b'At5Kl`O(wqY_M)O?lfdeFR${(d&S55bDf>M7jeQvtVhr9XcV5ID{8Er_DP$WGpzrdfA#7b%pRc)?4(RY@+#uWox#R&TSp6i7I0tg'
    b'#{mz=Czc=V-'
    b'PPY?TYM_@HYYCxlO|Q5q1zh9_l`K#wAKJLxuO@#hRBpBSEqF1p7r7|M8wBd_2enG_xWaOSNb24IeYv09&<6m_V8Rg5>qtoju@rMr'
    b'V%Z)Ee88ym(`353;Tv!^%^sRSC99%7lZOfhcK#;^C>z1Gi8H31zES>~{joS5<%+IeGI%&4x*iU$c?2JwctL92RhCnjo~Rg>L@M-'
    b'OwubBPxLZTkElHeuDNZ*P2LjbZNHrbn0H`IUEA?s{~YNVRaC5YmnvnoT8vG#>W{i5i54y%V}C{y^9s`@fl(b_2NZv+nvD<`7l3{J'
    b'u48FpUER^;Cow!$6emwTi@QF*%ZOmGC#z!A8Qk5Vb2B_ZBOE0wlCauSQHz--6?PwNQ`!5hf7=PF+DMHbn6um>4e#9oE=|8G<Jt}0'
    b'j31<WWrZ|%OX%n!-'
    b'S=$i|vgDcGxk_4hx)mgjFQFveUbD&x<gLDwK5#Rss086JxM#F3iD<AUg%_%ifL_7o!CoLgfre1cKU6Wqq0o2DL>=&f{eiXR*3C*p'
    b'kePSlcx{7wItVCJM$7bRRgvR^jz54?0b?n~u4EEBTM?$ZS9&Lx|aKD|sxoGwsoX3q+)2qgYqxhV7f@yHCqLpH|_&OAG~O0~Og2y1'
    b'8Puin>4a<8*qS$1V1{?~Ya$h8+LH7teUUDV05|7w$GKh~=Z!dip2Uc$h$j0YSE&e(5uNn2CrX7@BcBpq*%xk3IaO0Q1eo(nr^$sQ'
    b'd#*hEJWvOnB354=-8HfHJ)8Qvqvojx`k2T}+<+Egxj!#K*_;e35fF%W0NwYxDAY-Li(~;^%at5}MIL27^fC5oWRjfrdQz{CCLBM@'
    b'=@IXwpD%f~@tdDMh|V$_2{Z=7XSE(H?}#aXAkhZdUGLFGdt4Hvcw*x~zd4Vc=@frUQj2dS+{3ZCK!$RSZuZ8=h~|0LTyuWZOQbye'
    b'Dn5wrS(%VbNVMv7~JbH(&lrw;w8i04a^)D&eC^#o|ifba#O2w~^tiCL3*8V@mAkE2N;n=9i2R*EA2J5&R@XK-W=XLB-hV6631-'
    b'+VR!lUezS1lueDViU``^!N~)99BGx2RkTK#nzqezVXF2CfMH^tIemOtTd!pw^XAhyj2rOD_>1?n-'
    b'W;Jlnk2!jOdv6NoLZ&o(UYM#)9=U~FT_i!*o%cPotG!JSO$GMb%&3;M)Q^Ig$9yd*J6Q}O;^KP1O3%m`ZwucADu#e)hH_$t448^C'
    b'nwEv@o6V1Vy#7iL6&0^DXb#;C-$QBP_-{))A=TN#%S~X+cTxIo^F=YBV4q)bqM*M$GL6tIu9d?gOr^w+*@P;VDleKkH2*c^ikf{-'
    b'+HP4D?jF=odVxL0fH^2y{tnr#l!9;pw;P_i0z#>k{Apk_~D&Sj^SgDW#f?d5FDgQp<Rvz>#)9T2gYRWw{>;Ra+2u5oXK1AwZ3kL9'
    b'2}SJ-tL#s#*i|9iTjzsWlpEH8hl1Oy!uNBPUw5{Vj&}u5jO)4&dZv>`P-'
    b'c3qa{|FTe4G?a?jWcIMuPUbJ@$q!a4wx7}!ze=6YV)<8Xp(G~c<!Ul5(cO#j`?zwu5aLeuQ9pdOR}IylyzR1lT13k%L)f^f+)gZJ'
    b'1uz`E^E<#;N@>Ncr0^~jFfgcY6*S%C@HqYtyN9A4E~^(&r)>o=#(wl#{TWcvbuv8Y46!sG`-'
    b'_M!lWV7(?VkGOB`f{yTTEehT*6?jH4K`+sX<`X!QZJR^0EG6{#Ds9VFcL6+MHv!-_qAT*9yVSo8caFd4R)zB=ShMZ?P%7-'
    b'HvzczkkXC0E4`tUmGX_4}Z7$(7tFitbJF~D)`PV%)!0WOm5Q$<96ucG%(md`Do_HEvi&GOjiuxI`R=*w5j^%k;Y!SjtwyDBCt<V|'
    b'7aNBZ4b#UM7=}CVQfCyI}KCy`=i~r6Ms#v;3!S;r=E~RbAINOIci4IxD^Ylw3kRj(rA*hdFibz=X<NB$OF5MvR*qY-pE|4UYr>`8'
    b'0)-zV8*u;wsM2JPigPjtJ6cpAGPQ+PyyD7K30+8#m4>R?jOzV5w)6_ndtj>9OEe<8!!=$FeZj{A&!N}kCap6-'
    b'6ai0#UFHf6PTb^aF0l-M>&uv1E^x#91JZ;LG*gDgmAu;=$-(C<vS2}piMg-'
    b'?x5GHtmC3nTkF7#Sh5ujV!(P8GZ91{TnrkV`ce;Xdn+a7`w`-'
    b'WpVz}5i`fGUq*f2(9uXgH~vp(ZiK%}$&a7C3nLm$V(uU7f4m(9L41ZthoBU>>1+CC^{!0*U3fnH<XNbe8T#Y`a%^&u=DCXy`4D=e'
    b'aePs&gaSZzmnG7=?GS@6Q>9&yj+2+JQq9^zYa_TZv-'
    b'C85WE~U2xsBpK{UA`!n3wQ8oee7zoC;wvEh3^H}hqkzZ%@+8}z~_3@;BL<F7!WmsHOuWTK|Y6b-'
    b'L#<iSM4XjtEk;zxTK3e@mdJtyWWLvKFHWGM=bibXW6rxk70v`BuHWwFCEnvsmr!yXs^G@IM;*V$&ufPI4R)u4uPHyCZ^8r^QkY>W'
    b'k!tgFEx_fdckAVk?3%lg`9xmAG_c3kf>><a`js>h@6$W(084<R*>7K_Y9t8Yyv{V5F!Nn`ZZ=17xMU&uyJ();Gd_6q2a=;k0Z&mA'
    b'o0h-'
    b'|v8DDNgG25{!hV9SVuH*PEiT$RqyN2q3XRrpC@P!9qzTfGzF(29z66IVOaIV>~G>2gqUeBf+cKuGn;%C!s_ojicPeF7u?{=9rZ3V'
    b'OA&v+8{c{*><nu1`tK;N^N3-'
    b'Y=qE(~=XgpEw3v#2+jhUf%Mb3&cE*(`6ceY#W6n`5UhYn!c_`?!*Sd0BXQet5tGt9%0X{Z!%i+l*l6&N;}!b|Hbci<h@dV?0TtZ&'
    b'%zPbMj2fTg+96Fj#xS(dywu%mxQ28yNM@@36h<Wjkd;pQWYm+_Jd=kToLY<diVNg?C9r$mi^6dsqO@OmOCMo^7@vl!@8<w%2F<om'
    b'&>6a;6tU#|PHkphzBStt3ymVb}`-XG{V)gBck>7?A<C2Rr?pBQ%3>xh-RauI~T=mnok_np{kvK@~x^_>KviPhh8cC|G1JzbE@3xN'
    b'hH_`-2;v*-V!6VUXi#F)Cmk=_!aip6q8wiSXW#B_iSP*t{DP4p3!mK3gMrjRjRYTCPwlyPBTQYxb*qDO^24-'
    b'|;jbsDzN;rwJWv1=Uzp8(Ra&ER?hyPG-GQ&7R&k5gmg7wj7XB6U3$O_Ks+Ws;)qc+o{`AIgH6$421`9gV3q}%mqwPE&excU18jNZ'
    b'hb49;q9o0FuZrMC)F<hOxRlkdW4RIQo%@1bDj>TA;{cL6Q-'
    b'?7ipkjl_1pH6r;Sf1OeW!&cJj7qpmhe2);4)^lQ7tMmbfOzqO;)Bp+T-'
    b'ed0lhEM5YAQe4)VJ^Ra9Qb`9Y<p%~fQ_39KCj4tu%IpP_Rh4q|^eq47~z2+N9utehI)w8zJ)@UtyU6TpGyn+Qv022`nv$E;M@zf;'
    b'0jKT`y=-EE+TGzDOTJ$WF$AO<(L2%jvZdx|x;l9I(3D6E6-s89HzZjRDMpm$4{-'
    b'J_7&IgB6vIc_~bE1!ig#i*mTM<SS79{;D{cWT3QDpe4pXfIwY9A4kkH&+1lv4Rs$;dZZWFJY^k2ajIu6CCvz!<Bru;Ofbmf%<!Fm'
    b'%wEIArTJ2a{!w*H}Zn=W6XOm>b1ZlzTa#(dJb*A;p`D_Vf|KrVp=t9n*9UN6N(~S=vPZGo5ei%@FEw-'
    b'==jVxnlw;kXM(n+{@xDi)1U;Q>{?P9fGYB9l+O*?vejH&o?yZw-'
    b'=WYd4q{8`5w{{sWv>XAdIE^SjlN<EMPWB+aheH_9o7laRim}PHZ@k4N(x<_N0F}e($o_R2kIm&)i|jsb=#`;04If^>Iq2og$u6JQ'
    b'-m)qtzhZ>LN9#h5dY3b&Dzly{~wA8NMAv1l>XHw2!ZHzBvZ!&6a);%xQxrSY&;=AUJ$NVOF2vV8(@6=SB3l<^fwGMi8sdcX+_zxo'
    b'okkzuDRrWx(bmNHd8EWpx$?vT`@uN<yEeVaj~HfTZ@C{~g8#jy$1pUJkuFkK=e+Sw@>47{JT2T`%9fZ8UTf?eC{!CW8E5&O{GSg%'
    b'+>6@HGGiX=ZVpjj51}XCby-_u<(qVFMBaoJonT^lL}?9U2OQ8j#cjvNCY3#zyjKD_cM>;fjDW;fH7F#UqHC?U#GPw}^MYJ$fxPGN'
    b's9u=go&j-~b+8z8-Eo`)7+&3({I9mc^6|<lU~S?-'
    b'(nI>RFGCxkg)o&O=$umdcQvN@<QGA+B7{fzaUz?|>FN>(kaVZwv<nA|~uGk!Ui{uFapca~(k)Vm|FX1VRvuBisw)b|(W!b-'
    b'wAQAC-)JREG6YPMb6;I+k_X)@9j!;kfZ5rzl5&syiOR)?-c%N8y-'
    b'fcZV|U1PERJxRjbWcu3r!*<m?(ly7Wd*)py@QzI{b#pJFD>{WJc*Uc_fC+C&)F{9`XVM2|f2-sHP-'
    b'Q1Ul5u$F<`ksTi#1Z{w4FHrrSJ*(>3kz7^ULAh~qAV4N@3dU7bZbASEpd%oPa2a)ZnK?4K^84W+o}*Os$<0LY4SFbn5VLqKiJTK_'
    b'?)tA+l^0{M{U=06m9BFo0tX^ps(a@!Zq=#-+P89i4HTe9%|Sq;u-'
    b'w3tcXR~TlKa!{M<?*M~r09*@9l)^)OZAr2@gR2{H#8f6Rs4kBh)%OK#{B+6S_gY;TU6AK<^IwTO&P1lGcSeCj}L7AJxbPpXL)-'
    b'lrk>=aMW18$jBE>Y3d=ATcvtwL{E$@aXAZa%hvIMZ@86WD}>e6OOR2=*(VoUB}ZQ6N1jN5N2lPKls#yo{jl!pM5nx5}WwXrtg%4D'
    b'XakZlmNmarYGdh2Ge{#esnvvtaQvqne^Lf8aFw@fXY;GhS$byqC+_sl;pSvyGo?pq2X>0gXma=Pwm+s5Ou#J+D&uA6o?}H-'
    b'?&G=8XINTdS^_qQ)e$XAbMF)_tbpDg3{Cc=$CCdbne<4X)HF0S*T<95d;+f2zWGHt$DIPQKHxBIfU#D*pPI+qYS*pn5I4A(y1RO+'
    b';$NSlj*~UTXZH}t`mYncdSyf^?WDp&T!VZ)o*t|sU=Oeo@YUBGo1PbAk@*#4xSy7d*C27UE3+qxUElfb%(=!+{Yx|)wbK_QO!~d+'
    b'Xy&Mj1gwCtuC5amK5Q70*HdRc#U#85c=(Z^O5vu-hd2`h`bLNCqM6l=iM^SWH0~j=w~xWS@#I~1A;(hJ}$}K+cgfj_F%tRwv-'
    b'%Y)J9#HQ5n!Jc+&0RApy=?$wU2oSow7t>CKt_`1sK2=I{n0LNvYaylg?25lu$6UA!$~op@hSFZ3(G&r`zt;27&SQ>w5zJM_ZyZ19'
    b'6vWmk;;wDU3T>Y15+Sh#O3#4{bG!oa7)tXqBawi@vo*GAu%NR*}(XgGPt#h|*j^s#Cfo_ToPUhV68TYoV{z<Yf=5#giY+hEtkq7s'
    b'o9_a5G5;*rNQ0L{}q7PP8BZx&~IwG7+Gx9u@`9pmMG(-'
    b'W;_A520*MjBXlb2$4P^}}mnzr^H@$u3M0(?k6c8tZg=alAk7Q2x=8{71y(qozLR^>nVS%ZsWx96HjhYc$NM9i_A^FaHeJ$b^a=9U'
    b'dO=9|x($-+P9mcy|Sd-mnqkK$3y*My2Fvd89-'
    b'zZHeFRvE0}8u5fPNc7E;QsDIm#Iam+6fZ49$%oK##L9m1rjN%<QvGr*YFuUD0b}axJs^Z-#us6-'
    b'q!;t%qvIMVdVX{tx1Z<<nMn|_LiP!ecW~bH(^KS%<@%9yncHFoUdc8UAdGby+bVk^v;k09us)O0;hm%MXMhr-tJZq><h!|hjKwD0'
    b'KIj733bx<4U1-@*Dh%r~E#}}vRc=URhR2-*`Rm0Qb@pT4PEjuFDylCfL;1~zg7zZoZW3uKdRR>-'
    b'Mg;w2Or^4`H2s~MQua1#yfw1P7aMaXp=2|Zp9<Rc7KRxMTB$w&t&oKuemf@<~3uHp!{F7x^U$quz(ZcnR*~6U95S$?ToYIvIX}V2'
    b'UcE&8i>S^}v5@FIJ2RivxchgdmqC#)hdk}1G2fZDSXd5~F(lWPan!F6->M3B-'
    b'gk{Vg^852KH$>0zW~ZIZ5g3`zMS2@AEnb}VQSicOFGo9KyD0wWEP~ffZxQP7+|UNCh!!ZCb!Hjju)RY7+{!Z_{#?OvCsziCOH4L='
    b'YBr5H+Hdi4ZU*Y%C?jjYXK{Y%4T7^y&8F4yscV4!U-p^+QLQQ9!BMmOy*#-c1LM^7dwW)Dsk-O$?9S8h+4QDjtqz3ds16T9-'
    b'dYYKN{=_k<TUO!&-'
    b'ilOV2bvka<&82oW!LQMT}KhpLgIx<(Uq{2i^~0mTyxIzAB6O<|=1P?GrkwJNpUC+Bi!yy~9#L+p6(Tw|x+^EhhnHU>5}Al?ZCTC2'
    b'D90Z{hf2qpi912=jwi!ujf97lEv70VzTW;SA?KoXZQ@v+dOWlXoy5v8}W3IRId2vvxmPefssPpRivAD1kUd8$0rA5~G+a<N^y<G`'
    b'#KloyrIaCI%pvo>0dtPUj4RCU+{^(=yLFFWcbS>WuB$(`KgD#s0)89u=Z%K0Eu3oHDBbI%+4%Y~{s`L*9<suE`;!HsU$<Wga`5x_'
    b'<%;Fo_TV>|xk@*)5EB+8aVs97V-SduoPPZac|h6pq2*eR#<3;r!1M6Gt@<s8M$eH_8vNfxRFAS&-_m$n3GL=Y}I#0GS}J0O6W-'
    b'oc-IuQ6JgOZ~}qdED#^gn1r5~0PT^V6gEl>DpKVl;6U%44UBWfr}^u3y~_7KD@1tO&|_}k7T2rTp|drLcNeGGl_#v52jNQ`x7g0w'
    b'JXnpM2)$?NmW9I5Lx;v*4#zzUyOgv68}3h#%o7+)%KX2>k$4bDv_QS)E9X6jzK0E)`enW0(`n*f!vS7lFRQ~E>NrDe&~62O-'
    b'KTTI9lRQT(a$=cE`prX8^60HwPpCHVFHoBw6<VM(aGxDsLgTNyAS&eW%lA*wuOv@7*rDltfS)*h}sR(c<PegZ>6WpVzvQxAJP1)?'
    b'yPuEoZ@>#mXD`>cR)kksd>GOE?qc#w%PV`qUB&PRE;?n&OzPC6Hv_N)3tn@f8$i1WiEVo<j+KkE|#i4B%+$(a5`(5$F$#p2w>|0E'
    b'bDlhMZecvD2r{&Ay_kj9;FecT|jW|8Bf5lc|m~CO9^%qEJ3X{>}CZC4ezbTN3!fTNp&9}NvxgCbeR<8)q})owhJN@E(J{WR_l{Xl'
    b'oq?{i8d1EeVQ0-'
    b'_NdS#1Q|lYX%{HlB$y1+yj6%7FNVoona6{Xi9N|8=KU=ds3660wBku|M>;$6H|6jQX0r~#5v+vy_)o8pE&g>!L0BDcC*qev#vEs#'
    b'CXMh3#p$*gPT4N;%SNbROk&wRh?;hCoX~gMsg60uO9dAGb=wbsMfT1S`q>kE$rcM9-'
    b'5Yo?#=}l?aMQ4FIPnZ=iEqW<gBO$V;TjG1WHktt&`nfRN%rrEvw5?W`f1%Tu;vtDINuQ~k?eTSM34Klz!)yj9l1RmPh*>cgH?hhV'
    b'2CiZV<3O=@^*#gCpw7vIZ=ES3=AXK=O>!RoRL#G+GZiaz!wq=M~qMQ0t#D-'
    b'JF|(y0L!7z&v(}Gj`rXhsXk4FV59ah&6Y4jhX(+K42$ELWpdfW?%H>7*eiqqvHx}`4+w#3Ln>rmvB7DDRoQ)-O+L-'
    b'pO8SCi!m{py?|2zrJ=yLK@p$hwpVk=}!%!A@#5{eal%1$>NL{-JBq>iL6ybC8>-'
    b'X)HF7vxzpDK;WQk@kU`_;|AM*2IeVLFtuLLqPy=(^*6h%)do419W1ZWD#K7nvvK;mL?Hzd4Tnv^1*di)+PUmMJzZl}wIoU4DGJpM'
    b'wz=?|i#dLOc7ixB7FGUcAl<G8y}1@bk%mJ*?b*j-iqMm-j9Bkj0_D8~zP1{%9PLNfx`qtE#OxVI+r5o9ykBhdD63!-'
    b'7Ud$GJGw`RPHI=8?S%M$ElErJAx1oId($PC4uFhgqx=0M5O1$=x(55R+$eNCaQJPSa#<HvI+|hufN)cqF;mWhIJ~5rcC$d#Kik!*'
    b'SYjjEt$IL=T51VLa*jSP1ReLPceSocMHbAG<rvy0`DwiHvTgTH~}=gv>!QE=zhGyagRZvwd8I`ccWqH#dn;cj*XN8u2$Gxp#d?Z@'
    b'kMn*|=yh@DnWv)22h;JOZ(NJ2&J0tsY(GiaVl{XZ1q#@YcooUY=iPtPXj9+IYQK`*ugx?>cM%fyMLrZ?*bugC%DWT`k#Gkg(vcKs'
    b'<Pw>w*W$)jGRXhs|%nMX(>G-RrN1r{ujAFF|~=xWpc8#W9cDrc37rnN58-'
    b'@feQ>aVYN`RaM(gM8_+HB1*G+TL!1XYzX?z`Eo1T_Qe+0wuLh7K+3mNwJAHL?Ld0IY>V(@fkg-'
    b'p1R@%;R~!%{Pg(O5(wf;+yv~)n%j2CJ_!VH4JN%AL0b@2mle67590S;&G=++)+O`YkrESBNys@9pb^498&48QJtiDyg4wAU<XX2j'
    b'qlwP1%Lg?f~s9qxU1aoF0L4tkf^KNq@@9EeXyJ~%VMD|&R-8Yba*`dK1Ugvyn9ec6uC-K;%2UJ+u)>}E0?Q#%-'
    b'eRDVBU(?y=Ta);=#=AoK@=X+k!|dXjzbybK0bqcFO=z%NfY%I;RkIP<=_GoKLN<W+@r<R95@)_@bpB1&>IDl%g;kj1CIVq*tfiIA'
    b'Sgy^wolUx|=_f+gs{~bcG@ZME#r-{8K({UX)Y<9AqJ~RGh2F>GL9hx#UJ4tK)Z(<m;x)%<5#;R*^<Dv9owyX&{WP-'
    b'(fLK3^MWZk>7-?9b7SIPbL81{3`@P*s+ZbA<aQAPEdz?JSk3&rOc3b`j%f9+-$OWFMHE%-g#RbBkI<Nc5d~=MDtv-'
    b'+Zjt6n<x#_?*LCFYPUXuTUO2agH_%WM?uG>yg-AB*R9Rj)&GU0~5y${C`oeOk5!$o09)sdR(nJr|$K1DjlaGDVeL$CE20jVA_ynf'
    b'uFTtR#~`Q-'
    b'+L*bE@A*<SCtQyfwXUO2U<c({Qa7)*28P=)=Rc;2^+;v*1+juT$D)oExaXfbALLg!U%u*))|C2W<^Od7IJG=VcTd%O<lN&R>r2Nq'
    b've1;_I>9Pwy(pUXmxJxz0psE?7o=5P+Lr6Q+E1DRD&X0P%mXXSh(5_wdFS;AzYVbjB_Hf%!64^=oVFwCm*n1gr7kBm>t>@hGfoWC'
    b'v2KDrNgD&4Vntn)<Nbo=;$g(cfm7w&pG?8A)JtRdO8__Qhs*sw+6Z!+3P*XkdkUuW5Yw|4ok5VG2M=RKoC9GZ#$*vD`V#o>ITW&V'
    b'mu^0%$5+242E;wo;F8TF3XAYMi<%bZGEVmmA>vU>Rr_N%?mr`Y^(s>)q~`f_~Tsc4ok!g(L}KTYXOU#+$@=+<`6XZYE6cD6l@Qbf'
    b')>Qe#Ma*v9+gs^e}6=bjm-P(}A@?L+V0&^g=`&qA_XlaM03X2}0?CfuPN=l<K@?*^8pO<wWJJRg4|LfHwM?}v@Yks=hpQ-'
    b'*Ox0IjOGdq-@H`Cbt00oAurp~)1m>al_Kb*+9qwRR253yu&wgIzNC#pk5SdIszygg@EiWh4~^;F7J4;ve7&mI^mB497xv-'
    b'}Ues2c<Ew?`UaOg-xuP^z>JHoKTnxWSS1D1FpAW_enlCLNpK0GjRc#*3DJ+@yzH(C(ioT!F+@_p8CQ-Pmge+mh7*+;}C%5oX&^YM'
    b'4hyW!H%r~8?FH?oqNT8@I-HWNgiT`LgW#oJ#w-w*RZ>VN0AVS!?rWP7s7%lRBgrqSq@f(t{ARw@y3aIrb(LE7R-'
    b'*ZBMEBVHXyg1KW&53;-jaJY457+2`dyV%g*k%CUK1j($wx@J^^H6%FjI<<jX5|2Pc}kVE33yhgsp7GJ5&aZ-abR3A;nX!=W4zbUM'
    b'Jp9@mDx&@RWlcCYS^aS+Nd2G};%bDaDD;^NIOX33h39?ivDAqy0Q+-'
    b'@$)ye*QvS|jk^*832Lz0R_72d3lv_1{9v?F7t&$b1$^lC*#*0;zC@x)A~HWp8H3AKlOF`L<_S?7sa}-'
    b'%B^|v+5O{c0z3S(r!4$kRQPcO?H*25x*T&;Dv+iHo=09r^MmovB2s6=O)Kvcb2wGiS{#`gt!+1E(@J)ou##b|I@B_V6QzMZLk*ab'
    b'YXbV#L<dH&W`GZ8o{qZuu`hR5?P3B;JK{2yIIGU60(RLM>w@_t1G^`yW5_n9Qf~Pd&`8Wcl#ZgfbRIvXIy<K{4uYn%!D}DCHjICf'
    b'Jtx1;OlhW<07UI0QNOgah$-'
    b'iPM6i$+hme+nnJrh03HA&+BfZSs72nMnfu5smu+4i8(nNEjyq$1h&P^t%}cc<BF4lUmuY+U_s1*G6LfrYuXzNMOK)4xq&aR8GeGK'
    b'~5hfS2<viKt<nDP~w{`HVqgR}N24=op4m{vlj!Cn6Ylzpue<2dI+wPXO-_l_&n}+1p)C+#*#>{``PyMZ<4hL6z$hU3k5-'
    b'*=4WAGJ85_Lg#ACBw|Q#K*648)hyxwaSO^-U`B_-'
    b'=%wF3{J*@qEom0CC2{Voz~6sM}>98gzqgi=n5<N*UH_9&f49C@2s6M%tLyKIkLc2Z}w_zFCs79?$1tp?iBc2OFbNn413e_Der(!-'
    b'Yymgc4Y`ZH}RjID98sU<M)c$LsWzWP<?{EIrpVbppq~ew!8&PFl6ZVp$K#OV7j6fHN$mqnQYosa6hP^6dMl-gE{#%b?faep>|naS'
    b'@|EA*-0&bII?79~Q)xr_YiW-M$l-'
    b'z|!3^tFRsGalIEy_|oOz4R+DK&GTXjZJqGkoIE$*Ho55bfwK??I%WD|f%9H_hxcic75WWImv!9J&c=3OD~{nsfL<n`wa#ju@fih8'
    b'>{j7fDz1&rk0-r<bIJcv8{}f|Hz*N%QEdK-'
    b'3yAWI?S+X{@2TJoY!MJ_DWBbDkIk1y6E@!KijPupiPU#`QgUKCJ?vp4Fw|(G`8n)tYb60R(4kFZEKB0fXUsVdRo^?`v}?9|P*Gq&'
    b'{2&*_^|;JfXgtLh^D`WdxPbd%^eoFWp!;yr-_J{(<9gcOt!I3hP1eoa-'
    b'?k(u%YNEVtt|m`S?<|F@<y&bZPZ6Q!>=qWX{3kKp@(m$v6RNEoFg}fp+|7kkqnSV0zHq{!5+9namd4Ob;Ui0V{Za+gukzWmAXqak'
    b'+#ok5kHZwVE#=+#NI+29csGvp?FyD{nX`^0?P?$S+;V+H;BL}#GV3ieISyCy~gbw4>=WoL-g$bu$lh-W_36h^M+O&1NLJ1RI~LF8'
    b'wf^QcG{jZQue6`jaCT|7)=12{I7)9!?D|Wny$nzMaK;6W!8UmU{g-R0S8vU%@kQj;zTAST+(+FpT2H9JS^J+nu6V27GD;G!N_-xK'
    b'BuUb+dVG~0xw9`au18z9dv2N=(ky9#ZLCgq3jlC4HsADkZgx_DoP-'
    b'p6}>quZhcZDZcCPK7)5o`^S2k0k)PTgi9w%W45btgpG`a5c5m~(?CC*oL;8}f{dJ9C{LUh3FTHlMnO#+QAiUBqh&2(Ofx3jTG|$|'
    b'Ix8Fj6O$ACa&WCbIettXK!$)qLf;m>NuwVQ)T2qGd!TAoePzee5F%r(A?AX{xAC_5_6o05dhqEVp=?6up1t_KjA=C+!*Mhm4oxH6'
    b'y+bQA0Pt6d#%wkE4w10MrRSZk5YF&HtK+}GVHP|i)T05WHb<k02mw5fd)PD&EJ2GDMgIcct)7-'
    b'fo*=++s)G;^^7x4ze0SO=@m(%q*bS>oo_#x?UwYrxNV5WO8(_J?RR#;W%hNG#0&F=E>@q+4wB)-'
    b'0_nu6gCj;vx<0B||H1e%Zw0CO&WXrq~jUR5mHEevgaKJ)T3^as&iS?+PBJzQs&-'
    b'(MeSQUMX2_qf&Q54~7ein%Huy2^9hVD7#hpP%F%)v=u~1iEYa!pHpm&!2xhf4<Z<BfMl{5zy_{mn`u)(Y_RaX^FAGlmy~6VA(t<5'
    b'D?%2Cem2g>ou|X=!EIK+1fy>Ua!+JnwSgd;)FB<<Q#~!NtIQ$Q;W)}^Mc{9=dBmHp!?^QaRse9a=%z-9(vbDKO!dH?gr+VjDc#-'
    b'+&G9<=Q9qPTG8EPer)Xf)nLOnf#)MZlMM{Y<s4y6Z8dhSMS)Eguu>x->26_nk<-'
    b'NUGRU1Q=FP)&aP6(Y^a)Sj?3i=fQ^zBioum>8Kvt$~s-'
    b'6c3N3X$EdEmo8nt=?xg5QCdT?g4&HL=TfW(~Z0Z^VSoXSZ~NGFq^k?bcp60{*#AAsr!!`1)-Fmx$tk1H;~Ir>|i*N2d$x*3+-Y-'
    b'lmcJ*h$WS6J8%KX!eq?eyn_yY{-bJBL>nrv49=VChB(@8~n)<v>-PuN)Z9JnZI-$w{uY?@<sjDz7K12M>00a@Govf-KXAVEde+(t'
    b'PI5MI1@L`r>)NYTATiMGqB`uxnd_Iw~Gw7Zje3k3jEl`76frZ2}mwiPn1sr0D+Y-'
    b'UYqIVXWft&9#IU{u6umKLT&7JHTa0f%N*ryQ^F4Jr4Td=3&3!L!(ItkfU%P>QRr(ZJ<kW<tF;M`)}&YK*i_mM(Pr{n`c!xyq`1h1'
    b'y+a?@$-g_t+$YKC(J@otl|XC}Cs?%#`{@r4gr0+l46+SnHAiD!UQeuoK!C4StkqNVtnLVuqD9^k4~w-'
    b'(Vqn9_)?pJ@u=rUDiF+RTw;byVEIBy%VN-'
    b'j`5DpT#ljWxHqM7|&nwH8!LN2IqAFvP2r21L={hsMe`MlPb30$&+^45J@`P(<q{^X}&TwO;JdnT)G2=RHElfQ3YMp8Ind7|Oeq8P'
    b'fWYuQ<BEFK~O;EP+}+m>YJP(cJf$l|a)albCtdWqQ7xn?gsTQRU=#G~2^NS0EED{?)P-'
    b'RGgZqKJU5ECRXSTABE8DNzof;rqZz6<jkQ-}`d!YxN#wj#`@?TmGeK_+WQ}Gu|NjQHdXRWA*&eZ6Y~4Sit2FPnRlChuH+QW|Nv-'
    b'@WhW$&RQB9bv%Yh?_dLDG2OQvy`=WNZ7*ZPt5iPN0X-P)GwB;51d5a$g-0v}9#~!t&Yk-'
    b'J3bR?2l!EG7C1k~ewSlDvpolMyJgp>)w#<5j3cL|bw)(!Q3$Ac!o5h;H4to|<^_wi9YDYzczLN~r+!{z^4dB=jk$tl~QhiTtKQf>'
    b'P^x00~_(RV2lmk62nL(zxZks82=s?4L=paQ>8>?omcB78<ua+XT0Y<=<yY&!iosH@o;=Qab@%~}Lk0n-'
    b'@p4?m++hbcYD$`lW`fXADBbyqjEjvlyfH7^=WLFdQI~W-'
    b'B3Jd_c5*vm(Y$6DYU(E@tgZM=_`Szwhs`!G7o$6a*T6+fPnD2%a0|SGD{T;@X8o@KE%dxeeCKhgJPdMN94mH1vyeFn@!GQp82i43'
    b'DrcQfnIu}CRcUFD0MTon=3zitB)s=5E!$%@PU)2#mIvOGx=4f8a);g*lQha+pPB=Hr1GwxwAQ#cNWT2SdrnYfM7VEDvwpOE-'
    b'G1vr0(mTD2UvBk<hLJ(FmvedY4}>T-'
    b'&H#K=3m|sY{EGEfTcolDq3VCob_^(!*EH8hsNxN}$N=wVS!fVKH}{tGL@fVP%Ku7QkBx2f@ipu{OTa26Kdj*#lby`N0)8lCqfd4;'
    b'#{rZ>hk^pSNjpC;{8Fe^t7US+Mfv~`X+P+cYu`(=EtTVJmkx*ak}=1Nz{VPms?@$$qY!e3Wgm$zQ;tbJ5yw5@<%bhbgk|jnVd{r+'
    b'TwE>G_}cb&yybyWt@qh)0Rp%V(Vm_c(dW?BXwfI@PKIP1A*?|;oGlgumAw;}iUmLYaHnP(Rc(CMN@sVHAG*CYk3}HKuaLiOA-XMG'
    b'@d?YminoC)oO`Mn(+MB!aZgm#3)Fv>OptlJtTG;|Q)2;g{AeoJkXAvouYp-'
    b'6JDy9MPm;AQE>oeLNBOxpDGrUk&r_&<%YY^!Ex0n^<RFcAu;G!IgpAd;qra6OTQ_#57N*56O%k?sjMKc5HYv1&Io9x0VXcq5(nzG'
    b'%V~L3W4O`^}PSl6pd*Ns7ZZ2s!Hg(EB0j657kFrLqzf==GI&KAxJ!aPApcMNf<zw$m3-'
    b'_ZKd>jtz8F!;$(IfhGa(~_6vga#=bFnlmvKIUIq3dw3%Wi;{=60MEi0yF3LCVWO3pVItgS!hyw@2+euDSmD7e(U7=>'
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
    candidate = modp  # noqa: F405
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
