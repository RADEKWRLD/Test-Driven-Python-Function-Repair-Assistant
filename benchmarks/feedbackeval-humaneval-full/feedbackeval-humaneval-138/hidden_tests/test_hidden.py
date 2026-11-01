import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[4],
 [6],
 [8],
 [10],
 [11],
 [12],
 [13],
 [16],
 [20],
 [22],
 [24],
 [30],
 [36],
 [40],
 [42],
 [48],
 [50],
 [28],
 [41],
 [21],
 [39],
 [23],
 [25],
 [35],
 [19],
 [49],
 [51],
 [52],
 [47],
 [37],
 [34],
 [-79],
 [29],
 [53],
 [57],
 [56],
 [-2],
 [0],
 [2],
 [5],
 [9],
 [15],
 [27],
 [100],
 [105],
 [8],
 [-3],
 [76],
 [101],
 [98],
 [3],
 [97],
 [7],
 [1],
 [6],
 [99],
 [-50],
 [102],
 [-71],
 [-1],
 [-72],
 [-27],
 [104],
 [96],
 [10],
 [-26],
 [-39],
 [-55],
 [-29],
 [-66],
 [11],
 [14],
 [-42],
 [4],
 [77],
 [-38],
 [-30],
 [-25],
 [-34],
 [78],
 [103],
 [-65],
 [-49],
 [-18],
 [-7],
 [75],
 [-37],
 [-73],
 [-51],
 [106],
 [64],
 [-52],
 [-8],
 [-6],
 [-10],
 [16],
 [12],
 [107],
 [26],
 [18],
 [108],
 [109],
 [17],
 [110],
 [31],
 [-98],
 [-87],
 [-5],
 [-40],
 [-88],
 [-4],
 [55],
 [-86],
 [13],
 [32],
 [54],
 [-68],
 [-90],
 [-91],
 [-78],
 [-80]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-'
    b'rlkJrV*T428AOd)QeyOMpN+FJciO%=TWu%4*BC^0MxD2FLN|aexo<c#nk3=62t$p6fL4r|o%EiabxpI#3;oaI}HE7PCC$P9=uia*'
    b'Iy9<`Rjd7<cc;DR;+4EjSH9il49ZxPBQXwJO|G;+g|_i%BWv1tRLZ)ZlwzOObQp#@a-sY7MHv5?Nh#c`fF%iuy^3fdS_G6Alb8-'
    b'`^Qf6nq1T;Tz1wI1Ms|ghS&0`9R~sk#I;1-@rG(p!p&UxGBtj=u^M|gGUsZdJo194@(f8WB'
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
    candidate = is_equal_to_sum_even  # noqa: F405
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
