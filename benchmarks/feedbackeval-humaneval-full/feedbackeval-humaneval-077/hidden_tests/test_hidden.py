import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[1],
 [1],
 [2],
 [2],
 [-1],
 [-1],
 [64],
 [64],
 [180],
 [180],
 [1000],
 [1000],
 [0],
 [0],
 [1729],
 [1728],
 [-8],
 [27],
 [125],
 [729],
 [512],
 [-27],
 [-64],
 [1000000],
 [-1000000],
 [120],
 [57],
 [-63],
 [510],
 [728],
 [999999],
 [-999999],
 [55],
 [123],
 [56],
 [26],
 [-1000001],
 [730],
 [-7],
 [119],
 [-28],
 [126],
 [-6],
 [-62],
 [58],
 [-5],
 [727],
 [-26],
 [-39],
 [-1000002],
 [-46],
 [999998],
 [726],
 [731],
 [54],
 [725],
 [-29],
 [59],
 [-47],
 [31],
 [25],
 [509],
 [124],
 [-40],
 [511],
 [99],
 [45],
 [-45],
 [-999997],
 [121],
 [-48],
 [4],
 [732],
 [-726],
 [1111],
 [1331],
 [-13824],
 [1000000000],
 [-1000000000],
 [987654321],
 [-987654321],
 [-13825],
 [-987654320],
 [-987654319],
 [-13823],
 [-727],
 [-729],
 [-1000000001],
 [1332],
 [3],
 [-25],
 [2],
 [987654322],
 [-725],
 [5],
 [1112],
 [6],
 [-1000000002],
 [7],
 [-68],
 [999999999],
 [-728],
 [-24],
 [-724],
 [-13822],
 [-987654322],
 [1110],
 [8],
 [-69],
 [-70],
 [-723],
 [-730],
 [999999998],
 [-23],
 [10],
 [-13821],
 [1113],
 [122],
 [-987654318],
 [1330],
 [-1000000003],
 [-1000000004],
 [-71],
 [9],
 [81],
 [-22],
 [999999997],
 [-21],
 [-987654317],
 [-75],
 [999999996],
 [-73],
 [-13826],
 [-2],
 [-13820],
 [82],
 [987654320],
 [1109],
 [28],
 [-41],
 [46],
 [-1000],
 [99999999999999999999999999],
 [-99999999999999999999999999],
 [-1729],
 [-2147483648],
 [2147483647],
 [9223372036854775807],
 [-9223372036854775808],
 [1000000001],
 [127],
 [1108],
 [1333],
 [130],
 [128],
 [129],
 [1107],
 [1334],
 [32],
 [1336],
 [1000000002],
 [-18],
 [1000000003],
 [30],
 [-19],
 [117],
 [69],
 [118],
 [1000000004],
 [-999999998],
 [-94],
 [-1],
 [29]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-rmQKTd=p5QcFr)T>w-'
    b'7+`?Ti&zXWWP2}QWwqtE_jThLHt|m$YVs@Q&A`CN!{sU5eXqCU`TY2PGAVkTU+bD(cda^GmgJ?H)K+rqmUf>x?V(<awyH~Qb?eh+'
    b'Hp^bcXYA?tJWlsFV`h*UM%Us&k`4D3+Lm#JR$Jw|&)O&=eYoxvC7SN2E-'
    b'OdNxsMw&zpFMRMN&VQ6eWhC8DL;wU|?WiU|?WiU|{$L;^hnT|C)gk!@$76aHNwI3=9km3=9m@7Sk4i6F3YE3=GU)xnTU|3);1@e*'
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
    candidate = iscube  # noqa: F405
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
