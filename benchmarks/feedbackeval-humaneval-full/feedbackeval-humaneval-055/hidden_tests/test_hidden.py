import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[10],
 [1],
 [8],
 [11],
 [12],
 [0],
 [1],
 [False],
 [True],
 [16],
 [2],
 [17],
 [15],
 [14],
 [63],
 [64],
 [13],
 [3],
 [71],
 [72],
 [70],
 [35],
 [62],
 [69],
 [12],
 [36],
 [34],
 [61],
 [67],
 [4],
 [5],
 [11],
 [66],
 [10],
 [65],
 [74],
 [73],
 [75],
 [44],
 [28],
 [18],
 [6],
 [45],
 [68],
 [8],
 [29],
 [7],
 [27],
 [86],
 [60]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-qZYIg({d4Fv-{_JKu6snq2CjbJDT#rN3&7FL_hCRqh1iGH<$GAN@e?yGk*HJs_6fBN@-'
    b'{_=<a{rvssUw{1hAHUa7`}yNHaW#&?YfK-'
    b'MS-y3d-o<>x7e`dnR@pWD`j$m8&ZcC`p*s2JzkdGy#~;7VdDr39THbVmZe`1iq($e>eWof+mK|#)nG-XvxfDJYi<AC3CS=9Ac)sz'
    b'zPvds5?xnYCXR4mXUXosW^S-'
    b')PpS8y_RF$*GryAW&jbqC8(A?5ti_*=fjj?s#a<@50ahPm={gU_E_pCYM(^Sp5t%_$_u6w0QM91cqeN&I33a7(tbBS2jxfY{wC+!'
    b'wH^6MC$F<;>_4`r;0>bx#Dja))Bh6r=v%)2%jVdkf<9MV`cHud+8`2VXK%#e;s(v@jxrzLrcOpoYGO9rO7th{;}_snJ#&K>)7A06'
    b'_&)i~Yjabq0<+}Ot4m$C4SOU6z_bykZkeRuR4e8=FkZAq<+&oRXeGEJUm-YEk|iYIkXAdC~J#vh<+MYdt4ogUhDF41P!s$a+4z8t'
    b'`+TWxU8bS~f((?~33mW?J{6RUmFjXnJ|DqqriG6C2Rr&vneQiH(aopM{)a4?4`Mivn=i}o0W&kk6hSEv`Jv`q5DDG-'
    b'3%@w#&4aqXD5$+Lv-spTN54DY>#(WYuGm65E_i9;@**%%Wvq=lS@3&bY(o>v}6bq>>k9%mi%Qf#MmZY@3dZ4&};Kh*3q0vOd9!`+'
    b'qe4wI^^?FQO!Gndo?M^X13<)_XBQO(0K<4;q8+c$|Z2%Bix{ea8svNG@$i*M8oJ1d+DNTAC+&U~c7-'
    b'Sa~Ry#p%HS2iGf8r4!6AKwcVTmS@@cK|DdH3Bp$?iU!xZCY5~2gS6r0yl@Mm2?3^fUge&XwKlew4qxo*F0m*mFW|*w4mEOWUkMq1'
    b'S8wM>%n1Tzh>5s()8`_JW!tthyY4$<8HnXcMxK>#8}HeLV;rOC46f)TAv3ih6DzKX*KaIO?g2`(|w4KDr?k^&5E0wK4gGemR6jHr'
    b'w!6LK<38gyC9Nd=T+<Qn2+p*v7*kk4tQLK^1fG##~nIp?F0q`D_&edq+7O4yk>wPW+Hy~fF=c8NCl0~!c9}+OVR_cq5bi|Nx%mlR'
    b'G}r9BhYcsK=?drhEL)Z0#EI+56sJH&ku^xzhPJDePF^Z7Z=Y~X}c>%IOME0O=>>l^bQ5w*Ays*vY35llh^tjfWQIu0nE{L-'
    b'Z_DbJEW*Ub38a7%x=%Z`v)t-'
    b'*E5?woHEOtfl4qU5D)e^cLRcYHz~Y#R)$?@5kQ1ehurYp6DBO+>(^`$At2$8m3v}`52S!7O#O@$o5!|DmSL!TI1O?RRdJkt&NQTw'
    b'Z}xDAT^ghGXkD`9@;+gZCur&*2a=$l*nZfE$4>(9XV&B5o%Z3>H^n4%OkQ#-!*tIOSOJVpVOdzt1sul(1!Il%>H=4J!-'
    b'+&T90NH0j98!w*bU?Z(+6#v9qzWE;f;0ynjO>N@^ejkN(zBIBz<ve0$g8u;|vg}g<}}ca04#@!=zv%!+lH+1BnNSL;}Of+hK~pJ3'
    b'g`fwJAqV$O%135Kp0`7mM4V<f#qRk3|zin`o~cxCTF6K=vbW5^Vn0G1!M6hgw4+*{{_KY!h`O7yxwy{q9o)t0+$GY~Z?hdBJA4$!'
    b'AkJMs`A2;p1>77yvYb0Y7>pG$@M@Yr@z9%|~N%Cm-'
    b'c=G~?f&WAZ3EdU>EC*AC1H3k}7Zpav7^gx0EcPu$f+kY;)iK|Xa5>9eUPPBu~h%O9r-'
    b'#a_y7%+XSOXcbmA^jHBYui{ifVPLs~cpssF5|3wPSmAiU85a%s(DpY<(3`d$EDe!BiwI!Oez9dD<t61;qQIfZG5aD@AqDwr-'
    b'c?v0z%G~<wij=Y&`V^95DPhTh~+e-'
    b'p83rw9pMKX2C59K0bHSy&}w2))q7jV3s)Cu3|4_e=nhJx1!jzyVT>O#3^s@Xy4+<5shTf2vX7@dk%QnkeL;8xlZ)JfrV>*b^6Va('
    b'@P(WE!V4~=!chwlDlh`d+y?=Rpj`cg1zy%*s6XOb5sn8C;I$uT$OF+U2n-'
    b'UI!mWtS9z5|TdLru4sV{F}K6_1=D~udjb;GT_KgVDn{6YXS2;dC~K?j)XGxKLo{*o6$-GyUhB1{J7g$M%$P!)JSj=6vPFZ!tgIR'
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
    candidate = fib  # noqa: F405
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
