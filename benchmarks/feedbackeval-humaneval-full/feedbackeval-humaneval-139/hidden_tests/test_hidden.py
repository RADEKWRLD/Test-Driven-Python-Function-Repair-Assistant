import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[4],
 [5],
 [7],
 [1],
 [2],
 [3],
 [6],
 [8],
 [10],
 [13],
 [20],
 [50],
 [15],
 [12],
 [11],
 [22],
 [7],
 [14],
 [4],
 [9],
 [21],
 [5],
 [51],
 [30],
 [29],
 [32],
 [49],
 [77],
 [52],
 [23],
 [48],
 [19],
 [33],
 [16],
 [53],
 [27],
 [34],
 [35],
 [17],
 [28],
 [26],
 [47],
 [74],
 [24],
 [36],
 [95],
 [18],
 [31],
 [45],
 [37],
 [38],
 [46],
 [78],
 [39],
 [73],
 [75],
 [79],
 [80],
 [72],
 [1],
 [81],
 [25],
 [76],
 [96],
 [44],
 [94],
 [40],
 [43],
 [93],
 [71],
 [42],
 [83],
 [41],
 [70],
 [97],
 [84],
 [54],
 [85],
 [92],
 [91],
 [55],
 [82],
 [69],
 [98],
 [86],
 [56],
 [99],
 [57],
 [100],
 [101],
 [58],
 [87],
 [68],
 [62],
 [59],
 [102],
 [103],
 [60],
 [88],
 [67],
 [66],
 [104],
 [63],
 [200],
 [500],
 [199],
 [198],
 [499],
 [197],
 [497],
 [501],
 [498],
 [502],
 [496],
 [201],
 [503],
 [495],
 [493],
 [196],
 [492],
 [195],
 [202],
 [504],
 [505],
 [203],
 [491],
 [204],
 [105],
 [90],
 [494],
 [89]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-pO+Io2dO5y!!RlVD)+w1h$-'
    b'Z!UtNE#CNC01Io(=Dz%*sLZ}V&tsYXx>~6W{a020`!D~UfBVztpMU=N`yYS(*YC45{qe_dsWq=T`PCu)+&jJNnL}phr&hJr-'
    b'E~UcC&`o}X{2*J%jSP9-}K`@KYsu7AHNmvb=tCXb2ic1(!FP-RK2^-'
    b'olf_1`t)6Io|5IxvCdl4ZuKqqewX3bZSFm!T+M0Bm9LApaV*a!>)Om|PLbAo>tn2zmp4Bx_q*Fv`7R@J*NNYn-'
    b'P5te)4Ym}w9>h3U0O?$>$bH<(w=hOZQW$OtXz9)-(~z1tNS*w(s^LY!sA=3i;*PusoLvk^R&M1y=C?@k7O0?)^l&=yG-TZ=k{*ud'
    b'Hd|SX^LOmyX+p5&a+2Pp3n9n)l9Ci)xNwk!tpHgIgBN;>TJs9^T?-6FYK9DV;jrG+LWGa8r4?g_^MA{kEflf-'
    b'(?a<#S;$a*%_*3=FEyW*OB`;xz4)l6jzR6t;2r$Eyar!8KoY7PD<JuSpdUIb^5Bi%sFjq;$xPEpJa^odOtfeVD*xVT@%jc0-'
    b'f(NxtHuV?=FnMPOW(rbAFkQkGgct(Wi{zdd2))HZ?Wv)#o^?wewwOwQhWHG+w=>$sF2}JKFBs*vLvig)!T#oh>8>68T!$lb_V8{T'
    b'Z?P&c5ccdgmFyD$7~*9A+~1-'
    b'o|#v44?rgIlBYR)wQ$*CUn>5z#YOcx@Pkn+j(9yU2U%94p8|=B%jlJn(j?oY7Sm>2ace{Gh)51?83u4T+EdTIw&b(dFMQ8sT|21$'
    b'-D3=Nwte;E^<y=yE4`9G6RB)Vem6ULA(2=CNOMoZ6ZS*oGezmY#KaR1<-R3)g>$E^)Ng&h9+g~rnigw;cOP_z^_-'
    b'ASfJ0`3S7@~?$rj9>)>T?DCBGXT82-Tjs&d&bfCfnMpqc;I;^N=q&Bi?@dSTz+f8~1Q%THp7y|IV)Gtv#wyCFX5Hb0qOt%-'
    b'C<DN7&C{6G|Zq29d*%!o-'
    b'l|+}O8hbOS@m*#+%dTaOfow1PG}KC`nr+^e1vx=eVQ_kwALGdeza2hlK{S4?7HcX9)=js!));{dw83X{t#;FqyS2}LPh;Ub=Ypaq'
    b'qee+#!f5T4Ezc!O%M;p_yXKaqY`mV<ATtBaH^a`^4fR4eI4!s19o!;g<GV~_1l|%O8NT(T>vy$%#e?+D%!`7U%Q#v*=CoQR!3$H~'
    b'@|OHvhBrp}*h^_AmD+YK1+sKzJX9btfa{D>o6b=aFUrfHJdC$8o=1ys<@7mOS?;%7!9PY4FsykDXoFXrfLlJd-QMpSU6_rr^jf7o'
    b'yD>(qcMntodDLL#Oo4W3_ofA!R+=eae4#N{hjQDQ5{n2X^1`p4oe+y$T3P!rWJ%Czp#fl0OIo82WO`|9wo55puR9DbI_;F_q+r<4'
    b'*~enkhu??rxC3P8<l%JUT#CblVb;;!f(Y$9(#B?o0is8Xu{Cw5qJ8w!(>7Poi}xi&N3C~ZoDBsWVgch+VarCMcxChXqF7VjBe1_P'
    b'p#jnXwU>+UwmW#P&VVn7Y})Za{pd{5a=>Wb-(}9k)_tBFYIm#wy`tMTa*2u_7RX-jKI{f1smrkk)aDilBC9+vh4N%xfpu~FV>ne|'
    b'<_f24?@*t&ZMAh!Re2P41*WD}j0bd~j88E6Jb-z`^sZf?j8R}YWeb|vVBca%#f#S-'
    b'iD{gMh>atp0+nYOJ{f0N7`#Hs8>Ci_HC(raM0JPKgcno`7#DbhSCkFuIG6I%H4mS{Bbn#ixcmku1LZaTC_BZCc_SIOo}$(cIF>F2'
    b'NG^PIK6bZx%RY=pU{>2NT5KJ*LoQNLjlH#LGAlnG3qQ>39HfF*zv}gY-'
    b'`c3*=>Xg=%5x@)mu^*ceuh<c(iiXLlX!y6BQpyt<CGGoiWWX79^%gF9-'
    b'!REXZs)!jfzP+np19FU}okMp#}*6GgwC{xki$DPO6{=yupIoC<$Q!IoM|uA`&cRL*RMCkdXIGOsI{IU|C|Av^@;p>{>0C)Njft;b'
    b'7l&R6&Q(?JOitpoX8?xPm0k*=M=Avz0mh&3+MQ>bx9Rl^#~KkW}<7ak4zF7Glh7h$kFKl^r3;J1hgnR}|%ubmrdhUouojC=f~%=%'
    b'9YMpP|1*T?7#G7}(!-P$tAB9p(s&{FJR-gjcydw?*Xa<bnv&03N!_nS9tAHno#U=w0N$D&Q0dqKc3C-'
    b'UVT20GSARuWd(0!y{N;Z*bfbWH6$z8ot}k9ub;1-0c3qPqp=YR8SEFxw0IB-'
    b'$+JsaxQ2Br;G)X!1#UAHyL$=2!=l*aL;ZaF8i*PKn}SWl5)^Xu^NVhJ)y$P0vHVizQn*9Dse9HWDz4C*IYCOk{H29iGi?vMCeoFM'
    b'H{ApJAn9(uOev#O@4V>QXbh9EZUPq8$aq8c~g`MNhca$spQ#JSs;_{q55$^#c+646h8+>1_r<ko&(2?cM#ST7394yT>!~2kR`l60'
    b'oDe=l^)X57-'
    b'$7TQ#Yn2gD83)q1gEKK(FWnoS#w=7$QwaH}Z*>j(H={FjRsZzs<&4sd_@9*yp3g#IV`0SyF9;`rQjQ+rS!u$ANR61T@l5S&f)O_7'
    b'aJ}0TxdbpEoASj%3503u%E7_EPzyTL{-'
    b'AFr;tE+(9L56g<s!`4^psITFO4mzsGnZ<4rzT=+u0!12hpaEZmHF{@40%lOy8{FSks9cM=8As)QWfQL*YZ(S(ECI~I4Zo+*zP|5J'
    b'(rcOHbWr-qal#h=3jTW6GKf56`m}dxEaU)<X5{ZbEi{|c3L7<NvsD)9c8PN%j)XQm8<|?0j4jf#$8_}IKMLyQ8AfHX}nU2OQ8eck'
    b'{1}WsHx1AvHxoA}0r9LS=QR7g)g}03J5pcn)*-'
    b'm(ZGUJ0r^aL8wK@$7!v{lriE{jm9zqW_dPk0wZ8Y!B&Mp!2;<$_{l&W1tZyQ5ZI^#CVa&o1%wBNYZP9!_CSxu+Nz;g6_DuF4gG**'
    b'I6hsz4p2Oq~^I5(QJ{Rk0l6Da?KJCOgRn3xKcp3UP9x`gBO1O0p3>1r;VaEOLi3z05N!VTBqx!<(L$BK?Aw<gzRAhd?~heHe-'
    b'`MNjrZ;NlH9Ta<c-'
    b'gK&T_q+LN&^^K4t5J$?#9ssYU5T+jX5c#FS%{VQrGipVO9!mZE^ii~0>ubK+kORQ7=mv?j?t~>|7h~*}su3W;eFf&S-'
    b'Jve0Sz#cA$fLZ=AZ6&aX~gh_5kZW4(JVGeOPP3e;?FTBAlDG)Z4|sD%$&rK9!`-'
    b'(D({kN!^#QLNG|jxnj>Tj9*nqrVL<|vU_rD|HAD;}+!0P5+=LBMj&{pLC{|(;C<Rf1Qe(j^BGQPY#S<`gQdFvW(T5`F0?cO_xJOD'
    b'R=R<EgPo*EOXzQ~rLXxb0>84Z=V(wre9G?_wA;rM8zaAdG1ZY?zw=sa*rdPo#=|uEw3GhP6#HwwsknHIxZg({9Ox^>(2h-'
    b'd!6iQaDEiP$@>jR6SqX1gupXmuB%o}YZ-x9wPqfUk5*Wb`a-'
    b'9ws*!xpbW9?=O4S0n+TgI?;*kte%>TEh7_cM5)4B~r}mQ)3m6m`DodpmUUi=$yz8$993Dqc)6!QhxO^tB!e$5{b0bNBxl9PEfuY#'
    b'tNs(#6w6Ta1#+X_CYbqkU{W%2_dKBCh8Dbp04q}l;?ynI59Vuh_wnACHX>B5M<q$_#zVmwRoK?@qg*;dvI-'
    b'k8w}4~87HB?nBZkm+7qrw=;aO1q6FPInFinxLgYTGKmR6l`ue&iMYGY2!7j&r2CFOp#$*iW)5dmA3?93q8On*flF(clEB(>2<wrz'
    b'Yq!L!xoA9|h{iaY~0ZoOQpLeiX6ROEusLx3dC2C^DxXBuiq$|KDQ=`WmVgZ90b~EvGHKN@ulnwF_9Tq{x!x_A^fssdOuJ4HP9IPK'
    b'PFe5~dO|v%?f6j1Wd`U2Cn4*+xiqM6uOW*?L5I-9a!wF;zlW;sQLPJ@&FqHUFqbYP|-}Yp-'
    b'm^+mZda!R|Kjzspt^aK>iR}!{sc9wdljzAa#C9WMA!s<~SUOycKWl^o5(-i<d)?!s36E^~48-'
    b'EB2!9Y6A%wa$Q^za?p0Ej$^NIUgn2&;mgA@#(s$9z3?&u3dz1rhmf%rmPo7B9PfL{pl!rThUl1PkJpM*A+v1dFJSk7m}#Ae`bXQY'
    b'lL5GYGTXbc^DMTUEYR`hr5I6QI=vPzCzapM}-'
    b'>Vq4Y?10QamJ3x9Q=zZYTj`s_*=i!lb3B0ZW;=;Qh8f%9r758g86vM(iYx3m8QzZiL@uCgq``_31_VwDB^4wR%reVRLXPZt2=C8H'
    b'VH}k_KKmi3AyBiEhhaiodV(~13mUEp9-'
    b'+gI1m)B=1<Y|<@rWqfK=?JTc|q2=NF`4idU~T|k(X0|8b5}m9hpD|>P3=3enSA?d%ta=M%XSC|6CeD;o@<xi?R@lGhG3?(TGMN&v'
    b'Y3*?&c2bbBd4p;k)EGwo8#)S_`1oXs>YOM#JRO8#ft~HpJs(@5mA<t~E)v@&psiD8nTSrpG;I)Qv&r!Qg1*L~9D_!Bnv;M-'
    b'Vx$ps=5cxVQVpB%-'
    b'6z!x~b%4JJ`sqPLS4U@EzRw1nocq0|$O<%yKH4!t4uLgswGt^j;&^U@2c*$(rB|LP(5IZX#|j~f#&6k__dlb=FJX23~sus4{*MOd'
    b'h}kOSyIm(Vh@cI=q5D5{h6O6Mic#0@vW6>FwV-Ox;{&xj>)-YW;?kfYIiCYgWSuhUfGHXKh_K}srBM+m9gr<}Ohjr+@onxsL8-'
    b'O=4rCQKI|4|_o_fOOzZV8bFipXvk`C_wC+5jqww_68Fiq|w^RVx*opCW+7#7ZQbW5#|^dnR%t+^cOm)%VgG0F5orqdkL-}8z-'
    b'$&FXBMXcXV`<s_<=B^xz^PW66nTj+}uTdI(eYh_4SdOWYy>qk<@gf)ce?G+{7sDKrRKEVycmP=+w0hrEkp_GC=j@S}dDs7>0qeeV'
    b'dsJ@*se=|mZq1eD2ov^t=SoOjTH+K%|bV&P&)!b43m^2IP%-'
    b'r_bX;RPDGAd^e+ETt%DbfSo~j`?*AGH#XdZw~ZlWt}8x&rUV)hSlP;Q#bt>a?tG&P_ns)%x+hL2VohqtSCksdwvWCO~=m`feaFHA'
    b'o&oAoO52h2@IcX50g8UUZkmwhRQ^c+^}K(yi3O{7HR_Y0N~(7K2bB1jhH}+Kv*dMOqc4-'
    b'Y^}w83JD4BICy$Eg#u4{=!g{*_W*h9trg#(mO_Fd75)_6X9y)cVs%U>?%v}H?3HxXnodhxU?w3p=<Vj<0L-'
    b'9kAUuS<q@ao_0seOM(KAVql!x@-'
    b'2Fg=skmys8yEvu;foKJp79Y}W<HU6ycp4}NfUF}111>Yxbzk+1i>6Wb%q70=p+?08nHvQ@#9&}HXdNm`1jGsBdyD`?*Z3wezhq!-'
    b'!WtDNzOx`GCJ>7w+{(`=Sfr6VG9f3&e_9P0#eDKcOKSCJ89qGdBi#VyMa$zdfnrtYoLQn7b>1nyGE`tAEO!WrxH>Fc4E??8i0iS9'
    b'-C-'
    b'6yIWDIG2yJi46p+Jsc}3iFB@awP55m?Zh;6j@<d+O9MZoRxC9M!F(47TPIoY@pUW8krTfzCb^d{ROvYC_|*Ib7f_C(0IQ6RwA&)3'
    b'IjKLSR5r_fP#dX9oPfd}oIabY>6CFF|eP$v`H?@RHVs;G9bJidTI0&Pnz6V<?Lqimgu7!sIC-~)=|(j-'
    b'Gv4tPDz5O?fM6L^pzE7nYU<*}jG6e_40u5GEyzKaYKX)vylsIr6(eW|$}-xPjU;@cL<asLRC(LiJ|$9F*()&zOf3d^-'
    b';)dSROHh@YVcxFT1v4{sAHvtq(?2QB7yijD;0-'
    b'#}Bd{c&vk^PaKyRF7;Vo7@5ODU`;F#<n*NNX$s*mqoG$Jgx~M%1E>)mFQNB|b^xJKBhMIKDm0;DQ%tcFGv+qOatd?k1ZcDTpd*4M'
    b'n9Q;kxlv>*u>60+Pg+zS7<ZNjae*Mct!#yHeacuN80J=0S0pNb3YF5*lYc;}DbtLl+8heVgw<rpk%?zI@PMN`bJMTXI9Wt5>`Zf9'
    b'4(I>!cB1QRV~HG8%#$YkKW&RRVg8Wd6}~TZ{czXX2O}gUhlFlgIcFmH*#QH@1q3U`g}6k|%|gPGX~xguUhq%8>Yja<2GZg7gzN|E'
    b'x~xLQ+v&;=lwQko7?^K8czjx>ThT7t9cAf}#awVMP4>0{Wfab2gSi*LTu0IYullMP9uj*i*6Tn55OE3Rt3(^^bc-_DmeurBF9C*i'
    b'u}whn8U{%6XyR&oZE?gF$+-#_dmwv!yOj>j~RDj-*UJrpaKgU}{qs$v4qF5{;_Ab>1b#-'
    b'}4A=VL>xan<`GrWi4kDMjV0BJ*+|VUFOW4W@+)o&+Fk7bHZrkBKk0eEod0642IBn*$ed}#b03|{P0fX3epx$GyX!x&ubt=Qj_Jle'
    b'm%6xxHpRH2(p>Sm$Dn>ReTTMtU+2~HYJ)&^n6Y%PU`;SfBjH*3j'
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
    candidate = special_factorial  # noqa: F405
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
