import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[6],
 [101],
 [11],
 [13441],
 [61],
 [4],
 [1],
 [5],
 [11],
 [17],
 [85],
 [77],
 [255379],
 [-5],
 [0],
 [2],
 [31],
 [40],
 [103],
 [199],
 [1009],
 [8999],
 [1234567],
 [9000],
 [32],
 [9001],
 [-1],
 [39],
 [1234566],
 [-4],
 [9002],
 [-6],
 [102],
 [101],
 [200],
 [56],
 [38],
 [37],
 [1010],
 [1234568],
 [1008],
 [33],
 [35],
 [64],
 [63],
 [1234564],
 [34],
 [1011],
 [1234569],
 [197],
 [-3],
 [1],
 [8998],
 [57],
 [28],
 [-2],
 [3],
 [1234563],
 [36],
 [9003],
 [30],
 [1234570],
 [-29],
 [9004],
 [-7],
 [16],
 [1012],
 [55],
 [-30],
 [-17],
 [7937],
 [34981],
 [42043],
 [-10],
 [10000000029],
 [123456789],
 [-9],
 [-18],
 [10000000028],
 [42042],
 [12],
 [11],
 [123456790],
 [-16],
 [10000000030],
 [-15],
 [7939],
 [7938],
 [7936],
 [13],
 [7935],
 [23],
 [42044],
 [-11],
 [-14],
 [7934],
 [7933],
 [10000000027],
 [14],
 [34980],
 [24],
 [15],
 [42041],
 [-8],
 [7940],
 [70],
 [-13],
 [-40],
 [18],
 [-12],
 [-47],
 [-49],
 [34979],
 [42040],
 [34978],
 [-41],
 [-42],
 [22],
 [25],
 [10],
 [67],
 [-39],
 [26],
 [62],
 [-48],
 [66],
 [-20],
 [7941],
 [-50],
 [-37],
 [61],
 [-21],
 [-28],
 [-101],
 [-255379],
 [-2147483648],
 [9999991],
 [7567216125],
 [34982],
 [34977],
 [123456788],
 [123456791],
 [-91],
 [93],
 [10000000031],
 [-90],
 [92],
 [17],
 [34983],
 [-92],
 [-89],
 [4],
 [-78],
 [82],
 [-76],
 [45],
 [5],
 [10000000032],
 [42045],
 [44],
 [46],
 [-100],
 [19],
 [72],
 [91],
 [-38],
 [-75]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-rllF>V7P5Ji(BIZG;QcYpypU&O@#gWTr=sZwpZxvwpkuG3`mIKV^t@6RCd_4ac)y*$ok|JdF?uO><N?c5jXORJiEkzmceEM-bd'
    b'v5Yd(T7#9AL~3)LVU^W%uIe)4YBAOp_V4}rx}EdrRcFrHOO)U#o8)qbR135A7-'
    b'mz?NlVtDHmcQbJ(@+&;{AThkukp%F{b`X#D~NjQaEetpUo86fT1^J0|pE;g(-'
    b'w%3Je%NUf4Hac<#W^8(NHTMiUGeFkry&PJyAtv=~!FOvISN6d3A<DI$Kx_~{1kKRP@'
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
    candidate = is_prime  # noqa: F405
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
