import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[2],
 [1],
 [5],
 [8],
 [10],
 [12],
 [14],
 [20],
 [0],
 [15],
 [23],
 [21],
 [25],
 [1],
 [14],
 [13],
 [19],
 [57],
 [22],
 [24],
 [56],
 [18],
 [False],
 [True],
 [58],
 [12],
 [11],
 [2],
 [26],
 [60],
 [4],
 [59],
 [16],
 [27],
 [28],
 [3],
 [17],
 [61],
 [10],
 [62],
 [29],
 [30],
 [31],
 [32],
 [48],
 [47],
 [46],
 [55],
 [49],
 [50],
 [51],
 [52],
 [53],
 [54],
 [33],
 [73],
 [34],
 [63],
 [45],
 [72],
 [98],
 [100],
 [97],
 [71],
 [43],
 [9],
 [35],
 [44],
 [99],
 [102]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-pO)JFaCrZiel^o`5IOkwH-pidj#@fhbYvyn&88a&*J%`TA3Jtr|fUa8T#5w-!bIFYbT-$N&A~zy9sVzyJC3FMs^!-'
    b'~YC>k3awTYik*&#O=$joGH2d);3*2PPTno@6t-$Gs0z<l(KuIOw%aUr2qN9fBx;?|M+WZv-QKT+7X}8THm&^Tv3lIqFQSytM1I$G'
    b'9=18E9;RyLv+jic?>VzseSfqCa07;uV;i>j)-'
    b'9`%06D~>`|t+d8fv0?Y49G8EW?Pm=@i+N2^)IWv$w!nD$j>k9)7L>^WpqkC|oKsHWFWv^}e?;pgWuE;>|(`kK^|Q+rmv*Kx;PYf;'
    b'{ouC`8-I{5Cy4m#;qv(GWt&tr1s+*?{*OPss47_Hvbd|&#}vPCO<-'
    b'>$P9tK8CkYZlqP(f6{yW2~OKoN_(2$+&y$kaCC7%C0Iib+lM|+(+Z&v6-'
    b'TmbLT2oziMi_j=bBBo;Lj2ovm4{s7F(x)_I(>xyUMDMC<GnKBDw0Q?~u)fye0is+?(lDigNd=**GYM)$F<@RN)pqfKS{^nPz+)Rn'
    b'>R^7ELpwfgo}MyUxdr}x;y`m8zn>b1z5c-oj!Pk?a--AejwSr-lYssY^H>h(e&O-'
    b'qr!T3$7s0^I0y?b@nZJGpL_A#}E`B2BW1eJ$QiA}w;%-OjE6*k`xC-'
    b'W4Oxa?muGKO?Hg+TL6=3P=mTbYFgNi+>Ytc7gTvP=dMI<>7bL;eCW<PKlV7Yg5sTo4KmRT;pUdUZQG#)kJ26uo@=!_8J8Qs+HFC)'
    b'cbhC7-ioK2EUZ^yh837+3rCcKD|lWK?^r6D@c-'
    b'akH_z0bh^9Eowcs*x^4Cq`)cn~e3Vnqk+b7t_#AT8OLpoWvrE;(oC4gRN=dSsOm5iVu&=&G8)b|2c49VP<L5CG9tl@RDYuPVM%PU'
    b'P0ZIq0F7&7EUWWU8*m0Vt?SiX}u^`pg8z2or&)V9&3W{7MZC);k&heGV0m4juH1^DWx&digw2zJbwRjXCLi<s@?gzcgcYj8|PL5H'
    b'E!R2;&5dt(chIZ&tLN-&#^zwV*_nVHfg-orP2swrXm9@;xyjx!jxrnI;38+z9$f~v4!&e|{P8;O<@73Z)V|8t)C0xxJ;eP166cq<'
    b'@wHbh4JWaO8rt$YEvZ705EUn)$zsG#hMOQc}5}Iu;l<y2&QudEGwb0fjKz9gc2oj}_6YfEYqLM$4S-'
    b'mK_uQz3@dV(UTfNBhev^c2GqXliHf_Y(r*9z~?J;=teuQ%LuGR}@(n=!1?5XcVIp$2-'
    b'o$3VOL0=sBI>OzJN!rg{VW4NCdgUEt@G`}2Rb#Al<#lO*XZ_uQBN+Bcg)_xY<YudSzPdE5lzTO0Xy8UqJ8Cc%PEOt8`zpY~qiZ_^'
    b'{#C7XZ!O799&c&2JmYwZWzqH<OK*eR2w5<urf_XlY(E#@|E%2CrX;?`Rr3m2DB4mAkl735lXy7sXb&-'
    b'G~Q&)7}P;e$wQp1?=wa;|{*N%TFpxn6?Jp5kVI2Lrg4%7=eC>N=PXBI31XDErPgwf}tqOld{I!0cS;ccUApZYCg&<_(CPtCk|!+^'
    b'Jr!?8M;?3`d`<LrfM5XzJ`)9scnm$v@iw6$_96r{ZA<m7%EV;QTX=?jx{z_4h=hT(NrR5GWZLo`4vklW80ctvk^!|6<kSx5lglwx'
    b'!toY|@K7Fs!8WLiHkO_<zp=1eO3CY7&k7!}y+G3w|~w16-_=ZhlvQyVx{Y#eP%G;-'
    b')(7_aa@F8eFAJ>Rkg4c~2AILeQ3r7<b=4jO}*VR>USMW$5>!%(?sef)9;bW=$~&7fjg(qU;-'
    b's6fX$VVYi)IJAzuWB`w*H6J4n=i`j)%YMtsd5Lgzter1_95d#ArqcK5Vv`Kvpm_s`N_Z=Myd+--'
    b'ysF=%1T*S;$D5Pj+5Ld5GftUHUbsM564hlyN<6=Lb}mHMb{>9pKM_qFpKw4U4ZJ5pvZYSWesQG&B@N^UVJ3{7(JRDz$-'
    b'szgZJgu3sM)ld6BkLviy`0y0YW-'
    b'5Hct}h?#q;<7YI?_HPJ}wC59+rZ+?1HE0j{;<wQB%WXwL>MSWuqk}dXBF@CznCenA@l1UUBvkG_6Pm71<=Gt8z*bK2E8ZM$h@L*|'
    b'>xpOyK85kyFL1S-rJghHi&*462Kw_H}R;s;LD)ED~b5WRdxuh8-'
    b';uz@(yM<MR+sEFaq={odBYwGNPs$IV#cD<99e6f=iT+re7m(yWIaaiYCW*a#+i5$F3TeI;gImOxM?L&TXDIy)I)E)v6tA9VA~9l8'
    b'iQRZJFr<F!0$TLp=P}q+HF6_i=IJ0Vy=Pa5h_Hg6k=-'
    b'};5RJ^;e#9Nzo$N5?z~6u2W+ys#pc5YT+{!0>A<1zZm`lH;wLDZv=)G<f&YJkJm^=sj{BZNqp%OgG0(hO#5UQXT@yp!m#_*KQVP2'
    b'SkYogmwZ-Eh<weqWPQqJl0N}*Y#7EF|ET9HhGUt^<yg9r}LDT|5WVmJ|eCN9p^?sp6;5#qu`gw)S$3hoa$9XlYM8sj5(VqWABs!&'
    b'0bSf}=q302_Dcg%XsCsyFE5CUFSV?rCzAKVMULbQmXf^v35xe}-'
    b'Zg9YSHi2aV~<f?k_**)<o<hQVCT%1e^4(l?Hx87q2lS}n*+?OOuIV8qr`t9MU=Hb%qV(x&3kN~#)^m}JO&%sjo6b*6;Z&d>J+L#?'
    b'FmvYG&A2lz}BM7tUBa;kCdB+{qj}rx6AZRSQLbB<(AuytHrz4rF2+R5<TP(~9Oy|?lg=+PY&L}&Y%hmmTT%pu|S)<4FAgx9zXHU|'
    b'+kMs5Bwlc}4(1Cr^g7r0r+e-'
    b'oC<;XK^aS{%(D|5LOQDk=Ok&BDRcZ?z;TklH<+_YT~%BsT>IfFK%bNA(K)=*+CaDnNDPFT4X<Lx=$r3kxtC|gY+rh^_-'
    b'#GfLF1LhE4Bkb8X6e!?Mz&eJH3!2mIuQxo9eVAO&PRp*2{V?C&^fuCVCU0~$q?|18oZwJ=nhOAjW+dt_CV^Ct&g-'
    b')*w0}KHt+9eV4PTtq5cy%D-VTR9iDzjAo6gAIM+3i-=;g&MqcHIrmPz38)ficQk>-5@VDjSmSmYLeLYRk)c;RU$QvF(>Ng-'
    b'(B#Pp%_`qv&$!0S)1sw>;(0KJ$tj?i$7O2Wh=*}3EVkgfdh{|9))k{A'
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
    candidate = fibfib  # noqa: F405
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
