import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[14],
 [5],
 [12],
 [1],
 [2],
 [3],
 [7],
 [10],
 [15],
 [20],
 [25],
 [30],
 [100],
 [13],
 [6],
 [101],
 [99],
 [29],
 [19],
 [27],
 [14],
 [26],
 [8],
 [28],
 [5],
 [11],
 [102],
 [18],
 [16],
 [98],
 [17],
 [4],
 [21],
 [12],
 [9],
 [1],
 [62],
 [22],
 [103],
 [97],
 [10000],
 [27345],
 [48271],
 [99999],
 [1000000],
 [10000000000000],
 [982927638],
 [1073741825],
 [9857654321],
 [9999999999999999999999999999999999],
 [9999999999999999999999999999999998],
 [27347],
 [1000001],
 [1000002],
 [10001],
 [27348],
 [27349],
 [10000000000000000000000000000000000],
 [27350],
 [982927639],
 [10002],
 [999999],
 [982927641],
 [982927642],
 [982927640],
 [48272],
 [1073741824],
 [100001],
 [1073741826],
 [100000],
 [1073741822],
 [9857654322],
 [9999],
 [100002],
 [48270],
 [27346],
 [99998],
 [982927637],
 [999998],
 [99997],
 [982927636],
 [37],
 [1073741823],
 [982927643],
 [1073741827],
 [10000000000000000000000000000000001],
 [82],
 [999997],
 [1073741821],
 [70],
 [36],
 [10003],
 [76],
 [9999999999999],
 [10004],
 [9999999999999999999999999999999997],
 [2147483647],
 [9223372036854775807],
 [9223372036854775808],
 [9857654320],
 [10000000000001],
 [10000000000002],
 [27344],
 [10000000000003],
 [9997],
 [67],
 [9857654323],
 [27343],
 [9996],
 [9998],
 [10000000000004],
 [9999999999998],
 [27342],
 [52],
 [27340],
 [68],
 [9999999999997],
 [83],
 [9857654319],
 [9999999999996],
 [9999999999995],
 [9999999999994],
 [9857654324],
 [48273],
 [48274],
 [27341],
 [35],
 [27339],
 [54],
 [48276],
 [53],
 [9999999999993],
 [982927644],
 [34],
 [982927645],
 [33],
 [999996],
 [9999999999992],
 [9999999999991],
 [1073741828],
 [96],
 [999995],
 [55]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-qaHJJKw-4TbH%-ijT$0KPzG+K2-_z*6oFIC7*=UW)hU4^y}MZeRjQRrjHPrbz+^=fT#$|MK7e{q0YmfByOV-+%k-'
    b'zkZ#mw%>pICGVwj)6sReoHgWR9eRDHo6pU5YT7$_p4rE}vc{5>vgtH+?PdJ_pWlD|^KZXg8A)fAQ%}+&rI)qu_LGxWySJoO`|U~G'
    b'W%*%Azg47_F?H3g_Tw@0-g%CX?M25vmk&+Lw@#Im??~;AJ-bdRnwGXKt?|%n>$JU3&p#fMP7zJV%I&Ugoza`mF6&Auy?4&kN87`e'
    b'vO8_k&Xr`<$2yWU)$cy$ONaVnb*i~eR!(Il?X^}jFZZ5N_*ME^*Xv>%=UiuvyMSA6V`cv8<@o;YZamjJRw>PmwItnAQ<XXz-'
    b'`wZ4qIZ;Id_%U-&N0pJ9F-'
    b'p}v7NqqsBi5?(&>9@sjZK#t?6!~4DcqkWpG)2UTMC!?7B0knYLA{HuvqxzY9N|rOkZO=98l&mCWHwK4bcty7QRBl1$l+<+AMIxAZ'
    b'Ysxm#sQemsUY-on8SCrTP!U%QFy%b%!sVhcSlHoWuPwdSL3q^zoaYUe*ZxKZ1MDq8M+dfs#Rs?4JmXA)v6SiG>o_BrD==h5R<Kk6'
    b'shgPUI0q2y3u40m1Y6gJ*Yzp3wRCO7k?R4c$Jb-UhVH;K`5`ZS(~&#YHOJzb?=J|s7Gw%cUz4mENc*?j5nnTxMfZMV%s%HA`6{M`'
    b'xv5^lc4et$695;i^zNU`C{39VBEX;V|la_*_-t?r{oD?1-jP1>+_gk|c_3AeJmw0oPm>M7j@xLcLc=HE@%GrQ<amYZ$cY^-'
    b'SOxfY;!M4m$dC!cNdn<mlXH?t=<pwF&aOvPoM_M}98q&d!VdgyI)CW`dsPUXv3floU=hvqsMW9g!cUGD4*&#r}MRJB~^Elo%50)o'
    b'}X@c!d5was>%CN<h~ph4>lQ%ytCT8oBIUTIY8*dC2%Ngu0SEimBDd3^U!^;}~U%`a4bCe&2tc4#Rt4q&rtP<`4p8;qWFwYj&~#0F'
    b')KTfR%8f2@XkI>8KHQs&44Rb21Ebv_~KqkS=#d<}N+VX`>#ysHkEJhV&w?o74JQP|}WSkYm0h<7zKvmZ+t(m1KlIyN+oexk8Eq@|'
    b'0M0T5+Ahl0phE~k~7_03XsvJig;c^u_X_oYA<QTDn4KyJ#mCN<-'
    b'e&tpbi8<|^kUTE}g$n>_Zb}pNe#;?&Ur)+l02z7vpwBLgtSgx;z)0yR+6`?y<CJH-nR3|+;t0~lV+qhz5ORdaGhNpSpN(CiN?b*#'
    b';DW7!`AC?^RIj0+h(&mDCYBD|%$_Wfs&OIa1TCPe*?KsCX;pS&vbhV#BeGuy`eFped=}PT0r-'
    b'qD41xW%^70rlit}9e8KNAks4jrpg%WgR_Gv$J<z01MG)FjI+gtgYefSVZ50_$^~3mLTbqWDm@m^vFU$jR`)9SAN1>8I{-'
    b'C|W;^OR<tuI<%H^<*0K>_Z8pjv^E1XiUAt#ygJ9^sTZ@wFo)mRvoSDY${3Y_8Bk;};lk3>aNLY6L|GTKv;h&YO7k#8%@V>7e}KRd'
    b'51Q9tz}xX2ka|M5_I`GQA<V1c7w6b@2`beoE7PN$g{|QLyN3HI35PJc$YNIUP*|#(Ufj?a%kHenekTxirR@#Jkgw9XX$>37D0NRv'
    b'n=*VO*>vU*LTgXMyQ82@P@O#2Li}OnOgZc79amMEk9_PydI&LNu`#YO4w4!ze-'
    b'4#Iz!lHPFv#HXAaC1PlvC+*YG6aI!$dBOZl_M*QF!h;naw@B34X#DXPFFig?OBL(*k@orEcL4fd8=0&LGzTscM#r?@o-'
    b'!vzq~JLomzN>2esn787%fnVF;X8Lq&>T4CZa)-lGIzi1gK%IAR}YKARz(Q8GijzVo>ZNM-'
    b'=j5raNthxcSB`5@kYZ9K&O6n~9%+wvmmNRXr;NoOtph~`TV(;f_P*g~babPqDHD#U<A|L!^%(uj7)W%5T9QX2(U<*7DrJEzt2m^;'
    b'&rUHF~qFp0|>@yc5g>c=U4WC1>e~p^5KJA*hdIbZcATPcVtb{w7G~tFvF=T=flp`^lnA4}ko3n3}5PGDP9Ug1|45TH_=Yr1?3L7m'
    b'4FI6KJdA}0^hxdy<C_adwL{}y=zTj96Q5Um0OX8p0%f20aqAl<QWQt=*6SI`qyFR<Y{ny^HTMmGlq9|AkMyZ!`dIO0oO`1|#M2SA'
    b'vE*Xc2(qU(8zAl}?E&<MV%T6=+7rtcH#WDDKRB*;=M?VOVc7}dohZjmgxETbw2RDV71GHI%sg<+Yy)CR$4WdC^6Qz)=WWv=I!+_8'
    b'oppJKiBl`nC+TY{rM*{Db(FNJeQaA(R)Xst0c5T9c=vJ>~;W7)3YvMO%dWS*Q%CP)oCQB=vzn%^YFMjg|K^P%Q29&|-'
    b'XJ5oB%z&Ul3ctSg+EeKOm@d_Fn4x+JF_~iDTnI)I<AbAV$Xo+7R+`}C6pG(4#&?a$2G;D3Sd5ghF|^}A??ou#oe|<TE(t@4P0D$t'
    b'03Pithdmv;&uFsPKp|7v1@Z$4bP?TKq&kv!!vsRlz82vmn0aF&dI>^?M$44PZE=?F%=ZC11QhfW)hjSvhL@=+js=SgV`P*iwZ8Ds'
    b'n2VJ@rb?bpSwi~Gtwf*2Pc<Wd7h{3O4W+>lwFeFwn6(279HJ<PUc(`=`{-'
    b'0;O4I{ymPRIcT&dpJ346zC0FO?OJp9irtAM{cdsK@@qeQQvC5{k}G4aw;v3(Qq9uHn<dqN0t`$mE+8MGysp-=1}OeQ!AW-mP@4h6'
    b'*?pkxE}CN?KP6QqfL%Fya*-9`&Txab7|+z0U!KRJTh-'
    b'a}pXGZXv891#o*_yw2HIM91brmYKFj^<6Xa8VqKAVS+S8+{&wF=e76fE5r9NUc>2R>p}CY)OMiD2L-'
    b'&^b6}%i;?h8(+X7kvl|xa8PTO**j2g<iNY0XlMX@2Rj3F!=T9geW82m>AwN@dMEiM6Bk<$!k#CfZl*nAcSZb*b2!|;rwdOQ2+pR*'
    b'v(6r$ki3BH@{k<`%xu>aMPlyuu#A0dF67WaN2bvc?EeqU$?bDeY#)V`IFLZ2!KND_Xqx8rxiezQh#7kFP6H$c^(+q5twY8vmh1$='
    b'UF&pSCzIW6ovZ|nu$&+>L=*=-'
    b'ugt_2ecf&y613t(x6d6^;bYpXJhX4RineY7#`VLDF9XojfolMs{x&a$p{>oRv??jf`GlZ$7aH{AJ@gOVu`=EFus+n<Qrf4c6;}DS'
    b'E8e)t<X2q2<4p7&X!<66xF}PrHhpT^ZbMqRVkP~+$2@^^7OMs(J9x`Y;h8RH==nlsPR!Fg}^ft1gd0n4$2cck_Ix0e>^#aOmfe<w'
    b'>J6sI_Wd2Eq=3z8&9Po0+@PK5p<ujTTMlo5ZN9DjrL2Hl#K1BHL*Q3`+B5s)4L)En*(?cQ;G)UvA4InKCe>gp6c6}^3fV>^(p&2{'
    b'^xv4xDGe9e`WTmSpi66_H-fJLH=cuNz5M~R-BhDb>pkrcS$jKhki~3MM)Fn<_LT2;gDXjQVI;??R6R2ZAX(@&Roy{Q-'
    b'xFS^4AS|+90n!+8>Rr+BTS<OhQ+k~!kmLI!fB0LZbsQfX#0Ao3avzZelR+RNJsfX$oq3qm9v3tE?Hmrp0es-H!-rrfZy4J-'
    b'3p&v|SzyQAF~fD@9=M@Ai}6unbzD~M@7_YTNPWv@B;3H@z|+r*6;0G2=j$re1PYogKaX4ZAoyMiz~snp^1U6)*~lIo!Vox4=0;hu'
    b'9t%y)27sBDxg&x!+;@-'
    b'`L;;9Oe%%)4E|dVv*fCcn26}~w+u3{DHS(>(4|EuA9ndTKN&8lzGddsmaiA^0a$+LUs1)SQz=LdHc_Xai^jG7k_?5^t3vDJ4QR!W'
    b'N#`#GS(KDhCS&1G}@aRNNO9L80@laJIv=F(`9S&Tj&bC32laA~8uD?ObP;DXZdelfzj<_ukBaVJVcG@Yd4i@9UhSc~XP{byP_|Ee'
    b'l3eFd(X!0$3#nCzjIN{O&3S=39mnatZC-'
    b'4p=felAwPYSmOcphcwJF@P<*?^CUM1kJ}$mqPs{c2K(eKTzE&Fl%BI^Lpo4QiaPPI;u|;oDk4!*lp)W@Di-'
    b'9eYEBYOq%(KKpHP<p5}GUi>Q4qwh?SD~tqyjlnR%-)O4fmeMZlo+-k9!%l^{ZihL?<4X;pFL>bLulGAS?5-'
    b'g&$t=<ddOn6mylMsW0BK$G1VzWa2bF;yA!wAAe9&L-hrwm?_%wD915abxia^f*IIbHU&8avv>ZTdd-q2}^w-'
    b'SU5DDqWJ&Jlz=N$4m$sZg0MK8j*+mXt%1a4*1u3Xvv>LwI~90n=6A>%$;u-'
    b'=EI_lZoUK;v${I+2mMLbZLO&P5*;Pp;&3<f?<5vd;})N9kr0?&UOZ{fHc)cD7~%CiQ*(BM~?aNnD{vYE}7WyyZ8#s-'
    b'$N9TlLsaQBFC1|(rX9bhyx>BIL;j2Ap<Qb_X5q$WHdZDdBV@@wsJm^TgW^MSCKY9M`9z!hL?hpF)ZPY#t2m4#)!fqSe6lYlUd&6+'
    b'i3^mj3*T5w~zO-'
    b'p*!xV<3<)~@UVJS6;@k%JT?xt<A(U*8_Uc$QZVpH8W+}56f;P|r7yYMc%yY37VQNy+v63_kxZWI6dX4A?mHL_^K5ZLqu9U|*|Y|T'
    b'Ha-1ZbWYql%G*}3%^;eI$7K|=LOIv|?v=b%;yN{eXyUGD74UL`-W!ugT?gsmFd6^?XFaA3r1uWTS@ZaAZ)S-'
    b'6h!UY2U<2<}c1&O(9yP(1GP2UeakAJ1j15iMb&!RCxUcu#Z$b!^8F7wxw4ed7LI(qMOx&p;Z@rLHOIXh^@sL+I761-'
    b'kJe`VHmX7{{{dO4v97lX*)0aq^8HI%*FGcP_+Bk|7HPe`gHD0ri)WM5H6%!PTP&MOjj~H|!wG8G8-'
    b'MtG|O{1dr2$<ld5Z_yWzC0l{MY!b%&>*?R;e-?S>R6#pyn{zBi7#%LH$P1wWATo&Y0h!^^>k{IVK=pPXt>>kU1TI9-'
    b'T8<=fh9a@oh5XJ9l-'
    b'm9o48Yi5$gN4Y~0<WmKa!Mjagm^0$SS`=$hHcxrd75rmdcE0RR!hUlK+T=6Fzi;BW#h8rSP)_d9M2gD@EfHV~}UI2Zy)Z3CWU^&R'
    b'(q0wP=<odUe^8W^+${ssdX7gx9dzwwffL;8w!EvPYIiZI8JAThpA`?7`PzcC&pbm}*m#~Jry4L-itF+wCbsF~b2K`rJt-'
    b'T`;~8UYj^&}Dr0)p0mBJj}&t#1;r)qPcutJu(q^zcj+_al-KPLLefHj&MEJu}<$hUlW$d_>50VIVezRV~6DgX{a=mb22ve#>G}13'
    b'^mFXmv<?I;W7Ii1IHHUA)V25DqLA?#C1333hBEc`@LWx3vT}qg&+Xd+!j&t?G)NdBPK&%AilIMjAO(O$cdr0xcti4RY)V=FtfxWg'
    b'E|5cnc~YYBq<AM1j-'
    b'l0wFBQF20kz*O0a1adR7u6<X1^<%tk|#!&!=9q4pa+;{S6X_7x+vVa;sk#3oQmYJqddMz%}TV&rE^n7s};ow%rU=+U0*!;sJ!w@G'
    b'OWju}@%m^%cP@a+*++szogad6=p?^xn)8E(<T1g`fz12Gf3F~~!lNa9kEl*tHJiiJmK`ZH^6j5Kc8NH_#ndVs$G5#anK3J6V@{kY'
    b'2w6B;k-Qe3!Vr^69y+|fdOHp8v)fY>1P9HGnZ&meSG+$AxAX`+Z2OtHAL=t=h-VFYg>uw)w9m(u~F!DS5!-'
    b'ta)*eOY_PL3RzJKjIBB!CMbGH8VT>4X}_x(8D2s6zfia$P3fDWXJ2O^^{m55N3t>R_wBe;5BCPbGnEepcQ*jl84<r))~%mjbu{bt'
    b'{jHe|M7phqhvD'
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
    candidate = get_odd_collatz  # noqa: F405
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
