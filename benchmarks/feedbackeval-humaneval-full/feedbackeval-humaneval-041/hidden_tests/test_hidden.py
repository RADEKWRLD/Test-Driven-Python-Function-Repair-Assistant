import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[2],
 [3],
 [4],
 [8],
 [10],
 [5],
 [6],
 [12],
 [15],
 [20],
 [1],
 [25],
 [7],
 [100],
 [500],
 [24],
 [101],
 [14],
 [99],
 [4],
 [8],
 [3],
 [23],
 [19],
 [47],
 [48],
 [46],
 [26],
 [499],
 [27],
 [98],
 [28],
 [18],
 [45],
 [498],
 [13],
 [102],
 [11],
 [17],
 [501],
 [68],
 [21],
 [30],
 [10000],
 [987654],
 [1000],
 [1002],
 [97],
 [9999],
 [987653],
 [22],
 [29],
 [10001],
 [16],
 [31],
 [9998],
 [89],
 [44],
 [9997],
 [1003],
 [83],
 [43],
 [84],
 [100000],
 [1000000000],
 [59],
 [58],
 [999],
 [987652],
 [998],
 [57],
 [997],
 [996],
 [56],
 [9],
 [55],
 [92],
 [50],
 [42],
 [54],
 [10],
 [53],
 [87]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-qaFJCZFqZiXd8@?~iYvJ`xQ0KM7B7$5=0_}YLhS#7rVtB*HsR%iiZOdH)@r%o|R@PFoi|I7dW+rR(QuYdmf=YRb1umANoZ!-'
    b'V<<1f9GlTA#nYKdB}-'
    b'IaSc&AIo~vFnLdHO{QohFxp>j&Voa6SJxQ`9FXD?Vtbn%NVsCU!&Yv_LVte_j|VZTCuOMdt}#@Gs^HB?Tps1ne1HiM%?my84cOZy'
    b';vP9!fx>G9?`u@uWhz-@3HJ2UC!92Wz1Sb*I631-Tix+^qi%d)*ccw#Ii&`lRdRn`<gM-8e0vY<BU_!e!G;D*=|VB-'
    b'^*B=GVjnmlVceF^5a&S4I3D5CT;XyEO*wl-J;0g8+C6T47B}T=Bg#LO-`?}d-'
    b'c$}=hVv>wsc)g;>^vrqDH@^@;eQUS?pF;{SLKT4bHRgah_C$jWzeQGF1v|=nyUAZJ^J7SS@F2x3ddFirRlK<71rZ&Vc9I$t=BhX{'
    b'X+Pa!H8#`2~bIcJK3g<g|8uo^o!V@hxL>t}^%Cm${ui@8pVeUTvHzHjnkf2!>d!qwVx@WX>v$Ap)&$nIWT`b8L#vZk&8X)by2ioB'
    b'A!;O7X*Ed@P&hOY*i|?wwLkU;YEX+)=qg*IU90E8IS86%L={#1Q6H`?0;*wU%1JV;0l4Yu6&*p|WmPt$ErNzCYGw)fLs{_I9&^v5'
    b'|cnLl=ls<{GQBYrw~8KNS1kHfp4fGHr5rJze_F;3KX&tQ{L3z5qT<bL*frM{i8WwcYQ+wJ`>^s@iOphm&l%T6O^}J=dvC!UPDry3'
    b'S*oO;5Otx%uJuGUqb-'
    b'{SXUH%8pYkrlw5?*fT+hcw74oXh^hCm|>r}`2{#N`@IaPU!jaX3wMyKnrkVu4An<%bfg*sj<SrIu3>)D%W=L@6{h@NrWh!JPzcRA'
    b'Gjm)w<fpIRn?@QxBQVz3$lM(3jk0M!e3YzuelH^>S)19%Xn>#5aG$Nu){zVqmsyv9!p3EVr-'
    b'<AKygW>49RGv@G)9Y9Wu%;yrmIc>d<w^EJ6u=srPF}44wluTy>%Z*O>Vp6A5ymdPFid?WoAedC{rMC8(G?Xcg^!1X!@$Bj>>-'
    b'^Ljes|3#aZ1zwM*uGLei#u3Br8MPj#J6rlnm!CHI5?b;Tz5nD(24GN0fFpQHQiaG3DPq?-'
    b'ilq|9IpuTlj`duEU!R=yJ*X~mw6+F@|KKUMM{Gk|Sm2(?hiaqv@1ZyKa29z&Z1*#!QTw?={3wm%`rfJ-'
    b'0K(r6VOWLU54g`k<vN8$-1<sk(7W)8GPp6j%RO|-'
    b'?PY!RR?9J%r?_~g3U1u}G>goNduU><wwW7h?`sr1s9PO};4N8DJzFW%$(Y1aT4(J|m5w^Z`SKH>jU`l)K&9ba|SPq!1TT@CcV%Kq'
    b'##%)CT4%Hc=xV_7(oD7JvF?QU8IW=wrWtk1gj5U&+fX!GpE?uAuw()zJ4N|shCqayJo;P(xK$}-'
    b'S5mH0{#g3KG4jF>eW59IcMn~}C(_*}4&vL7zuC2kD)s~jk3SPi`J#hhn{W#6)>kL7Eij!m-'
    b'EN>qfV${PJ5#dCVgYU9m_ET_A#*b_*V$DHLqs&(8&WVIf1#kJN_lYRbzLC&zuuw;>;X=_X*Z91lIfx?y<J*zIVlWOz$BW?uU;Yl&'
    b'_PMALM@56!Y+KVicZyYP=7Y+k@!<})iatg{&nM;FhM<?9-'
    b'Wa5Lw#*>pbQElX@?~p{I<d^Gz#ax6vJGGN(~*B%A*3if`U!13X6&}5nZw&LvpkR%V18fZ!8v!$qRhWOTAc}$&{Hk|(JAvou~#_bi'
    b'II+G7+Vq~3Xy|nR{XQd;5VINAFX(wqlHHqP$#&|xxbrILqeY2lQ|Yz)f<LA5BFz}1^Y=6YffADovtxL-AF5m^whpTGRV?fIVHdlz'
    b'N@w21mhCC49LQ^iKyR#lo%cuekWIP1ACql?DF#|e^UD#fdA>sI*S1wWPm8u0OE7cfyUO{FOw10bb+l}p6U2^sESV|4$qT}`$gYK6'
    b'|umLHe|75vYaTFS1YZn3v`qe2*y*Sej_erYbO+OeG~R7PO{6ma7x}sj2%IemsZaxObH2EPnw}01lIM9xB;6j*^E<hH=7j(K#TU|5'
    b'GlBvfJKQL+ziGw7A|+&quVU<EyI1_u?^aCF^%~Px~I&cFm_q{S-`32G%Ctg3?k(@!WfZ-'
    b'@xv)_0S6H7#KgUUuIn#4!XFf~VPM=$tSIVuFT~=oL-Fv6Nv`wh4fJNGn-'
    b'o{hQ$NIxr$YHdC_VHPOqQRSmKB(#$ZdiF!YM`){w2``4{>=1VW_+8OYZ0tAw%W%AZ?L*yw_)~ZKDm4YN=q##1dEisM#>|$6RREiB'
    b'bgosF(m_E{Dy>Rt8J3s?$N73(hPDgz^QH(aukz*iT|1lB)p+GI=vn?0LNaAeKpEI8ID?)9`mul!2&PnL0uFvpb>|@@trI!G8C{%Y'
    b'5DjYL#0*3vES_kPJmXy#?AX{LL)u{{<7EVT9Bd0db8&qL8|r6Jd-'
    b'@{65+mRbb^Z=gi4Mw;M6h5fJ%MOpN3DgfQTy*olsXFLtGXuo98Hzl7aMs)XL&(F{y3NOes9#l)XPLBg=$Nx0a?+Ta6nbHVi{&kV('
    b'qUTi`Jo3DcM%jH;yR6$eg-'
    b')^!UQl=tS<8HbOR>rxzUq*PzlFW+Fh>mN#k~3c9s~a80$CcUtgtqdAu$j)))K_8X7e}DYe%?mN7%YwX((XKwpW;Xv^reGk{n{P(_'
    b';hdK(EIhUhvB4lB__egv^m6gOzis?L(zQle_2wj(2RcU?!FK=!2_<?3D=}7D&-'
    b'{@RB~e=dmCc<Bn*;QS`u2vWL$114L$huh7gg&sx?5zU5dd1i(cki;n8dfg>L;q-'
    b'@?QSlMfPbGGeEvejctMbv+%k2OYx2p~0>o(IonQ5|)!ss?iqwnDY!XGy$58r}`hK4pvGdVG%Y!Y6z&;*G4g1C?du<WuT@MvAv#2o'
    b'%ySj1^~c)zhI(-yo6MxmlL335CXsplvZwTR89!%l!pUMK2J1<na>xC&i#4S5lM&Mfn{pn<RX0HHmFI2V4?-'
    b'8qF(r_qind(=md(sR&{?@8b7WXh(Of&ZtulOP^?_taGaY!LW7*#P`&crFA%ZNL57T45HMAL>`s#IMvp9a@9O*&4YT^D#4bc}5T8O'
    b'OG_Q1ds_GsKCwnh6D1Y$t=T%34uPvT?kW~lDPfqTaynr#i4(9#5<V~z$G%R0Ap2g*NA~|gNPz+)>tg1TB&B1A2+$RQ+{tLAR7@i='
    b'f_Iz(S&_@CDw5EDjbI}iegrXDzxW1k^`IGY8rE2TRFwc9r(7oXwPA}Yp=nN)=D)DY@|HNw{B|jZKLFXhXQaa*UA{JOUe*oo6zy#~'
    b';cEXhL%K3XmLm18BKcQ_5vN=b>K$tIpr?sEw{3xmMm&|z!?KR7Lxgquf^L+0cFrJ?mFXh;?fyAE(Rk$nQpl4iG<cA$bzG5Awf$DE'
    b'QY4|W{;3E5Q)qh-*KGE~GP&zc_3v()KqEd0{i}b&;B-'
    b'j(jUHtWvI;e7zoILDncTw}=UXvM;f(INeG!qOVNmI1XCnN7o$!k6IsDUpcf9M&iKqCJFE&N7!V^H0mq0oTp3&rU5K+R{P|B@dOuY'
    b'<#v7^PAcU)SfC_54s1m4-'
    b'$WHDI?jjSSRZ@OrP6piQNZlvnCl;JHDIeKys0U8wV33;p0`3c2Y$n?chnh(=KH^mSG3T+|hV3^hu2socFEnk#j$<)T`DD0V?l^qI'
    b'gRI^@uos5jN0jBqgx){XW6Iy+$*B#|dxX5kBDjr@6Gx19b%Dy+2OeqUmWgGVDz@RFiExVF6#wd40(!;vLQ(xgg|5`OYcEDC6+uh6'
    b'c^cEkl#BkqOI7azvwZp=hQ5kLFoX>!=m#lh)r>j%YTGvVJmu3lJl?1B%09Wl4H_gW2!t=!c-?{gfmljvS%L6OSe_nqi_%}I-'
    b'Ufo2<%<e3Da!F;J-'
    b'=sjoI=mpk%2tF{kE_HZO85Sq~@(rFdUfoC<GSz~fg67O;45%X2PVvj<O57xmBX9Z*+SGe5NN(__H~F9c2iDK4!v'
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
    candidate = car_race_collision  # noqa: F405
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
