import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[123],
 [12],
 [3],
 [63],
 [25],
 [19],
 [9],
 [1],
 [1000],
 [500],
 [777],
 [10],
 [15],
 [27],
 [35],
 [50],
 [89],
 [201],
 [51],
 [11],
 [26],
 [778],
 [88],
 [202],
 [28],
 [200],
 [31],
 [30],
 [999],
 [32],
 [36],
 [87],
 [779],
 [998],
 [203],
 [86],
 [33],
 [25],
 [14],
 [29],
 [34],
 [24],
 [204],
 [13],
 [23],
 [780],
 [85],
 [781],
 [206],
 [16],
 [499],
 [84],
 [207],
 [17],
 [205],
 [997],
 [199],
 [498],
 [9],
 [37],
 [776],
 [775],
 [22],
 [19],
 [52],
 [83],
 [774],
 [782],
 [78],
 [21],
 [208],
 [773],
 [98],
 [209],
 [497],
 [772],
 [996],
 [18],
 [8],
 [53],
 [7],
 [38],
 [79],
 [90],
 [20],
 [771],
 [97],
 [82],
 [6],
 [496],
 [770],
 [77],
 [62],
 [91],
 [783],
 [502],
 [61],
 [210],
 [92],
 [60],
 [12],
 [93],
 [503],
 [501],
 [76],
 [75],
 [59],
 [888],
 [555],
 [400],
 [978],
 [505],
 [506],
 [401],
 [979],
 [504],
 [96],
 [556],
 [887],
 [507],
 [889],
 [508],
 [554],
 [977],
 [402],
 [399],
 [553],
 [95],
 [890],
 [398],
 [509],
 [886],
 [99],
 [510],
 [511],
 [891],
 [94],
 [552],
 [551],
 [550],
 [397],
 [885],
 [980],
 [396],
 [884],
 [100],
 [512],
 [994],
 [995],
 [57],
 [395],
 [892],
 [557],
 [982],
 [993],
 [80],
 [883],
 [981],
 [983],
 [58],
 [984],
 [403],
 [404],
 [5],
 [976],
 [974],
 [405],
 [985],
 [4],
 [3],
 [973],
 [975],
 [893],
 [39],
 [494],
 [986],
 [101]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-q}sJCY?u3<Lu%f`dhrKK1js2!=jYfzJi7u-07eOZGAoTtG$#V@$kxGp$x-'
    b'DpOLw`SXXrf1>Zcef{?J=Py70@w;&!U%&k7hi6<5H<Pusox9p5BO%com-fEWrYx0q))Hl<*?G0Gn#k7q^{=nLfB)rIIU2Hfoqf$$'
    b'w!63K9KxJ>rB7zjHpbrG+Eg<i{W_g?;`DV|`v?<k>rC!WlrgkZQ*NDPTA1^-q|H~;@y^&S@tZ-'
    b'`j<ax|$JR%fBNo(IbIZ=vnrMVxN=ct*-'
    b'EoM<?q^xI7CL*&txJY=pL{&@Bg_`tckFW|BQH_EliHp)(l`m(xrR4!>TZ2&5}W&0F^<fos}>tqpwekc7r#2r;@#FxnbCP9<9_S5a'
    b'X6G&Hx4Uuc&H<Prf&HeW}KK;h1T4F@W?%_&t;_4S3e*fpvvsMbL`A$azy8h7T5Z4{|KXF;_baD@b?6$<!)y`-'
    b'WVYF*w$62M<n^Q1KLI$;+r>kANkA%_wvz3cOT<uvq?b?PG=Vh6y6+XblbaMfRP}Jmt3GCd`}+w%%+=e8`SQN?jx-'
    b'?JuMf3WK`@WNfeTY$-'
    b'e6M1THq7cjg}Vjx}o`E+V|B{JdY}$<cJKJD~|xXozg!Ty(je4w?w;m{PVjY`2Kj{G3h~fPRMYg%oFwN&T2xIC2dZyg9BJR6BCbGY'
    b'0asBeOXr^P)igtaj}qj5WGGG!!WUZXTUbLYsrv;NCVObz~L``hE_4=D4$sXjkL0oKK?wOxmBS>y7y~mVx8V%REV^N<1zVtZ*=AJF'
    b'1SHvoA*_jWtH?q25J!kr;}YqGr631bN4t=3UL<*sJ%I;)ga`4#{rq=|p>3j0U4$eA4A1q86K?x+%)0C`^$TzsqmdvF!#IPJwjh+W'
    b'2`RWyliU{p_^iSL~Tq=%y0Q=Y<IMn8Z_R#elAJ(I0Jhd|x(^cuzz;sMy<l0vXK%MacDL3Z#>d#X^w>E~Hv96k$`u)Vs!{cU5swHb'
    b'r&wzwA@*GKzOGRWx1~LHsgoioCd{GZYObMTA%Fnl&cMd09;`hhs}O6d$(th1)lb?-v-'
    b'ayRo<LJNs=7tRozbuOKV7FVEUAFMBFbv%wT8ya?iVb%uBOO%cTJ+U|;Ms|cGSORuV%edbl%#f22>orEF6AW+0^gQsJk!(HK_eeeM'
    b'V&vV+AP>aEsij6`d1}^4owpPoW+I(Y+^llx9pk>LzzIlh*FgnQ^A(s=9K66{Va!D)_LlNQcQg{)>E4o6>$F3mpXx=7<9DSa-UpV-'
    b'{D4~Mm;Tnamn34Sm_&<_vI_RB7QG-p<#}!3{S1m#{Och~M)TfFdE;>|^-'
    b'&BnPHH23wye+!NC7HbQM54Gt20G@6wtA+W6}oYPZqMagY27@y0eS8@Yr_-~j;3yiEV(YOlj%-'
    b's*YqJPJC?P@Xpb}Vz*AR_ow?80ac~n5&mUoi=wRFd4%9sSZaVv9poIE>E#p|I6Wn^7-'
    b'Ehv0y(Zb4#>VTEPcH^XXv+t^euy+EYAM4x(D9+5^rcUk1a?A#6*e5QhkMRk_`@^fzo$u&%@gIc2DZzCRX2HJ9ytbYZuemL0lgDsF'
    b'IgSuz(@jncE4T5`V6Dbhm{N!^8nTa+ukJS=$ec%4FNE{VKyN``FOUD*+<Xwu$)n2=r*-'
    b'sim<^TbWt)mXIoFt+!*#S1*M>IJ^g4Hnxr%o!JwlPf;fpG6w{$k+qr8sRb&)J<#!Wf0x2W_yX!O&Vq`uWc)vhq31|ZFBWO!blo2D'
    b'mq4|OUu(N6jFOp_aHiC`ixH~HyYyphi#O5>9A6#)q?+H-'
    b'B9!Bh~82X1X4G568UociH%_1=rg(<?ONDNh$UV}|h`Bh1C+#MaWGzXe2-39BqhIJ4wAQ(^?w?1v-<qYmHD@7yCzA#&Fk-'
    b'c8o8Hxz6T3Ktv@UAdLVkoNOq8|RPL%mCyMGx$X!W0erMTEa=XDAXw72!3{Z{B4TMPZ7n_+9Ro=ow+*a4jt83<@yF;s@Rl`*v^-'
    b'qnY_{(nJ_!I~q$Iqn`KhC*j*-'
    b'JQYE+Nw<L+xWni6Jt|>6uron!IOVs`aT}y#F2L(~u!trt#hY(Ym?CVdsyIepozUeM`!>mK8?M#lXur~|-'
    b'^3iV25pobIA5tiRv_VS5vjHRQ2s8aiY&e8Gnldmb|rNKe-'
    b'B_Yji?Lc$mH#Ls*fz%#>_H(E}mm{Zfl31)hz+r@i~PiJ)PnF@()_rI5G'
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
    candidate = even_odd_palindrome  # noqa: F405
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
