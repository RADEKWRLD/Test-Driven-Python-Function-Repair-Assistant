import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[3],
 [7],
 [10],
 [100],
 [49],
 [2],
 [27],
 [101],
 [235],
 [500],
 [999],
 [1000],
 [36],
 [72],
 [81],
 [499],
 [234],
 [73],
 [998],
 [35],
 [22],
 [23],
 [1001],
 [74],
 [236],
 [82],
 [75],
 [99],
 [76],
 [77],
 [24],
 [28],
 [80],
 [238],
 [29],
 [237],
 [56],
 [57],
 [3],
 [997],
 [30],
 [4],
 [102],
 [37],
 [233],
 [103],
 [78],
 [55],
 [5],
 [58],
 [21],
 [83],
 [25],
 [1003],
 [996],
 [11],
 [501],
 [34],
 [232],
 [100],
 [995],
 [231],
 [33],
 [79],
 [502],
 [1004],
 [54],
 [1005],
 [1002],
 [20],
 [230],
 [98],
 [32],
 [31],
 [53],
 [65],
 [59],
 [38],
 [52],
 [19],
 [97],
 [64],
 [12],
 [51],
 [1006],
 [39],
 [40],
 [49],
 [60],
 [61],
 [10],
 [6],
 [96],
 [63],
 [26],
 [104],
 [239],
 [41],
 [88],
 [42],
 [84],
 [503],
 [43],
 [62],
 [18],
 [127],
 [1321],
 [500027],
 [732312],
 [1234567],
 [732313],
 [126],
 [500028],
 [1322],
 [732314],
 [1234568],
 [1320],
 [500029],
 [95],
 [500030],
 [732311],
 [1323],
 [1234569],
 [1234566],
 [500031],
 [50],
 [732315],
 [1234570],
 [732310],
 [128],
 [732309],
 [1324],
 [500026],
 [71],
 [732316],
 [131],
 [125],
 [500025],
 [70],
 [48],
 [47],
 [46],
 [994],
 [69],
 [124],
 [1234572],
 [1325],
 [500024],
 [132],
 [1234571],
 [1319],
 [94],
 [993],
 [130],
 [992],
 [129],
 [1318],
 [732317],
 [732318],
 [990],
 [44],
 [989],
 [732308],
 [732306],
 [732307],
 [732305],
 [732304],
 [1234565],
 [732303],
 [8],
 [732302],
 [92],
 [93]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-qaHJ+^EsvYjPE?{!6%Mi2x6c<P7@2w*&49grpKnWg^fi!&;-'
    b'I*`V>qwcM9cJ5?BFk}9}`al2e|NXoCmp}jfuYdga|NOWA{U1x4|KmUZr`g@7?AKO*a)#VBU$rr1%efZES`#ZZ#@<uBODWOzmC<#V'
    b'+NJ&D|Ni4Y{_D?%nX4D8z4sO-XU*BIZoOTO&gynNYMsmLvvSJxYNf~Q&DJ^QtmvP^Xz|wh#EYEP@7ZgO*G4@@79U8g-'
    b'o|<TZh!5ng}r%tNa=M&tDj+xmK}F!TkaNf`>p%g(^iDhq_o3Y8k6C(8fGEqwYj#p+js5rx3w`V8f%(77Y3smyS~_sDxLiplW&!I{'
    b'fMn=8m9G)!AR5JIZu8&n=;2PrS5sIy01}}$-aE?bhT5~l0|7^oTaC=>b30Rr;XNv$BO-'
    b'P80Ov1DxzDpfyiam<Fc!bfltU#>#ddJTCdIMulF^KDpy~%_-7dDGK%-vXN}Xm$&_(?=m8hPSWK&weQquD-M-'
    b'#(Wgst?DwKZxpTpE!UtRO8YVSzcTK#|sy*jSGJ=PPw;Wg@x0Vdu%Tio}35z9w>hG}tQu_<DH?17dtMcAj+n1>&4(M^GMVm5I!XL+'
    b'+z;x5(SXEt|hIj1oWg9*DbZ2I=WuCTy2y0tE5D;DLAKJN9~>j*Z|X^;BPVW{b@w@7QwK=0l5fX$r4K<;{DjkV^Mw)=d{?tvfx?#*'
    b'KYj<J4=n^V2BEq-UVcq;>JZuXaLF&h5db*NG0-{)r-yOfPv)+mQQAMdxbSu6W=!Vz~qGdA|HW9{7A_S-'
    b'jNHhz0nCMkflm;vBhX59snlJZ-kIH!UN5Z2ZLR5aCCbF6#EFxuRlVzoV+PHR*M5Zau|)>1(M=s)J0MC1)7y``vvIO|nQOnXt`m?-'
    b'=O7H&YYjtUlaHon1w=%V`BDFO5Q(s|qAD{C|u9lur_#vb9iJCj=cuq~mcwTE?|5F5>^{e$8g^R8eHw?Or+lyZfBGM!uBTYEhUyEn'
    b'a{XHe3j!y9-P^h9l(e<=gBd3Kw<o+j(Idq$7Dnhdc!;Dlb`Smst}PT0&xiR=1?#PQE;9^Hm0(Q%-'
    b'11JBdncJB|`W#V+wU}>A*I_1<Sh0prw$7Q^-'
    b'^)nmsu>nbA<@ePwW|=T%k1|eC9|y)5^A3Z`De_zEC0IuR6|qO$e=Q0noD{h}xPdJi@9iWuO}1pD3r~1q=NcM!uCNo$H}vI|b^R88'
    b'we+@v3i&JX;MeAof4O&44q7@Tsl$mU-ZWNiFuUx&U!_f^eo6FCQGpK%JsyaL^gxW(3B6Tn50UF)h|*P(;Ge!#cC7=SU?1A@xn`9|'
    b'msJSb*K}|jRFOR|NDU|(0R@eLgpG!~&<J*{K?Xdke@Z+QbrWC!G-'
    b'&~5lB^y~(33n+UX^w9)VbdbnZ}%fGgU^}PW^3b>PiTAEq$F=JGG<4$07>)fOt}NV_9`=9!Q_jdu2DoO|e8r_NT=1rrI)q*?az;)<'
    b'u)m(Kq{%f;P{)v@_2K7mxwE>;=0euT%I>i638t5$U=6yh@;OUe>#*ZFQhLr`=tQy=P&MO~&4Z!xfc3yz*<C^qXO{A3Op~hq%+`7>'
    b'PT8-@%4KVi!TKNa=YP%QMEpq4bhwLPc<s9}Ry;M+IdzG+ixhv{H%bo$f-'
    b'LzzcPP^w#0XtN4v|3}54LFMXt6)vN)lE;cZ+ENjm+e)vGF&BgjO2HU21CjQ;=T3>h|{-!)4=HFT3-'
    b'wcCE1o57Jk>ai`v~B3bc(qvV%IV`z5FjHwOlG~1fEkcf2x>?BE5)}?PmqnhB9cyntWq%-'
    b'b>gUD&RTGsy(oP;nOWB0sW?Ifm6h`T$^`SHbSL;+X>Vf0=*is%)2$a0o7i?V1#@wiU|-'
    b'<8G$T0pvCly7Vj`rUo*H=VBE2?<Qh7l92`1$h9KK_%k)tZrP@Pnpg=NQQ429WB85%!!qRykr?MzUW?%fV~DiY@;R`<H;WN?cw0N~'
    b'N&;!uX|*wlu2E8om80{KdYJ<xD^RRx{o+*}_L<`buezs5{pIt;wCwnnY+-'
    b'Dlg!m?RXgjs8d5h+XI@LIL^Xq~c}}(%2MYJ9&zr*V;*oa?<*xv;S=l54@aW=qfP`cfo}40<SSpE4v$#O@-'
    b'Ba9KprmG%DHnZmYJ@qx;!#klhS)7lI`adF}*eDpif(sHF;3l|gTtBd>k)yYR?kn+T-'
    b'r?O#b0e>jhhO+)a?<xg0uYBEx{;fdF)U8aZMQ;AZ+1550?B?@-'
    b'^)CNgMzDRr~cn2J2?Z}?oOF*R62%GUTl3k~#V$pK60vc$_Z)5s@n>8!*6oP_ZmTG><;bY?YY4s7E^e$C}5Gi@UfnJvMhvyXPm9hK'
    b'dZ_b#JtA8hmof+tF4_1=i&ndJmFr$aOFXZ`&6V!nnvI?N-@Xw-'
    b'95OjV5*_fCm8Mr+*iN)b&>J_RoH|gdzI^wb2Pw3ZvAZ_wanO`S*Dqn%6C_B{_WrIAhaEMf&1b6&D>r`@2d6H4|&Oo+A!Kr-'
    b'~we}wHBXODZK$ganRs6&~{D{zTm^h2bDE(xo|E~_I5rP2Z>iVIr4n}n?8O7!~K-LyiaOx^JVs-fK1>Hs(hpcz##dH(FCxlEk`Ih+'
    b'avI4|YEIrO=<#7x+gPnw^t|>ND7PSnvjczIL_Vx&_(@u&4qV(F27xg1wd?1>N97A;ZH6^Mru!9>TNI!O*4L`Kwu5GgG2S3Ql;M<x'
    b'u{_pgDsM%He2N3cFQgWOOgRa&^3P6o6)BQa?dYym3DTpQZ!g5x=BpR6QWl6q^*{nYC+X311WZNKn&RYkN^`}gv??Q)dV>ljwIr^<'
    b'?5~hd&ktZ9Q)vEHO%Ac*_&!RJX>>DX6c-'
    b'*U{J(%Fpm=G$d?0fF_BNTUFgu&CD$EJ_UI)35|m=H*k$0?hKQ+mk>(DKY2dfK<$48ZfZ7V-'
    b'`gQVsspR%@CYii4OqFDN;4JOPQ&)2gN~XNkTSo#O|g-'
    b'v2rk_`95_`<w=M7UiR6W>}b~R;VDm*7zZX#yX<8<n*gVHMY*$My^@x_iT%OEG+}z^E_@tGV{P5XyB?O4|xv-'
    b'?gPDR2W{WAz9!o<^s_G?6py+GA|UOKECTlNjne2C^fOO98ZFURot-#Q$fO(2f!Vjqz^gp{E&K!tr^)-'
    b'|%Y^0@?T;<e^l3H8F3$i9YeLiM5HzmlLA&NvLSxhaO4=eWfZT-w?`FAKUK{<-'
    b'7Xn`jH|gHJ<On(n&P6;Zg1b&!EA{;CPQBN$HgwkWKL-'
    b'f7uHFxjD9{glf@6kE!%NZ(UWo`v6GlNsumtjVYIxD(miIaGFmG5$%qHZNZZ-Whxwmzgb*1>>P1+F*8|GFoF@MD0d0X}?vk!^l8D_'
    b'Ap8<KL(1G&?kWq7R_i}Oka-v^PBHE<d*ES|#5(ampb60+z_9$5KZln8gibI)o63w)gvx+LyFEyx5!YFI0eRCjvyE%H6vLa$-'
    b'B{dBg|A#{v!+u#f$#Qd&`t=4F1aCSku>%rF0EX1KY`llHJ#9zd+2Eh!`Vxk>+B_pCP%O3re9foe~vo|g^wOIUyV#we72uy(>w~_>'
    b'XDv>TPBg)GoGkUV;t>dEMq7sD2(3NoF<=9@sXNRiBheWkgSf~n}uG7gFYK;Uktvp1U9EfgiyaTCkzuDi|{o&0HLNy<=`fNDJ3?{R'
    b'h-qwwfVIvRbSGy0gw2R`hw1Y!5D74I8dS@T-=}hpBkJ%@Jb-'
    b'0F{z3<~I6pB(65C98jM#?k&eRxt8c7g)ssnHsZP(&2_@C`n*pUY_bn)7fmy!~Kt6nN$(reI|jPJvYYgz*>13K-'
    b'pCsPgqU%%Ky!tOSSw$VDj^d1PWdyAb@z??H0RvgXmK2++tW2Q7TtUumxqB0Dkpje7%JHL$j3%Ug+x{e#4z<HQ{9j~b4Vr%J3BkGS'
    b'#T{m1N=Cp(0;;q)GPZW7tS%WD+A-9y9DiDdglmuu~-WjeeKK;buA`B=z_U&!99(Xg2S%JW8I<~5TeRbv`bO-'
    b'#7f^F$1%(|R6eoJGI7e_cA-L|o-'
    b'7aB<PpIwM6R;*u5_q2AlFcBq$EJS0Jc%?=@D*Hu3k1Xf9`c_$vAa1T#kaf{S@W?nG%FcQwfBoUwUkcpN#d5<0WSETf}mu|S=R~Z)'
    b'9JNU-U^BX3yB~O#Ewt7YLjA7@oAsHQB)n4JQ;rwiTNz|d%?8i9^eL#y^arT1fj`b_}V6BIs-'
    b'@wXyuvh^s!J2PgF1N20DByDreunag_B?mfp0|GF1;krDSP3|;dGN<Rux2oEwIpqQTa(@<=8s;O=gIdht{fJL=;<s;WY&kGg=b;nu'
    b'>i4C2HBIV*s}Vet&K5;s+;racrb%tUgGXM?ked{XzqtW?#XN<8Zrd4<U_BWhkY;INTH}hEhsibR0$y(e5{xJ)BM3HcBuE*%%?B7A'
    b'7D*PiPD~E|EI*79tLjQ6cb)S1o~q6#59w<4IV67J6#8X3IDl=of6oODC{<VoEhx$l^b>mFhM&-'
    b'AH=CmiYgVX&BLlJ?}^{U=r@#<5W!FwctXIB-PVtq0UK}{(vL7f|Kwd$Oe>tZ4uXXpu!T~uCTJTfHE>cDbFgfPZL$6hLMt-'
    b'?nzV7SC}lDaeQmTA)5H=l%nA5KxL8n-YN}jAYF54Vdwj^uC*?4HCK(WFURP(rVMpnqnb-'
    b'A9ug(pBj1K4&PKJU8lVSsYTw=iK3rOYh<U+B>yJ<Ku5o1FjHwxndTZnez5j@{=>Nnq68H!kcI$ZODZdo{p$Bd^>n4tRNr3?uXggp'
    b'0VkfDm&@bNa3oE?m5=s%u~u*m7q%9eL)5Q8yADf|Fsisp$TJDo4M+{6E^L$~3EU^*=L_#S4C^w-j-'
    b';|`!4)`LkyXRs)Q!EG~7y%FUtj5wPRWnf*hGv+-'
    b'o?w?_pIe5%ld{#jDUz~g;L?#5f5V1w?;9fLe`U1o&4F>^iL5VTHr;wz1RzNtP4xkoGMByN+Gz4(CVE_-'
    b'Q>d)I>sZ6vEX&R4e3h{gw^*Y{nv!FS7IO`Cs*(&9>0Ft{>GIS4b5tc6t6zzH8>W9kvX83=-'
    b';)EE$j*w%p6rih%`t?ZWM+dZFKxo%uDg<g~g_UDaUr*WHzw$*rEIFU`K1r<TAe1~OvR-'
    b'#AGn_<#)<codj=TOOiG_iu?wEDMS$uZtk!RT!1O&6Yr13u#Qwr!FpktC{aO9{VX}6GboZ2l&VKz1W-'
    b'fMP+j7pne6%w8uwOL3`CT(^r-<8Q20(Ok*l+#m=%cd6u%_5?IHynB9_bZR=d5MG+dcKKx^X;LlEN|p{Y8WPkd$2Yx=-'
    b'|WMW4PW|d@C*=iO*Du65x3?9#TM9p|U8^9C@2YFIi$s&puc-_Ma3o`u7zlS}_lWJZLjI0y}+BL;@cSf-'
    b'5QPch8#%Yj>PXCi#Y=5aATlThI8u)uF`xmZ=wMrtKbn7A}W*aK<AKVsL|W<Y<U$p)bnLv)EhkdGy_vZx98VuUr@hU{XHNY6!_Bdt'
    b'CxX^A0i3d}DG9{APx-HfzY7sK+-'
    b'm;54nDVD1;8&m$%JZ^0e72tEUP<UQP_EZlsbB^@79v2y3U{C1}hinD#=MH;E;k>|WAN_QHQ$+s}_<cSJnFOV~fKW>e5uy#V|e)xv'
    b'|B3@o5W1WRTaIyC56GK*s+9xiyM++LKJ73CL74F9uE_@vN`^^k=@)(o{m%suc$}l#ImO29pEm?$Huy72r=`D;mN%{<04v}A9m)-'
    b'*+E{GzA?UqHENqB^NxVeq<=gp|7i9A%2&mN98-'
    b'x0+wEvf5%{msna1M@+;2>F34G>`w<JdS*~2RpLkM1`63@a9?8)9&WJ+|Q!0?fDi9QIu|@c2$YG2u*C9UNZ2^H}&vFIE%dS&C6A#e'
    b'=Z?^{p*@54@`*>WyH&HtJoWy3E!^SWG!EZWr0qzdHh<l&0iPM_aQ+ApZ#qHi3B(G#VwWcaJ3hCh3PjFGJ5dL0z454wD%3&*|~NQq'
    b'I^gA`>udCR%@@M%P$jSj+xHmZ!|%%r!0ufmgh+5Nuyzq1jNQ@p$RrWL~$#sv;>!gMWdo7d6z8NnkGyFt$Wlrcsx-'
    b'6t|o?zKldc8s{ZhZ?Ea7c5An^(w*'
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
    candidate = largest_divisor  # noqa: F405
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
