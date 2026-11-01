import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[15],
 [27],
 [63],
 [330],
 [13195],
 [100],
 [256],
 [500],
 [873],
 [9999],
 [121],
 [1764],
 [4096],
 [243],
 [1024],
 [4097],
 [1765],
 [120],
 [501],
 [4095],
 [10000],
 [255],
 [1025],
 [4094],
 [242],
 [1763],
 [254],
 [9998],
 [872],
 [9997],
 [502],
 [119],
 [9996],
 [874],
 [253],
 [252],
 [1762],
 [122],
 [4098],
 [871],
 [1023],
 [9995],
 [870],
 [99],
 [98],
 [118],
 [1761],
 [117],
 [123],
 [10001],
 [87],
 [92],
 [869],
 [1766],
 [93],
 [875],
 [244],
 [9994],
 [1767],
 [1760],
 [124],
 [245],
 [116],
 [9],
 [88],
 [10],
 [86],
 [246],
 [85],
 [115],
 [247],
 [1022],
 [91],
 [248],
 [125],
 [94],
 [10002],
 [249],
 [1768],
 [876],
 [38],
 [868],
 [1020],
 [8],
 [1026],
 [90],
 [866],
 [39],
 [867],
 [9993],
 [1027],
 [9992],
 [1029],
 [1028],
 [40],
 [18],
 [60],
 [49],
 [95],
 [48],
 [114],
 [96],
 [72],
 [1030],
 [9991],
 [13433],
 [456745],
 [568623],
 [32767],
 [4],
 [6],
 [12],
 [21],
 [13432],
 [13434],
 [22],
 [32766],
 [13435],
 [20],
 [456744],
 [568622],
 [81],
 [456743],
 [456742],
 [13431],
 [32765],
 [80],
 [456741],
 [456746],
 [32764],
 [32763],
 [568621],
 [82],
 [568624],
 [32768],
 [13430],
 [456740],
 [13429],
 [456739],
 [32762],
 [32769],
 [456747],
 [14],
 [32761],
 [32770],
 [568620],
 [24],
 [52],
 [568625],
 [51],
 [456738],
 [30],
 [15],
 [50],
 [32760],
 [13428],
 [13427],
 [1000000],
 [16],
 [25],
 [13436],
 [456749],
 [13437],
 [26],
 [456748],
 [568626],
 [13438],
 [27],
 [13439],
 [456750],
 [456751],
 [456752],
 [28],
 [32759],
 [84],
 [456753],
 [65],
 [63],
 [64]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-q~XJ+fsx4TT|qu@F(VWm|UkCPHAza=n}h5D~rbF%V|R=S!bk48TDb-PO0c&c4S#($ZQ>_WsA8{`K$thp#_>`~5G!{rT^|uG0GN'
    b'zx^_o<|?Y%yr#Y8)GAg&(=Jnb-'
    b'Q7jz>T+t{d3LE;eQK*~@7fvT_kaHW>mPsnrT01OI6D^}wOVVbeoD<PJhj>QaE>0!OCI}36p5jJYBQ7Fb;yrlcFE>3N?W~GpVmX{)'
    b'Kgkcr;U``o~bt$!!z+(J?+!xvfe^Xbbf}}Qc9HYwpO=TLk9D&h%stgvvyY6Y_>9M6WL;3=PZ%aHvZN0V;Gseo!G;cySDoyOjwxAu'
    b'~*(M*`4r}WI7qr)6i2=k6yNooX?M89)<YqGQ^|RQSMkN*OgOiEM9wJb-'
    b'k<1wsupCh_ZCAU30I5SF^VAb~QHT_+D+=UTYE9NZRI@by>=bSu^2ZMR%%1pJmoMT91=Pw2}AztcJ8$)9wU!jWjB0-'
    b'YOD3SFOJ1Hfw1Vrl`HzkrFA{;rG^Tz2&zFe+0irnR--Hk5;o+Is0fj{p1))z1#>3>sp7@%dor_(HWXb*{!XS%MR*9);6D?gpZa|H'
    b'I>b>&t!J5a*W*60Uj+iHnY^3$A#?+A>X@^4cVnpV{cL16Hh{C0X~NS^fFS3ATX=-'
    b'F1AbQY;$K&?JY$LAJyC#W*fWx5Jkz|V<q;p`d}0DM6#^qu58Rp5PqU9lYBzk=|g7S%xdi5G<&<L7*vx?lCr&%iO2<zhmlhEV$tUy'
    b'tXalcZKX=t$Oax$gMqAmGR2-YNU}D`R!b`yRH$r|dgNPU^$c(-Avu}ZWosYVA-'
    b'^+{@BV>bZGIBCp{BgF>2gN5G_`B(rFdgN)eg8<9$h?BOP2IdhpeTH#}$4T(xO4*Q?(=l*`!-3Ey`f#Lcqr){F$t=<01|ea-'
    b'*ueMn0d|>_JBO)=fu37}#CalS#QK<(bC;=cX&R9@a6TNr2%NHrl1OAH#rm)3cNuoU%Z879OTGwzMxA)u7e`@G$Ifiq6_)(Arz^Qq'
    b'~8>?qJg9*3{=&VIg11L9be0l)Lg+7<8pesIdYR!p}O!I9Wfjfx%z^IDK#3B~~qoztz>!?z2ZF@O_j)i7GOft#3~*gWMSm^jXbj!U'
    b'ZW_=s*?xugZ|hvS*^~<*3vkb*J@`JPYU?!qn|z(xkja@uOkRMiSO8+Pcq$vW)}o4{%<?oIH7+N2b6Y7mU%ROV+50s+F_K+hHE*6b'
    b'LTFohW3=vGkPhxahG<FK*y$C~MI?n`A3+%sg120-'
    b'&>$^TAC$5K_vcX0Hr)`3V&nHa+C#SV|?H2nSeM2iV0D9ScBfwfH8{)@Nxp0PkV>vSwc=!wKCp6umqLb%+W<cMuGONEJH@aY$&k9U'
    b'l~9C`N9+)`=j7Ms>zUvV_Tm8A$l>E-lvsd!>o60(YXfb4Cz<41;*}niQ%-'
    b'h}a>FV+CUeL@&YM{F;_xtG0~@dc)_`yW0{2FX*3P8gYo4!Iwc%)F09dzNR~+2i><g{Mb%{ea&n_3{p{uGAV*P-'
    b'#XEs%O<7hk=mKmBywVH@CyQC?n%HMbAaiiB&TMcfe2YXY@;5>uXKKjfjuld#_qj9l&j^HQtvHI(ZD=O!Z#A`naTi6Y<gY5w>FXd0'
    b'kOW-@K>sN_6XZX5PAuU%9n_E%emzqm=bbiQB0E+-'
    b'&!h~**71v36Iwu%p=;m5{KC@Sr>*?4ZoFiS4Z@XusGR6cp21cjm@BZY7IUpv*(>YA<ke;N}sq!DyI<u)u}5*?qmi@-'
    b'UY#G$n&mq&m{qnzyXz+V@rKo;g5>p5s6mdkI~<m=D`F6lh<WrORl%<1F5#4iGcSB+H#U%wlEu{SQ+$jY~JwA&y}f1HTCMm<V}cQo'
    b'l(58*N;f_=kk92coDHYao(p(Vo8{2TnarWYq-'
    b'XM)+g6JDmr&P5Xtb{P-Fht=%;~B1zLml>6Y<oDh(d!Lkm&C)*uOpB}q<_Y3g&vzr&{V<GGn`mA7*Ds5BqJFVA6kEjl42vQrC-AYs'
    b'4cD&)TB6N>_O>hzva+%y?TYopyBm8E?wq(ZX!HlU4>=#~l{5pJYFzX(W&F@bradi$6a7lU2Vd&I(K!N@1!_h@CMkvASyn>zlZMKy'
    b'CQ-#RmS?IP(Oa?lxy@10sc6hTGGD&5gr6hFevBNRWv&9e%Bb71!-Hjj!yCf0}ke-cr8>s5*IT!khFwAR~4Wp;>jPSZiMh4*v6!2@'
    b'N`^_D0eWeRZ4eNT;ccB<I-'
    b'#Mx1F?5f^#!lo<ZiCxD%N3k=nys}$GcY1`sb)sDfs)2&qkF|5z0nhF<lL)w{v@sdS$f3$2I(>AUSKiWC)+l|yH75K%qLk^>0aR>|'
    b'SCgEDy&K?1EtgJD0faFa+X~6xsZ&#SuD{gBN2_oA&7;*k3h|=~e-xXaY&DODp|LrOl-'
    b'@(8b!!=d$$QewMB&SIc%oPt_|Ws;E(s^z4MNK{e2lllJi4EP1Dr1wL<DcquWRj<Zq%$a>_d?Sb(Z24+j38XX!eMjNdRzJ{;gAtEs'
    b'P4k6`z+DrTCfUG}&VgO8VMiPa=mzT;IHk3ev_Gps5dSv25gijLdc+tu@tB7rF&@wI-'
    b'f?L&usA;O`iPl%y&a7m_>aPWe+_bNyU5(63zjRvk!-FB<=gyx6rc`=lc(N|wUG!7)X*29Utp1_pQ^@AK%i$LD@;ZavPtmw-'
    b'S8(dkDrUP6Ecl<qmz+cj1aG<HYohX!%pw9&gy`aN91d~B2OnOS?j$J<$O8-'
    b'^%mdIKZhIP;mV%em%c4MMgj<+3ud0>Zw_2gQjJtlRNgT3e;SrS`_m)$WxCi1b}`*jOi#%##>44N+(T(*PqqE{1f}PKc&^;)yGm>1'
    b'6sIzIi-'
    b'A8jLteK9&Hy5Z!(jwxnVbP8s<V8%+^9Vi;WFa0`pUx6$s7NZ6#5(hV09)b>bmtmGh=7(8sHk>&r14HQ7P#RC?5WVQR&fa9#rz=0U'
    b'uvM)Zw`l%*SuiB?ulRV3JG2m{X(0*@`V4IVJKpnW-'
    b'A*I?&*9}E=$S~2CLqZVze{USKXJ&uwZ{#4Mn|)I;ggdQva9xFO2}Ra))6HxNEemyqBy0plOX~=*E}?vs;a)wDsbhhH_!@&frG(j}'
    b'7DzPWO$yW9N!*=+(WokYpFHOG1wn2|j!j9ULBoudI(-r}3lozm_=y!lYhz&1Su-91pw$Ba$3^t_YWBT{z1R4-^=jS+G(`-'
    b'xwcP2OZR&*yOC?>$>pgm3g1e2}0MbWbaP)BDp~XwLBfgiA3%Y_*cf^KV3&heH6Z{Tre-'
    b'4`PSl3S@uIcSD(4g>iUfi_ocg_Qy>#Cp~!|&;?9ePJfsic)RO*>8LCS-TQHQvhIqt+v;umLs>#U6)(<CJ?pGIG9zJTQb&Y=c<@4V'
    b'9rKyZW_=gj-49XB3D5u0tc?SD?9=<Z51q+LAJACx_+kGiX@++`EUJm!7+v4I_Ncix+K=PU4H;shA-'
    b'&^f)*efYkjSfV8NI@Za|>j_t{#N=?`W0fhA3-I1FLAP>6G%BWNY!UbW$zv2)gu7$+MEq$Wz_a!zP2@7QRc=bbDNLZ)Bug-KFjQN~'
    b'0sB$OiBSRSYHo2-'
    b'qWo_D{OcP9Dz<`vveKu9#ksI3v8P92yX_NcnLIF&P9Cu_nEtWT~tHXX}iUGZ%HXG#oxb=XnDc%}%cU5viT@$T3(V2L`FXo}@v1~x'
    b'asR7FtByGhR0~Xr;mTw-'
    b'N3Otg#S9f=iQa$&cFobR(O&oolIIz0xY8sI#T0td^0L^{EKi?ybk|$Z${rFHSVW(imga5KCHK#JG1Y`^F!lBpjo{{#AQ=j)h6NXi'
    b'&1+V2j9=|E|a}Dz-;n%8SUamesSL60h__a8}4@ZjhW|-ne=JV<$^-'
    b'7UIpaTud<mbbF>8cmqWn~YxXc#L_CK9YF6mel(dNi4Ud!axJca0IpTcb>@QU9Oc6Q%iqgB`L$t1G0t4qhd$HsO)<>TYfO+&4)nEL'
    b'8h;1sLZ_{0ZBq7^>d(VC=~dLTdqw>bf^<^Q(Uy73sqJ;bal6vd|{P2sUIg4LbVIYH$~~Z;^r8GE>JBHRi+J!fj$;iCCbAsVvJ|rt'
    b'h=Lowm815|81RN(;;gs*Ef6Dsfvxp#@sKZr4peh#N*Au0gmA%wB`;h~&)miH+6E&Im_AHfd54#-'
    b'On$S>q@nrDtQnz`OA?EZsNmt`A6P^<Mq^tyLV-'
    b'J;1n^7(u5+*MNCAhM|RR#CVv%b8{awkex;%FEfR5$aswUmeL=cQ9Qb=rLSl=u<O1rwJm)$Ig3S)+cYntH8Hl-'
    b'`=OPhF{0x*=|BN%T>JaU6dv!s>4TBREL_zEQ}omt<GN@TagPQX@XOeOzV^7`rU}P|IZk@Mbrg?o%O0)9g1@*CEU2|2a&8VFT0VfB'
    b'$q9Dnz6GfnzE0PgiD3N~WZj^t^tLpAo;Shcum1tB2s9J'
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
    candidate = largest_prime_factor  # noqa: F405
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
