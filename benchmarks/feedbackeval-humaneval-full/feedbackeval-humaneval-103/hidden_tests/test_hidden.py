import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[1, 5],
 [7, 13],
 [964, 977],
 [996, 997],
 [560, 851],
 [185, 546],
 [362, 496],
 [350, 902],
 [197, 233],
 [7, 5],
 [5, 1],
 [5, 5],
 [1, 1],
 [3, 9],
 [25, 35],
 [10, 30],
 [100, 200],
 [15, 15],
 [10, 10],
 [50, 100],
 [15, 100],
 [200, 30],
 [51, 100],
 [51, 50],
 [30, 200],
 [3, 101],
 [35, 35],
 [4, 3],
 [50, 50],
 [4, 9],
 [9, 50],
 [6, 5],
 [3, 6],
 [9, 9],
 [6, 6],
 [30, 201],
 [5, 5],
 [25, 25],
 [15, 16],
 [9, 6],
 [200, 6],
 [3, 16],
 [9, 3],
 [1, 200],
 [201, 200],
 [16, 30],
 [6, 7],
 [201, 25],
 [14, 15],
 [2, 9],
 [10, 6],
 [10, 4],
 [7, 30],
 [16, 5],
 [9, 10],
 [2, 2],
 [101, 16],
 [6, 4],
 [16, 16],
 [49, 49],
 [101, 200],
 [29, 30],
 [7, 3],
 [15, 14],
 [201, 31],
 [4, 2],
 [201, 201],
 [2, 7],
 [2, 10],
 [4, 1],
 [15, 25],
 [30, 16],
 [8, 31],
 [5, 3],
 [4, 4],
 [31, 30],
 [3, 1],
 [14, 32],
 [7, 10],
 [10, 5],
 [202, 25],
 [202, 15],
 [999999, 1000000],
 [10000, 12000],
 [54321, 98765],
 [123456, 789012],
 [1, 100000],
 [100, 1000],
 [3000, 5000],
 [99998, 100003],
 [10000, 20000],
 [3000, 20000],
 [100, 12001],
 [3000, 1000000],
 [3000, 3000],
 [1000, 100],
 [100000, 1],
 [100003, 100003],
 [3000, 1000001],
 [5000, 100003],
 [100003, 1],
 [3000, 999999],
 [101, 1],
 [123456, 20001],
 [1000000, 100],
 [1000, 10],
 [1000001, 20000],
 [20001, 100003],
 [54322, 54321],
 [3000, 3001],
 [2999, 3001],
 [20000, 20000],
 [19999, 20000],
 [1000, 1000],
 [1000000, 1000000],
 [999999, 3000],
 [3001, 3001],
 [999999, 999999],
 [3001, 1000000],
 [1, 12000],
 [789012, 100002],
 [75, 100003],
 [75, 12000],
 [1, 3001],
 [99, 100000],
 [999999, 1000],
 [10000, 98765],
 [100, 100],
 [999999, 1000001],
 [100003, 20000],
 [100, 99],
 [1000, 1000001],
 [100002, 3000],
 [99, 1],
 [54321, 100],
 [100000, 2],
 [99, 20000],
 [54321, 101],
 [99998, 100000],
 [100001, 1],
 [100002, 100003],
 [100001, 20000],
 [19999, 100001],
 [75, 75],
 [1000000, 999999],
 [5000, 5000],
 [2, 54322],
 [99, 99],
 [1000000, 54322],
 [19998, 100001],
 [54321, 54321],
 [10, 1],
 [20001, 99997],
 [101, 99997],
 [99997, 100],
 [999998, 999999],
 [54321, 54322],
 [54321, 12000],
 [999998, 12000],
 [10, 9],
 [100001, 789012],
 [123456, 98765],
 [20000, 99],
 [999997, 123456],
 [75, 99997],
 [100005, 789012],
 [99999, 99],
 [101, 100000],
 [101, 1000],
 [54322, 789012],
 [101, 100001],
 [10, 11],
 [999999, 12000],
 [3001, 99999],
 [5000, 3000],
 [99997, 99997],
 [789012, 789012],
 [1000000, 54321],
 [54321, 99],
 [1000000, 1000001],
 [3000, 75],
 [99999, 99998],
 [19997, 19998],
 [2999, 2999],
 [100, 98],
 [99998, 100],
 [98765, 98765],
 [123456, 99],
 [100, 99997],
 [1000000, 75],
 [10000, 2999],
 [11999, 12000],
 [100001, 100000],
 [5000, 100004],
 [3000, 12001],
 [999998, 999998],
 [54320, 54321],
 [12000, 1000000],
 [3001, 123456],
 [99999, 20000],
 [100001, 789013],
 [20000, 19998],
 [20001, 12001],
 [54323, 54321],
 [98, 12000],
 [12000, 12000],
 [999999, 100],
 [54320, 12000],
 [10000, 75],
 [3000, 99997],
 [100, 19997],
 [1000000, 2999],
 [2, 100000],
 [999997, 3001],
 [3001, 3000],
 [100005, 100003],
 [100001, 100001],
 [100000, 100000],
 [20001, 20001],
 [19999, 1],
 [2, 123456],
 [2, 1000],
 [10, 999998],
 [99998, 99],
 [3001, 2999],
 [12001, 12000],
 [98, 99],
 [3000, 2999],
 [100, 999998],
 [101, 101],
 [99999, 100],
 [100, 54320],
 [12000, 11998],
 [54321, 999998],
 [9999, 9999],
 [99997, 999999],
 [98, 100002],
 [54321, 1000000],
 [75, 11999],
 [98, 98],
 [10001, 10001],
 [12001, 12001],
 [789013, 789013],
 [19998, 1000001],
 [54320, 3001],
 [100, 99998],
 [73, 92],
 [100001, 100004],
 [54320, 54320],
 [100004, 100003],
 [1, 5000],
 [100000, 100001],
 [54322, 99],
 [20001, 54322],
 [100004, 99997],
 [3000, 3002],
 [789013, 100004],
 [789013, 1000000],
 [1000000, 1],
 [98765, 4999],
 [3001, 1],
 [99, 20001],
 [2999, 3000],
 [54321, 54323],
 [99997, 54323],
 [54320, 3002],
 [99999, 20001],
 [20001, 11998],
 [999999, 92],
 [19998, 20000],
 [100002, 19998],
 [1000, 3000],
 [10001, 100001],
 [3000, 789012],
 [1000000, 999998],
 [2, 1],
 [100001, 10],
 [3002, 3001],
 [99998, 99998],
 [10, 1000000],
 [100002, 10],
 [3001, 100003],
 [3001, 20000],
 [20000, 10000],
 [1, 2],
 [1, 19998],
 [1, 20001],
 [1000000, 789013],
 [1000001, 1000001],
 [100, 101],
 [2, 99],
 [20000, 100002],
 [9999, 3000],
 [2, 92],
 [100002, 100002],
 [4999, 20001],
 [54322, 54322],
 [12000, 19998],
 [1, 10],
 [9, 75],
 [789011, 789011],
 [2999, 54321],
 [54322, 100],
 [3001, 999999],
 [12000, 999999],
 [123456, 1000000],
 [3002, 75],
 [3000, 2998],
 [1000001, 73],
 [100001, 5000],
 [5000, 92],
 [100003, 5000],
 [100004, 100004],
 [20001, 123456],
 [99999, 100000],
 [1, 100],
 [20001, 20000],
 [20000, 3001],
 [1000000, 100004],
 [12001, 11998],
 [20001, 98765],
 [99, 100],
 [19997, 100000],
 [2999, 54322],
 [99997, 10001],
 [75, 20000],
 [3000, 99999],
 [101, 100],
 [100, 19998],
 [20002, 99997],
 [2998, 3001],
 [5001, 99998],
 [99998, 19999],
 [10, 99997],
 [98766, 98765],
 [100001, 100003],
 [3000, 12000],
 [20000, 12000],
 [100001, 999999],
 [2, 54323],
 [1000000, 10],
 [5001, 102],
 [1000000, 3000],
 [54320, 5000],
 [19998, 99],
 [2998, 2998],
 [98765, 75],
 [999997, 100004],
 [789011, 99997],
 [100000, 20001],
 [789014, 11998],
 [789014, 789014],
 [4999, 3000],
 [101, 54322],
 [98, 100003],
 [11999, 11998],
 [102, 5001],
 [4998, 4999],
 [100001, 1000],
 [10, 100],
 [12000, 999997],
 [100002, 3002],
 [100002, 99999],
 [75, 9999],
 [3000, 98],
 [11999, 11999],
 [3000, 98765],
 [1000001, 2998],
 [999997, 999998],
 [12001, 999999],
 [19997, 19996],
 [2, 999],
 [19997, 19997],
 [98, 11998],
 [99998, 98765],
 [1000000, 101],
 [100005, 20001],
 [74, 101],
 [4998, 1],
 [99, 19999],
 [123456, 75],
 [10, 789013],
 [3001, 3002],
 [102, 102],
 [100000, 1000001],
 [100000, 20002],
 [1, 3000],
 [98765, 19999],
 [19996, 20000],
 [19997, 100004],
 [54322, 12000],
 [11999, 1000000],
 [18, 98765],
 [5000, 100],
 [101, 99999],
 [5001, 100],
 [19999, 1000000],
 [999, 4999],
 [98765, 9999],
 [5000, 19997],
 [2999, 99],
 [54321, 20002],
 [1000001, 92],
 [100001, 54321],
 [1, 1000000],
 [99997, 100000],
 [100002, 99998],
 [100001, 54320],
 [54323, 3001],
 [19999, 999997],
 [92, 1000000],
 [12001, 75],
 [789013, 3000],
 [102, 1000],
 [123455, 99],
 [2999, 2998],
 [100001, 3001],
 [999, 10],
 [101, 11998],
 [100002, 74],
 [2998, 100002],
 [999997, 999997],
 [54322, 3000],
 [98, 10001],
 [789013, 789012],
 [102, 19998],
 [98765, 99997],
 [5000, 100001],
 [4999, 5000],
 [1, 1000001],
 [789012, 12001],
 [5001, 19999],
 [99997, 99998],
 [1000001, 1000000],
 [98, 10],
 [999998, 999997],
 [999, 7],
 [100005, 100],
 [19999, 19999],
 [999, 999],
 [789013, 789014],
 [123456, 123456],
 [10, 99998],
 [103, 100002],
 [1000000, 9999],
 [12002, 12001],
 [17, 98765],
 [73, 999999],
 [19997, 75],
 [75, 999999],
 [100001, 54323],
 [10, 20002],
 [99997, 99999],
 [789012, 54323],
 [999998, 1000],
 [11998, 11998],
 [100004, 75],
 [789012, 20001],
 [99999, 99999],
 [102, 101],
 [5002, 5001],
 [3001, 100002],
 [11, 10000],
 [1002, 1001],
 [99996, 99998],
 [789013, 98766],
 [100006, 12001],
 [54319, 3001],
 [54320, 999999],
 [102, 999],
 [100000, 999],
 [3000, 54322],
 [998, 998],
 [100005, 100006],
 [98766, 98766],
 [74, 11998],
 [999998, 12001],
 [11, 9],
 [54320, 99997],
 [999999, 999998],
 [123455, 100],
 [98765, 98766],
 [101, 10],
 [10, 98765],
 [102, 54320],
 [123455, 3000],
 [54320, 999],
 [20002, 998],
 [5002, 12000],
 [789012, 98766],
 [999, 3000],
 [100000, 99999],
 [1000000, 73],
 [10001, 998],
 [20001, 19998],
 [5001, 10000],
 [1, 73],
 [1003, 1000],
 [100006, 100003],
 [7, 2999],
 [12001, 20001],
 [3002, 123456],
 [19996, 19996],
 [19997, 1000001],
 [98, 10000],
 [100003, 54320],
 [2, 100003],
 [103, 10],
 [789012, 98],
 [2998, 20001],
 [99, 2999],
 [98765, 3001],
 [1001, 10],
 [998, 997],
 [93, 5001],
 [20001, 4999],
 [54322, 2998],
 [66, 66],
 [99998, 99999],
 [1000, 20000],
 [3000, 100000],
 [99998, 99997],
 [100000, 54321],
 [1000001, 100002],
 [54323, 54320],
 [100, 92],
 [9999, 5001],
 [5000, 998],
 [123455, 12001],
 [54323, 54323],
 [11, 100],
 [999, 1000],
 [999, 1001],
 [99998, 54320],
 [54320, 3000],
 [123455, 123456],
 [5000, 2],
 [1, 99998],
 [123456, 123455],
 [10000, 10000],
 [100, 789012],
 [98766, 1],
 [10002, 10000],
 [98765, 10000],
 [99998, 9999],
 [789012, 10000],
 [123455, 123457],
 [10000, 20001],
 [100, 1],
 [789012, 789011],
 [10001, 20000],
 [789011, 100000],
 [10003, 10003],
 [1, 98765],
 [123455, 100003],
 [123455, 123455],
 [123456, 789011],
 [789011, 1000000],
 [123456, 1000],
 [20000, 9999],
 [99999, 54321],
 [98765, 98764],
 [99999, 789012],
 [12000, 789012],
 [98764, 98765],
 [123454, 123455],
 [123456, 54321],
 [98765, 100003],
 [123457, 98766],
 [98764, 10000],
 [98762, 98763],
 [1000, 100003],
 [100, 98766],
 [10002, 789011],
 [98763, 123455],
 [123458, 98767],
 [98764, 123456],
 [10002, 20000],
 [123458, 1],
 [98763, 98763],
 [98764, 98764],
 [3000, 99],
 [10001, 2],
 [100000, 789011],
 [11999, 789011],
 [1000, 123456],
 [99999, 98765],
 [123457, 123457],
 [789011, 999999],
 [98766, 5000],
 [98764, 9999],
 [99999, 789011],
 [1000, 98767],
 [98764, 20000],
 [4999, 1],
 [2, 123455],
 [123456, 99998],
 [20000, 54320],
 [10001, 9999],
 [789011, 12000],
 [100, 20002],
 [12001, 789012],
 [1001, 1001],
 [20001, 19999],
 [20001, 100000],
 [21, 6],
 [98767, 98767],
 [99999, 789013],
 [10002, 10002],
 [12001, 100003],
 [5001, 5001],
 [10001, 10000],
 [20002, 100000],
 [99999, 1000],
 [98765, 10002],
 [123456, 999999],
 [4999, 20002],
 [1001, 100],
 [1001, 1002],
 [12000, 789011],
 [5001, 5000],
 [101, 54321],
 [98764, 10002],
 [98765, 1000],
 [10002, 54321],
 [10000, 54321],
 [123456, 20000],
 [20001, 98764],
 [789013, 54320],
 [19999, 5001],
 [12000, 68],
 [98766, 5],
 [1002, 1003],
 [99999, 123457],
 [10003, 123456],
 [10002, 98766],
 [98764, 1001],
 [5001, 99],
 [98763, 98762],
 [9999, 10000],
 [1000, 10002],
 [123454, 98765],
 [10000, 100003],
 [98764, 100],
 [12000, 1001],
 [1002, 98763],
 [10001, 10002],
 [12001, 68],
 [789013, 54319],
 [123458, 99],
 [4998, 19999],
 [5, 54321],
 [98765, 789012],
 [98763, 99998],
 [98764, 99998],
 [99998, 1002],
 [1001, 123456],
 [999999, 54321],
 [789013, 789011],
 [6, 2],
 [123455, 54321],
 [54320, 1000],
 [10003, 54321],
 [20000, 3000],
 [98762, 3000],
 [54319, 3000],
 [10000, 123455],
 [1002, 1002],
 [999, 9999],
 [98767, 98763],
 [5, 98763],
 [99, 98],
 [5002, 98764],
 [10000, 10002],
 [98764, 10001],
 [20002, 20002],
 [10003, 5001],
 [123454, 98764],
 [10003, 10002],
 [98766, 99],
 [10002, 1000],
 [10000, 54320],
 [1002, 1],
 [98762, 98762],
 [10002, 5000],
 [123454, 123454],
 [98766, 54320],
 [5000, 99],
 [54320, 98765],
 [10003, 5002],
 [98766, 10000],
 [19999, 100003],
 [789010, 789010],
 [98765, 5000],
 [20002, 10002],
 [1, 1002],
 [101, 20002],
 [1, 98763],
 [100, 19999],
 [789013, 54318],
 [98763, 99],
 [98762, 10001],
 [5002, 99],
 [54321, 5000],
 [68, 98762],
 [100, 789010],
 [98762, 123455],
 [100, 98765],
 [1003, 1003],
 [54318, 54318],
 [5001, 100000],
 [123458, 123458],
 [789014, 100000],
 [5003, 5002],
 [789012, 9999],
 [68, 98769],
 [68, 67],
 [9999, 789012],
 [5001, 12000],
 [10001, 54321],
 [20001, 3000],
 [123457, 123456],
 [999, 99999],
 [10000, 11999],
 [67, 67],
 [1, 6],
 [98762, 9999],
 [1, 5001],
 [12000, 54320],
 [10001, 789011],
 [2, 5],
 [54322, 98764],
 [5001, 99999],
 [5001, 123456],
 [1000000, 67],
 [5002, 100000],
 [1002, 11999],
 [12000, 98767],
 [123455, 123454],
 [21, 99],
 [98761, 100003],
 [1000, 67],
 [99998, 101],
 [54322, 2],
 [1000, 999],
 [2, 5003],
 [20001, 10002],
 [123457, 5],
 [5, 1003],
 [21, 7],
 [100003, 54321],
 [9999, 98762],
 [789012, 1],
 [54321, 1000001],
 [98769, 98769],
 [98, 1],
 [99999, 5],
 [1000001, 1000002],
 [5003, 100000],
 [54318, 10002],
 [100, 789009],
 [123455, 5000],
 [10001, 10004],
 [20001, 98769],
 [123456, 101],
 [10004, 99998],
 [9999, 98763],
 [20002, 1],
 [9999, 54320],
 [9999, 10003],
 [12002, 68],
 [123454, 100003],
 [10003, 100001],
 [100, 1001],
 [54318, 54321],
 [100, 20000],
 [20002, 20001],
 [123454, 11999],
 [123456, 3000],
 [100003, 3000],
 [1003, 1004],
 [100004, 99998],
 [1000, 1002],
 [1, 20002],
 [1000, 99996],
 [100003, 100002],
 [68, 101],
 [1002, 2],
 [9998, 10003],
 [789009, 98767],
 [9998, 6],
 [68, 789009],
 [10001, 11999],
 [12000, 12001],
 [1000002, 1000002],
 [1000001, 789013],
 [123458, 123456],
 [54321, 20001],
 [54322, 99998],
 [998, 20002],
 [789011, 54319],
 [2, 4],
 [22, 20002],
 [98762, 123457],
 [123454, 12000],
 [98769, 10001],
 [999999, 4999],
 [54321, 20000],
 [123456, 123457],
 [100004, 20001],
 [99996, 99999],
 [20000, 10001],
 [100001, 10004],
 [789013, 20000],
 [54323, 98764],
 [123455, 123458],
 [123457, 54321],
 [10001, 123456],
 [98765, 12000],
 [54323, 5],
 [123458, 123455],
 [100002, 9999],
 [99996, 100001],
 [98, 999999],
 [789011, 101],
 [100000, 100004],
 [10001, 98],
 [54319, 54319],
 [54321, 99999],
 [100003, 10002],
 [10003, 67],
 [998, 11999],
 [102, 9998],
 [1, 54320],
 [98766, 98761],
 [100005, 1004],
 [54321, 123455],
 [98763, 10001],
 [10004, 10004],
 [98766, 10004],
 [123457, 101],
 [789013, 20001],
 [1003, 54320],
 [1003, 3001],
 [4999, 789010],
 [1, 100003],
 [98767, 98766],
 [9998, 999],
 [789010, 1000],
 [100003, 2999],
 [2, 54320],
 [3000, 20001],
 [10001, 99999],
 [10002, 66],
 [101, 20000],
 [98765, 1003],
 [98766, 789013],
 [4999, 4999],
 [123457, 100001],
 [54319, 101],
 [54323, 98763],
 [21, 5],
 [123454, 54321],
 [54322, 99997],
 [789011, 1001],
 [99999, 20002],
 [5003, 5001],
 [789015, 123455],
 [10003, 2],
 [5002, 5002],
 [789012, 11999],
 [99996, 22],
 [98763, 98764],
 [54319, 789009],
 [1002, 1000],
 [7, 999],
 [101, 123456],
 [11999, 1002],
 [12000, 9998],
 [100, 4],
 [20002, 98762],
 [1004, 98764],
 [1000002, 10003],
 [54317, 54316],
 [100004, 4998],
 [21, 98765],
 [9997, 10003],
 [1000, 98761],
 [5000, 5001],
 [67, 1000000],
 [24, 98764],
 [99996, 1000000],
 [54322, 123457],
 [999999, 789012],
 [3000, 100003],
 [9999, 9998],
 [98763, 5001],
 [54319, 100001],
 [789013, 5001],
 [1, 99996],
 [54320, 4998],
 [99999, 102],
 [5002, 1000],
 [7, 7],
 [102, 12000],
 [98, 1000000],
 [99998, 10003],
 [99998, 54319],
 [100004, 1004],
 [100001, 12000],
 [1, 98766],
 [20002, 5],
 [123455, 100004],
 [98770, 10001],
 [99, 1000],
 [123457, 20002],
 [999, 20002],
 [19999, 20001],
 [99998, 123457],
 [98, 98764],
 [98765, 4998],
 [123457, 98770],
 [1000, 54318],
 [22, 101],
 [123458, 10003],
 [54320, 1000000],
 [100003, 100004],
 [10003, 54315],
 [100, 54319],
 [67, 999999],
 [67, 999998],
 [98765, 10004],
 [99999, 5001],
 [12002, 12002],
 [99995, 1003],
 [54320, 20001],
 [10004, 5001],
 [98, 123457],
 [7, 6],
 [54317, 2],
 [123456, 9997],
 [9998, 789010],
 [99999, 1000001],
 [99998, 20001],
 [789009, 123458],
 [97, 97],
 [1000002, 98766],
 [4997, 19999],
 [11998, 12000],
 [1000, 123457],
 [19999, 789012]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-rlqJGO1Tah;{WR#zN(04O{&b;JQ)HI%ypjvOhJy5x5Gn~OaAS41gT)Y!bbB>xA`-'
    b'Dhnqpla5fKvm)Y{I`Gohrj##zteyI*T4LafBx_P`=4ei^<Vz^AJdMhr%~3<IiFg5#k1Y}xFN()?)J)GrOc4?&C%+bwJz^F^$|i_|'
    b'MGwT<)8lkpZ~Gd*3zo!c(L7Qs;z`Q(y%*yW=|HEx9wwFNoiy|HbM!b)IM`gq5b(W&u@4;{nlLX7&V5L_q39G$UWPN*=>2Lr7Vj%M'
    b'$g-<hT2am_mn?BW?Jn1j9GK@(N-ROu8mMnN^RT9r|ceDTW6fRt({d1bI|U&$4`y-'
    b'&yQJFd<5TV#MN_MyQej0U4hr^wRWbi2EVHp^E!g{mcp65UCm{sm3~IEgL$-'
    b'D82(|3VodGMzIWT_@@;9SxYEvh<bIg08rqp9_2zM{eZtRU+SxUS6`R#wR%8J;>$Z69u?Mf08>^6x7O;e~(>g2)Yh-iBc;lZRQ$3_'
    b'ISr8WQ=3BkyYtx%~kK;I>_uF>k$7}T3c;A>J(^OaQvDBZ@l-U{j-'
    b'8osele*V5Qf#}#(aLSXTGRjUp<0f6&y>gROm~dOScUoL$K0@3!NJe?QWk9GH5*@@)5)wBYn);@Ebh6%c0Sij%62c`wofei-'
    b'N&TL6x@W}+?X*3JFB07k;a78>}0K%ll|Vfc}~Czm}chr^wZmjpO?a2+G0JhvV+lf^Agi;@lNZ>c1<i$87oz5KF2DRU$3)xu6x)0<'
    b'5Lmq4?X!BKIR;!^u|o`yEo#dGY8gpot)-OvFcTQ+&k-'
    b'CZexVCe^x5l>@sax8Eb!;rs*+u3%QJ*nx*J?6*w>oUp1b^N_%LYn9ZNjU|=akJRk3`3)h>I*EHt$w50i+m)SXZ`@%YzuHZOsi@qn'
    b'r`WX!{gGn=QYpj4@<pN;LQLw)@ZO0N;%`94#%Z=DD%u!14GKc#pKRy-WEsO8NCY`q%C2Ca643nF}Fx-'
    b'B~8<(HS42F_C4J^Qbm0%yAdI`4p;sG>_HFC+RGuCm(n%i?qe(=k(c!$VTwOVV!?gC3TI*Xmc@*lflp;`{k^vpf$K0Dt8Jj{3*HG>'
    b'}3q7Z{s3JEZZI9DvqZJxo`_II738xXn!-'
    b'Vpg1CJfMk3c|dw@opm|fXi_&;EcbR=;1(A*faLC&by<@(F1sBEK|RcRh@Xoh=5RDr|rA<63&5{ec_Zu3_dtBFbYD=@iRA5^IAO2Y'
    b'Be5yJ59&nBEhAt1^)4}&WOR}i~;0QF|9yM>bY05&)nP+dT$2@POb4i?n{^%8GRu{l^uvP2Uo;+7to14W#Ap3_u=;P+{|-'
    b'(>M_J6%q4=i87iw3BZks|U%V@n)?yfqV7drLYdU_jixU|7SK`e}b5ln3j7QG2a%chQj({)^B?N+9?XV=F6Q}098{Pr#6ZR{7W6W@'
    b'~{{TfJ65x-eXZ^-3#@AkmKx0J-pgFg?t&Vg~@P&ObM+~@N5Xbh%8D5&=WT_?_x1N0$?_`1aoC+R$6SF*-'
    b'u2d|vG%CNxPmAb~x7<?Qb+&iI-5e|g9(fiK4d)MTtN?s!BnRnnP98YHzEypLv~}MG`U4+)aLga`%X0%8p~6a<UK-G5&?(McV-'
    b'?m!0z%>q<BpZl))pDVDB(8VHI1)i6fXssmqtUx90oxHl&0UZPs;ofL^kBh>hX;LX24y6!;TqY4ik`cILsJj?{`PT!Vwc&hC>69r5'
    b'e6@*O`j}VGC^nX~b%*VuzaXsc!Ye8hUVG>(qCB>a8h0?T*SUpX$d6CE_Ffm{t`Aa>FkCAKwd+Q!+s#I)=>4BTV9q-'
    b'}zE+#qe?Az&Lr{@H7KUh+D*?15yD78_~x*72_><7%yq~|L_@!8&V=)>6)-jq*P>8XPjsx3&=V6W@l-'
    b'pr$(&kt>x@TdTfELrTg~X!a&aL`<*NG4i*!3`7pEV>q5v%tOV9{2PU5jj^dLEXRe4cwdV}PI4-'
    b'`zY8P(O)4Q7CyNJmz`53Ila#>in&vhU_Eo2O4T%J3whl=t+C{AP5<LKR);bV2}T}sSe-'
    b'z9C|1)?tr=wEU)FD>|YIm1i*rjAPR31_8)YGqu^O)=K0oy<3QJj5p^uM=~y-'
    b'P!`y3+|#x(@ocZWxQF0475DYu#x9V<Id}Mgg6N%7o0iKFV<ZhEmD@5*e-#*ud{YIp8&ItTipDb!^?~~Q5-'
    b'7^;UeC18k4`a{@g}`Ca=EHS!c|Jz6$fRn^fx#g%M4N-'
    b'<n7uux*{54of&<a>7p&*16?D_+NLoTLz||M#BEjhfx@sEi>Sbmu_Gy@~p>RaxU#OX{Xd6lJU;d%7Ck<)(k$=9K8MWV?04(5O>Tj;'
    b'5Vi|yuF4RJ9-SebVBw{P|&);=1jahr`%Q}Y@aCp$L@8Rm9U!z@X4HH!t-'
    b'kS+M<27otf6USK<A<VBME5f)fy=LHqu*nR%E;JCzAWxQ<j>pYCYo?2&Lh+L<w?%ZnEPDI=%%?rT@XYz)Tx{s2X5T4K~oU_fT84nV'
    b'wPBPm{ch+Nke*^V7f;Ri=sn&`-'
    b'j@wXoeS$3@uzT~sJ_TZ{sx^x)NfDQH>LMzvu$q3EB#?J6XR}03)B77vPcjWBq@nJ8}SokcKxGzL-VIHwzE*-'
    b'Og|G+xD76?kgc9?Ab<+Jh9rx7E4M{5<rp<QF5r!D5FXj_5N%bK?iWcpx&vCs?OS~<?JJ`2uhG0x`jEf9pSYPF*4fKT6e2a^=%nW>'
    b'Daqlgfhm(lNKD42EqVWJb$f@YN|*@7FC%}kWD<^pbV;>E%fx3~4Vy}%D)Vl(13;d$0~;!QE$02W`E8GIsIj)etDvq8}>Mi48qH-y'
    b'u|2??3D_*P=zmhIpE?i6QHAg~{L93iOqL0Z6gIfV(<X7L^AU=7+kEG3;j@+k-'
    b'7M4|+2?%lb0>7{=2;=g{l+jU9zz$=8U;P?%SSZ$mhV76r?H0*7uP7wJRmb8La7U@(^et9?PC7^ieF`#~nhe)QNO6bWo7n_FuX0kd'
    b'epdscBx@&hUv=4j^dYL8yAf|BNeT)xB;Xn-'
    b'<0@uSJFgHo%<Z$Q72OFBV&0%BSdUZ;A&>m&9*fMdiyvuLiBD4jT;>4VG!YpWkDpkN&Cul9P8(h7|Vz|SyH$^yN)PBG$19d;JHG2Z'
    b'`(vHnS(^=8MQo~x+Y!kN|tO<U**1QPu=m9~$Jt5voW}d@%7q$X)D=?A4Vq>=Xr3_OcQ1kJ8wRK*+C58AIPun>{DDsGb7c7Yg{IZ8'
    b'PV$wacZOCQX2vu9*o(u=d@V)J=Ln`oxuH1~+;2W9f)$NqbdYsSMT}caSxiX^Zc2)rfx^i>qNkn#R#@OI>yq3&R+rpxSOekcu-Org'
    b'Xp$~R5=4L^lBpWhh+R}$S?SY9)t`MhmhK(sg>f$c(!eKDU>p$k_45Gp4%2H}TYSStb?)0f+I^L=>fYmZI`#K7=#Il<tXM+#%tuKc'
    b'=IP1ldhdh}-k052s{Dkr5JH?}mLj;KYsbgC!^u-t_E_b}c2;bdH|1J-I3n-fMUoPMoAoF*PgIn63y_<Y>@!>o|-'
    b'g)$aLAJ6xnieQz3VS*2Hx>AI9|JUWN4W3+unpy5WdI&%k0od}ytWu}YZ6ZfaB^IxG(l-FA$fRt|Hh%J)ACJ@%-'
    b'M_rr{WWBWG@akN&OB001*ucWh4<EfN)&Ig5&Y!-K5sglep%cz)?Z*-'
    b'f{>=gr@>xIin!5TmpCrg!*pUq$C`NG~(ViU!EIVOWe#?NLic)sA$$oO%XYGnW5VuHGPc3+@Z$9f&e`SuOK5odN;@9t&LvSmJ=$!p'
    b'KhDjsN-Fw>{S31Q8gXRL&}^xvrTNlg2P?QsAwNv@^j8$9*9kwh*S-d%AeIErlg!Y5HR$6T7+ffOL!)%F;HSe=$-'
    b'Ize`t~!F$>Hsdj|8)${xU^oL#1JMQn#!s_~mM1;W$Tj%H#ljBjcP`>$N^3n?VjLOKi!h7!dSdg*gro_{p=BUhNf#osMMPB08*7ZU'
    b'm#i2JfE8>bA$IQ#5AY~sGWNl(MIgiv>=1<%sq&&p>JvJ$Ml9c_C8>e+r=)4f(${RIIsFRKk0*mR$650(v|JZyV#Tj+AWV&A(kt+@'
    b';XTJOG8Ey`>-QWOwUo|mvWFwzoUlVLv*Mu}bWztXjjhLt<!j7SgCRX>`+8-'
    b'f1nc#AcLiZz*E3?<AIwXdViq&q!f!}`jlgQ<3M4`G6m^_LEJ*uWt2B!ra>IJiyd5t6lpRNCf;wv+&S&`F4&FlTJ3fB_+-'
    b'Gy1Ph1*{YxtqJlP!SEWC6md_~ZrbbXgUC5<!SF+cW@qWm4kN}ATbVyTMc4|&(SEdH8F9i;@*P9R==?H-'
    b'>!KO<L@P|(SLtE9cRel#_-'
    b'1|irCuWYFKs)Ej;ByO)zQGo!RH_+5~nCe=q4IIg^}|f);bK_0=yd04m%j&(nosW#5@;Pi>|B{eYt^TL*6P6D_T{yAgT~-'
    b'Pu&uNi)hUZqU;ZW?0jW55XcvrECAwowuL>P<k%u!q<nQ|2?sp{t;o*?BPZ5R^f7vw5b!b<JNURk+EsS8VU}amUb#aamJX5YK{hE;'
    b'+-'
    b'tt2gcH#vphqW&GREh$Y!(l3x4ALFM6ih+(FB0kMNC1)!7Sz>3PAyK0Ei~K!~+1{l+y4kA9H=zOZn144_=oJY%VO~?!qlV3h%wdDK'
    b'gmPKH<q6%uoi_+ssObcYJb8h@>|Mo%z^;_F)PMf@H<vN2Mnnz(%O3&S4ogymIb~*$7o6(!VpnOf4nkK}P_si#BhblOoi5t>W7+90'
    b'Guahk$_5Yfps_8$9#G^>*&HgMQYNcng?t3k>@7Hgz<&Qrg*v6T%>}8Gj3ep>z9fmpR@_(fQKMO!P$5aVqX#!&Qo`6H~j_1A4>Vn+'
    b'^A8=X^$@q?dS+7fna@4r_c_PrY*@)GBHg!@1)OVre>cp?Icpm7ib|OI#pcXm$d>7dk-'
    b'c76D0HM7;SfFAh>=FdJ`pAwu9B=Y4wZe0{^D!7YS2F$da@(!(iR2I5C7#PnA8=jhl*<r_juvB-'
    b'z>0_B2f4|ZN<@MJ)}I~w02d?VDz6zz15O%U)$Pes)WTwaGb-'
    b'o}XVOnBF2iSAx~T9P`eI*A8%2o7bQ3{@Iv&4EljZ=2uP?QZ6@WnN>)h{AGJ2;k@Uc1^GXa?e8o8%nn)UJq%h3+?+$Ylg1<ikKHr$'
    b'MZVY=5ut}OOHu%dZ^qj%roNgjMgq=<DMOrp95d;l^*_Gk1^$NrERr!_`^vk?ybx(NRrASQC=AqI5E8L337TScm!J~V&6u%`B|x>y'
    b'(OF(Rtq0l8MkaIAN8W&0YVn&#h9%eG|9Z#SXSZ&3+cVQOiVU1!yu1YnI*;f(!x7H@pktc;TXxIu*WhqA_oFghRYry(jjn_U)rbEE'
    b'ydtOwVVyWK!|E29^6adMyD)dIk6{C?X@8VwomPwHo&wUB-gw7H^O4fq-duY({ZeD<J$c!_nDNr<epa78Dk_=^;;)~HbBE21|a|P6'
    b'nAhKM36eJ`OY=X(UW|j03dw#h+^AC^*%lTAD$j<EJBy}`^l7A46H8Ot&ZGF$VAn(Esj!fnxbk@Fle45F30eS_e~(G#K0MN{!h4z%'
    b'woYfAy(rsi+o*guH!$fl}V3>Rnj5eIN7CQ5T84QN=$?N&R_b}qr(H>4qz9vWXR$hbz})a$b?Q2V?Gh0<Xt~Lg+3t^RpYrf%j3((T'
    b'p2Q^l3sj<XU(CCE9eV0Qg@Fh;ZPCG!<lO2zsXcY9-'
    b'DTbZ~mkWE*4T1;ira$5^AoUlGBpd*{Kdo%PaI9mHLICsk67x4L`;P8P3}qy&almSFW(@(jG~vH=#vl$;;q`=;x$ko3N97_`<lx5!'
    b'cuL``bAt?lHgxQHD1{lXOzBR@@ahAK?HAhZ#Wt-lRl}t!mgIa-'
    b'5n{^3o4YVvW#HB`e1c+Gk1y(1AkMC<*pGLL*riux=&oNB1S}9RRtr>#&c9^NwSx*b{yVUgQX15l48lu}0ejwZsy$o?A&~XXb_wYR'
    b'Wy+w(q-JWG~GPWEt{~EGV;gRy>5YC&W30R3X;Kf(C;Xv*IjPQi;oIb2^Om><_(u$u*T+u$Tpiy8Ohk2_8J-'
    b'WC{otxgtQ2y4#Q>I_)w9L!7y@G)v**^HQl#<;Tu>Z*ZVgNQ+!uBQIsuwqX2wAigZb>X?g{9ao7xA@|RT(603y=@YewAQ)wpF5KiT'
    b';{!N#OUqFjNqe%BSg0g!h?BIMI!*jcu@bXxsfF*gB#oYCEwKNn^N|AmNJ0nbD{DxoD7?yQNc^TltGHe!`!Airpt~4(fC5(4e8BKn'
    b'%H-N?9pdTOTC6u?$2ZQkq1LiwO*CHveSi0`_9d<P785-cB895RO7Xg&^__5RJ$GA%dlM6^@u=8g3a6G7CiLP!7htCA<!tA-'
    b'!ri_T@8Jb1HiMH!^t8F!v`pS{8LKf?+Q4ieL_t%OMvXBO$P`V!G8yfy1c+KQ;V&RJ6RWO+dAPG*ZHCQDsO0w<3}eJ;w3!BtH58b3'
    b'{8c0RJ5}Z1O;vd-PxSX;?cc~_Fqfl5qI`zRJxygHt89lMKv1k<GDWo+5bmO`R2_1MmqS=#azxdanP@e5;)ReCL?Ah<TUV71<STc_'
    b'8V%A_M%I@MejjqAZ4?)!3oZXq*iHC%WaAhNejahG)m4;8RIGa08nl7l0@S<k^aVVq&J}hU@~1}V)_YKhb|!L=+1OkAR<N|IR#L(2'
    b'dIWMirhW*S6$-xyjBN!tX1Vs;{QiBdSy(+*ViHmd>~~s>slZ6nJ|gE;=Z00=Vd!-'
    b'2i?4u9wz>7q<J0|1TavaL*pZX_hLE7`3#?;ZbUnxwBN(N|F&GI@sAO93=qTlUG=ICPPudKa=Lmk4DzNulJQNz5M$j8<0kl7vNjvm'
    b'0K;@J$X`&Sr=H0@lx7v2SQ-WV(wg%ONNQFF+77RPjkP*K}M_j68ClWYrIdZ%k9$J@np@%ZHKI-lz1@qF}9LV%Cor)ZmK(%E#EAap'
    b'wk~<0jA?8V9(c!49ma6rq%FPr|-P*g^&M$Q;+5-'
    b'iRUm_QHUQx0@x64A|U`1sw2z2H;T@_w5sQ}~eq5+sO;r!*(d8QKVwFu|#qhWx<I{wr~RAxv-i!{OoBBZz^kl{M@N-'
    b'tw2@t&8nR*|$wUQ`wz^*JWrt{O+g=1q5>tz;RbFV+^-Ppq5<$-'
    b'+qt+iSPJOOv2${pRIcTSOb#r!1Gga0Wc^bojfDa*)mjJQ}MQf!%d=7?y{B5<Fk3<i|AXt_N+)B5oaPrlCq)oIomVr&SEN1EdB0O0'
    b'tA)4hY6pE@L16Cf#&to23*~CJ5TF&JpeD3%R|f6c3)QgGweybwOSOQ`4AgRNMG~XaEt$*6y!<Ei#IbH!OE9zba0|0O84~t$@`f@s'
    b'F;KZ~Gu@Zu!b8z?TkdOHWqO@8|}Qr=5k>W1uVsnjv3pgk~KJfLholQ^R6r)x!;+=&<yg-'
    b'~5d|CKen&bUOiFr6&NWAwOGS_SEDL0KF^!Y>gg@c6gxH&|GN7*q^#P!!d!QS#(fNWC0gXZr8)$+kGlQ3ZBzruF#-'
    b'#0OE<smjE?zXhVN@<K?Ar_uFp%!f}OXmSDDhk$j7F&@TC@YP68%h8eB{fQAzss*1HtLwnuB!`8Lj(!2b|K&7V(M}W&KOCGXs$^<>'
    b'&AK@~nnr!Et#$75U3@Y7isM~^qydRPHU6J9A%;c@Cvj?U5)C~Q~Y68j+i0Dw60hg#9rs+r-'
    b'bY>cOGV`b{_VktMrs2Rt_$ofYytiHu>!;pYp3QI_Z8WuBRezjWhM)6vT{ut;D1v{^!(XcPc&n5;_YGFYp$sjE5pg!BgaxbRmD(Es'
    b'd>dAH7MjlMg&h{<*{Vk_=KXet-Bi~SP;=xt0Y#h-xVw5wh*Oxn3j)h0xJi&Nh40Eb&IaHehbv!M6!ubv-D_L&-'
    b'8=zFgdl9NtA`Udh$;=B%wl~5hN;fHDd%>k>WT}LE4eRB<Gfpj^*c`e^*fZ0gFC6mdJbwyn{x(kfnPO);fLT>@id`Icd$|x7jpDq-'
    b'#~-'
    b'e{N2OuKX3cc&dv$qhl)h)mxzX0N@2{EI0qxhEDb8L+i2<lrHWX<gk@EhR(?5E<*0E&Mc}H@6l66M1#U}8Jp^V{iA+hekL^9}t*t4'
    b'K(VH%LcuFPbcUJP(%H%?%aROr9C{Mz?nu51pYg#pHo1XaIh8l3GmsSJe(TZv~__-'
    b'~j_Q_LFtE=gBHiwAT&@~Xf=3IG`k%?3zU58!~NBiDSCYB$Rf!WLFni&DzD+>{nB<6T6@zRK+EfP~yDaWg*=^fmtmsCsFu{O_Aigw'
    b'GNz5*(|)a4Bu?0$ANu64LttY{$R*sTeV%prG}G3%r1UEeC+M&Y;qon7NbQNC#nGcC0bZLr7&Jt6`-929@E23gy|YKUqNzhb-rb(O'
    b'VEczSxffJKIdX5b%0;YnDm2)YO;`@GfRHhDpD>tehJzI@YAsU94#PEVii7*jiwIruPzQ^?OfVsFa)%NxtJw7VKK-'
    b'k4SCrfpi6@PxOXR?Bym#J;l)^wvuyOhfJbQ?BT!r<4!NkAz1ZwuR<Qzd?A$MS9h#q?Z!4xg`$XKV4PynKKOpVCrMnK}v)~s~^1b%'
    b'm)j18-'
    b'}Sa&rA9HX~obAGXX4~@!7o|rh>*g7z`xwo~ec@gNQIjIJu^)f+e6!WuckrxlFlk6}W1h_e)1j>*_+d_rTKAjfFYRJH#iK=Ky*cd|'
    b'uiq8kV3rsfKM}mTqg<j=6oMNPI0aY=U!Y*@y#+_<LdsI%_Vss+*%PBA}Wn%0CfY&jn2ex{ouFJfCB(hA}By>dv0WUBvG*W6e^RUe'
    b'&tXD)=>s3+WK#Ct~&KjRYd70pcfXbsLbX{zF6#B|I+q0n4x-'
    b')$}Ac;R>iv{9)_?R3GaIX1=z6l<!Ll=B)rTn(9e=CYCH{m<`3%T62Arj)lVfFO(b}4f~K8OtlkC%-3b`Us)mfT0e?+nCMH@T-'
    b'Ac97mChTv9PUbpTjal#5&mAM^!RJt~&NQ84Xl1Y?c;vo9|s;S@iyvNPH*V^vf!1fj^}bc9uK&b<hQ~Sh%FA-bmNgMV;H9a4I%T6j'
    b'8q%XUL(NpZQy|{`*^G3vB3){Lqbh?qT!a2=^SyRqfhh=&=S7q)CtiLx?N*r>hTb`DDDjlsNNiHpmCDAa!G^1E1<FKnG8DpKb-'
    b'j*j0Dop-oAmz#2gvcn*I$I|A@Oxz}-k&IJ{rdL?z_TgcTSOIMcm>BAN(Kc=kCg*Uc5tvODPvxqExXTD$QFx-sYB_w%67A;)a5hP7'
    b'1MviTsptH7z#cT8WsvaIPjRy1hdsFH^aLW2lr|B<iKr&;8Q_QUHm>pQzu*sbvtBAV|6;c`Z9W~`}TTi$L_!R-1r-'
    b'{~mdH*IsdTm|Z7pHIcsMNO$O3tc=F=0Z2yL!h)%_-WV<_J+&n+`Z-'
    b'^RLXk=Id)$pPO*iFek09GKN?Y!daP5+BHHO6xSsx0T4p`oZ{-J1BYwn-SerJn$JO#M$z@I9su0?oB%07wxggx7GbbTWs{Qi0nVn{'
    b'sCMI4KcU#)&LVp$Z|isP{V$f@J{?)?x_J<RT!ZB>#zmHE{|b4ZRe+_7lO3g@>y>Ip@2e^vj^O8$;Q7*Vh4WeM4t5>pp2lc#u;N5='
    b'6qz>Fq-Dnhbvlf3AjeYm2w)z>T>I=%ymWLNhTj-<cv(h6)7P{n(m~C2TGA~aIpP(k2k;LeB+bSk5ZECGuy}pv5g-'
    b'A@5tPL0t(<^l$tqaEqsI+I7Bx6al5?%qWFCpzup<a$#m_$-'
    b'u3W8n2}P<;cHP_shs^4tNk~Yxl(=0(+`49`tBpcks%APx`#K=W%ehHM+uT~{{uJe%^EAVQ`l&HjQmQq0j1=iJ#Kk&CbxA)t9%BY_'
    b'd>M=T7@%i3+HmovzT-i6Hm_Z<+_A>!t61_D+)M!6Fk(|D1=V+N>%TG<p8=oh-3-4a*1FDI@*s9q0<LZ%4_-'
    b'`r8tFnc05@G`K6IBKLM6oSyqWO3`WJs!t;Yyb`_c-ji<dvm4d5d!s>5N?CD2C&!wFWDmHUh!>)Dm7hR5Xjm2ColNk;KfLx7iBZ@$'
    b')#0+82!^q8}C-4aoi0CQ%GK)?9LbH=-'
    b'MaXKq}b&#jyvH%)u@Azjl+8Ost#30t~uGC#y^{Vwt1g6YX2j2?Bo9Q`(%REO5?c7zj1l=e7i(r~Y-'
    b'W@LPl5k1obv>zu#+3{2=mqg7*Hw0Ls${6}$Xl(C^T(Ea7*Z{B8{>iNs0nUi#7=}$co>1$Jym%>3jutH%EiqJKogJukTzW-'
    b'3oUY#5C3{~6*clXLUC$|Na>5fxk_!lj`a1b%b)L7tH8C5_4!iR!i_g-p1_C`pRHORRwkdW^roHEg&`L-'
    b'HWoRw@zbHtL6=XYixGb3x#l|y{?<zYpio18)$o?=0D@}vM$;an_`R;i2v0AX(A#s7xXxK%`mRO!Idp?B*067%>D*YOdKe^@3#D)p'
    b'B*sJ3VI@H$1@OakVn>+STbqz8ob^lZv}Ik%sM`Ogi*H%n45I@xSHxsRmtv`^W<l5^lyvp2uD^hAYcI>wR~9e-'
    b'mh*q<I_XyugL^1MvPHnIZ4g?b&g!IK<y;H3J9ASfu`zj;P~@b3bY1dcSw}hF3F!<v=+;N(LZ{1upN_6C8x5pnJXc<nmk?I6y)P`I'
    b'&Z%n~AQyk^ZK2?YZe%=WA?gm;$)j@6ebhv7bgHj~7zTl!Zt7~2iByH5ln#*}?Q^bqnl{-'
    b'=Ip+k`j$L#x122tXs77|&eV&|WHP<aVpUH_(8ZV#!w3jRq)C-2}X=yJ6K~b~G-'
    b'tM#IeDrTEoUA;m>&p&`fzP1Sl`RB6{TU5&nhH|sK(hO)jSnCfQvpEIgwbX3Ep?)cDRvkOEQmE<1r5dzKQ~$`3njoxc(18OqCr<kZ'
    b'49xaQ#Zs&Xw=8Va9|3I;6RME=lFDvdzqy_muGIww2!2Gu?#a=+7621M3B?Ydm<2;biz7uw#!6=L}z6z|2y&KrJ{H3iq};7EeETSr'
    b'AAec*W1Nd!?7|UsybBnSwR3uLB2Vpq~nr5nuz_H7aW@HS_n;;#@1!-4Q+8$)Mq)Vgcif9JO(-'
    b'qKHxJd@m5crkq|lgJ9W77)UGk|Q%kY5r$s+GZpdENo`XbH(IptVa9EeU9Wex50nv0Oci-JjT2D^fJiu3Lge;zictW5|qSIAbj54}'
    b'PfTm`3kMDINu^_LAdo*SI%4)9PkNGe5nA`!*ZLQ5NBdxx4w~4aC<IJ(BVPPW>PM;g%p$k61(s2OWgadw>&sEhtoKE}&lXVAm_tb!'
    b'S)R>MxipDo~{L|P<(*Akt(6zdT_4M(nmu~xf=`mlnDfP~Y&|9N<=Th{yjsV~3IFoYH9rN)Bf2R(C@Q$Rj>}f@fVv&{!c`{P2+Ale'
    b'}Or|Kyg9u{fcTw2inlrp~ef^i6!F<(AoygpKY_{BBnJFHki<;!;!Vh-'
    b'6SvqX{>FPO9rxd;pS3<hz{!hVNP~E<|V7ii=r;@aLL@C&A$b4^4K|#>XUQ?Y6%sQ`vSTi*2gr~jTrBX!{d?S&=5-'
    b'O%6vXQkq<Me_JqKtRZ9_v^HNni#}Z77<4hqpLB{kCjq_sC0sit6~s(RuyU;ES#!=eLudBzV=i0Uy@Ix~&n?KDh$FduINv+`i|^Q+'
    b'Ms5TwNM5MyVhd+#YgupeCc=7<bce5IW0U2CgA`gE~Q!_GwShEF4{lrdyStf(4@Re&q1N3ddS^DF12IR^=`uwd<D6V;SmI{Ik<WSg'
    b'gcmkHgK0gawV0gQXhKGK`KfDM`5(ZLQ38VT9A08aaiE&Uw2{AkMt2ZpP#vip>M>O6mkwSHr|N3dnVX^kyj5FB+>J#90gtANkI_bn'
    b'WQFF*C~wJK0T1;0wXpbx*cxd+_a)yhnJ2y89-Oq}_Y9Q`Peyt?*oZxOI{~{bE^2Sc8LHuv-_FD<2a>vYU|lHpf&u_Sn=}xIee>d>'
    b'WASpl76wb|xsMv_OobU8JS^*$YT*=w;sJT-'
    b'}P>L24%1PzY8&d!nfCiLO<TMX=gC9)Usz5aTM4ePQBRRp%9U)R@goHJMd9yR1JdPxj3*I8$d#E69|2D3p>ZysEHnVe{A?yu{H<g>'
    b'R0sI>X>6%={>C7lrB6lGm)76}SZvhgS*Ur-'
    b'821)E9>++WLU@s{3(men4Zw6p?0p63Sb)*wu8Y7M@tp?X3`M&zSfyroDF8g@o!>6SV`0xaZFYd^NVW?;z;0>Z8NgLECL@iy?uM?!'
    b'+L>xT`qK5M<iDZ5QFTZ@gJmV|&7!>|MP1B_Tb`loB?f#IdGrDI7yLJS=tN*KG;1ayW_gr%Po7z~Y?6+O~5~{hWtm(V;_@l)uZAwW'
    b'e%lTQL(3QdhTueC?d5Y+%$)QR4H&ki5g@^2^5+TePD!Rn*pAlkR#rMO_Ee)`l4%HSdLApTTJVlp(j^YvcCI=ljq0p|0WBSY7XJ#E'
    b'TE;xZ>(n(+2GVdJAhDcO3|*E>wk-lwG>>;xN|lJcF?<_dj?!;c?uOiPgGS_JSBG60Qj1TU!k!Ie4Y}CR0Ez?@`_U*y^x?l})5*)+'
    b'vlvR&nV(bExz#0K6X1t8*~5O*PiA+_1`wPcKGr_B(fz80acB62v@O2v|dj41I-'
    b'g7`X!bh^C7+(bt#1gEr&2_XIpzZx<6H2*#=f=T@0e>boHpYS@H3g0OC}Tf~%G#jkFO1WN31E|=S8FJG$eU^`~~u~G%@b5>#nN!xX'
    b'5Ib5=-'
    b't4cxlPFORf$i|<D%=~<ukl$sZfL@5so4{C_^5m{ce4FXO)z{t_Z^k*=(M1^iP*v1@#NJh#3i15X3*+B0zr9>{VmKd$yH4Um-'
    b'i{=X=*At?oB#|!@12ByBvYLrY^q<^Z6T+<8>gUC5SFeYFCq(^&1!JC2f9#KDHml|loXTl!j9TD3fp0S#QMuu{m|>J9w|?&R}i{EZ'
    b'cSH_09x4PiH<K7-'
    b'T5_Tk+4)Zb%JO%4gOy1r}OK<iu(*K4Y83Jhxh;t&!6Dq%vG~;)|saf7_%;g+DKqt8e2pKyqw1KU2Txx0*aS9zrIsW^A@4qru*c|N'
    b'&~~f&Xsi=VjUQbtT)f5Yrz_vgHReb#0e##A4A9d?03=ct;5=1G5w1_Lb8HKx|m1(qiQbd^sIe#5UT@wz0Uz#4tQFDLa9s#kVOBE@'
    b'##bR+%Kvkb$$<^8eXMTQoO}#tQ#V#8H*qZfF6-'
    b'A>g!n`8b0R%N?ztSLMpZPGlXfd?3?e{#2LP<sc#%nEh2LfQUF(k*rpmcPp?6j&H3-0w*M>-'
    b'ua$|%NC<{)PXtWmORW;+;7bI#u?bBN-|JRzsOm9aY!Z8tMSW-zhP9PNTYE0P2Sn29x)&Y~!BxGiD-|4h>{A7lsoWIS-'
    b'3&!nQ^ZfER60*r_6?fGJj76l9R$auCQ6xkIkT0s4iB;hIoe7uy!gc-;{Vci^U~Q}DH7kEK!#|J2M%=e^`q-Sh-aoQChLx^uin^`i'
    b'uNWWBQ9Q~+Ismwa*9pG5Q;huPsPE4jph?G0I_!V8A68a4E3{DJ3aMNRm0_CN0k`gS+Rto8}YgHF+!UmqYZI~$binOWdh&_FVwcNT'
    b'<o^1?3}KG_nIJ5;aw*BYl7%I%~^o5IhE0=D<z&P`m0-;Q$4wb)-'
    b'A+65#FeZg*P$z&sCF0se}999AxKQbdf58y*zzTf#vaZ=RvvMp;Gp+@JmaRs2p)I--ag1S#2cFC-'
    b'^qxi*lqvT)si~D^&&T1evcP$(_e);y7bPNOe?EY6K0K8G-'
    b'+Lw|4%mH07__u>1X(zd95BHS;K{G+Reex45RRJv*hekrMM1)Pz2ioH`6!ffPx1#Bs|i2gQVQrgur3I)0|pLJ39JDXo>zK^qk88#$'
    b'I&@Y49V=hli$+`#E;kExEV#+vr>LAEY5&d4pGQr8bX`xIMyGfk31so&6)SPuhI+phR%VYNjYali^+j^WLsN(Re09h>cU=_+$*tm+'
    b'i`H|+}T16yRup*p^mYsw%m)2YdiUwNt4syLrLcgMC#fYQ-XzXu_wW-'
    b'2|OnuqAN3hQfAx5CJT51T3N*8O+C^#8<;!QZ6AUpiKQ%Qe3$kK#2QuAAJU{OD8_*ma<M-'
    b'qL}K>B$lg+07lYZn|}`fW<oJ<E^Ld+rHB^U)$&%AibZ%pJsx@2)Z1Hh>0jw-HL8@hQUT=1}X^UPIF_Pb1TQ;rtg&VL|a&RDO0zp#'
    b'@SE{kD&9VN<3F<JXO5co^;A|RNz$!G8s92_8;LcD3Pra1GoC)7ahSMZL``z*KNCZ9HWh*cFi7DkPIzLI06i<sB-pG>w)A+aSrJg^'
    b'9a*+4>khAN5vLcq0-a4HncARi}z_z4ei6J67Ia)w(ECf`0H;2;X^20cnD~EpQ?j#!#wJx-'
    b';R1@wv5mk;1T5HDK;=zOon+izWtNYI}xQ*9pSppn}J*h!j?aG!p^68{ZT%5QfowOdmUZqi!GkXhtj8>K@DAV^SN|>+O8@F_Ex)^e'
    b'K&Sy=;_J#oZc$(bq?!TA(#Lo<J;zE-'
    b'!ER=K^@4uZco^!*no5O_3*QD@Pi$Fowoa)GpPPZiS$wVS;)&DD^?jhjIXVD)ZoV?gK>|1pOMVc4q-+Y?u><c$#CoL!-'
    b'A==Z27cb3bBWR0M8X^9p#NSRiu%6Kp*E@OJDFWHG^BLK)p8341I*uUUBbto6j9^1=ijX>F{VCb96bPdR1P(*v*a|NsTNCd+KJm<q'
    b'pdjedFZ@3jEp)WVKygb%!+*l5{{CRU6qst7WVr244s~Yfqi&WlP1!g%lm#HaYs+{X}2M_p24+coWhNy&bA+4=MuVPXin^(m}})c8'
    b'~(5u_9a4ta|R42qo#0v!DF9^7E?7NEf3nx$&JhYM=iQPfR`ELPtU7M!4b8m9U`ABx2IH7HJ4;0;-W2K&>@AYmLAX^8n%-'
    b'0qe}BI$sgVqnj3D@3ZewRbrjP2PpI#7|ZnMu1A~2K^|glSv99I`D^RXZM4Nuaco5WfDu*0&%-B;2S_-'
    b'9Ave5k=P_d$$<Y3~C?r0Yrj=Y#0?TY^3=viAfRNg`qz@L4>baLW)xo7{XD?3crkpQju(UH)3J@}N6avpxh^{Vaxrd>9Sze||vxlJ'
    b'OHwetNgRHIRr%5hm#AImyPFoE;_fDe5)}^%Ch-}vU=1=1qwW#k&UE(?m=1-MH(jF~gg5ZN%-'
    b'Rc@184{LQdG8L?!Z08E_Vun$y)?zjM=7Ih!mTgZUqbjVh03b?ev}lfdms^WmX-'
    b'U#JGNVf+G`ALbe?x3gNg5{E1Hr9$3j^iW!VLtCd_Dg9%zDUnTgG?zNpHxjEe`AZMC<PL!g=MY0K_9qCyqmgb6|m4>;**ZZx#}40C'
    b'L(#A)X0wiq%?8VV%hkDE{-n09@StJC}n32sg2hEYYx-'
    b'L*}l22+c7UsHXzcAmUBCa7zfJ}<@3qv?Xz$Xj%^8cDhv8Vd+BX7$bA2wmmVx%%L$hcChVs(3S;m(vDq;O$7+av=>R@1kR!u5J)_S'
    b'4j6XtPdKoB+_qPsh_GQm@L1Z{?QEDWb<%Oh^MBYTvHfIao28Q2Cz;om~}&7=Q;*UUY@&~qV6Ky;de{=|A6u>RfST(#4;RN)kKg(('
    b'+wl|VL`d??#fEes*f#2H|K^qhVK2^tAA&XNrOIgNO98@Vv#?>Rp5{Zq#JG6#)fi+J^`vH3zSnwW{fbE@OQs7hZa+>+Ghb?r;<AR0'
    b'Szx0Z!?M2uuzp3t%L_6*XA<^9TBgpm%G264HV!F8F{2nqoH#rI-s6Ha@7n5++H`k?4^9lt9<ZYQ$-'
    b'=gsO~%IbKl(r)`+@ldg`UR+Bj)@9mUf?%xQW^P<qo;EuVUoB|c`MZWgM4XNek|M-@t?@uF%jgoacHHLxA>a4$5rD#0-'
    b'iTk58}wa0;wiSC$b{Pe%c1ZN|5%{im1%S}L$9@qzpSDW-'
    b'j#U@~Wfy0%ex>h*v33W8oqrZK_T#nl2&BJTN)~25({dH7VIUO5gJq$xr$xb=X9hwfau-'
    b'0_nVY+Xhdc2b>0H;p6L?$W7mInIqfvjGgCEW3_Ctb^wbJb*bZ5jA>DQTi-'
    b'S}(s;tS~*)EG}NO*_JA()py#(v`Mxk`_!PMg>`d5`Kai|)QGa}kUwmzo_%!*`W{*LC-SxkW3_H9D8WtGOlb!lmZ(ll{mIZ2eIbEP'
    b'(0R-G$^(M$I-mNkY@nC=i3Z(S295QG8Ym#xd2WSM+CJY5c=Nrw3X@3bCG-'
    b'$S%TF`uqHOlMe{Ze+r)|lHi&?j$4%tbCodvhv2_2Xk${hnzuQuClqVpvZwci=rWC>9g>18VLQmw~JkZz$N!n!Kn`}D2%MiZ$#;Az'
    b'Hq@8OTnRwY@=%0oakUWxp<l<+j)P7GEfdCXgzzzE(nD!)EbSnyFRXG0LKdO^Y22u11`GS--hcvH2V_mwG?UzWyGE1ocNZc(jNktb'
    b'3!t=OJH=S_>iuErNoQGXIapRj>~gh9<a_PbkTx+PC-3J(OlqRCNEE{*C~+7k+4f9~40t}|i`a!&@@;CTo03-'
    b'40MUlRQwHc!*V>Hz`-'
    b'^*k(!BvA_`D=XVILzft|qQwqCFpc~v4u2;^<n2Cf@AR;Pmi08$&>eWvCRsciE;y9h8Oq&W`KuJXl~F~jy0K(=*A3#*N1wd(Q+imv'
    b'@N(s>%oEfPvTBIC1`H|oBxjCrB|e9pcV4yiIqs>SYW0_j-hapNzm>LKzi&1AOEFxH>Jnxxb9b8rn4^mvhsrXx6z;Mvo~>K0eXTvh'
    b')}^Uutx!LN_RIRTy_4Yi+r$6rKJ{G2<j@Z7Q(P4YWijJ+<3RfJ0LGAVgv*v=6+z&bn4~bFE5hYoCi`g66Qx7>f>ISGA-'
    b'2fRp|A7jjyD*lx|9;Y2&+M@Ep%UX+#A<<d8JSVGsI-'
    b'L)U>r*k;>f6&s6v?Yt?m;CPNJ+b6f$*aL^&Jgk`CvcNxW(b;Y%k0jwdsQUj$$q;7WObM~Sfm82#T=KJYU&9^N~YROo8_W7Bcm#$m'
    b'%=!03^2P3%METD^qXbol&;OcSJD66SEC_e`=rj9>T^$`=A@~wn6;0SmEE*q6sig7H<Dr;(}y5*QpA6~VOqgEXd&Ct_DXKrk5y!=u'
    b'Nxf{wZTTT5$>r%ou(9YKo2<i%ON(w0Gn6A)$GRe=10WI;)UmDU&-'
    b'%a=P1y*SywHHe;)NiDV0N;CcCLNzE&xpqeVccaL)xhW6&$xfcvZ>DV$1h(Lb|Y-'
    b'I*{}L65XDVLF#IsruAGvi;_+0bk`txeJ~yH2^59f_`y>*8ITu74{kFg>DvyU}uZ#fi{Bb=#i61H%>PZ`J{nOj|muv$6ZOx$Kiu2A'
    b'MRluwC4n8^}YA5NoJoUMn+Omob7wTc3<Zc06R7-'
    b'hZ``ym=@v3h_&6NNPfg8Q2nN4?3El_$zY_RY;$z+c@^#g8(+GrZFu@w8tt8d>rXW$QV^xnk?7)#W>Wi6n6O}SAE`8=VuhAU?D^sR'
    b'*m)@N0wqb@K0Y{{qHi&nA2v0yGWB)s_gh(%XhL4=ja0VHg2f%OTuJ8M1m7JRhtJUV_Sjpvu#2KtSDfBhVjzI$U0blv>uE1o>j20#'
    b'T-vRz$?B~rTa-'
    b'J~|T>P*}Tj+L*jA&xKY;Q3DPLzJI7=8dr+BT?<pam+J`44Wy4kmAYLSA(qA0rSuUM+Q|1?eOT=n}`i(Jc!gDdOuIT2H>H5w6adlI'
    b'9qHx!f3Q-sH|OYdp`S+erNdsQC8H7_znLsbCg%qb;}IJU{C}-8%bx}>F5?9Db`hWoxJG+7Te|5-'
    b'c5R?Rm?BhCh)DjtuUo7VNuY19i|fl_;u~HwK&>H>Zx*P#ue>g=zQR&rE-SWZoMy`mSqbNvT;%mIkud-'
    b'a%T#(ZL7)4QAzYNsEbx79TwGcT5BnKUE?z!3YoIH)Mb@nsHMzFm`jDZAmY<(sG2;%&%=uuoPWqFAY!9twEiE&MA>5&U}6cOQI2|Z'
    b'_Jd;2LFpg0AQxqu@EvqSXtC^#TF~7(-'
    b'qz=O*HY^oy7UVP4{EQfG~|w~`O|IErQ0oPo`V=k>x`UkE@$(#P3)q4&R}fiGA1*?Oe(vTX+YDkNHq^)`c6uHmnuuZ%urPT0pm79*'
    b'2F)qYB~|JSyd7~h!?3upi;RY0pKcrbSoT6Z|nM9pNqwlTH0y=2yN@uzVce&-'
    b')!qI1m7BneJdp8M_E*ky*A%#eC}>jr@9N*UD!EP_u#H=4#xM$eoV3b%IKF^n*`%Jr)M8mtt7SYbk$V#qRFxcyMc&PrV3PfkV<(8!'
    b'#UM^ntg8W0e(W?NY|+Ltc!12>XzX+Bd7=nGL&+F(~{A`E%mO{vK#Hp@~QI;c|AGWX$N&{ggG>ZJEA|gTr<+Cy3(7WI~BH5k-'
    b'Yf3nnFYt>io_I`djNq@ntOitFGF9DdphYijVK{$aKb;Yc48o({^t~MCo>6C*I+*TNx}P5Y%T%5bzY!r*X|ot?-'
    b'nbyf;)T6X*=T#jy$H@CV1iw`W&IBaB412&m*JA@&G#N89{N(0A^bKv|$B5JTI|?2Ik)ood>tsBib_I__W*fkcaZz%}zlM}C_pX^Q'
    b'{#|NX<?J^y*02i|!Vo=%lq!G$W65l*E$cN&s+Ol4ObW_gqpMGb4}YLct+^;y319{Z^GRmBm4W@;e1-'
    b'5{?bar5L*LE(1St%Pgzr#a7Y1mX47F|Lmt!p7Bv0|E<y2xT#1%TI>i(tWPZxARa0BVN+fLOe_*9Hs!l&F8Z_HF`=>RnIQ_TLceW1'
    b'Fjy`b>9xLPYua>LSix-y5~s!#Ul&GLhlbJn7km-vl8Icxk5Y!iq1ROpKgj{`WFJjb*qr-'
    b'@|3HiD~Ib;5z{9n9G4&>4rOGOu+r%=m#mzz9l;<3{!l{Al;l^kuc`ZPf9^RM6T$GErzq<2jPUPEyPs98y^7kZ+&*fCb?178m?0Ga'
    b')D;6H-'
    b'C91|*1hAGrd_}HJpMw8=E0_U***G1EdzlCEg3ID^*RwL^pn*jMO#P%sXdkd#&_+jMj$nQG)Ol@2y*=}&7n__@#<2N8Ft=Fj-'
    b'$=`nMTUF5vK@iMa`kq8JQt}=Vk@0nd#9TWoURQnhRrZD#}%}uBVx1NTY<24Gs;bPY!8LI@;K;=W@T)XVO=0V~jTV2TLXbQA;!RaY'
    b'LE`>5zg|VLWT5H9Qb$hHfZFj@0QXz1&N2&iZ&`9;R!&Pd02ubw1#KT|qZemQlO<m8(sCL8%}m8Cik|UAgA{pZ_1fZ~g='
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
    candidate = rounded_avg  # noqa: F405
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
